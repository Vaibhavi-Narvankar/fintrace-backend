# AWS Deployment

## Current Architecture

FinTrace backend is containerized using Docker and deployed to AWS.

### Components

- Amazon ECR — Docker image registry
- Amazon ECS — container deployment
- Amazon RDS PostgreSQL — managed database
- AWS Secrets Manager — application secrets
- CloudWatch — application/container logging

## Deployment Flow

Developer
↓
GitHub
↓
Docker Build
↓
Amazon ECR
↓
Amazon ECS
↓
FastAPI
↓
Amazon RDS PostgreSQL

## Current Status

- [x] Dockerized FastAPI backend
- [x] PostgreSQL containerized locally
- [x] ECR repository created
- [x] Docker image pushed to ECR
- [ ] RDS PostgreSQL
- [ ] ECS deployment
- [ ] Secrets Manager
- [ ] CloudWatch
- [ ] Production configuration