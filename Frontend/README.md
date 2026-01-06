# Frontend - Social Insight Engine

> 🏆 **NCCS Business Hackathon 2026 Winner** - Frontend Component

---

React + TypeScript + Vite application for social media sentiment analysis dashboard.

## 📁 Project Structure

```
Frontend/
├── src/
│   ├── services/              # API services
│   │   ├── sentimentService.ts  # Backend API integration
│   │   └── themeService.tsx     # Theme management (Dark/Light)
│   ├── types.ts               # TypeScript type definitions
│   ├── App.tsx                # Main application component
│   ├── main.tsx               # React entry point
│   └── index.css              # Tailwind CSS configuration
├── public/                    # Static assets (images, icons)
├── package.json               # Dependencies & scripts
├── vite.config.ts             # Vite build configuration
├── eslint.config.js           # ESLint rules
├── tsconfig.json              # TypeScript configuration
├── tailwind.config.js         # Tailwind CSS configuration
└── start.sh                   # Development server startup script
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
npm install
```

### 2. Run Development Server
```bash
# Using startup script
./start.sh

# Or manually
npm run dev
```

### 3. Access Application
Open http://localhost:5173 in your browser.

## 🎨 Features

### Core Functionality
- **Dark/Light Theme Toggle**: Persistent theme selection
- **API Configuration**: Secure localStorage-based credential storage
- **Post Selection**: 
  - Auto-fetch recent posts from Facebook page
  - Manual post ID input for specific analysis
- **Sentiment Dashboard**:
  - 📊 **Pie Chart**: Visual sentiment distribution
  - 📈 **Bar Chart**: Sentiment intensity scale
  - 🎯 **Statistics Cards**: Real-time counts (Positive/Neutral/Negative)
- **AI Insights**: 
  - Positive takeaways & recommendations
  - Negative concerns & improvement areas
- **Comment Browser**:
  - Filter by sentiment category
  - Pagination for large datasets
  - Search functionality
- **Search History**:
  - Save analyses with timestamps
  - Load historical data instantly
  - Delete old entries

### UI/UX Highlights
- **Responsive Design**: Works on desktop and tablet
- **Smooth Transitions**: Theme switching animations
- **Loading States**: Visual feedback for API calls
- **Error Handling**: User-friendly error messages
- **Empty States**: Helpful placeholders when no data

## 📋 Available Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Start development server with hot reload |
| `npm run build` | Build for production (optimized) |
| `npm run preview` | Preview production build locally |
| `npm run lint` | Run ESLint for code quality |
| `npm run type-check` | TypeScript type checking |

## 🛠️ Technology Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 19 | UI framework |
| **TypeScript** | 5.x | Type safety |
| **Vite** | 5.x | Build tool & dev server |
| **Tailwind CSS** | 4.x | Utility-first styling |
| **Recharts** | 2.x | Data visualization |
| **Lucide React** | 0.x | Icon library |
| **clsx** | 2.x | Conditional class names |
| **tailwind-merge** | 2.x | Tailwind class merging |

## 📂 Key Files

### Services
- **sentimentService.ts**: Handles all API calls to backend
  - `scrapeComments()` - Scrape Facebook comments
  - `classifySentiment()` - Analyze sentiment
  - `getRecentPosts()` - Fetch recent posts
  - `generateInsights()` - Get AI insights

- **themeService.tsx**: Theme management with persistence
  - Theme context provider
  - LocalStorage integration
  - CSS variable updates

### Types
- **types.ts**: Centralized type definitions
  - `Comment` - Comment data structure
  - `SentimentResult` - Analysis results
  - `Insights` - AI insights structure
  - `HistoryItem` - Saved search history

### Components
- **App.tsx**: Main application container
  - Theme provider
  - API configuration
  - Dashboard layout
  - State management

## 🔧 Configuration

### Environment Variables
Frontend doesn't require `.env` files - API configuration is stored in browser localStorage.

### Tailwind CSS
Custom configuration in `tailwind.config.js`:
```javascript
export default {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Custom theme colors
      }
    }
  },
  plugins: []
}
```

### Vite Configuration
Optimized build settings in `vite.config.ts`:
- TypeScript support
- Tailwind CSS integration
- Development server on port 5173
- Proxy to backend (if needed)

## 🎯 Component Architecture

```
App.tsx
├── ThemeProvider
│   └── ThemeToggle
├── ConfigurationPanel
│   ├── FacebookConfig
│   └── GeminiConfig
├── PostSelector
│   ├── RecentPostsDropdown
│   └── ManualInput
├── Dashboard
│   ├── StatisticsCards
│   ├── SentimentPieChart
│   ├── SentimentBarChart
│   └── AIInsights
├── CommentBrowser
│   ├── SentimentFilter
│   ├── CommentList
│   └── Pagination
└── HistoryManager
    ├── SaveSearch
    └── LoadHistory
```

## 🔍 API Integration

### Backend Communication
All API calls go through `sentimentService.ts`:

```typescript
// Example usage
import { scrapeComments, classifySentiment } from './services/sentimentService';

// Scrape comments
const comments = await scrapeComments(postId, config);

// Analyze sentiment
const results = await classifySentiment(comments);
```

### Error Handling
- Network errors show user-friendly messages
- API errors display specific error codes
- Timeout handling for long-running operations

## 📊 Data Flow

```
User Input → API Service → Backend → ML Model → Results → Visualization
```

1. User configures API credentials
2. Selects post or enters ID
3. Frontend calls `/scrape` endpoint
4. Backend scrapes Facebook comments
5. Frontend calls `/classify` endpoint
6. Backend runs BERT sentiment analysis
7. Frontend calls `/generate-insights` endpoint
8. Backend generates AI insights via Gemini
9. Results visualized in dashboard

## 🚀 Deployment

### Production Build
```bash
npm run build
```

Outputs optimized files to `dist/` directory.

### Serve Production Build
```bash
npm run preview
```

Serves production build locally for testing.

## 🐛 Troubleshooting

### Port Already in Use
```bash
npm run dev -- --port 5174
```

### TypeScript Errors
```bash
npm run type-check
```

### Tailwind Not Working
```bash
npm run build  # Rebuild to regenerate CSS
```

### CORS Issues
Ensure backend is configured to accept requests from `http://localhost:5173`

## 📝 License

MIT License - Free to use and modify.

---

**Part of NCCS Business Hackathon 2026 Winning Project** 🏆