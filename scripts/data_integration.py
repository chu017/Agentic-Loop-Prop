#!/usr/bin/env python3
"""
Data Integration Module
Combines RAG knowledge with live Thermia API data and database storage
"""

import os
import sys
import logging
import json
import sqlite3
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

try:
    from ThermiaOnlineAPI import Thermia, ThermiaHeatPump
except ImportError as e:
    print(f"Error importing Thermia API: {e}")
    print("Install with: pip install git+https://github.com/klejejs/python-thermia-online-api.git")
    raise

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_integration.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class HVACSystemData:
    """Enhanced HVAC system data with API integration"""
    name: str
    id: str
    model: str
    is_online: bool
    indoor_temperature: Optional[float]
    outdoor_temperature: Optional[float]
    hot_water_temperature: Optional[float]
    heat_temperature: Optional[float]
    supply_line_temperature: Optional[float]
    return_line_temperature: Optional[float]
    operation_mode: str
    active_alarms: List[str]
    compressor_operational_time: Optional[float]
    last_online: Optional[str]
    # Additional API data
    heat_min_temperature_value: Optional[float]
    heat_max_temperature_value: Optional[float]
    heat_temperature_step: Optional[float]
    available_operation_modes: List[str]
    running_operational_statuses: List[str]
    historical_data: Optional[List[Dict]]

