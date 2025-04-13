# Tour Management API – FastAPI

This is a RESTful API for managing tours, built with FastAPI and PostgreSQL. It includes user authentication, role-based access control, and is deployed on [Render.com](https://render.com/).

## 🔗 Live Demo
➡️ [Swagger UI](https://tour-management-api-4vfx.onrender.com/docs)

## 🔧 Features
- JWT Authentication
- Role-based Access (admin/user)
- Tour CRUD operations
- PostgreSQL integration
- Clean project structure
- Deployed on Render.com

## 🚀 Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Alembic
- Render (Deployment)

## 📦 Setup Instructions

```bash
git clone https://github.com/fuadhasen/matar.git
cd matar
pip install -r requirements.txt
uvicorn app.main:app --reload
