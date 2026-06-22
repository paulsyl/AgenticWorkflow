---
name: development-instructions
description: >
  Development Guidelines and Standards. Use for all development work.
  Covers project structure, design patterns, testing, and documentation requirements.
  Applies globally to all code in this project.
applyTo: "**"
---

# Development Instructions & Guidelines

These are the standards for all development in this project.

## Project Structure

### Recommended Organization

**Layered Architecture**:
```
src/
├── models/           # Data models, database schemas
├── services/         # Business logic, core algorithms
├── api/ or routes/   # API endpoints, HTTP handlers
├── middleware/       # Cross-cutting concerns (auth, logging, error handling)
├── utils/            # Helper functions, constants
└── __init__.py       # Package initialization
```

### Module Naming

- **Files**: `snake_case.py` (e.g., `user_service.py`)
- **Classes**: `PascalCase` (e.g., `UserService`)
- **Functions**: `snake_case` (e.g., `get_user_by_id`)
- **Constants**: `UPPER_CASE` (e.g., `MAX_RETRIES = 3`)

### Separation of Concerns

- **Models** (`src/models/`): Data definitions (ORM models, Pydantic schemas)
- **Services** (`src/services/`): Business logic (validation, transformations, external calls)
- **API** (`src/api/` or `src/routes/`): HTTP handlers (receive request, call service, return response)
- **Middleware** (`src/middleware/`): Logging, authentication, error handling, rate limiting
- **Utils** (`src/utils/`): Generic helpers (formatters, validators, constants)

Example:

```python
# ✅ CORRECT
# models/user.py
class User:
    id: int
    email: str
    created_at: datetime

# services/user_service.py
class UserService:
    def create_user(self, email: str) -> User:
        # Business logic: validation, authorization, etc.
        ...
    
    def get_user(self, user_id: int) -> User:
        ...

# api/user_api.py
@app.post('/users')
def create_user_endpoint(request):
    email = request.json.get('email')
    user = user_service.create_user(email)
    return {'id': user.id, 'email': user.email}
```

## Design Patterns

### 1. Repository Pattern (Data Access)

Isolate database queries behind a consistent interface:

```python
# models/user_repository.py
class UserRepository:
    def __init__(self, db):
        self.db = db
    
    def find_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter_by(id=user_id).first()
    
    def find_by_email(self, email: str) -> User:
        return self.db.query(User).filter_by(email=email).first()
    
    def save(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        return user
```

### 2. Service Layer (Business Logic)

Separate business logic from HTTP/API concerns:

```python
# services/user_service.py
class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    def create_user(self, email: str, password: str) -> User:
        # Validation
        if not email or not password:
            raise ValueError("Email and password required")
        
        # Business logic
        existing = self.user_repo.find_by_email(email)
        if existing:
            raise ValueError(f"Email already exists: {email}")
        
        # Creation
        user = User(email=email, password_hash=hash_password(password))
        return self.user_repo.save(user)
```

### 3. Middleware (Cross-Cutting Concerns)

Handle logging, authentication, error handling in middleware:

```python
# middleware/auth.py
def auth_middleware(request):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        raise PermissionError("Authorization token required")
    
    try:
        user = jwt.verify_token(token)
        request.user = user
    except jwt.InvalidTokenError:
        raise PermissionError("Invalid token")

# middleware/error_handler.py
def error_middleware(request, handler):
    try:
        return handler(request)
    except ValueError as e:
        return {'error': str(e), 'status': 400}
    except PermissionError as e:
        return {'error': str(e), 'status': 403}
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return {'error': 'Internal server error', 'status': 500}
```

### 4. Dependency Injection

Pass dependencies explicitly instead of importing globally:

```python
# ❌ WRONG - Global import
class UserService:
    def __init__(self):
        self.db = get_global_db()  # Hard to test

# ✅ CORRECT - Dependency injection
class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo  # Easy to mock in tests

# Usage
user_repo = UserRepository(db)
user_service = UserService(user_repo)
```

## Testing Requirements

### Unit Tests

Test individual functions/methods in isolation:

```python
# tests/services/test_user_service.py
import pytest
from unittest.mock import Mock
from services.user_service import UserService

def test_create_user_requires_email():
    mock_repo = Mock()
    service = UserService(mock_repo)
    
    with pytest.raises(ValueError):
        service.create_user(email="", password="password")

def test_create_user_hashes_password():
    mock_repo = Mock()
    service = UserService(mock_repo)
    
    user = service.create_user(email="user@example.com", password="secret")
    
    assert user.password_hash != "secret"
    mock_repo.save.assert_called_once()
```

### Integration Tests

Test how components work together:

```python
# tests/integration/test_user_api.py
def test_create_user_endpoint(client, db):
    response = client.post('/users', json={
        'email': 'user@example.com',
        'password': 'password123',
    })
    
    assert response.status_code == 201
    assert response.json['id'] > 0
    
    # Verify in database
    user = db.query(User).filter_by(email='user@example.com').first()
    assert user is not None
```

### Edge Case Tests

Test boundary conditions and error scenarios:

```python
def test_create_user_rejects_duplicate_email(user_repo):
    user_repo.save(User(email='test@example.com'))
    
    with pytest.raises(ValueError, match="Email already exists"):
        user_service.create_user('test@example.com', 'password')

def test_create_user_validates_email_format(user_service):
    with pytest.raises(ValueError, match="Invalid email"):
        user_service.create_user('not-an-email', 'password')

def test_password_must_be_at_least_8_chars(user_service):
    with pytest.raises(ValueError, match="Password too short"):
        user_service.create_user('user@example.com', 'short')
```

