---
name: security-coding-standards
description: >
  Security Requirements and Coding Standards. Use for all code development.
  Covers secret handling, configuration safety, authentication, database safety, input validation, and prohibited behaviors.
  Applies globally to all code in this project.
applyTo: "**"
---

# Security Requirements & Coding Standards

All code in this project must adhere to these security and quality standards. These are **non-negotiable**.

## Security Requirements

### 1. Secret Handling

**NEVER hardcode secrets.** Secrets include:
- API keys
- Database passwords
- Authentication tokens
- Private encryption keys
- OAuth credentials
- Webhook secrets

**Always use environment variables** or secure configuration management:

```python
# ❌ WRONG
API_KEY = "sk-1234567890"
db_password = "mysecretpassword"

# ✅ CORRECT
import os
API_KEY = os.environ.get('API_KEY')
db_password = os.environ.get('DATABASE_PASSWORD')

if not API_KEY or not db_password:
    raise ValueError("Missing required environment variables")
```

**In examples and templates**, use placeholders:

```python
# ✅ CORRECT
api_key = os.environ.get('YOUR_API_KEY')  # Placeholder; user provides this
database_password = os.environ.get('DB_PASSWORD')
```

**Never log secrets**:

```python
# ❌ WRONG
print(f"Connecting with token: {api_key}")
logger.info(f"Password: {password}")

# ✅ CORRECT
logger.info("Connected to database")  # Don't log the password
```

### 2. Configuration Safety

**Default to secure configurations** unless explicitly requested otherwise.

**CORS (Cross-Origin Resource Sharing)**:

```python
# ❌ WRONG
CORS_ALLOWED_ORIGINS = ['*']  # Wildcard = security risk

# ✅ CORRECT
CORS_ALLOWED_ORIGINS = [
    'https://example.com',
    'https://app.example.com',
]
```

**Cookies**:

```python
# ❌ WRONG
response.set_cookie('session_id', session_id)

# ✅ CORRECT
response.set_cookie(
    'session_id',
    session_id,
    httponly=True,      # Prevents JavaScript access
    secure=True,        # HTTPS only
    samesite='Strict',  # CSRF protection
    max_age=3600,       # Expires in 1 hour
)
```

**Default permissions**: Deny-by-default, grant explicitly.

### 3. Authentication & Authorization

**Use established authentication frameworks** for the tech stack:
- Python: `flask-login`, `django.contrib.auth`
- Node.js: `passport.js`, `next-auth`
- Go: `gorilla/sessions`

**Never implement custom password hashing.** Use library functions:

```python
# ❌ WRONG
import hashlib
hashed = hashlib.md5(password).hexdigest()

# ✅ CORRECT
from werkzeug.security import generate_password_hash, check_password_hash
hashed = generate_password_hash(password, method='pbkdf2:sha256')
```

**Enforce least privilege**:
- User roles: Admin, Editor, Viewer (no "SuperUser")
- API scopes: Only grant the minimum scope needed
- Database users: Read-only where possible

**Example role check**:

```python
# ✅ CORRECT
def require_admin(func):
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'admin':
            raise PermissionError("Admin access required")
        return func(request, *args, **kwargs)
    return wrapper
```

### 4. Database Safety

**Avoid raw SQL** unless absolutely necessary. Use an ORM or query builder:

```python
# ❌ WRONG - SQL Injection Risk
user_id = request.args.get('id')
query = f"SELECT * FROM users WHERE id = {user_id}"
result = db.execute(query)

# ✅ CORRECT - Parameterized Query (ORM)
from models import User
user = User.query.filter_by(id=user_id).first()

# ✅ CORRECT - Parameterized Query (Raw SQL with params)
query = "SELECT * FROM users WHERE id = ?"
result = db.execute(query, (user_id,))
```

**Schema validation**: Validate data before inserting:

```python
# ✅ CORRECT
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
```

### 5. Input Validation

**Validate at every trust boundary:**

- **External API calls** → validate response
- **User uploads** → validate type, size, content
- **Form submissions** → validate required fields, format
- **Database queries** → validate parameter types
- **Configuration files** → validate schema

Example:

```python
# ❌ WRONG
email = request.form.get('email')
user = User.create(email=email)  # No validation

# ✅ CORRECT
import email_validator

email = request.form.get('email')
if not email:
    raise ValueError("Email is required")

try:
    email_validator.validate_email(email)
except email_validator.EmailNotValidError:
    raise ValueError("Invalid email format")

user = User.create(email=email)
```

**Type checking**:

```python
# ✅ CORRECT
def process_age(age_str: str) -> int:
    try:
        age = int(age_str)
        if age < 0 or age > 150:
            raise ValueError("Age must be between 0 and 150")
        return age
    except ValueError:
        raise ValueError(f"Invalid age: {age_str}")
```

### 6. File Upload Safety

**Validate file uploads strictly:**

```python
# ✅ CORRECT
import magic
import os

ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png', 'image/webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

def validate_upload(file):
    # Check size
    if len(file.read()) > MAX_FILE_SIZE:
        raise ValueError("File too large")
    file.seek(0)  # Reset file pointer
    
    # Check MIME type (by content, not extension)
    mime_type = magic.from_buffer(file.read(1024), mime=True)
    file.seek(0)
    if mime_type not in ALLOWED_MIME_TYPES:
        raise ValueError(f"File type not allowed: {mime_type}")
    
    # Generate safe filename (prevent path traversal)
    safe_filename = os.path.basename(file.filename)
    safe_filename = "".join(c for c in safe_filename if c.isalnum() or c in '._-')
    
    return safe_filename
```

