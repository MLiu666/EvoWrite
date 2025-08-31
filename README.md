# EvoWrite - AI-Powered Learning Platform

A modern, self-evolving web application for EFL (English as a Foreign Language) writing assistance, built with React and Vite.

## Features

- **Multi-Agent System**: Intelligent agents for writing assistance and learning
- **Modern UI**: Built with React, Tailwind CSS, and Framer Motion
- **Responsive Design**: Works seamlessly across all devices
- **Real-time Chat**: Interactive chat interface for writing help
- **Learner Profiles**: Personalized learning experience tracking
- **Writing Workspace**: Dedicated space for writing and editing

## Tech Stack

- **Frontend**: React 18, Vite, Tailwind CSS
- **UI Components**: Custom component library
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **Build Tool**: Vite

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd evowrite
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser and navigate to `http://localhost:5173`

### Building for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

## Project Structure

```
src/
├── components/          # React components
│   ├── ui/             # Reusable UI components
│   ├── App.jsx         # Main application component
│   ├── Dashboard.jsx   # Dashboard view
│   ├── ChatInterface.jsx # Chat interface
│   ├── LearnerProfile.jsx # User profile management
│   └── WritingWorkspace.jsx # Writing workspace
├── main.jsx            # Application entry point
└── index.css           # Global styles
```

## Deployment

This project is configured for deployment on Vercel. The `vercel.json` file contains the necessary configuration.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.
