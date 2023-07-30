## Introduction
The aim of this project is to try to build an API that is as dependent as possible
on the web framework and the database.

The software architecture used is known as "clean architecture."
This is the name used by Robert Martin in his post:
https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html

## Installation
### Install dependencies
```
poetry install
```

### Run tests
```
pytest --cov=app --cov-report=term-missing --cov-report=html
```

## Roadmap
- [x] FastAPI framework
  - [x] Automatic validation
  - [x] Interactive documentation
- [ ] Flask framework
  - [ ] Automatic validation
  - [ ] Interactive documentation
- [x] PostgreSQL repository
- [ ] Alembic migrations
- [x] MongoDB repository
