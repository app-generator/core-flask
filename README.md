# Secure API with Flask, SQLite, and Flask-RESTx

This project is a secure REST API built using Flask, SQLite, Flask-RESTx, and JWT for user authentication and authorization. The API provides endpoints for user registration, login, and profile retrieval, with access restricted by JWT tokens.


## Project Structure

```plaintext
project/
│
├── app.py         # Main application file with routes and configuration
├── config.py      # Configuration settings
├── models.py      # Database models
├── requirements.txt # Dependencies for the project
└── README.md      # Project documentation
```

## Setup Instructions

### Prerequisites
- Python 3.x
- `pip` (Python package installer)

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/app-generator/core-flask
   cd core-flask
   ```

2. **Install required packages**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional but recommended):
   
   Create a `.env` file in the root directory for sensitive data like JWT keys:

   ```plaintext
   SECRET_KEY=your_secret_key
   JWT_SECRET_KEY=your_jwt_secret_key
   ```

4. **Create the SQLite database**:

   Initialize the database by running:

   ```python
   from app import db
   db.create_all()
   ```

5. **Run the application**:

   ```bash
   python app.py
   ```

The server will start at `http://127.0.0.1:5000`.

## Usage

### API Endpoints

- **POST /users/register** - Register a new user with `username` and `password`.
- **POST /users/login** - Log in with credentials and receive an access token.
- **GET /users/profile** - Access a protected user profile route using a valid JWT token.

### Sample Requests

Use `curl` or Postman to test the API.

1. **Register a New User**:

   ```bash
   curl -X POST "http://127.0.0.1:5000/users/register" -H "Content-Type: application/json" -d "{\"username\":\"testuser\",\"password\":\"testpass\"}"
   ```

2. **Login**:

   ```bash
   curl -X POST "http://127.0.0.1:5000/users/login" -H "Content-Type: application/json" -d "{\"username\":\"testuser\",\"password\":\"testpass\"}"
   ```

   You will receive a JSON response with an `access_token`.

3. **Access Protected Route**:

   Use the `access_token` received from login to access the profile route:

   ```bash
   curl -X GET "http://127.0.0.1:5000/users/profile" -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
   ```

## Configuration

Modify settings in `config.py`, such as secret keys and database URI:

```python
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret')
```

## Security Measures

- **Password Hashing**: User passwords are hashed using `Flask-Bcrypt`.
- **JWT Authentication**: JWT tokens are used to authenticate users and protect routes.
