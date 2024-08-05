# HR Portal

This is a Django-based HR portal application designed to manage new hires and tasks. The project uses Django Channels for handling WebSocket connections and CORS headers for cross-origin requests.

## Table of Contents

- [Setup](#setup)
- [Running the Project](#running-the-project)
- [Architecture](#architecture)
- [Design Choices](#design-choices)

## Setup

### Prerequisites

- Python 3.8+
- Django 5.0.7
- PostgreSQL

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/hrportal.git
   cd hrportal
   ```

2. **Create a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set up the environment variables:**

   Create a `.env` file in the `portal` directory and add the necessary environment variables:

   ```env
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PORT=your_db_port
   ```

5. **Apply migrations:**

   ```sh
   python manage.py makemigrations portal
   python manage.py migrate
   ```

## Running the Project

1. **Start the development server:**

   ```sh
   python manage.py runserver
   ```

   or

   ```sh
    uvicorn hrportal.asgi:application --port 8000
   ```

   for asgi server and websockets support

2. **Access the application:**

   Open your browser and navigate to `http://localhost:8000`.

## Architecture

The project is structured as follows:

- **hrportal/**: The main Django project directory containing settings and URL configurations.

  - `settings.py`: Contains the project settings, including installed apps, middleware, and database configurations.
  - `urls.py`: Defines the URL patterns for the project.
  - `asgi.py`: ASGI configuration for Django Channels.
  - `wsgi.py`: WSGI configuration for deployment.

- **portal/**: The main application directory containing business logic.

  - `models.py`: Defines the database models.
  - `views.py`: Contains the view functions for handling HTTP requests.
  - `urls.py`: Defines the URL patterns for the application.
  - `consumers.py`: Contains WebSocket consumers for real-time features.
  - `admin.py`: Registers models with the Django admin site.

- **manage.py**: A command-line utility for administrative tasks.

## Design Choices

### Django Channels

The project uses Django Channels to handle WebSocket connections, enabling real-time features such as live updates and notifications.

### CORS Headers

The `corsheaders` middleware is used to handle Cross-Origin Resource Sharing (CORS), allowing the frontend to make requests to the backend from different origins.

### Environment Variables

Sensitive information such as the secret key and database URL are stored in environment variables, loaded using `python-dotenv`.

### Modular Structure

The project follows a modular structure, separating concerns into different apps and files. This makes the codebase easier to manage and scale.

### RESTful API

The application follows RESTful principles, with clear and consistent URL patterns for different resources such as new hires and tasks.
