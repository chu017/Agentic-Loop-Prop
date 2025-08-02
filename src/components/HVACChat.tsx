import React, { useState, useRef, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Project, ChatMessage } from '../types';
import { chatAPI } from '../services/api';
import { Send, Bot, User, Thermometer, Activity, AlertTriangle } from 'lucide-react';

interface HVACChatProps {
  project: Project;
  onBack: () => void;
}

const HVACChat: React.FC<HVACChatProps> = ({ project, onBack }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      text: `Hello! I'm your HVAC AI Assistant. I can help you with your ${project.hvac_model} system. What would you like to know about your HVAC system or the issue you described?`,
      sender: 'assistant',
      timestamp: new Date(),
    },
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await chatAPI.sendMessage(inputMessage);
      
      if (response.data) {
        // Handle the actual API response structure
        const responseText = response.data.response || "I'm sorry, I couldn't process your request. Please try again.";
        const assistantMessage: ChatMessage = {
          id: (Date.now() + 1).toString(),
          text: responseText,
          sender: 'assistant',
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, assistantMessage]);
      } else {
        const errorMessage: ChatMessage = {
          id: (Date.now() + 1).toString(),
          text: "I'm having trouble connecting to the AI system. Please check your connection and try again.",
          sender: 'assistant',
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        text: "I'm having trouble connecting to the AI system. Please try again later.",
        sender: 'assistant',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const quickActions = [
    {
      title: 'System Status',
      description: 'Check current system status',
      icon: Activity,
      action: () => setInputMessage('What is the current status of my HVAC system?'),
    },
    {
      title: 'Diagnose Issues',
      description: 'Run system diagnostics',
      icon: AlertTriangle,
      action: () => setInputMessage('Can you diagnose any issues with my HVAC system?'),
    },
    {
      title: 'Optimization',
      description: 'Get efficiency tips',
      icon: Thermometer,
      action: () => setInputMessage('How can I optimize my HVAC system for better efficiency?'),
    },
  ];

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <Button variant="outline" onClick={onBack} className="flex items-center space-x-2">
              <Thermometer className="h-4 w-4" />
              <span>Back to Projects</span>
            </Button>
          </div>
          <div className="text-right">
            <h2 className="text-lg font-semibold text-gray-900">{project.name}</h2>
            <p className="text-sm text-gray-600">{project.hvac_model}</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Chat Interface */}
        <div className="lg:col-span-2">
          <Card className="h-[600px] flex flex-col">
            <CardHeader className="border-b">
              <CardTitle className="flex items-center space-x-2">
                <Bot className="h-5 w-5 text-blue-600" />
                <span>HVAC AI Assistant</span>
              </CardTitle>
            </CardHeader>
            
            <CardContent className="flex-1 flex flex-col p-0">
              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-lg px-4 py-2 ${
                        message.sender === 'user'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 text-gray-900'
                      }`}
                    >
                      <div className="flex items-start space-x-2">
                        {message.sender === 'assistant' && (
                          <Bot className="h-4 w-4 mt-1 text-blue-600 flex-shrink-0" />
                        )}
                        <div className="flex-1">
                          <p className="text-sm">{message.text}</p>
                          <p className="text-xs opacity-70 mt-1">
                            {message.timestamp.toLocaleTimeString()}
                          </p>
                        </div>
                        {message.sender === 'user' && (
                          <User className="h-4 w-4 mt-1 text-white flex-shrink-0" />
                        )}
                      </div>
                    </div>
                  </div>
                ))}
                
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 rounded-lg px-4 py-2">
                      <div className="flex items-center space-x-2">
                        <Bot className="h-4 w-4 text-blue-600" />
                        <div className="flex space-x-1">
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
                
                <div ref={messagesEndRef} />
              </div>

              {/* Input */}
              <div className="border-t p-4">
                <form onSubmit={sendMessage} className="flex space-x-2">
                  <Input
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    placeholder="Ask about your HVAC system..."
                    disabled={isLoading}
                    className="flex-1"
                  />
                  <Button type="submit" disabled={!inputMessage.trim() || isLoading}>
                    <Send className="h-4 w-4" />
                  </Button>
                </form>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {quickActions.map((action, index) => (
                <Button
                  key={index}
                  variant="outline"
                  className="w-full justify-start"
                  onClick={action.action}
                  disabled={isLoading}
                >
                  <action.icon className="h-4 w-4 mr-2" />
                  <div className="text-left">
                    <div className="font-medium">{action.title}</div>
                    <div className="text-xs text-gray-500">{action.description}</div>
                  </div>
                </Button>
              ))}
            </CardContent>
          </Card>

          {/* Project Info */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Project Info</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div>
                <label className="text-sm font-medium text-gray-700">Project Name</label>
                <p className="text-sm text-gray-900">{project.name}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-700">HVAC Model</label>
                <p className="text-sm text-gray-900">{project.hvac_model}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-700">Status</label>
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  {project.status}
                </span>
              </div>
              {project.description && (
                <div>
                  <label className="text-sm font-medium text-gray-700">Description</label>
                  <p className="text-sm text-gray-900">{project.description}</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default HVACChat; 