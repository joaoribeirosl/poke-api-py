# ⚡ Poke-API

A RESTful API built with FastAPI simulating a Pokemon world!

Live App: [https://poke-api-py.fly.dev](https://poke-api-py.fly.dev)  
Docs: [https://poke-api-py.fly.dev/docs](https://poke-api-py.fly.dev/docs)

---

## 🚀 Tech Stack

- 🐍 Python 3.12+
- 🪶 Poetry: Dependency management and packaging
- ⚡ FastAPI: Python Web Framework for building APIs
- 🐘 PostgreSQL: Relational database
- 🔐 JWT Authentication
- 🧪 Pytest: Test suite
- 🏭 Factory boy: Fixtures replacement tool
- 🐳 Docker: Containerization 
- 📦 Fly.io: Deploy
- 📄 Alembic: Database migrations
- ✨ SQLAlchemy 2.0: ORM for database interaction

---

## 🧠 Features

### 🔑 Auth
| Method | Route            | Description                        |
|--------|------------------|------------------------------------|
| POST   | `/auth/token`            | Login for access token     |
| POST   | `/auth/refresh_token`    | Refresh access token       |


### 👤 Users
| Method | Route            | Description                        |
|--------|------------------|------------------------------------|
| POST     | `/users/`           | Register a new user           |
| GET      | `/users/`           | Get all users                 |
| PUT      | `/users/{user_id}`  | Update user                   |
| DELETE   | `/users/{user_id}`  | Delete user                   |

---

### 🧬 Pokemons
| Method | Route               | Description                         |
|--------|---------------------|-------------------------------------|
| POST   | `/pokemon/`                | Add a new Pokemon to user    |
| GET    | `/pokemon/`                | List user's Pokemons         |
| PATCH  | `/pokemon/{pokemon_id}`    | Patch a specific Pokemon     |
| DELETE | `/pokemon/{pokemon_id}`    | Delete a specific Pokemon    |

---



## 🧪 Running Locally

```bash
# Clone the project
git clone https://github.com/joaoribeirosl/poke-api.git

# Install dependencies with Poetry
poetry install

# Activate the virtual environment
poetry shell

# Create .env with .env.example fields!

# Run the app (you can run also with 'fastapi dev poke_app/app.py')
task run 
```

## 🐳 Running with Docker 

```bash
# Run both the API and PostgreSQL using Docker Compose
docker compose up --build

# After building
docker compose up -d

# To stop and remove containers
docker compose down
```

## 🧪 Running Tests
```bash
task test
```

Tests are located in the tests/ directory and use pytest.
Includes coverage for users, pokemon, and authentication flows.

## 📬 API Documentation

Once the app is running locally or via Docker, you can access the interactive docs at:


| Environment | Swagger UI                         | ReDoc                              |
|-------------|-------------------------------------|------------------------------------|
| Local       | [localhost:8000/docs](http://localhost:8000/docs) | [localhost:8000/redoc](http://localhost:8000/redoc) |
| Production (Fly.io) | [https://poke-api-py.fly.dev/docs](https://poke-api-py.fly.dev/docs) | [https://poke-api-py.fly.dev/redoc](https://poke-api-py.fly.dev/redoc) |



## 📌 To-Do

- [x] User CRUD
- [x] Pokemon CRUD
- [x] JWT Authentication
- [ ] Random Capture
- [ ] Training System
- [ ] Battle System
- [x] Trading System
- [ ] Global Ranking
- [x] Swagger Documentation


## 🙌 Contributing
Pull requests are welcome and if you have suggestions or improvements, feel free to open an issue.

## ✉️ Contact
Made with ❤️ by a Pokemon enthusiast! 

Find me on: [Gmail](mailto:joaoribeiroslira@gmail.com) and [LinkedIn](https://www.linkedin.com/in/joaoribeirosl)

