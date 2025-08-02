#!/usr/bin/env python3
"""
AI RAG Chat System with Knowledge Base Integration
Combines LangChain RAG with comprehensive knowledge base for intelligent responses
"""

import os
import sys
import logging
import json
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from datetime import datetime

# Add scripts directory to path
current_dir = Path(__file__).parent
project_root = current_dir.parent
scripts_dir = project_root / 'scripts'

if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain.chains import RetrievalQA
    from langchain_community.llms import Ollama
    from langchain.prompts import PromptTemplate
    from data_integration import get_data_integration_manager, HVACSystemData
except ImportError as e:
    print(f"Error importing LangChain modules: {e}")
    print("Install with: pip install langchain langchain-community")
    raise

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_rag_chat.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AIRAGChat:
    """AI RAG Chat System with Knowledge Base Integration"""
    
    def __init__(self, context_dir: str = "context", model_name: str = "mistral"):
        """Initialize AI RAG chat system"""
        self.context_dir = Path(context_dir)
        self.model_name = model_name
        self.vectorstore = None
        self.qa_chain = None
        self.data_manager = None
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all system components"""
        # Initialize data integration manager
        try:
            self.data_manager = get_data_integration_manager()
            logger.info("Data integration manager initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize data integration manager: {e}")
            self.data_manager = None
        
        # Initialize vector store
        self._load_context()
        
        # Initialize QA chain
        self._setup_qa_chain()
        
        logger.info("AI RAG Chat System initialized successfully")
    
    def _load_context(self):
        """Load knowledge base context files into vector store"""
        try:
            # Load context files
            context_files = []
            if self.context_dir.exists():
                for file_path in self.context_dir.glob("*.txt"):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        context_files.append(content)
                        logger.info(f"Loaded context file: {file_path}")
            
            if not context_files:
                logger.warning("No context files found. Creating default knowledge base.")
                context_files = [self._get_default_knowledge()]
            
            # Split text into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
            )
            
            all_splits = []
            for content in context_files:
                splits = text_splitter.split_text(content)
                all_splits.extend(splits)
            
            # Create embeddings and vector store
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            
            self.vectorstore = FAISS.from_texts(all_splits, embeddings)
            logger.info(f"Created vector store with {len(all_splits)} text chunks")
            
        except Exception as e:
            logger.error(f"Error loading context: {e}")
            raise
    
    def _get_default_knowledge(self) -> str:
        """Get default HVAC knowledge base"""
        return """
        HVAC Systems and Thermia Heat Pumps
        
        Thermia heat pumps are high-efficiency heating and cooling systems that extract heat from the environment. 
        They use refrigerant to transfer heat between indoor and outdoor units.
        
        Key Components:
        - Compressor: The heart of the system that circulates refrigerant
        - Evaporator: Absorbs heat from the environment
        - Condenser: Releases heat to the indoor space
        - Expansion valve: Controls refrigerant flow
        
        Common Thermia Models:
        - Diplomat Duo: High-efficiency dual-mode heat pump
        - Calibra: Compact and efficient residential system
        - Atlas: Commercial-grade heat pump system
        - Mega: Large capacity system for commercial applications
        
        Operation Modes:
        - Heating: Provides space heating
        - Cooling: Provides air conditioning
        - Auto: Automatically switches between heating and cooling
        - DHW: Domestic hot water production
        
        Temperature Control:
        - Heat temperature: Target heating temperature
        - Indoor temperature: Current indoor temperature
        - Outdoor temperature: Current outdoor temperature
        - Hot water temperature: Domestic hot water temperature
        
        System Monitoring:
        - Compressor operational time: Total running hours
        - Active alarms: Current system issues
        - Operational status: Current system state
        - Efficiency indicators: Performance metrics
        
        Maintenance:
        - Regular filter cleaning
        - Annual professional inspection
        - Refrigerant level checks
        - Electrical component testing
        
        Troubleshooting:
        - Low refrigerant pressure: Check for leaks
        - High temperature differential: Check insulation
        - Compressor issues: Check electrical connections
        - Poor efficiency: Check filters and settings
        """
    
    def _setup_qa_chain(self):
        """Setup the QA chain with Ollama"""
        try:
            # Initialize Ollama LLM
            llm = Ollama(
                model=self.model_name,
                temperature=0.7,
                timeout=30
            )
            
            # Create prompt template
            prompt_template = """You are an expert HVAC technician specializing in Thermia heat pump systems. 
            Use the following context and live system data to answer the user's question.
            
            Context information:
            {context}
            
            Live system data (if available):
            {system_data}
            
            User question: {question}
            
            Provide a comprehensive, accurate, and helpful response based on the context and live data. 
            If the question involves system data, reference the actual values from the live data.
            If you don't have enough information, say so and suggest what additional data might be needed.
            
            Answer:"""
            
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "system_data", "question"]
            )
            
            # Create QA chain
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
                chain_type_kwargs={"prompt": prompt}
            )
            
            logger.info("QA chain initialized successfully")
            
        except Exception as e:
            logger.error(f"Error setting up QA chain: {e}")
            raise
    
    def ask_question(self, question: str, system_id: Optional[str] = None) -> str:
        """Ask a question and get AI response with live data integration"""
        try:
            # Get live system data if available
            system_data = ""
            if self.data_manager and system_id:
                systems = self.data_manager.get_live_system_data(system_id)
                if systems:
                    system = systems[0]
                    system_data = f"""
                    Current System Status:
                    - Name: {system.name}
                    - Model: {system.model}
                    - Online: {system.is_online}
                    - Indoor Temperature: {system.indoor_temperature}°C
                    - Outdoor Temperature: {system.outdoor_temperature}°C
                    - Heat Temperature: {system.heat_temperature}°C
                    - Hot Water Temperature: {system.hot_water_temperature}°C
                    - Operation Mode: {system.operation_mode}
                    - Active Alarms: {', '.join(system.active_alarms) if system.active_alarms else 'None'}
                    - Compressor Hours: {system.compressor_operational_time} hours
                    """
            
            # Get response from QA chain
            if self.qa_chain:
                response = self.qa_chain.run({
                    "context": "HVAC and Thermia heat pump knowledge",
                    "system_data": system_data,
                    "question": question
                })
                return response
            else:
                return "AI system not properly initialized. Please check the logs."
                
        except Exception as e:
            logger.error(f"Error asking question: {e}")
            return f"I'm sorry, I encountered an error while processing your question: {str(e)}"
    
    def search_knowledge_base(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search the knowledge base"""
        try:
            if not self.vectorstore:
                return []
            
            docs = self.vectorstore.similarity_search(query, k=max_results)
            results = []
            
            for doc in docs:
                results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching knowledge base: {e}")
            return []
    
    def get_system_status(self) -> Dict:
        """Get comprehensive system status"""
        try:
            status = {
                "ai_system": "operational",
                "knowledge_base": "loaded",
                "vector_store": "initialized",
                "data_integration": "operational" if self.data_manager else "not_available",
                "timestamp": datetime.now().isoformat()
            }
            
            # Add data integration status
            if self.data_manager:
                try:
                    systems = self.data_manager.get_live_system_data()
                    status["connected_systems"] = len(systems)
                    status["data_source"] = "live_api" if not self.data_manager.use_mock_data else "mock_data"
                except Exception as e:
                    status["data_integration"] = f"error: {str(e)}"
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {"error": str(e)}
    
    def get_hvac_systems(self) -> List[Dict]:
        """Get all HVAC systems with live data"""
        try:
            if not self.data_manager:
                return []
            
            systems = self.data_manager.get_live_system_data()
            return [asdict(system) for system in systems]
            
        except Exception as e:
            logger.error(f"Error getting HVAC systems: {e}")
            return []
    
    def diagnose_hvac_system(self, system_id: str) -> Dict:
        """Diagnose HVAC system using live data and knowledge"""
        try:
            if not self.data_manager:
                return {"error": "Data integration not available"}
            
            # Get diagnosis from data manager
            diagnosis = self.data_manager.get_system_diagnosis(system_id)
            
            # Enhance with AI analysis
            if diagnosis and "error" not in diagnosis:
                question = f"Based on the system diagnosis: {json.dumps(diagnosis)}, what are the key issues and recommendations?"
                ai_analysis = self.ask_question(question, system_id)
                diagnosis["ai_analysis"] = ai_analysis
            
            return diagnosis
            
        except Exception as e:
            logger.error(f"Error diagnosing HVAC system: {e}")
            return {"error": str(e)}
    
    def get_hvac_optimization_suggestions(self, system_id: str) -> List[str]:
        """Get optimization suggestions based on live data"""
        try:
            if not self.data_manager:
                return ["Data integration not available"]
            
            # Get suggestions from data manager
            suggestions = self.data_manager.get_optimization_suggestions(system_id)
            
            # Enhance with AI analysis
            if suggestions:
                question = f"Based on these optimization suggestions: {suggestions}, what additional recommendations would you make for improving HVAC efficiency?"
                ai_suggestions = self.ask_question(question, system_id)
                suggestions.append(f"AI Recommendation: {ai_suggestions}")
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Error getting optimization suggestions: {e}")
            return ["Unable to generate suggestions"]
    
    def set_hvac_temperature(self, system_id: str, temperature: float) -> bool:
        """Set temperature for HVAC system"""
        try:
            if not self.data_manager:
                return False
            
            return self.data_manager.set_system_temperature(system_id, temperature)
            
        except Exception as e:
            logger.error(f"Error setting HVAC temperature: {e}")
            return False
    
    def set_hvac_operation_mode(self, system_id: str, mode: str) -> bool:
        """Set operation mode for HVAC system"""
        try:
            if not self.data_manager:
                return False
            
            return self.data_manager.set_system_operation_mode(system_id, mode)
            
        except Exception as e:
            logger.error(f"Error setting HVAC operation mode: {e}")
            return False
    
    def get_hvac_status_summary(self) -> str:
        """Get summary of all HVAC systems"""
        try:
            if not self.data_manager:
                return "Data integration not available"
            
            systems = self.data_manager.get_live_system_data()
            if not systems:
                return "No HVAC systems found"
            
            summary = f"HVAC Systems Summary ({len(systems)} systems):\n"
            
            for system in systems:
                status = "🟢 Online" if system.is_online else "🔴 Offline"
                alarms = f" ({len(system.active_alarms)} alarms)" if system.active_alarms else ""
                summary += f"- {system.name} ({system.model}): {status}{alarms}\n"
                summary += f"  Temperature: {system.indoor_temperature}°C indoor, {system.outdoor_temperature}°C outdoor\n"
                summary += f"  Mode: {system.operation_mode}, Heat: {system.heat_temperature}°C\n"
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting HVAC status summary: {e}")
            return f"Error getting status summary: {str(e)}"
    
    def add_knowledge(self, content: str, metadata: Optional[Dict] = None) -> bool:
        """Add new knowledge to the system"""
        try:
            if not self.vectorstore:
                return False
            
            # Add to vector store
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            
            # Split the new content
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
            )
            
            splits = text_splitter.split_text(content)
            
            # Add to existing vector store
            self.vectorstore.add_texts(splits, metadatas=[metadata or {}] * len(splits))
            
            logger.info(f"Added {len(splits)} new knowledge chunks")
            return True
            
        except Exception as e:
            logger.error(f"Error adding knowledge: {e}")
            return False

def get_ai_system() -> AIRAGChat:
    """Get or create AI system instance"""
    return AIRAGChat()

if __name__ == "__main__":
    # Test the AI RAG chat system
    try:
        ai_chat = AIRAGChat()
        
        # Test questions
        test_questions = [
            "What are the main features of this AI system?",
            "How does the knowledge base work?",
            "What are the best practices for using this system?"
        ]
        
        for question in test_questions:
            print(f"\nQuestion: {question}")
            answer = ai_chat.ask_question(question)
            print(f"Answer: {answer}")
        
        # Get system status
        status = ai_chat.get_system_status()
        print(f"\nSystem Status: {json.dumps(status, indent=2)}")
        
    except Exception as e:
        print(f"Error testing AI RAG chat: {e}") 