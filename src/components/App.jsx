import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { 
  Bot, 
  User, 
  BookOpen, 
  BarChart3, 
  FileText,
  Settings,
  LogIn,
  UserPlus
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

import ChatInterface from './ChatInterface';
import LearnerProfile from './LearnerProfile';
import Dashboard from './Dashboard';
import WritingWorkspace from './WritingWorkspace';

function App() {
  const [currentLearner, setCurrentLearner] = useState(null);
  const [currentSession, setCurrentSession] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [loginForm, setLoginForm] = useState({ userId: '', name: '' });
  const [isCreatingAccount, setIsCreatingAccount] = useState(false);

  const handleLogin = async () => {
    if (!loginForm.userId.trim()) return;

    try {
      setIsLoading(true);
      
      // For demo purposes, show create account option
      // In a real app, this would check against a database
      setIsCreatingAccount(true);
      
    } catch (error) {
      console.error('Error during login:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateAccount = async () => {
    if (!loginForm.userId.trim() || !loginForm.name.trim()) return;

    try {
      setIsLoading(true);
      
      // Create learner locally without API call
      const newLearner = {
        id: loginForm.userId,
        name: loginForm.name,
        course_type: 'IRW',
        proficiency_level: 'intermediate',
        preferred_language: 'en',
        created_at: new Date().toISOString(),
        progress: {
          writing_score: 3.5,
          sessions_completed: 0,
          total_time: 0
        }
      };
      
      setCurrentLearner(newLearner);
      setIsCreatingAccount(false);
      
    } catch (error) {
      console.error('Error creating account:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    setCurrentLearner(null);
    setCurrentSession(null);
    setLoginForm({ userId: '', name: '' });
    setIsCreatingAccount(false);
  };

  const handleSessionCreate = (session) => {
    setCurrentSession(session);
  };

  const handleSessionUpdate = (data) => {
    // Handle session updates from chat interface
    console.log('Session updated:', data);
  };

  if (!currentLearner) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center p-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="w-full max-w-md"
        >
          <Card className="shadow-xl border-0 bg-white/80 backdrop-blur-sm">
            <CardHeader className="text-center pb-2">
              <div className="bg-gradient-to-r from-blue-500 to-indigo-600 p-4 rounded-full w-20 h-20 mx-auto mb-4">
                <Bot className="w-12 h-12 text-white" />
              </div>
              <CardTitle className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                EvoWrite
              </CardTitle>
              <p className="text-gray-600 mt-2">
                AI-Powered Learning Platform
              </p>
            </CardHeader>
            <CardContent className="space-y-4">
              {!isCreatingAccount ? (
                <>
                  <div>
                    <Label htmlFor="userId" className="text-sm font-medium text-gray-700">
                      User ID
                    </Label>
                    <Input
                      id="userId"
                      type="text"
                      value={loginForm.userId}
                      onChange={(e) => setLoginForm(prev => ({ ...prev, userId: e.target.value }))}
                      placeholder="Enter your user ID"
                      className="mt-1"
                      onKeyPress={(e) => e.key === 'Enter' && handleLogin()}
                    />
                  </div>
                  
                  <Button
                    onClick={handleLogin}
                    disabled={isLoading || !loginForm.userId.trim()}
                    className="w-full bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700"
                  >
                    <LogIn className="w-4 h-4 mr-2" />
                    {isLoading ? 'Loading...' : 'Sign In'}
                  </Button>
                </>
              ) : (
                <>
                  <div className="text-center mb-4">
                    <h3 className="text-lg font-semibold text-gray-900">Create New Account</h3>
                    <p className="text-sm text-gray-600">User ID "{loginForm.userId}" not found</p>
                  </div>
                  
                  <div>
                    <Label htmlFor="name" className="text-sm font-medium text-gray-700">
                      Full Name
                    </Label>
                    <Input
                      id="name"
                      type="text"
                      value={loginForm.name}
                      onChange={(e) => setLoginForm(prev => ({ ...prev, name: e.target.value }))}
                      placeholder="Enter your full name"
                      className="mt-1"
                      onKeyPress={(e) => e.key === 'Enter' && handleCreateAccount()}
                    />
                  </div>
                  
                  <div className="flex space-x-3">
                    <Button
                      onClick={handleCreateAccount}
                      disabled={isLoading || !loginForm.name.trim()}
                      className="flex-1 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700"
                    >
                      <UserPlus className="w-4 h-4 mr-2" />
                      {isLoading ? 'Creating...' : 'Create Account'}
                    </Button>
                    <Button
                      variant="outline"
                      onClick={() => setIsCreatingAccount(false)}
                      className="flex-1"
                    >
                      Cancel
                    </Button>
                  </div>
                </>
              )}
              
              <div className="text-center pt-4 border-t border-gray-200">
                <p className="text-xs text-gray-500">
                  Powered by SAGE Framework & Meta-Llama-3-8B-Instruct
                </p>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="bg-gradient-to-r from-blue-500 to-indigo-600 p-2 rounded-lg">
                <Bot className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">SAGE EFL Writing Assistant</h1>
                <p className="text-sm text-gray-600">Welcome back, {currentLearner.name || 'Learner'}</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-sm font-medium text-gray-900">{currentLearner.name}</p>
                <p className="text-xs text-gray-500">ID: {currentLearner.user_id}</p>
              </div>
              <Button
                variant="outline"
                onClick={handleLogout}
                size="sm"
              >
                Sign Out
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">
        <Tabs defaultValue="chat" className="h-[calc(100vh-80px)]">
          <div className="border-b bg-white px-6">
            <TabsList className="grid w-full max-w-md grid-cols-4">
              <TabsTrigger value="chat" className="flex items-center space-x-2">
                <Bot className="w-4 h-4" />
                <span className="hidden sm:inline">Chat</span>
              </TabsTrigger>
              <TabsTrigger value="writing" className="flex items-center space-x-2">
                <FileText className="w-4 h-4" />
                <span className="hidden sm:inline">Writing</span>
              </TabsTrigger>
              <TabsTrigger value="dashboard" className="flex items-center space-x-2">
                <BarChart3 className="w-4 h-4" />
                <span className="hidden sm:inline">Analytics</span>
              </TabsTrigger>
              <TabsTrigger value="profile" className="flex items-center space-x-2">
                <User className="w-4 h-4" />
                <span className="hidden sm:inline">Profile</span>
              </TabsTrigger>
            </TabsList>
          </div>

          <div className="h-[calc(100vh-140px)]">
            <TabsContent value="chat" className="h-full m-0">
              <ChatInterface
                learnerId={currentLearner.id}
                sessionId={currentSession?.session_id}
                onSessionUpdate={handleSessionUpdate}
              />
            </TabsContent>

            <TabsContent value="writing" className="h-full m-0">
              <WritingWorkspace
                learnerId={currentLearner.id}
                onSessionCreate={handleSessionCreate}
              />
            </TabsContent>

            <TabsContent value="dashboard" className="h-full m-0 p-6 overflow-auto">
              <Dashboard learnerId={currentLearner.id} />
            </TabsContent>

            <TabsContent value="profile" className="h-full m-0 p-6 overflow-auto">
              <LearnerProfile
                learnerId={currentLearner.id}
                onProfileUpdate={setCurrentLearner}
              />
            </TabsContent>
          </div>
        </Tabs>
      </main>
    </div>
  );
}

export default App;
