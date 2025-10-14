# Trails and Trails Frontend

A modern React application built with Vite, TypeScript, and Tailwind CSS for the Trails and Trails tourism platform.

## Features

- 🎨 Modern UI with Tailwind CSS and Radix UI components
- 🔐 Authentication system with JWT tokens
- 🎫 Ticket booking and payment integration
- 🏞️ Destination browsing and tour details
- 📱 Responsive design for all devices
- ⚡ Fast development with Vite
- 🎯 Type-safe with TypeScript

## Tech Stack

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **UI Components**: Radix UI
- **State Management**: React Query (TanStack Query)
- **Routing**: React Router DOM
- **Forms**: React Hook Form with Zod validation
- **Animations**: Framer Motion

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or pnpm

### Installation

1. Clone the repository
```bash
git clone https://github.com/bassy1992/tailsandtrails.git
cd tailsandtrails/Tfront
```

2. Install dependencies
```bash
npm install
# or
pnpm install
```

3. Set up environment variables
```bash
cp .env.example .env
```

4. Start the development server
```bash
npm run dev
```

The application will be available at `http://localhost:8080`

## Build and Deployment

### Build for Production

```bash
npm run build
```

This creates optimized production files in the `dist/spa` directory.

### Environment Variables for Production

Set these environment variables in your deployment platform:

- `VITE_API_BASE_URL`: Your backend API base URL
- `VITE_API_URL`: Your backend API endpoint URL

## Project Structure

```
Tfront/
├── client/                 # React application source
│   ├── components/        # Reusable UI components
│   ├── pages/            # Page components
│   ├── contexts/         # React contexts
│   ├── hooks/            # Custom hooks
│   └── lib/              # Utilities and API client
├── public/               # Static assets
├── shared/               # Shared utilities
└── server/               # Express server (for development)
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run build:client` - Build client only
- `npm run build:server` - Build server only
- `npm run start` - Start production server
- `npm run test` - Run tests
- `npm run typecheck` - Type checking

## API Integration

The frontend communicates with the Django backend API. Make sure to:

1. Update the API URLs in your environment variables
2. Ensure CORS is properly configured on the backend
3. Set up proper authentication headers

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and type checking
5. Submit a pull request

## License

This project is licensed under the MIT License.