# Frontend-Backend Integration Guide

This guide explains how to integrate the React frontend with the Django backend for the financial platform with MeTTa programming language integration.

## Overview

The project consists of:
- **Frontend**: React application (Vite + React + Tailwind CSS)
- **Backend**: Django REST API with MeTTa integration
- **Database**: SQLite (development) / PostgreSQL/MySQL (production)

## Quick Start

### 1. Start the Backend Server

```bash
# Navigate to project root
cd /workspace

# Activate virtual environment
source venv/bin/activate

# Start Django server
python manage.py runserver 0.0.0.0:8000
```

The backend will be available at: `http://localhost:8000`

### 2. Start the Frontend Server

```bash
# In a new terminal, navigate to project root
cd /workspace

# Install frontend dependencies (if not already done)
npm install

# Start Vite development server
npm run dev
```

The frontend will be available at: `http://localhost:5173`

## API Integration

### Authentication Flow

1. **User Registration**
   ```javascript
   const registerUser = async (userData) => {
     const response = await fetch('http://localhost:8000/api/auth/register/', {
       method: 'POST',
       headers: {
         'Content-Type': 'application/json',
       },
       body: JSON.stringify(userData)
     });
     return response.json();
   };
   ```

2. **User Login**
   ```javascript
   const loginUser = async (credentials) => {
     const response = await fetch('http://localhost:8000/api/auth/login/', {
       method: 'POST',
       headers: {
         'Content-Type': 'application/json',
       },
       body: JSON.stringify(credentials)
     });
     const data = await response.json();
     // Store token in localStorage or context
     localStorage.setItem('token', data.token);
     return data;
   };
   ```

3. **Authenticated Requests**
   ```javascript
   const fetchProtectedData = async (url) => {
     const token = localStorage.getItem('token');
     const response = await fetch(`http://localhost:8000/api/${url}`, {
       headers: {
         'Authorization': `Token ${token}`,
         'Content-Type': 'application/json',
       }
     });
     return response.json();
   };
   ```

### Key API Endpoints

#### Assets Management
- `GET /api/assets/` - List all assets
- `POST /api/assets/` - Create new asset
- `GET /api/assets/search/` - Search assets
- `GET /api/assets/categories/` - List asset categories

#### Portfolio Management
- `GET /api/portfolio/wallet/` - Get user wallet
- `GET /api/portfolio/portfolios/` - List user portfolios
- `POST /api/portfolio/portfolios/` - Create portfolio
- `GET /api/portfolio/summary/` - Portfolio summary
- `POST /api/portfolio/buy/` - Execute buy transaction
- `POST /api/portfolio/sell/` - Execute sell transaction

#### MeTTa Integration
- `GET /api/metta/scripts/` - List MeTTa scripts
- `POST /api/metta/scripts/` - Create MeTTa script
- `POST /api/metta/execute/` - Execute MeTTa script
- `POST /api/metta/analysis/` - Run MeTTa analysis
- `GET /api/metta/statistics/` - MeTTa integration statistics

## Frontend Integration Examples

### 1. Asset Management Component

```javascript
import React, { useState, useEffect } from 'react';

const AssetManagement = () => {
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAssets();
  }, []);

  const fetchAssets = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/assets/', {
        headers: {
          'Authorization': `Token ${token}`,
        }
      });
      const data = await response.json();
      setAssets(data.results || data);
    } catch (error) {
      console.error('Error fetching assets:', error);
    } finally {
      setLoading(false);
    }
  };

  const createAsset = async (assetData) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/assets/', {
        method: 'POST',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(assetData)
      });
      const newAsset = await response.json();
      setAssets([...assets, newAsset]);
    } catch (error) {
      console.error('Error creating asset:', error);
    }
  };

  if (loading) return <div>Loading assets...</div>;

  return (
    <div>
      <h2>Asset Management</h2>
      {assets.map(asset => (
        <div key={asset.id}>
          <h3>{asset.name}</h3>
          <p>Symbol: {asset.symbol}</p>
          <p>Price: ${asset.current_price}</p>
        </div>
      ))}
    </div>
  );
};

export default AssetManagement;
```

### 2. Portfolio Management Component

```javascript
import React, { useState, useEffect } from 'react';