### Test Coverage Goals

- **Core logic**: 80%+ coverage (business logic, services)
- **API endpoints**: 100% for happy path + error paths
- **Security**: 100% for authentication, authorization, input validation
- **Edge cases**: 100% for boundary conditions

### Testing Frameworks

Use the standard testing framework for your language:

- **Python**: `pytest` + `pytest-cov`
- **Node.js**: `jest` or `mocha`
- **Go**: `testing` package + `testify`

## Documentation Requirements

### Docstrings

Every function, class, and module must have a docstring:

```python
"""
Module: user_service.py

Provides business logic for user management: creation, retrieval, updates.
Depends on UserRepository for data access.
"""

class UserService:
    """
    User business logic and operations.
    
    Encapsulates validation, authorization, and service layer logic for users.
    Does not depend on HTTP framework; easily testable.
    """
    
    def create_user(self, email: str, password: str) -> User:
        """
        Create a new user account.
        
        Args:
            email: User email (must be unique, valid format).
            password: User password (must be >= 8 characters).
        
        Returns:
            The created User object with ID assigned.
        
        Raises:
            ValueError: If email already exists or password too short.
        
        Example:
            >>> user = user_service.create_user('john@example.com', 'secure123')
            >>> user.id > 0
            True
        """
        pass
```

### Inline Comments

Comments should explain **why**, not **what**:

```python
# ❌ WRONG
result = items.reverse()  # Reverse the list

# ✅ CORRECT
# Start processing from newest items first
result = items.reverse()

# ✅ CORRECT
# Use reverse sort instead of sort + slice for O(n) instead of O(n log n)
result = sorted(items, reverse=True)[:10]
```

### README

Include a README with:

1. **Project Description**: What does this do?
2. **Quick Start**: How do I get it running?
3. **API/Usage**: How do I use it?
4. **Configuration**: What environment variables are needed?
5. **Testing**: How do I run tests?
6. **Dependencies**: What's installed?

Example structure:

```markdown
# User Service

REST API for user management and authentication.

## Quick Start

```bash
pip install -r requirements.txt
export DATABASE_URL=postgresql://localhost/userdb
python -m pytest  # Run tests
python app.py     # Start server
```

## API Endpoints

### Create User
POST /users
```json
{
  "email": "user@example.com",
  "password": "secure123"
}
```

## Configuration

- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET`: Secret for JWT token signing
- `LOG_LEVEL`: DEBUG, INFO, WARNING, ERROR

## Testing

Run unit and integration tests:
```bash
pytest -v --cov=src --cov-report=html
```
```

### Change Logs

For significant changes, update a CHANGELOG:

```markdown
# Changelog

## [2.0.0] - 2026-06-22

### Added
- New user roles: Viewer, Editor, Admin
- Rate limiting on login endpoint

### Changed
- JWT token expiration increased from 1h to 24h
- Password minimum length increased from 6 to 8 characters

### Fixed
- Fixed race condition in cache eviction
- Fixed SQL injection vulnerability in search
```

## Code Review Standards

### Before Committing

Ask yourself:
- ✅ Does it pass all tests?
- ✅ Does it follow the project structure?
- ✅ Are there any hardcoded secrets?
- ✅ Are there any SQL injection vulnerabilities?
- ✅ Is error handling complete?
- ✅ Is the code documented?
- ✅ Are there any unnecessary abstractions?
- ✅ Can this be simpler (Ponytail check)?

### Code Review Checklist

When reviewing others' code:
1. **Tests**: Does it have tests? Are they sufficient?
2. **Security**: Are secrets safe? Is input validated?
3. **Performance**: Any N+1 queries? Unbounded loops?
4. **Readability**: Is it clear? Are comments explaining *why*?
5. **Patterns**: Does it follow the project's conventions?
6. **Simplicity**: Can it be simpler (Ponytail check)?

## Error Handling

### Always Handle Errors

```python
# ❌ WRONG - No error handling
response = requests.get(url)
data = response.json()

# ✅ CORRECT - Explicit error handling
try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    data = response.json()
except requests.RequestException as e:
    logger.error(f"Failed to fetch {url}: {e}")
    raise ValueError(f"External service unavailable")
```

### Log Errors with Context

```python
# ❌ WRONG
logger.error("Database error")

# ✅ CORRECT
logger.error(f"Failed to create user: {email}", exc_info=True, extra={
    'email': email,
    'timestamp': datetime.utcnow().isoformat(),
})
```

## Logging Standards

Use structured logging:

```python
import logging

logger = logging.getLogger(__name__)

# ✅ CORRECT
logger.info("User created", extra={'user_id': user.id, 'email': user.email})
logger.warning("Rate limit approaching", extra={'remaining': remaining_quota})
logger.error("Payment failed", extra={'user_id': user.id, 'error': str(e)})
```

## Performance Considerations

### Database Queries

- Avoid N+1 queries (use joins or eager loading)
- Add indexes for frequently queried columns
- Use pagination for large datasets

### Caching

- Cache frequently accessed data
- Set reasonable TTLs
- Invalidate cache on updates

### Async Operations

- Use async for I/O operations (HTTP calls, database queries)
- Use task queues for long-running operations

---

See also:
- `.github/instructions/core-workflow-base.instructions.md` — Workflow phases
- `.github/instructions/security-coding-standards.instructions.md` — Security requirements
- `.github/instructions/ponytail-rules.instructions.md` — Code simplicity
