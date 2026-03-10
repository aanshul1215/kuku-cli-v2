# Portfolio Management Application

A Flask-based web application for managing investment portfolios, executing trades, and tracking transactions. This app integrates with the Alpha Vantage API for real-time stock data and uses AWS Cognito for secure authentication.

## Features

- **User Management**: Register and manage user accounts with balance tracking
- **Portfolio Management**: Create and manage multiple investment portfolios
- **Stock Trading**: Execute buy/sell orders with real-time price data from Alpha Vantage
- **Transaction History**: Track all trading activities and portfolio performance
- **Security Integration**: OIDC authentication via AWS Cognito
- **Authorization**: Role-based access control for portfolio operations

## Tech Stack

- **Backend**: Flask with SQLAlchemy ORM
- **Database**: MySQL (production) / SQLite (testing)
- **Authentication**: AWS Cognito OIDC
- **API Integration**: Alpha Vantage for stock data
- **Caching**: Flask-Caching for API response optimization
- **Validation**: Pydantic for request validation
- **Testing**: pytest with coverage reporting

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd portfolio-app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Copy `.env.example` to `.env` and fill in your values:
   ```env
   FLASK_ENV=development
   DATABASE_URL=mysql+pymysql://user:password@localhost/dbname
   ALPHA_VANTAGE_API_KEY=your_api_key_here
   COGNITO_REGION=us-east-1
   COGNITO_USER_POOL_ID=your_pool_id
   COGNITO_CLIENT_ID=your_client_id
   ```

5. **Initialize database**
   ```bash
   flask db upgrade
   ```

## Running the Application

```bash
flask run
```

The application will start on `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /users/login` - User login via OIDC
- `POST /users/register` - User registration

### Portfolios
- `GET /portfolios` - List user portfolios
- `POST /portfolios` - Create new portfolio
- `GET /portfolios/<id>` - Get portfolio details

### Trading
- `POST /trades/buy` - Execute buy order
- `POST /trades/sell` - Execute sell order

### Securities
- `GET /securities` - List available securities
- `GET /securities/<ticker>` - Get security details

## Testing

Run the test suite with coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

## Project Structure

```
app/
├── auth/           # Authentication modules
├── models/         # SQLAlchemy models
├── routes/         # Flask blueprints
├── service/        # Business logic
├── schemas.py      # Pydantic validation
├── config.py       # Configuration classes
└── __init__.py     # App factory
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License.