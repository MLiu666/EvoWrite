import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { Separator } from './ui/separator';
import { 
  TrendingUp, 
  MessageSquare, 
  Star, 
  BookOpen, 
  Target,
  Calendar,
  Award,
  BarChart3,
  PieChart,
  Activity,
  CheckCircle,
  Clock,
  Users
} from 'lucide-react';
// Removed recharts dependency for now
import { motion } from 'framer-motion';

const Dashboard = ({ learnerId }) => {
  const [analytics, setAnalytics] = useState(null);
  const [interactions, setInteractions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (learnerId) {
      fetchAnalytics();
      fetchRecentInteractions();
    }
  }, [learnerId]);

  const fetchAnalytics = async () => {
    try {
      const response = await fetch(`/api/sage/learners/${learnerId}/analytics`);
      const data = await response.json();
      
      if (response.ok) {
        setAnalytics(data);
      } else {
        console.error('Failed to fetch analytics:', data.error);
      }
    } catch (error) {
      console.error('Error fetching analytics:', error);
    }
  };

  const fetchRecentInteractions = async () => {
    try {
      const response = await fetch(`/api/sage/learners/${learnerId}/interactions?limit=10`);
      const data = await response.json();
      
      if (response.ok) {
        setInteractions(data.interactions);
      } else {
        console.error('Failed to fetch interactions:', data.error);
      }
    } catch (error) {
      console.error('Error fetching interactions:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Mock data for charts (in a real app, this would come from the API)
  const progressData = [
    { week: 'Week 1', score: 3.8 },
    { week: 'Week 2', score: 4.1 },
    { week: 'Week 3', score: 4.3 },
    { week: 'Week 4', score: 4.0 },
    { week: 'Week 5', score: 4.2 },
    { week: 'Week 6', score: 4.4 },
    { week: 'Week 7', score: 4.5 },
  ];

  const intentData = [
    { name: 'Answer', value: 35, color: '#3B82F6' },
    { name: 'Language Use', value: 25, color: '#10B981' },
    { name: 'Revision', value: 20, color: '#8B5CF6' },
    { name: 'Information', value: 15, color: '#F59E0B' },
    { name: 'Other', value: 5, color: '#6B7280' },
  ];

  const qualityData = [
    { metric: 'Clarity', score: 85 },
    { metric: 'Accuracy', score: 92 },
    { metric: 'Helpfulness', score: 88 },
    { metric: 'Engagement', score: 79 },
  ];

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <Card className="bg-gradient-to-r from-blue-50 to-blue-100 border-blue-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-blue-600">Total Interactions</p>
                  <p className="text-2xl font-bold text-blue-900">
                    {analytics?.personalization_data?.interaction_count || 0}
                  </p>
                </div>
                <MessageSquare className="w-8 h-8 text-blue-500" />
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <Card className="bg-gradient-to-r from-green-50 to-green-100 border-green-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-green-600">Average Rating</p>
                  <p className="text-2xl font-bold text-green-900">
                    {analytics?.personalization_data?.avg_rating?.toFixed(1) || '0.0'}
                  </p>
                </div>
                <Star className="w-8 h-8 text-green-500" />
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <Card className="bg-gradient-to-r from-purple-50 to-purple-100 border-purple-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-purple-600">Essays Completed</p>
                  <p className="text-2xl font-bold text-purple-900">
                    {analytics?.analytics?.essays_completed || 0}
                  </p>
                </div>
                <BookOpen className="w-8 h-8 text-purple-500" />
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <Card className="bg-gradient-to-r from-orange-50 to-orange-100 border-orange-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-orange-600">Active Sessions</p>
                  <p className="text-2xl font-bold text-orange-900">
                    {analytics?.personalization_data?.session_count || 0}
                  </p>
                </div>
                <Activity className="w-8 h-8 text-orange-500" />
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Progress Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <TrendingUp className="w-5 h-5" />
                <span>Learning Progress</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-48 bg-gray-100 rounded-lg flex items-center justify-center">
                <span className="text-gray-500">Progress Chart (recharts removed)</span>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Intent Distribution */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <PieChart className="w-5 h-5" />
                <span>Interaction Types</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-48 bg-gray-100 rounded-lg flex items-center justify-center">
                <span className="text-gray-500">Pie Chart (recharts removed)</span>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Quality Metrics */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <BarChart3 className="w-5 h-5" />
                <span>Quality Metrics</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {qualityData.map((metric, index) => (
                <div key={metric.metric} className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="font-medium">{metric.metric}</span>
                    <span className="text-gray-500">{metric.score}%</span>
                  </div>
                  <Progress value={metric.score} className="h-2" />
                </div>
              ))}
            </CardContent>
          </Card>
        </motion.div>

        {/* Recent Activity */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="lg:col-span-2"
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Clock className="w-5 h-5" />
                <span>Recent Interactions</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {interactions.slice(0, 5).map((interaction, index) => (
                  <div key={interaction.id} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                    <div className="flex-shrink-0">
                      {interaction.intent_type === 'Answer' && <MessageSquare className="w-5 h-5 text-blue-500" />}
                      {interaction.intent_type === 'R Language Use' && <BookOpen className="w-5 h-5 text-green-500" />}
                      {interaction.intent_type === 'R Revision' && <Target className="w-5 h-5 text-purple-500" />}
                      {!['Answer', 'R Language Use', 'R Revision'].includes(interaction.intent_type) && 
                        <Activity className="w-5 h-5 text-gray-500" />}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <p className="text-sm font-medium text-gray-900 truncate">
                          {interaction.intent_type || 'General'}
                        </p>
                        <div className="flex items-center space-x-2">
                          {interaction.user_rating && (
                            <div className="flex items-center space-x-1">
                              <Star className="w-3 h-3 text-yellow-400 fill-current" />
                              <span className="text-xs text-gray-500">{interaction.user_rating}</span>
                            </div>
                          )}
                          <span className="text-xs text-gray-500">
                            {new Date(interaction.created_at).toLocaleDateString()}
                          </span>
                        </div>
                      </div>
                      <p className="text-sm text-gray-600 truncate mt-1">
                        {interaction.user_input?.substring(0, 100)}...
                      </p>
                    </div>
                  </div>
                ))}
                
                {interactions.length === 0 && (
                  <div className="text-center py-8">
                    <MessageSquare className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                    <p className="text-gray-500">No interactions yet</p>
                    <p className="text-sm text-gray-400">Start chatting to see your activity here</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Learning Insights */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.9 }}
      >
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Award className="w-5 h-5" />
              <span>Learning Insights</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="bg-blue-100 p-3 rounded-full w-16 h-16 mx-auto mb-3 flex items-center justify-center">
                  <TrendingUp className="w-8 h-8 text-blue-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Consistent Progress</h3>
                <p className="text-sm text-gray-600">
                  Your writing skills are improving steadily with regular practice and feedback.
                </p>
              </div>
              
              <div className="text-center">
                <div className="bg-green-100 p-3 rounded-full w-16 h-16 mx-auto mb-3 flex items-center justify-center">
                  <Target className="w-8 h-8 text-green-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Goal-Oriented</h3>
                <p className="text-sm text-gray-600">
                  You're effectively using self-regulated learning strategies to achieve your goals.
                </p>
              </div>
              
              <div className="text-center">
                <div className="bg-purple-100 p-3 rounded-full w-16 h-16 mx-auto mb-3 flex items-center justify-center">
                  <Users className="w-8 h-8 text-purple-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Active Learner</h3>
                <p className="text-sm text-gray-600">
                  Your engagement level is excellent, showing dedication to improving your writing.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
};

export default Dashboard;

