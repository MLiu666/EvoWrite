import React from 'react';

export const Select = ({ children, value, onValueChange, ...props }) => {
  return (
    <select
      value={value}
      onChange={(e) => onValueChange?.(e.target.value)}
      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
      {...props}
    >
      {children}
    </select>
  );
};

export const SelectTrigger = ({ children, ...props }) => {
  return <div {...props}>{children}</div>;
};

export const SelectValue = ({ placeholder, ...props }) => {
  return <span {...props}>{placeholder}</span>;
};

export const SelectContent = ({ children, ...props }) => {
  return <div {...props}>{children}</div>;
};

export const SelectItem = ({ children, value, ...props }) => {
  return (
    <option value={value} {...props}>
      {children}
    </option>
  );
};

