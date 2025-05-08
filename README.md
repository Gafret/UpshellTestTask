# 🛒 RestFul API магазина цифровой техники  
Тестовое задание в EdTech компанию "Upshell"

## 📌 Описание
Тема пет-проекта - разработка API для интернет-магазина электронной техники.

## 🚀 Стек технологий

- **Python 3.10+**
- **FastAPI** — фреймворк для создания асинхронного API
- **SQLModel** — ORM, объединяющая возможности SQLAlchemy и Pydantic
- **PostgreSQL** — реляционная база данных (через `psycopg2`)
- **Pydantic v2** — валидация и сериализация данных
- **Passlib + Bcrypt** — безопасное хеширование паролей
- **PyJWT** — создание и проверка JWT-токенов

## ⚙️ Установка и запуск

```bash
pip install -r requirements.txt
```

### Заполняете .env файл 

```
DATABASE="postgresql://postgres:password@localhost:5432/store"
SECRET_KEY="KEY"
HASH_ALGO="HS256"
ACCESS_TOKEN_TTL_MINUTES=60
REFRESH_TOKEN_TTL_MINUTES=6000
```

### Запускаете

```bash
uvicorn app.main:app --reload
```

### Документация

Документация доступна по endpoint'у

```
http://127.0.0.1:8000/docs
```
