import React, { useState, useEffect, useRef } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Badge } from './ui/badge';
import { Separator } from './ui/separator';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { 
  Save, 
  FileText, 
  Target, 
  Clock, 
  BarChart3,
  Eye,
  Edit3,
  Download,
  Upload,
  Lightbulb,
  CheckCircle,
  AlertCircle
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const WritingWorkspace = ({ learnerId, onSessionCreate }) => {
  const [currentSession, setCurrentSession] = useState(null);
  const [essayTitle, setEssayTitle] = useState('');
  const [essayContent, setEssayContent] = useState('');
  const [writingGoal, setWritingGoal] = useState('');
  const [wordCount, setWordCount] = useState(0);
  const [isSaving, setIsSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState(null);
  const [isPreviewMode, setIsPreviewMode] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const textareaRef = useRef(null);

  useEffect(() => {
    const words = essayContent.trim().split(/\s+/).filter(word => word.length > 0);
    setWordCount(words.length);
  }, [essayContent]);

  useEffect(() => {
    // Auto-save every 30 seconds
    const autoSaveInterval = setInterval(() => {
      if (currentSession && (essayContent || essayTitle)) {
        handleSave(true);
      }
    }, 30000);

    return () => clearInterval(autoSaveInterval);
  }, [currentSession, essayContent, essayTitle]);

  const createNewSession = async () => {
    try {
      const response = await fetch('/api/sage/sessions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          learner_id: learnerId,
          essay_title: essayTitle || 'Untitled Essay',
          writing_goal: writingGoal,
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        setCurrentSession(data.session);
        if (onSessionCreate) {
          onSessionCreate(data.session);
        }
      } else {
        console.error('Failed to create session:', data.error);
      }
    } catch (error) {
      console.error('Error creating session:', error);
    }
  };

  const handleSave = async (isAutoSave = false) => {
    if (!currentSession) {
      await createNewSession();
      return;
    }

    try {
      setIsSaving(true);
      const response = await fetch(`/api/sage/sessions/${currentSession.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          essay_title: essayTitle,
          essay_content: essayContent,
          writing_goal: writingGoal,
          status: 'in_progress',
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        setCurrentSession(data.session);
        setLastSaved(new Date());
        if (!isAutoSave) {
          // Show success feedback for manual saves
        }
      } else {
        console.error('Failed to save session:', data.error);
      }
    } catch (error) {
      console.error('Error saving session:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleComplete = async () => {
    if (!currentSession) return;

    try {
      const response = await fetch(`/api/sage/sessions/${currentSession.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          essay_title: essayTitle,
          essay_content: essayContent,
          writing_goal: writingGoal,
          status: 'completed',
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        setCurrentSession(data.session);
        // Show completion feedback
      }
    } catch (error) {
      console.error('Error completing session:', error);
    }
  };

  const generateSuggestions = () => {
    // Mock suggestions based on content analysis
    const mockSuggestions = [
      {
        type: 'structure',
        title: 'Add a stronger thesis statement',
        description: 'Consider adding a clear thesis statement at the end of your introduction.',
        icon: <Target className="w-4 h-4" />,
        color: 'bg-blue-100 text-blue-800'
      },
      {
        type: 'language',
        title: 'Vary sentence structure',
        description: 'Try using more complex sentence structures to improve flow.',
        icon: <Edit3 className="w-4 h-4" />,
        color: 'bg-green-100 text-green-800'
      },
      {
        type: 'content',
        title: 'Add supporting evidence',
        description: 'Include more specific examples to support your arguments.',
        icon: <Lightbulb className="w-4 h-4" />,
        color: 'bg-yellow-100 text-yellow-800'
      }
    ];

    setSuggestions(mockSuggestions);
  };

  const insertText = (text) => {
    const textarea = textareaRef.current;
    if (textarea) {
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const newContent = essayContent.substring(0, start) + text + essayContent.substring(end);
      setEssayContent(newContent);
      
      // Set cursor position after inserted text
      setTimeout(() => {
        textarea.selectionStart = textarea.selectionEnd = start + text.length;
        textarea.focus();
      }, 0);
    }
  };

  const getWordCountColor = () => {
    if (wordCount < 100) return 'text-red-500';
    if (wordCount < 300) return 'text-yellow-500';
    return 'text-green-500';
  };

  const getProgressPercentage = () => {
    const targetWords = 500; // Assume 500 words as target
    return Math.min((wordCount / targetWords) * 100, 100);
  };

  return (
    <div className="h-full flex flex-col bg-gradient-to-br from-gray-50 to-white">
      {/* Header */}
      <div className="bg-white shadow-sm border-b p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-gradient-to-r from-purple-500 to-indigo-600 p-2 rounded-lg">
              <FileText className="w-6 h-6 text-white" />
            </div>
            <div>
              <h2 className="text-xl font-semibold text-gray-900">Writing Workspace</h2>
              <p className="text-sm text-gray-500">
                {currentSession ? `Session: ${currentSession.session_id.substring(0, 8)}...` : 'New Writing Session'}
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            <Badge variant="outline" className={getWordCountColor()}>
              <BarChart3 className="w-3 h-3 mr-1" />
              {wordCount} words
            </Badge>
            
            {lastSaved && (
              <Badge variant="outline" className="text-gray-600">
                <Clock className="w-3 h-3 mr-1" />
                Saved {lastSaved.toLocaleTimeString()}
              </Badge>
            )}
            
            <Button
              onClick={() => setIsPreviewMode(!isPreviewMode)}
              variant="outline"
              size="sm"
            >
              <Eye className="w-4 h-4 mr-2" />
              {isPreviewMode ? 'Edit' : 'Preview'}
            </Button>
          </div>
        </div>
      </div>

      <div className="flex-1 flex overflow-hidden">
        {/* Main Writing Area */}
        <div className="flex-1 flex flex-col p-6">
          <div className="space-y-4 mb-6">
            {/* Essay Title */}
            <div>
              <Label htmlFor="title" className="text-sm font-medium text-gray-700">
                Essay Title
              </Label>
              <Input
                id="title"
                value={essayTitle}
                onChange={(e) => setEssayTitle(e.target.value)}
                placeholder="Enter your essay title..."
                className="mt-1 text-lg font-medium"
                disabled={isPreviewMode}
              />
            </div>

            {/* Writing Goal */}
            <div>
              <Label htmlFor="goal" className="text-sm font-medium text-gray-700">
                Writing Goal
              </Label>
              <Select
                value={writingGoal}
                onValueChange={setWritingGoal}
                disabled={isPreviewMode}
              >
                <SelectTrigger className="mt-1">
                  <SelectValue placeholder="Select your writing goal..." />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="argumentative">Argumentative Essay</SelectItem>
                  <SelectItem value="descriptive">Descriptive Writing</SelectItem>
                  <SelectItem value="narrative">Narrative Essay</SelectItem>
                  <SelectItem value="expository">Expository Writing</SelectItem>
                  <SelectItem value="creative">Creative Writing</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Writing Area */}
          <div className="flex-1 flex flex-col">
            <div className="flex items-center justify-between mb-3">
              <Label className="text-sm font-medium text-gray-700">
                Essay Content
              </Label>
              <div className="flex items-center space-x-2">
                <div className="w-32 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-gradient-to-r from-purple-500 to-indigo-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${getProgressPercentage()}%` }}
                  ></div>
                </div>
                <span className="text-xs text-gray-500">
                  {getProgressPercentage().toFixed(0)}%
                </span>
              </div>
            </div>

            {isPreviewMode ? (
              <Card className="flex-1 overflow-auto">
                <CardContent className="p-6">
                  <div className="prose prose-lg max-w-none">
                    <h1 className="text-2xl font-bold mb-6">{essayTitle || 'Untitled Essay'}</h1>
                    <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
                      {essayContent || 'Start writing your essay...'}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ) : (
              <Textarea
                ref={textareaRef}
                value={essayContent}
                onChange={(e) => setEssayContent(e.target.value)}
                placeholder="Start writing your essay here..."
                className="flex-1 resize-none text-base leading-relaxed p-4 border-2 border-gray-200 focus:border-purple-500 focus:ring-purple-500"
              />
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex items-center justify-between mt-6 pt-4 border-t border-gray-200">
            <div className="flex items-center space-x-3">
              <Button
                onClick={() => handleSave(false)}
                disabled={isSaving}
                variant="outline"
              >
                <Save className="w-4 h-4 mr-2" />
                {isSaving ? 'Saving...' : 'Save Draft'}
              </Button>
              
              <Button
                onClick={handleComplete}
                disabled={!essayContent.trim() || !currentSession}
                className="bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700"
              >
                <CheckCircle className="w-4 h-4 mr-2" />
                Complete Essay
              </Button>
            </div>

            <div className="flex items-center space-x-2">
              <Button variant="outline" size="sm">
                <Upload className="w-4 h-4 mr-2" />
                Import
              </Button>
              <Button variant="outline" size="sm">
                <Download className="w-4 h-4 mr-2" />
                Export
              </Button>
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="w-80 bg-white border-l border-gray-200 p-6 overflow-auto">
          <div className="space-y-6">
            {/* Writing Statistics */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Writing Statistics</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Words</span>
                  <span className={`font-semibold ${getWordCountColor()}`}>{wordCount}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Characters</span>
                  <span className="font-semibold">{essayContent.length}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Paragraphs</span>
                  <span className="font-semibold">
                    {essayContent.split('\n\n').filter(p => p.trim()).length}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Reading Time</span>
                  <span className="font-semibold">{Math.ceil(wordCount / 200)} min</span>
                </div>
              </CardContent>
            </Card>

            {/* Writing Suggestions */}
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg">Suggestions</CardTitle>
                  <Button
                    onClick={generateSuggestions}
                    variant="outline"
                    size="sm"
                  >
                    <Lightbulb className="w-4 h-4" />
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <AnimatePresence>
                  {suggestions.length > 0 ? (
                    <div className="space-y-3">
                      {suggestions.map((suggestion, index) => (
                        <motion.div
                          key={index}
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          exit={{ opacity: 0, y: -20 }}
                          className="p-3 bg-gray-50 rounded-lg"
                        >
                          <div className="flex items-start space-x-2">
                            <Badge className={suggestion.color}>
                              {suggestion.icon}
                            </Badge>
                            <div className="flex-1">
                              <h4 className="text-sm font-medium text-gray-900">
                                {suggestion.title}
                              </h4>
                              <p className="text-xs text-gray-600 mt-1">
                                {suggestion.description}
                              </p>
                            </div>
                          </div>
                        </motion.div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-6">
                      <Lightbulb className="w-8 h-8 text-gray-300 mx-auto mb-2" />
                      <p className="text-sm text-gray-500">
                        Click the lightbulb to get writing suggestions
                      </p>
                    </div>
                  )}
                </AnimatePresence>
              </CardContent>
            </Card>

            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <Button
                  variant="outline"
                  size="sm"
                  className="w-full justify-start"
                  onClick={() => insertText('\n\nIn conclusion, ')}
                >
                  Add Conclusion
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  className="w-full justify-start"
                  onClick={() => insertText('\n\nFurthermore, ')}
                >
                  Add Transition
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  className="w-full justify-start"
                  onClick={() => insertText('\n\nFor example, ')}
                >
                  Add Example
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  className="w-full justify-start"
                  onClick={() => insertText('\n\nOn the other hand, ')}
                >
                  Add Contrast
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WritingWorkspace;

