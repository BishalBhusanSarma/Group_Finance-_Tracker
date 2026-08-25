# Finance Tracker API

A FastAPI and PostgreSQL backend for registering users, creating password-protected groups, joining groups, and tracking shared expenses.

## Features

- User registration and login
- JWT access and refresh tokens
- Protected API routes using Bearer authentication
- Create and join expense groups
- Record group expenses
- View group expenses, per-user totals, and a group total

## Tech stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- Psycopg
- Pydantic Settings
- `python-jose` for JWTs
- Passlib + Argon2 for password hashing

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install sqlalchemy pydantic-settings python-multipart "uvicorn[standard]" "psycopg[binary]"
```

Create a PostgreSQL database, then create a `.env` file in the project root:

```env
APP_NAME=Finance_Tracker
DEBUG=true
ACCESS_TOKEN_EXPIRY=30
REFRESH_TOKEN_EXPIRY=30
DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/finance_tracker
ALGORITHM=HS256
SECRET_KEY=replace_with_a_long_random_secret
```

`ACCESS_TOKEN_EXPIRY` is measured in minutes. `REFRESH_TOKEN_EXPIRY` is measured in days.

> Do not commit `.env`. It is already listed in `.gitignore`.

## Database tables

The application uses these tables:

- `user_details` — registered users
- `groups` — expense groups and their creators
- `membership` — users who belong to groups
- `group_expense` — expense records made by group members

This repository currently does not include migrations. Create the tables before using the API.

## Run the API

From the project root:

```bash
uvicorn app.main:app --reload
```

Open the interactive documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Authentication in FastAPI Docs

1. Register a user with `POST /auth/register`.
2. Click **Authorize** in `/docs`.
3. Enter the registered username and password.
4. Click **Authorize** again.
5. Call any protected endpoint.

FastAPI Docs automatically sends:

```http
Authorization: Bearer <access_token>
```

Use a newly generated access token after restarting the server or changing JWT code. Do not use the refresh token for protected routes.

## API endpoints

### Authentication

#### `POST /auth/register`

Registers a user.

```json
{
  "name": "Asha Sharma",
  "username": "asha",
  "email": "asha@example.com",
  "phone": "9876543210",
  "password": "strong-password"
}
```

#### `POST /auth/login`

Logs in with form data, not JSON. FastAPI Docs supplies this form automatically.

```text
username=asha
password=strong-password
```

Successful response:

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer"
}
```

### Groups

All group endpoints require authorization.

#### `POST /group/create_group`

Creates a group and adds the creator as its admin member.

```json
{
  "group_name": "Goa Trip",
  "group_password": "group-password"
}
```

#### `POST /group/join_group`

Joins an existing group using its ID and password.

```json
{
  "group_id": 50000,
  "group_password": "group-password"
}
```

#### `POST /group/expense`

Adds an expense for the authenticated user. The user must be a member of the group.

```json
{
  "group_id": 50000,
  "total": 600,
  "tags": "food",
  "description": "Dinner"
}
```

### Expenses

All expense endpoints require authorization. Provide `group_id` as a query parameter.

#### `GET /Expense/check_group_expense?group_id=50000`

Returns all expense records in the group.

#### `GET /Expense/check_group_expense_by_user?group_id=50000`

Returns expense totals grouped by user ID.

```json
[
  {"user_id": 1, "total_expense": 45559},
  {"user_id": 2, "total_expense": 600}
]
```

#### `GET /Expense/check_total_group_expense?group_id=50000`

Returns the total of all expenses in the group.

```json
{
  "group_id": 50000,
  "group_name": "Goa Trip",
  "total_expense": 46159
}
```

## Common errors

| Response | Meaning |
| --- | --- |
| `401 Invalid or expired access token` | The token is expired, invalid, or a refresh token was used instead of an access token. |
| `403 User not in group` | The authenticated user is not a member of the requested group. |
| `401 Password didnt match` | The group password is incorrect. |
| `301 User already joined` | The user is already a member of that group. |

## Project structure

```text
app/
├── api/v1/routes/       # Authentication, group, and expense endpoints
├── core/                # Environment-based settings
├── database/            # SQLAlchemy engine and session dependency
├── database_functions/  # Database create and query helpers
├── database_tables/     # SQLAlchemy table models
├── hashing/             # Password hashing helpers
├── jwt/                 # JWT creation and validation
├── models/              # Pydantic request and response models
└── main.py              # FastAPI application entry point
```
