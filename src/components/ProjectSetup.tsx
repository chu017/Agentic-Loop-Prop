import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { mockData } from '../services/api';
import { Project } from '../types';
import { Building2, Settings, Thermometer, AlertTriangle } from 'lucide-react';

interface ProjectSetupProps {
  onProjectCreated: (project: Project) => void;
}

const ProjectSetup: React.FC<ProjectSetupProps> = ({ onProjectCreated }) => {
  const [projectName, setProjectName] = useState('');
  const [projectDescription, setProjectDescription] = useState('');
  const [hvacModel, setHvacModel] = useState('');
  const [issueDescription, setIssueDescription] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!projectName || !hvacModel || !issueDescription) {
      alert('Please fill in all required fields');
      return;
    }

    setIsSubmitting(true);

    try {
      const newProject: Project = {
        id: `project-${Date.now()}`,
        name: projectName,
        description: projectDescription,
        hvac_model: hvacModel,
        issue_description: issueDescription,
        created_at: new Date().toISOString(),
        status: 'active',
      };

      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      onProjectCreated(newProject);
    } catch (error) {
      console.error('Error creating project:', error);
      alert('Failed to create project. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <Card className="shadow-lg">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-4">
            <div className="p-3 bg-blue-100 rounded-full">
              <Building2 className="h-8 w-8 text-blue-600" />
            </div>
          </div>
          <CardTitle className="text-2xl font-bold text-gray-900">
            HVAC Project Setup
          </CardTitle>
          <CardDescription className="text-gray-600">
            Create a new HVAC project to get started with AI-powered diagnostics and optimization
          </CardDescription>
        </CardHeader>
        
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Project Information */}
            <div className="space-y-4">
              <div>
                <label htmlFor="projectName" className="block text-sm font-medium text-gray-700 mb-2">
                  Project Name *
                </label>
                <Input
                  id="projectName"
                  value={projectName}
                  onChange={(e) => setProjectName(e.target.value)}
                  placeholder="Enter project name"
                  required
                />
              </div>

              <div>
                <label htmlFor="projectDescription" className="block text-sm font-medium text-gray-700 mb-2">
                  Project Description
                </label>
                <Textarea
                  id="projectDescription"
                  value={projectDescription}
                  onChange={(e) => setProjectDescription(e.target.value)}
                  placeholder="Describe the project scope and requirements"
                  rows={3}
                />
              </div>
            </div>

            {/* HVAC System Information */}
            <div className="space-y-4">
              <div className="flex items-center space-x-2 mb-4">
                <Settings className="h-5 w-5 text-gray-600" />
                <h3 className="text-lg font-semibold text-gray-900">HVAC System Details</h3>
              </div>

              <div>
                <label htmlFor="hvacModel" className="block text-sm font-medium text-gray-700 mb-2">
                  HVAC Model *
                </label>
                <Select value={hvacModel} onValueChange={setHvacModel}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select HVAC model" />
                  </SelectTrigger>
                  <SelectContent>
                    {mockData.hvacModels.map((model) => (
                      <SelectItem key={model} value={model}>
                        {model}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* Issue Description */}
            <div className="space-y-4">
              <div className="flex items-center space-x-2 mb-4">
                <AlertTriangle className="h-5 w-5 text-orange-600" />
                <h3 className="text-lg font-semibold text-gray-900">Issue Description</h3>
              </div>

              <div>
                <label htmlFor="issueDescription" className="block text-sm font-medium text-gray-700 mb-2">
                  Describe the Issue *
                </label>
                <Textarea
                  id="issueDescription"
                  value={issueDescription}
                  onChange={(e) => setIssueDescription(e.target.value)}
                  placeholder="Describe the HVAC system issue, symptoms, or concerns..."
                  rows={4}
                  required
                />
              </div>
            </div>

            {/* Submit Button */}
            <div className="pt-4">
              <Button
                type="submit"
                className="w-full bg-blue-600 hover:bg-blue-700 text-white"
                disabled={isSubmitting}
              >
                {isSubmitting ? (
                  <div className="flex items-center space-x-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    <span>Creating Project...</span>
                  </div>
                ) : (
                  <div className="flex items-center space-x-2">
                    <Thermometer className="h-4 w-4" />
                    <span>Create Project & Start AI Assistant</span>
                  </div>
                )}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default ProjectSetup; 