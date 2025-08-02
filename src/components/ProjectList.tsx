import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Project } from '../types';
import { Building2, Plus, Calendar, Thermometer, AlertTriangle, CheckCircle, Clock } from 'lucide-react';

interface ProjectListProps {
  projects: Project[];
  onProjectSelect: (project: Project) => void;
  onCreateNew: () => void;
}

const ProjectList: React.FC<ProjectListProps> = ({ projects, onProjectSelect, onCreateNew }) => {
  const [filterStatus, setFilterStatus] = useState<'all' | 'active' | 'resolved' | 'pending'>('all');

  const filteredProjects = projects.filter(project => 
    filterStatus === 'all' || project.status === filterStatus
  );

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return <AlertTriangle className="h-4 w-4 text-orange-600" />;
      case 'resolved':
        return <CheckCircle className="h-4 w-4 text-green-600" />;
      case 'pending':
        return <Clock className="h-4 w-4 text-blue-600" />;
      default:
        return <Clock className="h-4 w-4 text-gray-600" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-orange-100 text-orange-800';
      case 'resolved':
        return 'bg-green-100 text-green-800';
      case 'pending':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Building2 className="h-6 w-6 text-blue-600" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">HVAC Projects</h1>
              <p className="text-gray-600">Manage your HVAC projects and AI assistant sessions</p>
            </div>
          </div>
          <Button onClick={onCreateNew} className="bg-blue-600 hover:bg-blue-700">
            <Plus className="h-4 w-4 mr-2" />
            New Project
          </Button>
        </div>

        {/* Filter Tabs */}
        <div className="flex space-x-2 mb-6">
          {[
            { value: 'all', label: 'All Projects', count: projects.length },
            { value: 'active', label: 'Active', count: projects.filter(p => p.status === 'active').length },
            { value: 'resolved', label: 'Resolved', count: projects.filter(p => p.status === 'resolved').length },
            { value: 'pending', label: 'Pending', count: projects.filter(p => p.status === 'pending').length },
          ].map((filter) => (
            <Button
              key={filter.value}
              variant={filterStatus === filter.value ? 'default' : 'outline'}
              onClick={() => setFilterStatus(filter.value as any)}
              className="flex items-center space-x-2"
            >
              <span>{filter.label}</span>
              <span className="bg-white/20 px-2 py-1 rounded-full text-xs">
                {filter.count}
              </span>
            </Button>
          ))}
        </div>
      </div>

      {/* Projects Grid */}
      {filteredProjects.length === 0 ? (
        <Card className="text-center py-12">
          <CardContent>
            <div className="flex flex-col items-center space-y-4">
              <div className="p-4 bg-gray-100 rounded-full">
                <Building2 className="h-8 w-8 text-gray-400" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">No projects found</h3>
                <p className="text-gray-600 mb-4">
                  {filterStatus === 'all' 
                    ? "You haven't created any HVAC projects yet."
                    : `No ${filterStatus} projects found.`
                  }
                </p>
                <Button onClick={onCreateNew} className="bg-blue-600 hover:bg-blue-700">
                  <Plus className="h-4 w-4 mr-2" />
                  Create Your First Project
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredProjects.map((project) => (
            <Card 
              key={project.id} 
              className="hover:shadow-lg transition-shadow cursor-pointer"
              onClick={() => onProjectSelect(project)}
            >
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-2">
                    <Thermometer className="h-5 w-5 text-blue-600" />
                    <CardTitle className="text-lg">{project.name}</CardTitle>
                  </div>
                  <div className="flex items-center space-x-1">
                    {getStatusIcon(project.status)}
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(project.status)}`}>
                      {project.status}
                    </span>
                  </div>
                </div>
                <CardDescription className="text-sm text-gray-600">
                  {project.hvac_model}
                </CardDescription>
              </CardHeader>
              
              <CardContent className="space-y-4">
                {project.description && (
                  <div>
                    <p className="text-sm text-gray-700 line-clamp-2">
                      {project.description}
                    </p>
                  </div>
                )}
                
                <div>
                  <p className="text-sm text-gray-700 line-clamp-3">
                    <strong>Issue:</strong> {project.issue_description}
                  </p>
                </div>
                
                <div className="flex items-center justify-between text-xs text-gray-500">
                  <div className="flex items-center space-x-1">
                    <Calendar className="h-3 w-3" />
                    <span>{formatDate(project.created_at)}</span>
                  </div>
                </div>
                
                <Button 
                  className="w-full bg-blue-600 hover:bg-blue-700"
                  onClick={(e) => {
                    e.stopPropagation();
                    onProjectSelect(project);
                  }}
                >
                  Open AI Assistant
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Stats */}
      {projects.length > 0 && (
        <div className="mt-8 grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center space-x-2">
                <Building2 className="h-5 w-5 text-blue-600" />
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Projects</p>
                  <p className="text-2xl font-bold text-gray-900">{projects.length}</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center space-x-2">
                <AlertTriangle className="h-5 w-5 text-orange-600" />
                <div>
                  <p className="text-sm font-medium text-gray-600">Active</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {projects.filter(p => p.status === 'active').length}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center space-x-2">
                <CheckCircle className="h-5 w-5 text-green-600" />
                <div>
                  <p className="text-sm font-medium text-gray-600">Resolved</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {projects.filter(p => p.status === 'resolved').length}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center space-x-2">
                <Clock className="h-5 w-5 text-blue-600" />
                <div>
                  <p className="text-sm font-medium text-gray-600">Pending</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {projects.filter(p => p.status === 'pending').length}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default ProjectList; 