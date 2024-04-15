# DSNube-MISW4204-2024-12

This is a FastAPI project that includes user authentication and task management functionalities. The project utilizes FastAPI, SQLAlchemy for interacting with a PostgreSQL database. The docker-compose setup takes care of the necessary environment setup, making it easy to get started.

### Requirements

- Docker

### Run Project Using Docker

1. **Clone the repository:**
```bash
git clone https://github.com/dparejaUniandes/DSNube-MISW4204-2024-12.git
cd DSNube-MISW4204-2024-12
```

2. **Build and run the Docker containers:**
```bash
docker-compose build
docker-compose up
```

## Usage

Once the Docker containers are up and running, application will be available at http://localhost:81/

## API Endpoints

The API includes the following endpoints:

- **User Authentication**
    - `POST /user/api/auth/signup`: Sign up a new user.
    - `POST /user/api/auth/login`: Log in and receive an access token.

- **Task Management**
    - `GET /user/api/tasks`: Get a list of tasks.
    - `POST /user/api/tasks`: Create a new task.
    - `GET /user/api/tasks/{id_task}`: Retrieve details of a specific task.
    - `DELETE /user/api/tasks/{id_task}`: Delete a specific task.
