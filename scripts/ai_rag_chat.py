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
        self.thermia_integration = None
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all system components"""
        # Initialize Thermia integration
        try:
            from thermia_integration import ThermiaHVACIntegration
            self.thermia_integration = ThermiaHVACIntegration()
            logger.info("Thermia integration initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize Thermia integration: {e}")
            self.thermia_integration = None
        
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
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
            
            self.vectorstore = FAISS.from_texts(all_splits, embeddings)
            logger.info(f"Created vector store with {len(all_splits)} text chunks")
            
        except Exception as e:
            logger.error(f"Error loading context: {e}")
            raise
    
    def _get_default_knowledge(self) -> str:
        """Get default knowledge base content"""
        return """
        AI Assistant Knowledge Base
        
        GENERAL CAPABILITIES:
        This AI assistant is designed to help with various tasks including:
        - Answering questions and providing information
        - Problem solving and troubleshooting
        - Data analysis and interpretation
        - Code review and development assistance
        - Document analysis and summarization
        
        RESPONSE GUIDELINES:
        - Provide accurate and helpful information
        - Be concise but comprehensive
        - Use clear and professional language
        - Cite sources when appropriate
        - Admit when information is not available
        
        INTERACTION PROTOCOLS:
        - Maintain professional and helpful tone
        - Ask clarifying questions when needed
        - Provide step-by-step guidance when appropriate
        - Offer multiple solutions when possible
        - Follow up to ensure understanding
        
        TECHNICAL EXPERTISE:
        - Programming and software development
        - System administration and IT support
        - Data analysis and visualization
        - Web development and design
        - Database management and optimization
        
        BEST PRACTICES:
        - Always verify information accuracy
        - Provide context for recommendations
        - Consider security implications
        - Suggest improvements when possible
        - Document processes and procedures
        """
    
    def _setup_qa_chain(self):
        """Setup the question-answering chain"""
        try:
            # Initialize Ollama LLM
            llm = Ollama(model=self.model_name)
            
            # Create prompt template
            prompt_template = """Use the following pieces of context to answer the question at the end. 
            If you don't know the answer, just say that you don't know, don't try to make up an answer.
            
            Context: {context}
            
            Question: {question}
            
            Answer:"""
            
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
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
    
    def ask_question(self, question: str) -> str:
        """Ask a question and get an answer from the knowledge base"""
        try:
            if not self.qa_chain:
                return "AI system is not properly initialized. Please check the setup."
            
            # Get answer from QA chain
            result = self.qa_chain.run(question)
            
            # Log the interaction
            logger.info(f"Question: {question}")
            logger.info(f"Answer: {result}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error asking question: {e}")
            return f"I encountered an error while processing your question: {str(e)}"
    
    def search_knowledge_base(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search the knowledge base for relevant information"""
        try:
            if not self.vectorstore:
                return []
            
            # Search for similar documents
            docs = self.vectorstore.similarity_search(query, k=max_results)
            
            results = []
            for i, doc in enumerate(docs):
                results.append({
                    'rank': i + 1,
                    'content': doc.page_content,
                    'metadata': doc.metadata
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching knowledge base: {e}")
            return []
    
    def get_system_status(self) -> Dict:
        """Get the current system status"""
        try:
            status = {
                'model_name': self.model_name,
                'vectorstore_loaded': self.vectorstore is not None,
                'qa_chain_ready': self.qa_chain is not None,
                'thermia_integration': self.thermia_integration is not None,
                'context_files_count': len(list(self.context_dir.glob("*.txt"))) if self.context_dir.exists() else 0,
                'timestamp': datetime.now().isoformat()
            }
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {'error': str(e)}
    
    def get_hvac_systems(self) -> List[Dict]:
        """Get all HVAC systems"""
        if not self.thermia_integration:
            return []
        
        try:
            systems = self.thermia_integration.fetch_heat_pumps()
            return [
                {
                    'id': system.id,
                    'name': system.name,
                    'model': system.model,
                    'is_online': system.is_online,
                    'indoor_temperature': system.indoor_temperature,
                    'outdoor_temperature': system.outdoor_temperature,
                    'hot_water_temperature': system.hot_water_temperature,
                    'heat_temperature': system.heat_temperature,
                    'operation_mode': system.operation_mode,
                    'active_alarms': system.active_alarms,
                    'compressor_operational_time': system.compressor_operational_time,
                    'last_online': system.last_online
                }
                for system in systems
            ]
        except Exception as e:
            logger.error(f"Error getting HVAC systems: {e}")
            return []
    
    def diagnose_hvac_system(self, system_id: str) -> Dict:
        """Diagnose a specific HVAC system"""
        if not self.thermia_integration:
            return {'error': 'Thermia integration not available'}
        
        try:
            diagnosis = self.thermia_integration.diagnose_system(system_id)
            return {
                'system_id': diagnosis.system_id,
                'timestamp': diagnosis.timestamp.isoformat(),
                'status': diagnosis.status,
                'issues': diagnosis.issues,
                'recommendations': diagnosis.recommendations,
                'efficiency_score': diagnosis.efficiency_score
            }
        except Exception as e:
            logger.error(f"Error diagnosing HVAC system: {e}")
            return {'error': str(e)}
    
    def get_hvac_optimization_suggestions(self, system_id: str) -> List[str]:
        """Get optimization suggestions for HVAC system"""
        if not self.thermia_integration:
            return ["Thermia integration not available"]
        
        try:
            return self.thermia_integration.get_optimization_suggestions(system_id)
        except Exception as e:
            logger.error(f"Error getting optimization suggestions: {e}")
            return [f"Error: {str(e)}"]
    
    def set_hvac_temperature(self, system_id: str, temperature: float) -> bool:
        """Set temperature for HVAC system"""
        if not self.thermia_integration:
            return False
        
        try:
            return self.thermia_integration.set_temperature(system_id, temperature)
        except Exception as e:
            logger.error(f"Error setting HVAC temperature: {e}")
            return False
    
    def set_hvac_operation_mode(self, system_id: str, mode: str) -> bool:
        """Set operation mode for HVAC system"""
        if not self.thermia_integration:
            return False
        
        try:
            return self.thermia_integration.set_operation_mode(system_id, mode)
        except Exception as e:
            logger.error(f"Error setting HVAC operation mode: {e}")
            return False
    
    def get_hvac_status_summary(self) -> str:
        """Get HVAC systems status summary"""
        if not self.thermia_integration:
            return "Thermia integration not available"
        
        try:
            return self.thermia_integration.get_system_status_summary()
        except Exception as e:
            logger.error(f"Error getting HVAC status summary: {e}")
            return f"Error: {str(e)}"
    
    def add_knowledge(self, content: str, metadata: Optional[Dict] = None) -> bool:
        """Add new knowledge to the vector store"""
        try:
            if not self.vectorstore:
                logger.error("Vector store not initialized")
                return False
            
            # Add new content to vector store
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
            
            self.vectorstore.add_texts([content], metadatas=[metadata or {}])
            logger.info("Added new knowledge to vector store")
            
            return True
            
        except Exception as e:
            logger.error(f"Error adding knowledge: {e}")
            return False

def get_ai_rag_chat() -> AIRAGChat:
    """Get or create AI RAG chat instance"""
    global _ai_rag_chat_instance
    
    if not hasattr(get_ai_rag_chat, '_ai_rag_chat_instance'):
        get_ai_rag_chat._ai_rag_chat_instance = AIRAGChat()
    
    return get_ai_rag_chat._ai_rag_chat_instance

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