# FinTrace

FinTrace is a personal finance management backend built using FastAPI and PostgreSQL. It provides secure authentication, expense tracking, category management, user profile management, and analytical dashboard APIs.

---

## Features

### Authentication

- User Registration
- User Login
- JWT Access Token Authentication
- Refresh Token Authentication
- Password Hashing (bcrypt)

### User Profile

- View Profile
- Update Profile
- Monthly Income Management
- Currency Preference
- Timezone Preference
- Profile Picture Support

### Category Management

- Create Category
- View Categories
- Update Category
- Soft Delete Category
- Budget Allocation per Category

### Expense Management

- Create Expense
- View Expenses
- Update Expense
- Soft Delete Expense
- Expense Categorization
- Payment Type Support

### Dashboard Analytics

- Dashboard Summary
- Expense Trends (Weekly / Monthly / Yearly)
- Category-wise Expense Breakdown
- Highest Spending Category
- Budget Progress
- Recurring Expenses

---

## Database Features

- PostgreSQL
- SQLAlchemy ORM
- Alembic Migrations
- Database Relationships
- Database Normalization
- Query Indexing
- Soft Delete
- Automatic Timestamps

---

## Architecture

Layered Architecture

- Routers
- Services
- Models
- Schemas
- Database Layer
- Dependency Injection
- Environment Configuration

---

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- Pydantic v2
- JWT Authentication
- Passlib (bcrypt)
- Docker

---

## Project Structure

```text
app/
├── api/
├── core/
├── db/
├── models/
├── schemas/
├── services/
```

---

## Concepts Implemented

### Backend Development

- REST API Development
- Layered Architecture
- Dependency Injection
- Service Layer Pattern

### Database

- SQLAlchemy ORM
- Database Relationships
- Normalization
- Indexing
- Aggregate Queries
- Soft Delete
- Alembic Migrations

### Security

- JWT Authentication
- Refresh Tokens
- Password Hashing
- Protected Routes

### Dashboard Analytics

- Aggregate Functions
- Group By Queries
- Date-based Analytics
- Budget Calculations
- Category Analytics

---

## Upcoming Features

- Pagination
- Filtering & Search
- Sorting
- Unit Testing
- Logging
- Redis Caching
- Background Tasks
- API Rate Limiting