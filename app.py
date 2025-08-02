#!/usr/bin/env python3
"""
Flask API Server for AI Assistant
Provides REST API endpoints for the React frontend to interact with the AI system
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
from datetime import datetime
from pathlib import Path
from scripts.ai_rag_chat import AIRAGChat

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_flask_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Global AI system instance
_ai_system = None

def get_ai_system_instance():
    """Get or create AI system instance"""
    global _ai_system
    if _ai_system is None:
        try:
            _ai_system = AIRAGChat()
            logger.info("AI system initialized")
        except Exception as e:
            logger.error(f"Failed to initialize AI system: {e}")
            _ai_system = None
    return _ai_system

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        ai_system = get_ai_system_instance()
        
        if ai_system:
            status = "healthy"
            ai_status = ai_system.get_system_status()
        else:
            status = "error"
            ai_status = {"error": "AI system not available"}
        
        return jsonify({
            'status': status,
            'ai_system': ai_status,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat endpoint for AI assistant"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Message is required'
            }), 400
        
        message = data['message']
        session_id = data.get('sessionId', f'session-{datetime.now().timestamp()}')
        
        ai_system = get_ai_system_instance()
        
        if not ai_system:
            return jsonify({
                'error': 'AI system is not available'
            }), 503
        
        # Get response from AI system
        response = ai_system.ask_question(message)
        
        return jsonify({
            'response': response,
            'sessionId': session_id,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/search', methods=['POST'])
def search():
    """Search knowledge base"""
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                'error': 'Query is required'
            }), 400
        
        query = data['query']
        max_results = data.get('maxResults', 5)
        
        ai_system = get_ai_system_instance()
        
        if not ai_system:
            return jsonify({
                'error': 'AI system is not available'
            }), 503
        
        # Search knowledge base
        results = ai_system.search_knowledge_base(query, max_results)
        
        return jsonify({
            'query': query,
            'results': results,
            'count': len(results),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/system-status', methods=['GET'])
def system_status():
    """Get system status"""
    try:
        ai_system = get_ai_system_instance()
        
        if not ai_system:
            return jsonify({
                'error': 'AI system is not available'
            }), 503
        
        status = ai_system.get_system_status()
        
        return jsonify(status)
        
    except Exception as e:
        logger.error(f"System status error: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/add-knowledge', methods=['POST'])
def add_knowledge():
    """Add new knowledge to the system"""
    try:
        data = request.get_json()
        
        if not data or 'content' not in data:
            return jsonify({
                'error': 'Content is required'
            }), 400
        
        content = data['content']
        metadata = data.get('metadata', {})
        
        ai_system = get_ai_system_instance()
        
        if not ai_system:
            return jsonify({
                'error': 'AI system is not available'
            }), 503
        
        # Add knowledge to the system
        success = ai_system.add_knowledge(content, metadata)
        
        if success:
            return jsonify({
                'message': 'Knowledge added successfully',
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'error': 'Failed to add knowledge'
            }), 500
        
    except Exception as e:
        logger.error(f"Add knowledge error: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/context-files', methods=['GET'])
def list_context_files():
    """List available context files"""
    try:
        context_dir = Path('context')
        
        if not context_dir.exists():
            return jsonify({
                'files': [],
                'count': 0,
                'timestamp': datetime.now().isoformat()
            })
        
        files = []
        for file_path in context_dir.glob("*.txt"):
            files.append({
                'name': file_path.name,
                'size': file_path.stat().st_size,
                'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            })
        
        return jsonify({
            'files': files,
            'count': len(files),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"List context files error: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/context-files/<filename>', methods=['GET'])
def get_context_file(filename):
    """Get content of a specific context file"""
    try:
        file_path = Path('context') / filename
        
        if not file_path.exists():
            return jsonify({
                'error': 'File not found'
            }), 404
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({
            'filename': filename,
            'content': content,
            'size': len(content),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error reading context file: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

# HVAC-specific endpoints
@app.route('/api/hvac/systems', methods=['GET'])
def get_hvac_systems():
    """Get all HVAC systems"""
    try:
        ai_system = get_ai_system_instance()
        
        if not ai_system:
            return jsonify({
                'error': 'AI system is not available'
            }), 503
        
        systems = ai_system.get_hvac_systems()
        
        return jsonify({
            'systems': systems,
            'count': len(systems),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting HVAC systems: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/hvac/systems/<system_id>/diagnose', methods=['GET'])
def diagnose_hvac_system(system_id):
    """Diagnose a specific HVAC system"""
    try:
        ai_system = get_ai_system_instance()
        
        if not ai_system:
            return jsonify({
                'error': 'AI system is not available'
            }), 503
        
        diagnosis = ai_system.diagnose_hvac_system(system_id)
        
        return jsonify(diagnosis)
        
    except Exception as e:
        logger.error(f"Error diagnosing HVAC system: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/hvac/systems/<system_id>/optimize', methods=['GET'])
def get_hvac_optimization_suggestions(system_id):
    """Get optimization suggestions for HVAC system"""
    try:
        ai_system = get_ai_system_instance()
        
        if not ai_system:
            return jsonify({
                'error': 'AI system is not available'
            }), 503
        
        suggestions = ai_system.get_hvac_optimization_suggestions(system_id)
        
        return jsonify({
            'system_id': system_id,
            'suggestions': suggestions,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting optimization suggestions: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/hvac/systems/<system_id>/temperature', methods=['POST'])
def set_hvac_temperature(system_id):
    """Set temperature for HVAC system"""
    try:
        data = request.get_json()
        
        if not data or 'temperature' not in data:
            return jsonify({
                'error': 'Temperature is required'
            }), 400
        
        temperature = float(data['temperature'])
        
        ai_system = get_ai_system_instance()
        
        if not ai_system:
            return jsonify({
                'error': 'AI system is not available'
            }), 503
        
        success = ai_system.set_hvac_temperature(system_id, temperature)
        
        if success:
            return jsonify({
                'message': f'Temperature set to {temperature}°C',
                'system_id': system_id,
                'temperature': temperature,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'error': 'Failed to set temperature'
            }), 500
        
    except Exception as e:
        logger.error(f"Error setting HVAC temperature: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/hvac/systems/<system_id>/mode', methods=['POST'])
def set_hvac_operation_mode(system_id):
    """Set operation mode for HVAC system"""
    try:
        data = request.get_json()
        
        if not data or 'mode' not in data:
            return jsonify({
                'error': 'Mode is required'
            }), 400
        
        mode = data['mode']
        
        ai_system = get_ai_system_instance()
        
        if not ai_system:
            return jsonify({
                'error': 'AI system is not available'
            }), 503
        
        success = ai_system.set_hvac_operation_mode(system_id, mode)
        
        if success:
            return jsonify({
                'message': f'Operation mode set to {mode}',
                'system_id': system_id,
                'mode': mode,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'error': 'Failed to set operation mode'
            }), 500
        
    except Exception as e:
        logger.error(f"Error setting HVAC operation mode: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/hvac/status', methods=['GET'])
def get_hvac_status_summary():
    """Get HVAC systems status summary"""
    try:
        ai_system = get_ai_system_instance()
        
        if not ai_system:
            return jsonify({
                'error': 'AI system is not available'
            }), 503
        
        summary = ai_system.get_hvac_status_summary()
        
        return jsonify({
            'summary': summary,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting HVAC status summary: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug) 