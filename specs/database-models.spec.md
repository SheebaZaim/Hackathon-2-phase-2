# Teachers Planning App - Database Models Specification

## Technology Stack
- SQLModel for ORM operations
- Neon PostgreSQL database
- Compatible with async operations

## Entity Models

### Teacher Model
```python
class Teacher(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    first_name: str
    last_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    classes: list["Class"] = Relationship(back_populates="teacher")
```

### Class Model
```python
class Class(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    subject: str
    grade_level: str
    teacher_id: int = Field(foreign_key="teacher.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    teacher: Teacher = Relationship(back_populates="classes")
    students: list["Student"] = Relationship(back_populates="class")
```

### Student Model
```python
class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    student_id: str = Field(unique=True, index=True)  # School-assigned ID
    class_id: int = Field(foreign_key="class.id")
    enrollment_date: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    class: Class = Relationship(back_populates="students")
    results: list["Result"] = Relationship(back_populates="student")
```

### Subject Model
```python
class Subject(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)  # e.g., "Mathematics", "Science"
    code: str = Field(unique=True, index=True)  # e.g., "MATH101", "SCI201"
    description: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    results: list["Result"] = Relationship(back_populates="subject")
```

### Result Model
```python
class Result(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    subject_id: int = Field(foreign_key="subject.id")
    score: float  # Numeric score (e.g., percentage)
    grade: str    # Letter grade (e.g., A+, B-, etc.)
    assignment_name: str
    assignment_date: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: Student = Relationship(back_populates="results")
    subject: Subject = Relationship(back_populates="results")
```

## Database Constraints
- Unique constraints on email for Teacher
- Unique constraints on student_id for Student
- Unique constraints on name and code for Subject
- Foreign key relationships enforced
- Indexes on frequently queried fields (email, student_id, etc.)

## Indexing Strategy
- Primary keys automatically indexed
- Email field in Teacher table (for authentication)
- Student ID in Student table (for quick lookups)
- Class ID in Student table (for class queries)
- Student ID and Subject ID in Result table (for result queries)

## Migration Strategy
- Use Alembic for database migrations
- Maintain backward compatibility where possible
- Plan for data migration when schema changes
- Backup strategy before applying migrations

## Security Considerations
- Data isolation between teachers (each teacher sees only their data)
- Proper foreign key constraints to maintain referential integrity
- Validation at the database level where appropriate
- Encryption of sensitive data if required by regulations