import React from 'react';

export const Tabs = ({ children, value, onValueChange, className = '' }) => {
  return (
    <div className={className}>
      {children}
    </div>
  );
};

export const TabsList = ({ children, className = '' }) => {
  return (
    <div className={`flex space-x-1 bg-gray-100 p-1 rounded-lg ${className}`}>
      {children}
    </div>
  );
};

export const TabsTrigger = ({ children, value, className = '', ...props }) => {
  return (
    <button
      className={`px-3 py-2 text-sm font-medium rounded-md transition-colors hover:bg-white hover:text-gray-900 ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};

export const TabsContent = ({ children, value, className = '' }) => {
  return (
    <div className={className}>
      {children}
    </div>
  );
};