class DataIntegrationManager:
    """Manages integration between RAG knowledge, Thermia API, and database"""
    
    def __init__(self, db_path: str = "hvac_data.db"):
        """Initialize data integration manager"""
        self.db_path = db_path
        self.thermia = None
        self.use_mock_data = os.getenv('USE_MOCK_DATA', 'true').lower() == 'true'
        self._initialize_database()
        self._initialize_thermia_connection()
    
    def _initialize_database(self):
        """Initialize SQLite database for caching and historical data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create systems table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS hvac_systems (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    model TEXT,
                    is_online BOOLEAN,
                    indoor_temperature REAL,
                    outdoor_temperature REAL,
                    hot_water_temperature REAL,
                    heat_temperature REAL,
                    supply_line_temperature REAL,
                    return_line_temperature REAL,
                    operation_mode TEXT,
                    active_alarms TEXT,
                    compressor_operational_time REAL,
                    last_online TEXT,
                    heat_min_temperature_value REAL,
                    heat_max_temperature_value REAL,
                    heat_temperature_step REAL,
                    available_operation_modes TEXT,
                    running_operational_statuses TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create historical data table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS historical_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    system_id TEXT,
                    register_name TEXT,
                    value REAL,
                    timestamp TIMESTAMP,
                    FOREIGN KEY (system_id) REFERENCES hvac_systems (id)
                )
            ''')
            
            # Create knowledge cache table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS knowledge_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT,
                    response TEXT,
                    context TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def _initialize_thermia_connection(self):
        """Initialize connection to Thermia API"""
        try:
            if self.use_mock_data:
                logger.info("Using mock data for Thermia API")
                return
            
            username = os.getenv('THERMIA_USERNAME')
            password = os.getenv('THERMIA_PASSWORD')
            
            if not username or not password:
                logger.warning("Thermia credentials not provided. Using mock data.")
                self.use_mock_data = True
                return
            
            self.thermia = Thermia(username, password)
            logger.info("Thermia API connection initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize Thermia connection: {e}")
            self.thermia = None
            self.use_mock_data = True
    
    def get_live_system_data(self, system_id: Optional[str] = None) -> List[HVACSystemData]:
        """Get live system data from Thermia API"""
        try:
            if self.use_mock_data or not self.thermia:
                # Get mock data and cache it
                systems_data = self._get_mock_system_data()
                # Filter by system_id if specified
                if system_id:
                    systems_data = [s for s in systems_data if s.id == system_id]
                # Cache the mock data
                self._cache_system_data(systems_data)
                return systems_data
            
            # Fetch live data from Thermia API
            heat_pumps = self.thermia.fetch_heat_pumps()
            systems_data = []
            
            for heat_pump in heat_pumps:
                system_data = HVACSystemData(
                    name=heat_pump.name,
                    id=heat_pump.id,
                    model=heat_pump.model,
                    is_online=heat_pump.is_online,
                    indoor_temperature=heat_pump.indoor_temperature,
                    outdoor_temperature=heat_pump.outdoor_temperature,
                    hot_water_temperature=heat_pump.hot_water_temperature,
                    heat_temperature=heat_pump.heat_temperature,
                    supply_line_temperature=heat_pump.supply_line_temperature,
                    return_line_temperature=heat_pump.return_line_temperature,
                    operation_mode=heat_pump.operation_mode,
                    active_alarms=heat_pump.active_alarms,
                    compressor_operational_time=heat_pump.compressor_operational_time,
                    last_online=heat_pump.last_online,
                    heat_min_temperature_value=heat_pump.heat_min_temperature_value,
                    heat_max_temperature_value=heat_pump.heat_max_temperature_value,
                    heat_temperature_step=heat_pump.heat_temperature_step,
                    available_operation_modes=heat_pump.available_operation_modes,
                    running_operational_statuses=heat_pump.running_operational_statuses,
                    historical_data=None
                )
                
                if system_id is None or system_data.id == system_id:
                    systems_data.append(system_data)
            
            # Cache the data
            self._cache_system_data(systems_data)
            return systems_data
            
        except Exception as e:
            logger.error(f"Error fetching live system data: {e}")
            # Get mock data and cache it even on error
            systems_data = self._get_mock_system_data()
            if system_id:
                systems_data = [s for s in systems_data if s.id == system_id]
            self._cache_system_data(systems_data)
            return systems_data
    
    def _get_mock_system_data(self) -> List[HVACSystemData]:
        """Get mock system data for testing"""
        return [
            HVACSystemData(
                name="Thermia Diplomat Duo",
                id="mock-system-1",
                model="Diplomat Duo",
                is_online=True,
                indoor_temperature=22.5,
                outdoor_temperature=-5.2,
                hot_water_temperature=45.0,
                heat_temperature=21.0,
                supply_line_temperature=35.0,
                return_line_temperature=30.0,
                operation_mode="Heating",
                active_alarms=[],
                compressor_operational_time=1250.5,
                last_online="2024-01-15T10:30:00Z",
                heat_min_temperature_value=15.0,
                heat_max_temperature_value=30.0,
                heat_temperature_step=0.5,
                available_operation_modes=["Heating", "Cooling", "Auto"],
                running_operational_statuses=["Compressor Running", "Circulation Pump Active"],
                historical_data=None
            ),
            HVACSystemData(
                name="Thermia Calibra",
                id="mock-system-2",
                model="Calibra",
                is_online=True,
                indoor_temperature=23.0,
                outdoor_temperature=-3.8,
                hot_water_temperature=48.0,
                heat_temperature=22.0,
                supply_line_temperature=38.0,
                return_line_temperature=32.0,
                operation_mode="Auto",
                active_alarms=["Low refrigerant pressure"],
                compressor_operational_time=890.2,
                last_online="2024-01-15T10:25:00Z",
                heat_min_temperature_value=16.0,
                heat_max_temperature_value=28.0,
                heat_temperature_step=0.5,
                available_operation_modes=["Heating", "Cooling", "Auto", "DHW"],
                running_operational_statuses=["Compressor Running", "DHW Pump Active"],
                historical_data=None
            )
        ]
    
    def _cache_system_data(self, systems_data: List[HVACSystemData]):
        """Cache system data in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for system in systems_data:
                cursor.execute('''
                    INSERT OR REPLACE INTO hvac_systems (
                        id, name, model, is_online, indoor_temperature, outdoor_temperature,
                        hot_water_temperature, heat_temperature, supply_line_temperature,
                        return_line_temperature, operation_mode, active_alarms,
                        compressor_operational_time, last_online, heat_min_temperature_value,
                        heat_max_temperature_value, heat_temperature_step,
                        available_operation_modes, running_operational_statuses, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ''', (
                    system.id, system.name, system.model, system.is_online,
                    system.indoor_temperature, system.outdoor_temperature,
                    system.hot_water_temperature, system.heat_temperature,
                    system.supply_line_temperature, system.return_line_temperature,
                    system.operation_mode, json.dumps(system.active_alarms),
                    system.compressor_operational_time, system.last_online,
                    system.heat_min_temperature_value, system.heat_max_temperature_value,
                    system.heat_temperature_step, json.dumps(system.available_operation_modes),
                    json.dumps(system.running_operational_statuses)
                ))
            
            conn.commit()
            conn.close()
            logger.info(f"Cached {len(systems_data)} system records")
            
        except Exception as e:
            logger.error(f"Error caching system data: {e}")
    
    def get_cached_system_data(self, system_id: Optional[str] = None) -> List[HVACSystemData]:
        """Get cached system data from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if system_id:
                cursor.execute('SELECT * FROM hvac_systems WHERE id = ?', (system_id,))
            else:
                cursor.execute('SELECT * FROM hvac_systems ORDER BY updated_at DESC')
            
            rows = cursor.fetchall()
            conn.close()
            
            systems_data = []
            for row in rows:
                system_data = HVACSystemData(
                    name=row[1], id=row[0], model=row[2], is_online=bool(row[3]),
                    indoor_temperature=row[4], outdoor_temperature=row[5],
                    hot_water_temperature=row[6], heat_temperature=row[7],
                    supply_line_temperature=row[8], return_line_temperature=row[9],
                    operation_mode=row[10], active_alarms=json.loads(row[11]),
                    compressor_operational_time=row[12], last_online=row[13],
                    heat_min_temperature_value=row[14], heat_max_temperature_value=row[15],
                    heat_temperature_step=row[16], available_operation_modes=json.loads(row[17]),
                    running_operational_statuses=json.loads(row[18]), historical_data=None
                )
                systems_data.append(system_data)
            
            return systems_data
            
        except Exception as e:
            logger.error(f"Error getting cached system data: {e}")
            return []
    
    def get_historical_data(self, system_id: str, register_name: str, 
                          start_time: datetime, end_time: datetime) -> List[Dict]:
        """Get historical data for a system"""
        try:
            if self.use_mock_data or not self.thermia:
                # Get mock data and cache it
                historical_data = self._get_mock_historical_data(system_id, register_name, start_time, end_time)
                self._cache_historical_data(system_id, register_name, historical_data)
                return historical_data
            
            # Get the heat pump object
            heat_pumps = self.thermia.fetch_heat_pumps()
            heat_pump = None
            for hp in heat_pumps:
                if hp.id == system_id:
                    heat_pump = hp
                    break
            
            if not heat_pump:
                logger.error(f"System {system_id} not found")
                return []
            
            # Fetch historical data from Thermia API
            historical_data = heat_pump.get_historical_data_for_register(
                register_name, start_time, end_time
            )
            
            # Cache the historical data
            self._cache_historical_data(system_id, register_name, historical_data)
            
            return historical_data
            
        except Exception as e:
            logger.error(f"Error fetching historical data: {e}")
            # Get mock data and cache it even on error
            historical_data = self._get_mock_historical_data(system_id, register_name, start_time, end_time)
            self._cache_historical_data(system_id, register_name, historical_data)
            return historical_data
    
    def _get_mock_historical_data(self, system_id: str, register_name: str,
                                start_time: datetime, end_time: datetime) -> List[Dict]:
        """Get mock historical data for testing"""
        data = []
        current_time = start_time
        
        while current_time <= end_time:
            # Generate mock data based on register name
            if "temperature" in register_name.lower():
                value = 20 + 5 * (current_time.hour / 24)  # Daily temperature cycle
            elif "power" in register_name.lower():
                value = 2000 + 500 * (current_time.hour / 24)  # Daily power cycle
            else:
                value = 100 + (current_time.hour * 10)  # Generic cycle
            
            data.append({
                "time": current_time,
                "value": value
            })
            
            current_time += timedelta(hours=1)
        
        return data
    
    def _cache_historical_data(self, system_id: str, register_name: str, data: List[Dict]):
        """Cache historical data in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for record in data:
                cursor.execute('''
                    INSERT OR REPLACE INTO historical_data 
                    (system_id, register_name, value, timestamp) 
                    VALUES (?, ?, ?, ?)
                ''', (system_id, register_name, record['value'], record['time']))
            
            conn.commit()
            conn.close()
            logger.info(f"Cached {len(data)} historical data records")
            
        except Exception as e:
            logger.error(f"Error caching historical data: {e}")
    
    def set_system_temperature(self, system_id: str, temperature: float) -> bool:
        """Set temperature for a system"""
        try:
            if self.use_mock_data or not self.thermia:
                logger.info(f"Mock: Setting temperature to {temperature}°C for system {system_id}")
                return True
            
            # Get the heat pump object
            heat_pumps = self.thermia.fetch_heat_pumps()
            heat_pump = None
            for hp in heat_pumps:
                if hp.id == system_id:
                    heat_pump = hp
                    break
            
            if not heat_pump:
                logger.error(f"System {system_id} not found")
                return False
            
            # Set temperature via Thermia API
            heat_pump.set_temperature(temperature)
            logger.info(f"Set temperature to {temperature}°C for system {system_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting temperature: {e}")
            return False
    
    def set_system_operation_mode(self, system_id: str, mode: str) -> bool:
        """Set operation mode for a system"""
        try:
            if self.use_mock_data or not self.thermia:
                logger.info(f"Mock: Setting operation mode to {mode} for system {system_id}")
                return True
            
            # Get the heat pump object
            heat_pumps = self.thermia.fetch_heat_pumps()
            heat_pump = None
            for hp in heat_pumps:
                if hp.id == system_id:
                    heat_pump = hp
                    break
            
            if not heat_pump:
                logger.error(f"System {system_id} not found")
                return False
            
            # Set operation mode via Thermia API
            heat_pump.set_operation_mode(mode)
            logger.info(f"Set operation mode to {mode} for system {system_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting operation mode: {e}")
            return False
    
    def get_system_diagnosis(self, system_id: str) -> Dict:
        """Get comprehensive system diagnosis combining API data and knowledge"""
        try:
            # Get live system data
            systems = self.get_live_system_data(system_id)
            if not systems:
                return {"error": "System not found"}
            
            system = systems[0]
            
            # Analyze system health based on data
            diagnosis = {
                "system_id": system_id,
                "timestamp": datetime.now().isoformat(),
                "status": "GOOD",
                "issues": [],
                "recommendations": [],
                "efficiency_score": 85.0
            }
            
            # Check for alarms
            if system.active_alarms:
                diagnosis["status"] = "POOR"
                diagnosis["issues"].extend(system.active_alarms)
                diagnosis["efficiency_score"] -= 20
            
            # Check temperature efficiency
            if system.indoor_temperature and system.heat_temperature:
                temp_diff = abs(system.indoor_temperature - system.heat_temperature)
                if temp_diff > 3:
                    diagnosis["issues"].append("Temperature setpoint deviation")
                    diagnosis["recommendations"].append("Adjust temperature setpoint for better efficiency")
                    diagnosis["efficiency_score"] -= 10
            
            # Check operational status
            if system.running_operational_statuses:
                if "Compressor Running" in system.running_operational_statuses:
                    diagnosis["recommendations"].append("System operating normally")
                else:
                    diagnosis["issues"].append("Compressor not running")
                    diagnosis["efficiency_score"] -= 15
            
            # Update status based on issues
            if len(diagnosis["issues"]) > 2:
                diagnosis["status"] = "POOR"
            elif len(diagnosis["issues"]) > 0:
                diagnosis["status"] = "FAIR"
            
            return diagnosis
            
        except Exception as e:
            logger.error(f"Error getting system diagnosis: {e}")
            return {"error": str(e)}
    
    def get_optimization_suggestions(self, system_id: str) -> List[str]:
        """Get optimization suggestions based on system data"""
        try:
            systems = self.get_live_system_data(system_id)
            if not systems:
                return ["System not found"]
            
            system = systems[0]
            suggestions = []
            
            # Temperature optimization
            if system.indoor_temperature and system.heat_temperature:
                temp_diff = system.indoor_temperature - system.heat_temperature
                if temp_diff > 2:
                    suggestions.append("Consider lowering the heat temperature setpoint for better efficiency")
                elif temp_diff < -1:
                    suggestions.append("Consider raising the heat temperature setpoint for comfort")
            
            # Operation mode optimization
            if system.operation_mode == "Heating" and system.outdoor_temperature and system.outdoor_temperature > 10:
                suggestions.append("Consider switching to Auto mode for better efficiency in mild weather")
            
            # Maintenance suggestions
            if system.compressor_operational_time and system.compressor_operational_time > 1000:
                suggestions.append("Schedule preventive maintenance - compressor has high operational hours")
            
            # Energy efficiency
            if system.indoor_temperature and system.outdoor_temperature:
                temp_diff = system.indoor_temperature - system.outdoor_temperature
                if temp_diff > 25:
                    suggestions.append("Large temperature difference detected - consider insulation improvements")
            
            return suggestions if suggestions else ["System is operating optimally"]
            
        except Exception as e:
            logger.error(f"Error getting optimization suggestions: {e}")
            return ["Unable to generate suggestions"]

def get_data_integration_manager() -> DataIntegrationManager:
    """Get or create data integration manager instance"""
    return DataIntegrationManager() 