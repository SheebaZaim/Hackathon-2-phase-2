---
name: sqlmodel-skill
description: Use this skill to define and manage database models with SQLModel, ensuring type-safe ORM integration with FastAPI.
---

# SQLModel Agent Skill

## Instructions
1. Define SQLModel classes for each table with proper field types.  
2. Establish relationships and foreign keys between models.  
3. Ensure Pydantic validation is correct and consistent.  
4. Integrate models with FastAPI endpoints and repositories.  
5. Manage migrations and schema changes using SQLModel metadata.  
6. Maintain alignment between ORM models and Neon PostgreSQL database.  
7. Avoid redundant or inconsistent fields.  

## Examples
- Define a `User` model with id, email, and hashed password.  
- Add a one-to-many relationship between `User` and `Todo` models.  
- Use SQLModel session to query and create records.  
- Apply migrations after adding a new `status` field to `Todo` model.  
