# FinTrace

A production-oriented personal finance management backend built with
**FastAPI and PostgreSQL**, focused on secure API design, async
processing, database performance, and observability.

## Features

### Authentication & Authorization

-   JWT access and refresh token authentication
-   Password hashing with bcrypt
-   Protected API endpoints
-   Access vs refresh token validation
-   User ownership validation
-   Soft-delete aware authentication
-   Secure authentication error handling

### Expense & Category Management

-   Create, update, retrieve and soft-delete expenses
-   Expense categorization
-   Payment and tax tracking
-   Historical expense dates
-   User-scoped resources
-   Category ownership validation

### Dashboard & Analytics

-   Dashboard summary
-   Weekly, monthly and yearly expense trends
-   Category-wise expense breakdown
-   Highest spending category
-   Budget progress
-   Recurring expense detection
-   PostgreSQL aggregation queries

### Database

-   PostgreSQL
-   SQLAlchemy 2.0
-   Async SQLAlchemy sessions
-   Alembic migrations
-   Relationships and normalization
-   Query indexing
-   Timestamps
-   Soft deletes

### Validation & Error Handling

-   Pydantic v2 validation
-   Strict input validation
-   Standardized API responses
-   Custom exceptions
-   Global exception handling
-   Secure error responses
-   Prevention of sensitive error leakage

### Logging & Monitoring

-   Centralized logging
-   Request logging middleware
-   Request IDs and request duration tracking
-   Client IP logging
-   Authentication event logging
-   Transaction audit logging
-   Suspicious activity logging
-   Application health check

### Security / AppSec

Security work is guided by OWASP Top 10 and API security principles.

-   SQL injection audit
-   SQLAlchemy parameterized queries
-   JWT security
-   Ownership-based authorization
-   IDOR audit
-   Strict validation
-   Secure error handling
-   Sensitive information protection in logs

## Architecture

``` text
Client
  ↓
API / Routers
  ↓
Authentication & Validation
  ↓
Service Layer
  ↓
Async SQLAlchemy
  ↓
PostgreSQL
```

### Project Structure

``` text
app/
├── api/
├── core/
├── db/
├── middleware/
├── models/
├── schemas/
├── services/
└── main.py
```

## Tech Stack

**Backend** - Python - FastAPI - Pydantic v2 - SQLAlchemy 2.0 -
PostgreSQL - Alembic

**Infrastructure** - Docker - Docker Compose - Uvicorn - AWS

**Security** - JWT - Passlib / bcrypt - OWASP security practices

## Development Status

### Completed

-   Core FastAPI backend
-   PostgreSQL + SQLAlchemy
-   Alembic migrations
-   Authentication and authorization
-   Expense, category and profile APIs
-   Dashboard analytics
-   Async database architecture
-   Request validation
-   Standardized responses
-   Global exception handling
-   Logging and monitoring foundation
-   Initial OWASP security audit

### In Progress

-   OWASP Top 10 security hardening
-   IDOR / access-control testing
-   Security headers
-   Production security hardening

### Planned

-   Bank and credit-card statement upload
-   PDF transaction extraction
-   RAG-based financial intelligence
-   AI-powered financial assistant
-   Vector database integration
-   AWS production deployment
-   CI/CD improvements
-   Advanced monitoring

## AI / RAG Roadmap

The next major feature is AI-powered financial intelligence using RAG.

Planned flow:

``` text
Bank / Credit Card Statement
        ↓
Document Upload
        ↓
Text & Transaction Extraction
        ↓
Chunking + Embeddings
        ↓
Vector Database
        ↓
RAG Retrieval
        ↓
Context-aware AI Response
```

The goal is to let users ask questions about their own financial
documents and transaction history rather than generating generic
financial summaries.

## Project Goal

FinTrace is being built to demonstrate practical backend engineering
beyond basic CRUD APIs, with a focus on:

-   Secure API development
-   Async architecture
-   Database performance
-   Authentication and authorization
-   Validation and error handling
-   Logging and observability
-   OWASP security
-   AI/RAG integration
-   Production deployment
