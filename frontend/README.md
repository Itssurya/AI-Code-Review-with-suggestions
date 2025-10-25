# AI Code Reviewer - Frontend

A modern React frontend for the AI Code Reviewer application, built with TypeScript and Tailwind CSS.

## 🚀 Features

- **Modern UI**: Clean, responsive design with Tailwind CSS
- **Code Editor**: Syntax highlighting and file upload support
- **Real-time Review**: AI-powered code analysis and suggestions
- **Dashboard**: Analytics and metrics visualization
- **Multi-language Support**: Python, JavaScript, TypeScript, Java, C++, Go, Rust
- **Static Analysis Integration**: Pylint, Bandit, ESLint results
- **Responsive Design**: Works on desktop, tablet, and mobile

## 🛠️ Tech Stack

- **React 19** with TypeScript
- **Tailwind CSS** for styling
- **Axios** for API communication
- **Lucide React** for icons
- **React Syntax Highlighter** for code display

## 📦 Installation

```bash
# Install dependencies
npm install

# Start development server
npm start
```

## 🔧 Configuration

The frontend connects to the backend API. By default, it expects the backend to be running on `http://localhost:8000`.

You can configure the API URL by setting the `REACT_APP_API_URL` environment variable:

```bash
# Create .env file
echo "REACT_APP_API_URL=http://localhost:8000" > .env
```

## 🎨 Components

### Main Components

- **App**: Main application component with tab navigation
- **Header**: Top navigation with API status indicator
- **CodeEditor**: Code input with language selection and file upload
- **ReviewResults**: Display analysis results and suggestions
- **Dashboard**: Analytics and metrics visualization
- **LoadingSpinner**: Reusable loading component

### Features

- **Tab Navigation**: Switch between Editor, Dashboard, and History
- **API Status**: Real-time connection status indicator
- **File Upload**: Support for multiple programming languages
- **Code Analysis**: AI and static analysis results
- **Responsive Design**: Mobile-first approach
- **Error Handling**: Graceful error states and loading indicators

## 🚀 Development

```bash
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Type checking
npx tsc --noEmit
```

## 📱 Responsive Design

The application is fully responsive and works on:

- **Desktop**: Full-featured experience with side-by-side layout
- **Tablet**: Optimized layout for medium screens
- **Mobile**: Stacked layout with touch-friendly controls

## 🎯 API Integration

The frontend integrates with the following backend endpoints:

- `GET /health` - Health check
- `POST /api/v1/review` - Single code review
- `POST /api/v1/review/batch` - Batch code review
- `GET /api/v1/dashboard/metrics` - Dashboard metrics
- `GET /api/v1/languages` - Supported languages
- `POST /api/v1/refactor` - Code refactoring

## 🎨 Design System

### Colors

- **Primary**: Blue color palette for main actions
- **Secondary**: Gray color palette for neutral elements
- **Success**: Green for positive states
- **Warning**: Yellow for caution states
- **Error**: Red for error states

### Typography

- **Font Family**: Inter for UI text, JetBrains Mono for code
- **Font Weights**: 300, 400, 500, 600, 700
- **Responsive**: Scales appropriately across devices

### Components

- **Buttons**: Primary and secondary variants with hover states
- **Cards**: Consistent padding and shadow
- **Inputs**: Focus states and validation styling
- **Code Editor**: Dark theme with syntax highlighting

## 🔄 State Management

The application uses React hooks for state management:

- **useState**: Local component state
- **useEffect**: Side effects and API calls
- **Custom hooks**: Reusable logic (can be added)

## 🧪 Testing

```bash
# Run tests
npm test

# Run tests with coverage
npm test -- --coverage
```

## 📦 Build & Deploy

```bash
# Build for production
npm run build

# The build folder contains the production build
```

## 🤝 Contributing

1. Follow the existing code style
2. Use TypeScript for type safety
3. Write responsive components
4. Test your changes
5. Update documentation

## 📄 License

This project is part of the AI Code Reviewer application.