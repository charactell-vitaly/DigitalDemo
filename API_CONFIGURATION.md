# API Configuration Guide

## Overview

This project now uses professional environment-based configuration for the backend service URL, eliminating hardcoded URLs throughout the codebase.

## Frontend Configuration

### Environment Files

- **`.env.local`** - Development environment (automatically loaded by Vite)
- **`.env.production`** - Production environment (used during build)
- **`.env.example`** - Template for reference

### Frontend Setup

1. **Development**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   This will load `VITE_API_BASE_URL` from `.env.local` (default: `http://localhost:8808`)

2. **Production Build**:
   ```bash
   cd frontend
   npm run build
   ```
   This will load `VITE_API_BASE_URL` from `.env.production`

### Changing the Backend URL

Edit `frontend/.env.local`:
```
VITE_API_BASE_URL=http://your-backend-url:8808
```

For production, edit `frontend/.env.production`:
```
VITE_API_BASE_URL=https://api.yourdomain.com
```

## Backend Configuration

### Environment Files

- **`.env.local`** - Development environment (automatically loaded)
- **`.env.production`** - Production environment
- **`.env.example`** - Template for reference

### Backend Setup

1. **Install python-dotenv**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Development**:
   ```bash
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8808
   ```
   Or with environment variables from `.env.local`:
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Production**:
   Copy `.env.production` to `.env` and adjust values, then run:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8808
   ```

### Backend Environment Variables

Edit `backend/.env.local`:

```env
# API Server Configuration
API_HOST=0.0.0.0           # Host to bind to
API_PORT=8808              # Port to listen on
API_RELOAD=true            # Enable auto-reload (dev only)

# CORS Configuration (comma-separated)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

## Code Architecture

### Frontend

The frontend now uses a professional three-layer architecture:

1. **Config Layer** (`src/config/api.ts`)
   - Centralized API endpoint definitions
   - Loads base URL from `VITE_API_BASE_URL` environment variable
   - Fallback to localhost for development

2. **Service Layer** (`src/services/apiClient.ts`)
   - Singleton API client instance
   - Type-safe methods for all API operations
   - Centralized error handling
   - Exported TypeScript interfaces for all data models

3. **Component Layer** (`src/screens/` and `src/components/`)
   - Components use `apiClient` service
   - No direct fetch calls or hardcoded URLs
   - Clean separation of concerns

### Backend

The backend uses environment variables for configuration:

- `app/config.py` - Centralized configuration
- Loads from `.env` files automatically
- Fallback defaults for all settings
- CORS origins configurable per environment

## Benefits

✅ **No Hardcoded URLs** - All URLs managed in one place  
✅ **Environment-Specific** - Different URLs for dev/production  
✅ **Type-Safe** - Frontend has full TypeScript interfaces  
✅ **Easy Testing** - Can easily switch between different backends  
✅ **Scalable** - Adding new endpoints is simple and consistent  
✅ **Professional** - Follows industry best practices  

## Workflow Examples

### Development Workflow

```bash
# Terminal 1: Backend
cd backend
python -m pip install -r requirements.txt
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

Both will use localhost URLs from `.env.local` files.

### Production Deployment

1. Update `backend/.env.production` with production settings
2. Update `frontend/.env.production` with production backend URL
3. Build frontend: `npm run build`
4. Deploy built frontend and configure backend with `.env.production`

## Adding a New Endpoint

To add a new API endpoint:

1. **Add to `frontend/src/config/api.ts`**:
   ```typescript
   export const API_CONFIG = {
     // ... existing endpoints
     newFeature: {
       getItem: (id: string) => `${API_BASE_URL}/api/new-feature/${id}`,
     }
   }
   ```

2. **Add method to `frontend/src/services/apiClient.ts`**:
   ```typescript
   async getNewItem(id: string): Promise<ItemType> {
     const response = await fetch(API_CONFIG.newFeature.getItem(id));
     if (!response.ok) throw new Error(`Failed to get item: ${response.status}`);
     return response.json();
   }
   ```

3. **Use in components**:
   ```typescript
   const item = await apiClient.getNewItem(id);
   ```

Done! The URL is now centralized and environment-aware.
