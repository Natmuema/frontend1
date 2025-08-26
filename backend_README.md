# Django Backend for Financial Platform with MeTTa Integration

This Django backend provides a comprehensive API for a financial investment platform with integration capabilities for the MeTTa programming language.

## Features

### Core Functionality
- **User Authentication & Management**: Registration, login, profile management
- **Asset Management**: CRUD operations for financial assets, categories, and price history
- **Portfolio Management**: Multi-portfolio support with holdings and transactions
- **Wallet System**: Digital wallet for managing funds
- **Investment Alerts**: Price and market alerts
- **Transaction Management**: Buy/sell transactions with automatic portfolio updates

### MeTTa Programming Language Integration
- **Script Management**: Create, store, and manage MeTTa scripts
- **Script Execution**: Execute MeTTa scripts with input/output handling
- **Data Mapping**: Map Django data to MeTTa-compatible formats
- **Analysis Results**: Store and retrieve analysis results from MeTTa scripts
- **Scheduled Tasks**: Schedule recurring MeTTa script executions
- **Data Export**: Export data in MeTTa-compatible formats

## Technology Stack

- **Django 5.2.5**: Web framework
- **Django REST Framework 3.16.1**: API framework
- **Django CORS Headers**: Cross-origin resource sharing
- **Django Filter**: Advanced filtering capabilities
- **Pillow**: Image processing for profile pictures
- **SQLite**: Database (can be easily switched to PostgreSQL/MySQL)

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication (`/api/auth/`)
- `POST /register/` - User registration
- `POST /login/` - User login
- `POST /logout/` - User logout
- `GET /profile/` - Get user profile
- `PUT /profile/` - Update user profile
- `PUT /change-password/` - Change password
- `GET /user-info/` - Get user information

### Assets (`/api/assets/`)
- `GET /` - List all assets
- `POST /` - Create new asset
- `GET /<id>/` - Get asset details
- `PUT /<id>/` - Update asset
- `DELETE /<id>/` - Delete asset
- `GET /search/` - Search assets
- `GET /statistics/` - Asset statistics
- `GET /categories/` - List asset categories
- `POST /categories/` - Create asset category
- `GET /<asset_id>/prices/` - Get asset price history
- `POST /prices/` - Add new price data

### Portfolio (`/api/portfolio/`)
- `GET /wallet/` - Get user wallet
- `PUT /wallet/` - Update wallet
- `GET /portfolios/` - List user portfolios
- `POST /portfolios/` - Create portfolio
- `GET /portfolios/<id>/` - Get portfolio details
- `PUT /portfolios/<id>/` - Update portfolio
- `DELETE /portfolios/<id>/` - Delete portfolio
- `GET /summary/` - Portfolio summary
- `GET /holdings/` - List portfolio holdings
- `POST /holdings/` - Add holding to portfolio
- `GET /transactions/` - List transactions
- `POST /transactions/` - Create transaction
- `POST /buy/` - Execute buy transaction
- `POST /sell/` - Execute sell transaction
- `GET /alerts/` - List investment alerts
- `POST /alerts/` - Create investment alert

### MeTTa Integration (`/api/metta/`)
- `GET /scripts/` - List MeTTa scripts
- `POST /scripts/` - Create MeTTa script
- `GET /scripts/<id>/` - Get script details
- `PUT /scripts/<id>/` - Update script
- `DELETE /scripts/<id>/` - Delete script
- `POST /execute/` - Execute MeTTa script
- `GET /executions/` - List script executions
- `GET /executions/<id>/` - Get execution details
- `GET /mappings/` - List data mappings
- `POST /mappings/` - Create data mapping
- `POST /analysis/` - Run MeTTa analysis
- `GET /analysis-results/` - List analysis results
- `GET /scheduled-tasks/` - List scheduled tasks
- `POST /scheduled-tasks/` - Create scheduled task
- `POST /export/` - Export data
- `GET /statistics/` - MeTTa integration statistics

## Database Models

### Accounts
- **UserProfile**: Extended user profile with additional fields

### Assets
- **AssetCategory**: Categories for organizing assets
- **Asset**: Financial assets with metadata
- **AssetPrice**: Historical price data

### Portfolio
- **Wallet**: User's digital wallet
- **Portfolio**: User's investment portfolios
- **PortfolioHolding**: Assets held in portfolios
- **Transaction**: Buy/sell transactions
- **InvestmentAlert**: Price and market alerts

### MeTTa Integration
- **MettaScript**: Stored MeTTa scripts
- **MettaExecution**: Script execution records
- **MettaDataMapping**: Data format mappings
- **MettaAnalysisResult**: Analysis results
- **MettaScheduledTask**: Scheduled script executions

## MeTTa Integration Details

### Script Management
The backend provides a complete system for managing MeTTa scripts:

1. **Script Storage**: Scripts are stored in the database with metadata
2. **Execution Engine**: Scripts can be executed synchronously or asynchronously
3. **Input/Output Handling**: Structured data input and output
4. **Error Handling**: Comprehensive error tracking and logging

### Data Mapping
The system includes data mapping capabilities to convert Django model data into MeTTa-compatible formats:

- Asset data mapping
- Portfolio data mapping
- Market data mapping
- User data mapping

### Analysis Integration
MeTTa scripts can be used for:

- Market trend analysis
- Risk assessment
- Portfolio optimization
- Price prediction
- Market sentiment analysis

## Admin Interface

Access the Django admin interface at `/admin/` with the superuser credentials to manage:

- Users and profiles
- Assets and categories
- Portfolios and transactions
- MeTTa scripts and executions
- System configuration

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Static Files
```bash
python manage.py collectstatic
```

## Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### CORS Configuration
The backend is configured to allow requests from:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (React dev server)

## Security Features

- Token-based authentication
- CORS protection
- Input validation
- SQL injection protection
- XSS protection
- CSRF protection

## API Authentication

The API uses token-based authentication. Include the token in request headers:

```
Authorization: Token <your-token>
```

## Error Handling

The API returns standardized error responses:

```json
{
    "error": "Error message",
    "details": "Additional error details"
}
```

## Rate Limiting

Consider implementing rate limiting for production use with packages like `django-ratelimit`.

## Production Deployment

For production deployment:

1. Set `DEBUG=False`
2. Use a production database (PostgreSQL/MySQL)
3. Configure static file serving
4. Set up HTTPS
5. Implement proper logging
6. Use environment variables for sensitive data
7. Set up monitoring and error tracking

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.