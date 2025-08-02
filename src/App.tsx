import React, { useState, useEffect } from 'react';
import { Project } from './types';
import ProjectList from './components/ProjectList';
import ProjectSetup from './components/ProjectSetup';
import HVACChat from './components/HVACChat';
import { systemAPI } from './services/api';
import { Activity, AlertTriangle, CheckCircle } from 'lucide-react';

type AppView = 'projects' | 'setup' | 'chat';

const App: React.FC = () => {
  const [currentView, setCurrentView] = useState<AppView>('projects');
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [systemStatus, setSystemStatus] = useState<'healthy' | 'error' | 'loading'>('loading');

  useEffect(() => {
    // Load projects from localStorage
    const savedProjects = localStorage.getItem('hvac-projects');
    if (savedProjects) {
      try {
        setProjects(JSON.parse(savedProjects));
      } catch (error) {
        console.error('Error loading projects:', error);
      }
    }

    // Check system health
    checkSystemHealth();
  }, []);

  useEffect(() => {
    // Save projects to localStorage
    localStorage.setItem('hvac-projects', JSON.stringify(projects));
  }, [projects]);

  const checkSystemHealth = async () => {
    try {
      setSystemStatus('loading');
      const response = await systemAPI.getHealth();
      setSystemStatus(response.data?.status === 'healthy' ? 'healthy' : 'error');
    } catch (error) {
      console.error('System health check failed:', error);
      setSystemStatus('error');
    }
  };

  const handleCreateProject = () => {
    setCurrentView('setup');
  };

  const handleProjectCreated = (project: Project) => {
    setProjects(prev => [project, ...prev]);
    setSelectedProject(project);
    setCurrentView('chat');
  };

  const handleProjectSelect = (project: Project) => {
    setSelectedProject(project);
    setCurrentView('chat');
  };

  const handleBackToProjects = () => {
    setCurrentView('projects');
    setSelectedProject(null);
  };

  const getStatusIcon = () => {
    switch (systemStatus) {
      case 'healthy':
        return <CheckCircle className="h-4 w-4 text-green-600" />;
      case 'error':
        return <AlertTriangle className="h-4 w-4 text-red-600" />;
      case 'loading':
        return <Activity className="h-4 w-4 text-blue-600 animate-spin" />;
      default:
        return <Activity className="h-4 w-4 text-gray-600" />;
    }
  };

  const getStatusText = () => {
    switch (systemStatus) {
      case 'healthy':
        return 'System Online';
      case 'error':
        return 'System Offline';
      case 'loading':
        return 'Checking Status...';
      default:
        return 'Unknown Status';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <Activity className="h-6 w-6 text-blue-600" />
                </div>
                <h1 className="text-xl font-bold text-gray-900">HVAC AI Assistant</h1>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 text-sm">
                {getStatusIcon()}
                <span className={systemStatus === 'error' ? 'text-red-600' : 'text-gray-600'}>
                  {getStatusText()}
                </span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">
        {currentView === 'projects' && (
          <ProjectList
            projects={projects}
            onProjectSelect={handleProjectSelect}
            onCreateNew={handleCreateProject}
          />
        )}

        {currentView === 'setup' && (
          <ProjectSetup onProjectCreated={handleProjectCreated} />
        )}

        {currentView === 'chat' && selectedProject && (
          <HVACChat
            project={selectedProject}
            onBack={handleBackToProjects}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between text-sm text-gray-600">
            <div className="flex items-center space-x-4">
              <span>HVAC AI Assistant v1.0</span>
              <span>•</span>
              <span>Powered by AI & Thermia Integration</span>
            </div>
            <div className="flex items-center space-x-4">
              <span>N8N Compatible</span>
              <span>•</span>
              <span>TypeScript & shadcn/ui</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App; 