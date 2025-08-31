import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Badge } from './ui/badge';
import { Separator } from './ui/separator';
import { 
  User, 
  BookOpen, 
  Target, 
  Globe, 
  TrendingUp,
  Calendar,
  Award,
  Settings,
  Save,
  Edit3
} from 'lucide-react';
import { motion } from 'framer-motion';

const LearnerProfile = ({ learnerId, onProfileUpdate }) => {
  const [profile, setProfile] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    course_type: '',
    proficiency_level: '',
    preferred_language: '',
    learning_goals: ''
  });

  useEffect(() => {
    if (learnerId) {
      fetchProfile();
    }
  }, [learnerId]);

  const fetchProfile = async () => {
    try {
      setIsLoading(true);
      // Get profile from localStorage instead of API
      const savedUser = localStorage.getItem('evowrite_user');
      if (savedUser) {
        const user = JSON.parse(savedUser);
        if (user.id === learnerId) {
          setProfile(user);
          setFormData({
            name: user.name || '',
            course_type: user.course_type || '',
            proficiency_level: user.proficiency_level || '',
            preferred_language: user.preferred_language || '',
            learning_goals: user.learning_goals || ''
          });
        }
      }
    } catch (error) {
      console.error('Error fetching profile:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      setIsSaving(true);
      // Update profile in localStorage instead of API
      const savedUser = localStorage.getItem('evowrite_user');
      if (savedUser) {
        const user = JSON.parse(savedUser);
        if (user.id === learnerId) {
          const updatedUser = {
            ...user,
            ...formData
          };
          
          // Save updated user to localStorage
          localStorage.setItem('evowrite_user', JSON.stringify(updatedUser));
          
          setProfile(updatedUser);
          setIsEditing(false);
          if (onProfileUpdate) {
            onProfileUpdate(updatedUser);
          }
        }
      }
    } catch (error) {
      console.error('Error updating profile:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const getCourseTypeLabel = (courseType) => {
    const labels = {
      'SW': 'Scientific Writing',
      'AW': 'Advanced Writing',
      'IRW': 'Intermediate Reading & Writing'
    };
    return labels[courseType] || courseType;
  };

  const getProficiencyColor = (level) => {
    const colors = {
      'beginner': 'bg-yellow-100 text-yellow-800 border-yellow-200',
      'intermediate': 'bg-blue-100 text-blue-800 border-blue-200',
      'advanced': 'bg-green-100 text-green-800 border-green-200'
    };
    return colors[level] || 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const getLanguageFlag = (lang) => {
    const flags = {
      'en': '🇺🇸',
      'zh': '🇨🇳',
      'mixed': '🌐'
    };
    return flags[lang] || '🌐';
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!profile) {
    return (
      <Card className="max-w-2xl mx-auto">
        <CardContent className="p-6 text-center">
          <User className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">Profile Not Found</h3>
          <p className="text-gray-500">Unable to load learner profile.</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Profile Header */}
      <Card className="bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="bg-gradient-to-r from-blue-500 to-indigo-600 p-3 rounded-full">
                <User className="w-8 h-8 text-white" />
              </div>
              <div>
                <CardTitle className="text-2xl text-gray-900">
                  {profile.name || 'Learner Profile'}
                </CardTitle>
                <p className="text-gray-600">ID: {profile.user_id}</p>
              </div>
            </div>
            <Button
              onClick={() => setIsEditing(!isEditing)}
              variant={isEditing ? "outline" : "default"}
              className="flex items-center space-x-2"
            >
              <Edit3 className="w-4 h-4" />
              <span>{isEditing ? 'Cancel' : 'Edit Profile'}</span>
            </Button>
          </div>
        </CardHeader>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Profile Information */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Settings className="w-5 h-5" />
                <span>Profile Information</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {isEditing ? (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="space-y-4"
                >
                  <div>
                    <Label htmlFor="name">Full Name</Label>
                    <Input
                      id="name"
                      value={formData.name}
                      onChange={(e) => handleInputChange('name', e.target.value)}
                      placeholder="Enter your full name"
                    />
                  </div>

                  <div>
                    <Label htmlFor="course_type">Course Type</Label>
                    <Select
                      value={formData.course_type}
                      onValueChange={(value) => handleInputChange('course_type', value)}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select course type" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="IRW">Intermediate Reading & Writing</SelectItem>
                        <SelectItem value="AW">Advanced Writing</SelectItem>
                        <SelectItem value="SW">Scientific Writing</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label htmlFor="proficiency_level">Proficiency Level</Label>
                    <Select
                      value={formData.proficiency_level}
                      onValueChange={(value) => handleInputChange('proficiency_level', value)}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select proficiency level" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="beginner">Beginner</SelectItem>
                        <SelectItem value="intermediate">Intermediate</SelectItem>
                        <SelectItem value="advanced">Advanced</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label htmlFor="preferred_language">Preferred Language</Label>
                    <Select
                      value={formData.preferred_language}
                      onValueChange={(value) => handleInputChange('preferred_language', value)}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select preferred language" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="en">English</SelectItem>
                        <SelectItem value="zh">Chinese</SelectItem>
                        <SelectItem value="mixed">Mixed (Code-switching)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label htmlFor="learning_goals">Learning Goals</Label>
                    <Textarea
                      id="learning_goals"
                      value={formData.learning_goals}
                      onChange={(e) => handleInputChange('learning_goals', e.target.value)}
                      placeholder="Describe your learning goals and objectives..."
                      className="min-h-[100px]"
                    />
                  </div>

                  <div className="flex space-x-3 pt-4">
                    <Button
                      onClick={handleSave}
                      disabled={isSaving}
                      className="flex items-center space-x-2"
                    >
                      <Save className="w-4 h-4" />
                      <span>{isSaving ? 'Saving...' : 'Save Changes'}</span>
                    </Button>
                    <Button
                      variant="outline"
                      onClick={() => setIsEditing(false)}
                    >
                      Cancel
                    </Button>
                  </div>
                </motion.div>
              ) : (
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <Label className="text-sm font-medium text-gray-500">Course Type</Label>
                      <div className="flex items-center space-x-2 mt-1">
                        <BookOpen className="w-4 h-4 text-blue-500" />
                        <span className="font-medium">{getCourseTypeLabel(profile.course_type)}</span>
                      </div>
                    </div>

                    <div>
                      <Label className="text-sm font-medium text-gray-500">Proficiency Level</Label>
                      <div className="mt-1">
                        <Badge className={getProficiencyColor(profile.proficiency_level)}>
                          <TrendingUp className="w-3 h-3 mr-1" />
                          {profile.proficiency_level?.charAt(0).toUpperCase() + profile.proficiency_level?.slice(1)}
                        </Badge>
                      </div>
                    </div>

                    <div>
                      <Label className="text-sm font-medium text-gray-500">Preferred Language</Label>
                      <div className="flex items-center space-x-2 mt-1">
                        <span className="text-lg">{getLanguageFlag(profile.preferred_language)}</span>
                        <span className="font-medium">
                          {profile.preferred_language === 'en' ? 'English' :
                           profile.preferred_language === 'zh' ? 'Chinese' :
                           profile.preferred_language === 'mixed' ? 'Mixed' : 'Not specified'}
                        </span>
                      </div>
                    </div>

                    <div>
                      <Label className="text-sm font-medium text-gray-500">Member Since</Label>
                      <div className="flex items-center space-x-2 mt-1">
                        <Calendar className="w-4 h-4 text-gray-500" />
                        <span className="font-medium">
                          {new Date(profile.created_at).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  </div>

                  {profile.learning_goals && (
                    <div>
                      <Label className="text-sm font-medium text-gray-500">Learning Goals</Label>
                      <div className="mt-2 p-3 bg-gray-50 rounded-lg">
                        <p className="text-gray-700">{profile.learning_goals}</p>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Profile Stats */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Award className="w-5 h-5" />
                <span>Profile Stats</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">
                  {profile.proficiency_level === 'advanced' ? '85%' :
                   profile.proficiency_level === 'intermediate' ? '65%' : '45%'}
                </div>
                <p className="text-sm text-gray-500">Overall Progress</p>
              </div>

              <Separator />

              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Profile Completion</span>
                  <span className="text-sm font-medium">
                    {profile.name && profile.learning_goals ? '100%' : '75%'}
                  </span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Last Updated</span>
                  <span className="text-sm font-medium">
                    {new Date(profile.updated_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Target className="w-5 h-5" />
                <span>Quick Actions</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <Button variant="outline" className="w-full justify-start">
                <BookOpen className="w-4 h-4 mr-2" />
                View Learning Analytics
              </Button>
              <Button variant="outline" className="w-full justify-start">
                <TrendingUp className="w-4 h-4 mr-2" />
                Progress Report
              </Button>
              <Button variant="outline" className="w-full justify-start">
                <Settings className="w-4 h-4 mr-2" />
                Account Settings
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default LearnerProfile;

