# Task Manager Application

A modern, feature-rich task management web application built with Flask. This application allows users to create, manage, and organize their tasks with categories, priorities, and due dates.

## Features

### Core Functionality
- **User Authentication**: Secure user registration and login system
- **Task Management**: Create, edit, delete, and mark tasks as complete
- **Categories**: Organize tasks with customizable categories and colors
- **Priority Levels**: Set task priorities (Low, Medium, High)
- **Due Dates**: Set and track task deadlines
- **Filtering**: Filter tasks by status and category
- **Pagination**: Efficient handling of large task lists

### User Interface
- **Responsive Design**: Mobile-friendly interface using Bootstrap 5
- **Interactive Elements**: Real-time task completion toggle
- **Modern UI**: Clean, intuitive design with Font Awesome icons
- **Dark/Light Theme Support**: Automatic theme detection

### API
- **RESTful API**: Complete REST API for task operations
- **JSON Responses**: Structured data exchange
- **Authentication**: Secure API endpoints

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLAlchemy ORM with SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication**: Flask-Login with password hashing
- **Forms**: Flask-WTF with CSRF protection
- **Testing**: pytest with coverage reporting
- **Deployment**: Docker support with docker-compose

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd task-manager
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Initialize the database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   
   # Or use the CLI command to add sample data
   python run.py init-db
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

   The application will be available at `http://localhost:5000`

### Docker Setup

1. **Using Docker Compose (Recommended)**
   ```bash
   docker-compose up --build
   ```

2. **Using Docker only**
   ```bash
   docker build -t task-manager .
   docker run -p 5000:5000 task-manager
   ```

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///app.db
FLASK_APP=taskmanager.py
FLASK_ENV=development

# For production with PostgreSQL
# DATABASE_URL=postgresql://username:password@localhost/taskmanager

# Email configuration (optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Database Configuration

The application supports both SQLite (development) and PostgreSQL (production):

- **SQLite**: Default for development, no additional setup required
- **PostgreSQL**: Set `DATABASE_URL` environment variable

## Usage

### Getting Started

1. **Register a new account** or use the default admin account:
   - Username: `admin`
   - Password: `admin123`

2. **Create categories** to organize your tasks:
   - Go to Categories → Add New Category
   - Choose a name, description, and color

3. **Add your first task**:
   - Click "Add New Task"
   - Fill in the title, description, priority, and category
   - Optionally set a due date

4. **Manage your tasks**:
   - Mark tasks as complete by clicking the checkbox
   - Edit tasks by clicking the "Edit" button
   - Delete tasks with the "Delete" button
   - Filter tasks by status or category

### API Usage

The application provides a RESTful API for programmatic access:

#### Authentication
All API endpoints require authentication. Log in through the web interface first.

#### Endpoints

- `GET /api/tasks` - Get all tasks for the current user
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/<id>` - Get a specific task
- `PUT /api/tasks/<id>` - Update a task
- `DELETE /api/tasks/<id>` - Delete a task
- `GET /api/categories` - Get all categories

#### Example API Usage

```bash
# Get all tasks
curl -X GET http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  --cookie "session=your-session-cookie"

# Create a new task
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "New Task", "description": "Task description", "priority": "high"}' \
  --cookie "session=your-session-cookie"
```

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=app

# Run specific test file
python -m pytest tests/test_models.py

# Using the CLI command
python run.py test
```

### Test Structure

- `tests/test_models.py` - Database model tests
- `tests/test_routes.py` - Route and API endpoint tests
- `tests/test_auth.py` - Authentication tests

## Project Structure

```
task-manager/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py            # Database models
│   ├── auth/                # Authentication blueprint
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── forms.py
│   ├── main/                # Main application blueprint
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── forms.py
│   ├── api/                 # API blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── static/              # Static files
│   │   ├── css/
│   │   └── js/
│   └── templates/           # HTML templates
│       ├── base.html
│       ├── index.html
│       ├── auth/
│       └── ...
├── tests/                   # Test files
├── migrations/              # Database migrations
├── config.py               # Configuration settings
├── taskmanager.py          # Application entry point
├── run.py                  # Development server
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
└── README.md              # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write tests for new features
- Update documentation as needed
- Use meaningful commit messages

## Deployment

### Production Deployment

1. **Set environment variables**:
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-production-secret-key
   export DATABASE_URL=postgresql://user:pass@localhost/taskmanager
   ```

2. **Install production dependencies**:
   ```bash
   pip install gunicorn psycopg2-binary
   ```

3. **Run with Gunicorn**:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 taskmanager:app
   ```

### Heroku Deployment

1. Create a `Procfile`:
   ```
   web: gunicorn taskmanager:app
   ```

2. Deploy to Heroku:
   ```bash
   heroku create your-app-name
   heroku addons:create heroku-postgresql:hobby-dev
   git push heroku main
   heroku run flask db upgrade
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions:

1. Check the [Issues](../../issues) page for existing solutions
2. Create a new issue with detailed information
3. Contact the development team

## Changelog

### Version 1.0.0
- Initial release
- Basic task management functionality
- User authentication
- Category system
- REST API
- Responsive web interface

---

**Built with ❤️ using Flask**