---

## Coding Standards

### 1. Project Structure

**Follow the recommended structure** for the framework/language:

Python project:
```
project/
├── src/
│   ├── __init__.py
│   ├── models/
│   ├── services/
│   ├── api/
│   └── utils/
├── tests/
├── docs/
├── .env.example
├── requirements.txt
├── setup.py
└── README.md
```

Node.js project:
```
project/
├── src/
│   ├── models/
│   ├── services/
│   ├── routes/
│   └── utils/
├── tests/
├── docs/
├── .env.example
├── package.json
└── README.md
```

**Keep concerns separate:**
- Models in `models/`
- Business logic in `services/`
- API routes in `routes/` or `api/`
- Tests in `tests/` or `__tests__/`

### 2. Design Patterns

**Prefer established patterns:**
- Repository pattern for data access
- Service layer for business logic
- Middleware for cross-cutting concerns (logging, auth, error handling)
- Dependency injection for loose coupling

**Avoid ad-hoc solutions.** If you're unsure, use the framework's recommended pattern.

### 3. Dependencies

**Use stable, maintained, and secure dependencies:**

```python
# ✅ Good
requests==2.28.0          # Stable, widely maintained
sqlalchemy==2.0.0         # Industry standard ORM
pytest==7.2.0             # Standard testing framework

# ❌ Avoid
requests @ git+https://github.com/unknown/fork.git  # Unstable fork
made-up-library==1.0.0    # Unknown maintainer
old-library==0.1.0        # Abandoned project
```

**Avoid unnecessary third-party packages:**

```python
# ❌ WRONG - Don't add a dependency for a one-liner
from dateutil.relativedelta import relativedelta
next_year = datetime.now() + relativedelta(years=1)

# ✅ CORRECT - Use stdlib
from datetime import datetime, timedelta
next_year = datetime.now() + timedelta(days=365)
```

**Pin major versions** in production requirements:

```
# requirements.txt
requests==2.28.0       # Pin minor version
sqlalchemy==2.0.0
pytest>=7.0,<8.0       # Allow patch updates
```

---

## Testing Requirements

All non-trivial code must have tests.

### Unit Tests

Test core logic in isolation:

```python
# tests/services/test_auth.py
def test_validate_email_rejects_invalid_format():
    with pytest.raises(ValueError):
        validate_email("not-an-email")

def test_validate_email_accepts_valid_format():
    result = validate_email("user@example.com")
    assert result is True
```

### Integration Tests

Test components working together:

```python
# tests/api/test_user_api.py
def test_create_user_returns_201(client, db):
    response = client.post('/users', json={
        'email': 'user@example.com',
        'name': 'John Doe',
    })
    assert response.status_code == 201
    assert response.json['id'] > 0
    
    # Verify in database
    user = db.session.query(User).filter_by(email='user@example.com').first()
    assert user is not None
```

### Test Coverage

- Core business logic: 80%+ coverage
- API endpoints: 100% for happy path + error cases
- Security-sensitive operations: 100% coverage

---

## Documentation Requirements

Every significant module, function, or class must include documentation.

### Docstrings (Functions & Classes)

```python
def calculate_discount(price: float, discount_percent: float) -> float:
    """
    Calculate the discounted price.
    
    Args:
        price: The original price in dollars (must be > 0).
        discount_percent: The discount percentage (0-100).
    
    Returns:
        The discounted price as a float.
    
    Raises:
        ValueError: If price <= 0 or discount_percent < 0.
    
    Example:
        >>> calculate_discount(100.0, 10.0)
        90.0
    """
    if price <= 0:
        raise ValueError("Price must be > 0")
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be 0-100")
    return price * (1 - discount_percent / 100)
```

### Inline Comments

Use comments to explain **why**, not **what**:

```python
# ❌ WRONG - Comment explains what the code does
x = x + 1  # Increment x

# ✅ CORRECT - Comment explains why
# Start queue processing from index 1 (index 0 is reserved for the control msg)
x = 1

# ✅ CORRECT - Comment explains non-obvious logic
# Sort in reverse order so we can pop from the end (faster than pop(0))
items = sorted(items, reverse=True)
```

### README Updates

When adding major features, update the README:
- Description of the feature
- Usage examples
- Configuration needed
- Dependencies added

---

## Prohibited Behaviors

Agents must **NEVER**:

- ❌ Generate insecure code (hardcoded secrets, weak passwords, no validation)
- ❌ Suggest disabling security middleware or checks
- ❌ Expose stack traces or internal errors to end users
- ❌ Produce harmful, abusive, or discriminatory content
- ❌ Generate code violating privacy or data protection laws (GDPR, CCPA, etc.)
- ❌ Create backdoors or intentional vulnerabilities

---

## When Unsure

- Ask clarifying questions
- Default to the safest implementation
- Never implement workarounds to "make it work"
- Ask for user confirmation before proceeding with risky decisions

---

See also:
- `.github/instructions/core-workflow-base.instructions.md` — Workflow phases
- `.github/instructions/ponytail-rules.instructions.md` — Code simplicity
- `.github/instructions/development-instructions.instructions.md` — Testing and documentation
