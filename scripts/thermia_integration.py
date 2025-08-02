#!/usr/bin/env python3
"""
Thermia HVAC Integration Module
Integrates with python-thermia-online-api for HVAC system monitoring and control
"""

import os
import sys
import logging
import json
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

try:
    from ThermiaOnlineAPI import Thermia, ThermiaHeatPump
except ImportError as e:
    print(f"Error importing Thermia API: {e}")
    print("Install with: pip install thermia-online-api")
    raise

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('thermia_integration.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class HVACSystemData:
    """Data class for HVAC system information"""
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

@dataclass
class DiagnosticResult:
    """Data class for diagnostic results"""
    system_id: str
    timestamp: datetime
    status: str
    issues: List[str]
    recommendations: List[str]
    efficiency_score: Optional[float]

class ThermiaHVACIntegration:
    """Thermia HVAC Integration with AI capabilities"""
    
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        """Initialize Thermia integration"""
        self.username = username or os.getenv('THERMIA_USERNAME')
        self.password = password or os.getenv('THERMIA_PASSWORD')
        self.thermia = None
        self.heat_pumps = []
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Initialize connection to Thermia API"""
        try:
            if not self.username or not self.password:
                logger.warning("Thermia credentials not provided. Using mock data for testing.")
                return
            
            self.thermia = Thermia(self.username, self.password)
            logger.info("Thermia API connection initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize Thermia connection: {e}")
            self.thermia = None
    
    def fetch_heat_pumps(self) -> List[HVACSystemData]:
        """Fetch all heat pumps and their data"""
        try:
            if not self.thermia:
                logger.warning("Thermia not connected. Returning mock data.")
                return self._get_mock_heat_pumps()
            
            # Fetch heat pumps from Thermia API
            heat_pumps = self.thermia.fetch_heat_pumps()
            self.heat_pumps = heat_pumps
            
            # Convert to our data format
            hvac_systems = []
            for pump in heat_pumps:
                hvac_system = HVACSystemData(
                    name=pump.name,
                    id=pump.id,
                    model=pump.model,
                    is_online=pump.is_online,
                    indoor_temperature=pump.indoor_temperature,
                    outdoor_temperature=pump.outdoor_temperature,
                    hot_water_temperature=pump.hot_water_temperature,
                    heat_temperature=pump.heat_temperature,
                    supply_line_temperature=getattr(pump, 'supply_line_temperature', None),
                    return_line_temperature=getattr(pump, 'return_line_temperature', None),
                    operation_mode=pump.operation_mode,
                    active_alarms=pump.active_alarms,
                    compressor_operational_time=pump.compressor_operational_time,
                    last_online=pump.last_online
                )
                hvac_systems.append(hvac_system)
            
            logger.info(f"Fetched {len(hvac_systems)} heat pumps")
            return hvac_systems
            
        except Exception as e:
            logger.error(f"Error fetching heat pumps: {e}")
            return self._get_mock_heat_pumps()
    
    def _get_mock_heat_pumps(self) -> List[HVACSystemData]:
        """Get mock heat pump data for testing"""
        return [
            HVACSystemData(
                name="Test Heat Pump 1",
                id="mock-001",
                model="Thermia Diplomat Duo",
                is_online=True,
                indoor_temperature=22.5,
                outdoor_temperature=5.2,
                hot_water_temperature=45.0,
                heat_temperature=21.0,
                supply_line_temperature=35.0,
                return_line_temperature=30.0,
                operation_mode="Heating",
                active_alarms=[],
                compressor_operational_time=1250.5,
                last_online="2024-01-15T10:30:00Z"
            ),
            HVACSystemData(
                name="Test Heat Pump 2",
                id="mock-002",
                model="Thermia Calibra",
                is_online=False,
                indoor_temperature=None,
                outdoor_temperature=None,
                hot_water_temperature=None,
                heat_temperature=20.0,
                supply_line_temperature=None,
                return_line_temperature=None,
                operation_mode="Standby",
                active_alarms=["Communication Error"],
                compressor_operational_time=890.2,
                last_online="2024-01-15T08:15:00Z"
            )
        ]
    
    def get_system_by_id(self, system_id: str) -> Optional[HVACSystemData]:
        """Get specific heat pump by ID"""
        systems = self.fetch_heat_pumps()
        for system in systems:
            if system.id == system_id:
                return system
        return None
    
    def set_temperature(self, system_id: str, temperature: float) -> bool:
        """Set temperature for a specific heat pump"""
        try:
            if not self.thermia:
                logger.warning("Thermia not connected. Mock temperature setting.")
                return True
            
            # Find the heat pump
            for pump in self.heat_pumps:
                if pump.id == system_id:
                    pump.set_temperature(temperature)
                    logger.info(f"Set temperature to {temperature}°C for system {system_id}")
                    return True
            
            logger.error(f"System {system_id} not found")
            return False
            
        except Exception as e:
            logger.error(f"Error setting temperature: {e}")
            return False
    
    def set_operation_mode(self, system_id: str, mode: str) -> bool:
        """Set operation mode for a specific heat pump"""
        try:
            if not self.thermia:
                logger.warning("Thermia not connected. Mock mode setting.")
                return True
            
            # Find the heat pump
            for pump in self.heat_pumps:
                if pump.id == system_id:
                    pump.set_operation_mode(mode)
                    logger.info(f"Set operation mode to {mode} for system {system_id}")
                    return True
            
            logger.error(f"System {system_id} not found")
            return False
            
        except Exception as e:
            logger.error(f"Error setting operation mode: {e}")
            return False
    
    def diagnose_system(self, system_id: str) -> DiagnosticResult:
        """Perform comprehensive system diagnosis"""
        system = self.get_system_by_id(system_id)
        if not system:
            return DiagnosticResult(
                system_id=system_id,
                timestamp=datetime.now(),
                status="ERROR",
                issues=["System not found"],
                recommendations=["Check system ID"],
                efficiency_score=None
            )
        
        issues = []
        recommendations = []
        efficiency_score = 100.0
        
        # Check online status
        if not system.is_online:
            issues.append("System is offline")
            recommendations.append("Check network connection and power supply")
            efficiency_score -= 30
        
        # Check temperature differentials
        if system.indoor_temperature and system.outdoor_temperature:
            temp_diff = system.indoor_temperature - system.outdoor_temperature
            if temp_diff < 10:
                issues.append("Low temperature differential")
                recommendations.append("Check system efficiency and insulation")
                efficiency_score -= 15
        
        # Check for alarms
        if system.active_alarms:
            issues.extend(system.active_alarms)
            recommendations.append("Address active alarms immediately")
            efficiency_score -= 25
        
        # Check hot water temperature
        if system.hot_water_temperature:
            if system.hot_water_temperature < 40:
                issues.append("Low hot water temperature")
                recommendations.append("Check hot water settings and efficiency")
                efficiency_score -= 10
            elif system.hot_water_temperature > 60:
                issues.append("High hot water temperature")
                recommendations.append("Consider lowering hot water temperature for efficiency")
                efficiency_score -= 5
        
        # Determine overall status
        if efficiency_score >= 90:
            status = "EXCELLENT"
        elif efficiency_score >= 70:
            status = "GOOD"
        elif efficiency_score >= 50:
            status = "FAIR"
        else:
            status = "POOR"
        
        return DiagnosticResult(
            system_id=system_id,
            timestamp=datetime.now(),
            status=status,
            issues=issues,
            recommendations=recommendations,
            efficiency_score=efficiency_score
        )
    
    def get_optimization_suggestions(self, system_id: str) -> List[str]:
        """Get optimization suggestions for a system"""
        system = self.get_system_by_id(system_id)
        if not system:
            return ["System not found"]
        
        suggestions = []
        
        # Temperature optimization
        if system.indoor_temperature and system.heat_temperature:
            if system.indoor_temperature > system.heat_temperature + 2:
                suggestions.append("Consider lowering indoor temperature for energy savings")
        
        # Hot water optimization
        if system.hot_water_temperature:
            if system.hot_water_temperature > 55:
                suggestions.append("Consider lowering hot water temperature to 45-50°C for efficiency")
        
        # Maintenance suggestions
        if system.compressor_operational_time:
            if system.compressor_operational_time > 1000:
                suggestions.append("Schedule maintenance check due to high operational hours")
        
        # General efficiency tips
        suggestions.extend([
            "Ensure proper insulation around the building",
            "Check and clean air filters regularly",
            "Monitor system performance trends",
            "Consider smart thermostat integration"
        ])
        
        return suggestions
    
    def get_system_status_summary(self) -> str:
        """Get a summary of all system statuses"""
        systems = self.fetch_heat_pumps()
        
        if not systems:
            return "No HVAC systems found"
        
        online_count = sum(1 for s in systems if s.is_online)
        total_count = len(systems)
        
        summary = f"HVAC Systems Overview:\n"
        summary += f"- Total systems: {total_count}\n"
        summary += f"- Online systems: {online_count}\n"
        summary += f"- Offline systems: {total_count - online_count}\n\n"
        
        for system in systems:
            status = "🟢 Online" if system.is_online else "🔴 Offline"
            summary += f"{system.name} ({system.model}): {status}\n"
            if system.indoor_temperature:
                summary += f"  Indoor: {system.indoor_temperature}°C\n"
            if system.outdoor_temperature:
                summary += f"  Outdoor: {system.outdoor_temperature}°C\n"
            if system.active_alarms:
                summary += f"  Alarms: {', '.join(system.active_alarms)}\n"
            summary += "\n"
        
        return summary

def get_thermia_integration() -> ThermiaHVACIntegration:
    """Get or create Thermia integration instance"""
    global _thermia_integration_instance
    
    if not hasattr(get_thermia_integration, '_thermia_integration_instance'):
        get_thermia_integration._thermia_integration_instance = ThermiaHVACIntegration()
    
    return get_thermia_integration._thermia_integration_instance

if __name__ == "__main__":
    # Test the Thermia integration
    try:
        integration = ThermiaHVACIntegration()
        
        # Test fetching systems
        systems = integration.fetch_heat_pumps()
        print(f"Found {len(systems)} systems")
        
        # Test system diagnosis
        if systems:
            diagnosis = integration.diagnose_system(systems[0].id)
            print(f"Diagnosis for {systems[0].name}:")
            print(f"Status: {diagnosis.status}")
            print(f"Efficiency Score: {diagnosis.efficiency_score}")
            print(f"Issues: {diagnosis.issues}")
            print(f"Recommendations: {diagnosis.recommendations}")
        
        # Test optimization suggestions
        if systems:
            suggestions = integration.get_optimization_suggestions(systems[0].id)
            print(f"\nOptimization suggestions: {suggestions}")
        
        # Test status summary
        summary = integration.get_system_status_summary()
        print(f"\nSystem Summary:\n{summary}")
        
    except Exception as e:
        print(f"Error testing Thermia integration: {e}") 