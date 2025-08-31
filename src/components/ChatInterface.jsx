import React, { useState, useRef, useEffect } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Textarea } from './ui/textarea';
import { Badge } from './ui/badge';
import { ScrollArea } from './ui/scroll-area';
import { Separator } from './ui/separator';
import { 
  Send, 
  Bot, 
  User, 
  Star, 
  BookOpen, 
  Target, 
  TrendingUp,
  MessageSquare,
  CheckCircle,
  AlertCircle
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const ChatInterface = ({ learnerId, sessionId, onSessionUpdate }) => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentInteractionId, setCurrentInteractionId] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputText.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputText,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:5000/api/sage/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          learner_id: learnerId,
          message: inputText,
          session_id: sessionId,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        const assistantMessage = {
          id: data.interaction_id,
          type: 'assistant',
          content: data.response,
          intent: data.intent,
          confidence: data.confidence,
          responseType: data.response_type,
          srlSuggestion: data.srl_suggestion,
          validation: data.validation,
          suggestions: data.suggestions || [],
          timestamp: new Date(),
        };

        setMessages(prev => [...prev, assistantMessage]);
        setCurrentInteractionId(data.interaction_id);
        
        if (onSessionUpdate) {
          onSessionUpdate(data);
        }
      } else {
        throw new Error(data.error || 'Failed to send message');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now(),
        type: 'error',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const submitFeedback = async (interactionId, rating) => {
    try {
      await fetch('/api/sage/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          interaction_id: interactionId,
          rating: rating,
        }),
      });

      // Update the message to show feedback was submitted
      setMessages(prev => prev.map(msg => 
        msg.id === interactionId 
          ? { ...msg, userRating: rating, feedbackSubmitted: true }
          : msg
      ));
    } catch (error) {
      console.error('Error submitting feedback:', error);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const getIntentColor = (intent) => {
    const colors = {
      'Answer': 'bg-blue-100 text-blue-800',
      'R Language Use': 'bg-green-100 text-green-800',
      'R Revision': 'bg-purple-100 text-purple-800',
      'R Evaluation': 'bg-orange-100 text-orange-800',
      'R Generation': 'bg-pink-100 text-pink-800',
      'R Information': 'bg-cyan-100 text-cyan-800',
      'ACK': 'bg-gray-100 text-gray-800',
      'Negotiation': 'bg-yellow-100 text-yellow-800',
    };
    return colors[intent] || 'bg-gray-100 text-gray-800';
  };

  const getValidationIcon = (validation) => {
    if (validation?.approved) {
      return <CheckCircle className="w-4 h-4 text-green-500" />;
    } else {
      return <AlertCircle className="w-4 h-4 text-yellow-500" />;
    }
  };

  return (
    <div className="flex flex-col h-full bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-gradient-to-r from-blue-500 to-indigo-600 p-2 rounded-lg">
              <Bot className="w-6 h-6 text-white" />
            </div>
            <div>
              <h2 className="text-xl font-semibold text-gray-900">SAGE Writing Assistant</h2>
              <p className="text-sm text-gray-500">AI-powered EFL writing support</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
              Active Session
            </Badge>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <ScrollArea className="flex-1 p-4">
        <div className="space-y-4 max-w-4xl mx-auto">
          <AnimatePresence>
            {messages.map((message) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
              >
                <Card className={`${
                  message.type === 'user' 
                    ? 'ml-auto max-w-2xl bg-blue-500 text-white' 
                    : message.type === 'error'
                    ? 'mr-auto max-w-2xl bg-red-50 border-red-200'
                    : 'mr-auto max-w-3xl bg-white shadow-sm'
                }`}>
                  <CardContent className="p-4">
                    <div className="flex items-start space-x-3">
                      <div className={`p-2 rounded-full ${
                        message.type === 'user' 
                          ? 'bg-blue-600' 
                          : message.type === 'error'
                          ? 'bg-red-100'
                          : 'bg-gradient-to-r from-indigo-500 to-purple-600'
                      }`}>
                        {message.type === 'user' ? (
                          <User className="w-4 h-4 text-white" />
                        ) : message.type === 'error' ? (
                          <AlertCircle className="w-4 h-4 text-red-500" />
                        ) : (
                          <Bot className="w-4 h-4 text-white" />
                        )}
                      </div>
                      
                      <div className="flex-1 space-y-2">
                        <div className="flex items-center justify-between">
                          <span className={`text-sm font-medium ${
                            message.type === 'user' ? 'text-blue-100' : 'text-gray-900'
                          }`}>
                            {message.type === 'user' ? 'You' : message.type === 'error' ? 'Error' : 'SAGE Assistant'}
                          </span>
                          <span className={`text-xs ${
                            message.type === 'user' ? 'text-blue-200' : 'text-gray-500'
                          }`}>
                            {message.timestamp.toLocaleTimeString()}
                          </span>
                        </div>
                        
                        <div className={`prose prose-sm max-w-none ${
                          message.type === 'user' ? 'text-white' : 'text-gray-700'
                        }`}>
                          <p className="whitespace-pre-wrap">{message.content}</p>
                        </div>

                        {/* Assistant message metadata */}
                        {message.type === 'assistant' && (
                          <div className="space-y-3 mt-4">
                            {/* Intent and validation */}
                            <div className="flex items-center space-x-2">
                              {message.intent && (
                                <Badge className={getIntentColor(message.intent)}>
                                  <MessageSquare className="w-3 h-3 mr-1" />
                                  {message.intent}
                                </Badge>
                              )}
                              {message.validation && (
                                <div className="flex items-center space-x-1">
                                  {getValidationIcon(message.validation)}
                                  <span className="text-xs text-gray-500">
                                    Quality: {(message.validation.overall_score * 100).toFixed(0)}%
                                  </span>
                                </div>
                              )}
                            </div>

                            {/* SRL Suggestion */}
                            {message.srlSuggestion && (
                              <div className="bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-lg p-3">
                                <div className="flex items-center space-x-2 mb-2">
                                  <Target className="w-4 h-4 text-green-600" />
                                  <span className="text-sm font-medium text-green-800">Learning Strategy</span>
                                </div>
                                <p className="text-sm text-green-700">{message.srlSuggestion}</p>
                              </div>
                            )}

                            {/* Suggestions */}
                            {message.suggestions && message.suggestions.length > 0 && (
                              <div className="space-y-2">
                                <span className="text-sm font-medium text-gray-700">Suggestions:</span>
                                <div className="flex flex-wrap gap-2">
                                  {message.suggestions.map((suggestion, index) => (
                                    <Badge key={index} variant="outline" className="text-xs">
                                      {suggestion}
                                    </Badge>
                                  ))}
                                </div>
                              </div>
                            )}

                            {/* Rating */}
                            {!message.feedbackSubmitted && (
                              <div className="flex items-center space-x-2 pt-2 border-t border-gray-100">
                                <span className="text-sm text-gray-600">Rate this response:</span>
                                <div className="flex space-x-1">
                                  {[1, 2, 3, 4, 5].map((rating) => (
                                    <Button
                                      key={rating}
                                      variant="ghost"
                                      size="sm"
                                      className="p-1 h-auto"
                                      onClick={() => submitFeedback(message.id, rating)}
                                    >
                                      <Star className="w-4 h-4 text-yellow-400 hover:fill-current" />
                                    </Button>
                                  ))}
                                </div>
                              </div>
                            )}

                            {message.feedbackSubmitted && (
                              <div className="flex items-center space-x-2 pt-2 border-t border-gray-100">
                                <CheckCircle className="w-4 h-4 text-green-500" />
                                <span className="text-sm text-gray-600">
                                  Thank you for your feedback! ({message.userRating}/5 stars)
                                </span>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </AnimatePresence>
          
          {isLoading && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="mr-auto max-w-3xl"
            >
              <Card className="bg-white shadow-sm">
                <CardContent className="p-4">
                  <div className="flex items-center space-x-3">
                    <div className="bg-gradient-to-r from-indigo-500 to-purple-600 p-2 rounded-full">
                      <Bot className="w-4 h-4 text-white" />
                    </div>
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </ScrollArea>

      {/* Input Area */}
      <div className="bg-white border-t p-4">
        <div className="max-w-4xl mx-auto">
          <div className="flex space-x-3">
            <div className="flex-1">
              <Textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask me anything about your writing, request feedback, or get help with language use..."
                className="min-h-[60px] resize-none border-gray-200 focus:border-blue-500 focus:ring-blue-500"
                disabled={isLoading}
              />
            </div>
            <Button
              onClick={sendMessage}
              disabled={!inputText.trim() || isLoading}
              className="bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 px-6"
            >
              <Send className="w-4 h-4" />
            </Button>
          </div>
          
          <div className="flex items-center justify-between mt-3 text-xs text-gray-500">
            <span>Press Enter to send, Shift+Enter for new line</span>
            <span>{inputText.length}/1000 characters</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;