const PortfolioManagement = () => {
  const [portfolios, setPortfolios] = useState([]);
  const [wallet, setWallet] = useState(null);

  useEffect(() => {
    fetchPortfolios();
    fetchWallet();
  }, []);

  const fetchPortfolios = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/portfolio/portfolios/', {
        headers: {
          'Authorization': `Token ${token}`,
        }
      });
      const data = await response.json();
      setPortfolios(data.results || data);
    } catch (error) {
      console.error('Error fetching portfolios:', error);
    }
  };

  const fetchWallet = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/portfolio/wallet/', {
        headers: {
          'Authorization': `Token ${token}`,
        }
      });
      const data = await response.json();
      setWallet(data);
    } catch (error) {
      console.error('Error fetching wallet:', error);
    }
  };

  const executeBuyTransaction = async (transactionData) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/portfolio/buy/', {
        method: 'POST',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(transactionData)
      });
      const result = await response.json();
      // Refresh data after transaction
      fetchPortfolios();
      fetchWallet();
      return result;
    } catch (error) {
      console.error('Error executing buy transaction:', error);
    }
  };

  return (
    <div>
      <h2>Portfolio Management</h2>
      {wallet && (
        <div>
          <h3>Wallet Balance</h3>
          <p>${wallet.balance} {wallet.currency}</p>
        </div>
      )}
      {portfolios.map(portfolio => (
        <div key={portfolio.id}>
          <h3>{portfolio.name}</h3>
          <p>Total Value: ${portfolio.total_value}</p>
          <p>Holdings: {portfolio.holdings?.length || 0}</p>
        </div>
      ))}
    </div>
  );
};

export default PortfolioManagement;
```

### 3. MeTTa Integration Component

```javascript
import React, { useState, useEffect } from 'react';

const MettaIntegration = () => {
  const [scripts, setScripts] = useState([]);
  const [executionResults, setExecutionResults] = useState(null);

  useEffect(() => {
    fetchScripts();
  }, []);

  const fetchScripts = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/metta/scripts/', {
        headers: {
          'Authorization': `Token ${token}`,
        }
      });
      const data = await response.json();
      setScripts(data.results || data);
    } catch (error) {
      console.error('Error fetching scripts:', error);
    }
  };

  const executeScript = async (scriptId, inputData) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/metta/execute/', {
        method: 'POST',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          script_id: scriptId,
          input_data: inputData,
          execute_async: false
        })
      });
      const result = await response.json();
      setExecutionResults(result);
      return result;
    } catch (error) {
      console.error('Error executing script:', error);
    }
  };

  const runAnalysis = async (analysisData) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/metta/analysis/', {
        method: 'POST',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(analysisData)
      });
      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Error running analysis:', error);
    }
  };

  return (
    <div>
      <h2>MeTTa Integration</h2>
      <div>
        <h3>Available Scripts</h3>
        {scripts.map(script => (
          <div key={script.id}>
            <h4>{script.name}</h4>
            <p>{script.description}</p>
            <p>Type: {script.script_type}</p>
            <button onClick={() => executeScript(script.id, {})}>
              Execute Script
            </button>
          </div>
        ))}
      </div>
      {executionResults && (
        <div>
          <h3>Execution Results</h3>
          <pre>{JSON.stringify(executionResults, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default MettaIntegration;
```

## Environment Configuration

### Frontend Environment Variables

Create a `.env` file in the project root:

```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_APP_NAME=Financial Platform
```

### Backend Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

## Error Handling

### Frontend Error Handling

```javascript
const handleApiError = (error) => {
  if (error.status === 401) {
    // Unauthorized - redirect to login
    localStorage.removeItem('token');
    window.location.href = '/login';
  } else if (error.status === 403) {
    // Forbidden - show access denied message
    console.error('Access denied');
  } else {
    // Other errors
    console.error('API Error:', error);
  }
};
```

### Backend Error Responses

The backend returns standardized error responses:

```json
{
  "error": "Error message",
  "details": "Additional error details"
}
```

## CORS Configuration

The backend is configured to allow requests from:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (React dev server)

## Testing the Integration

1. **Start both servers**
2. **Register a new user** through the frontend
3. **Login** and verify token storage
4. **Test protected endpoints** by accessing portfolio/asset data
5. **Test MeTTa integration** by creating and executing scripts

## Production Deployment

### Backend Deployment
1. Set `DEBUG=False`
2. Use production database (PostgreSQL/MySQL)
3. Configure static file serving
4. Set up HTTPS
5. Use environment variables for sensitive data

### Frontend Deployment
1. Build the production version: `npm run build`
2. Serve static files from a web server
3. Update API base URL to production endpoint
4. Configure CORS for production domain

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure backend CORS settings include frontend URL
2. **Authentication Errors**: Check token storage and transmission
3. **API Endpoint Errors**: Verify endpoint URLs and HTTP methods
4. **Database Errors**: Check migrations and database connection

### Debug Tips

1. Use browser developer tools to inspect network requests
2. Check Django server logs for backend errors
3. Verify token format in request headers
4. Test API endpoints directly with tools like Postman

## Next Steps

1. Implement real-time updates using WebSockets
2. Add file upload functionality for asset documents
3. Implement advanced MeTTa script execution
4. Add comprehensive error handling and user feedback
5. Implement caching for better performance
6. Add unit and integration tests