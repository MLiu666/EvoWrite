import React from 'react';

export const Separator = ({ className = '', ...props }) => {
  return (
    <div className={`h-px bg-gray-200 ${className}`} {...props} />
  );
};

