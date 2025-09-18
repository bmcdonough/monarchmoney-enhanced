# Authentication & Session Management

This module handles all authentication, MFA, and session lifecycle operations for the MonarchMoney Enhanced library.

## 🔐 Authentication Methods

### `login(email, password, use_saved_session=True, save_session=True, mfa_secret_key=None, session_file=None)`

Primary authentication method for logging into Monarch Money.

**Parameters:**
- `email` (str): User's email address
- `password` (str): User's password
- `use_saved_session` (bool, default=True): Whether to attempt using existing saved session
- `save_session` (bool, default=True): Whether to save session after successful login
- `mfa_secret_key` (str, optional): MFA secret for automatic TOTP generation
- `session_file` (str, optional): Custom session file path

**Returns:** None (sets up authenticated session)

**Raises:**
- `ValidationError`: If credentials are invalid or missing
- `AuthenticationError`: If login fails
- `MFARequiredError`: If MFA is required but not provided
- `RateLimitError`: If too many login attempts

**Example:**
```python
# Basic login
await mm.login("user@email.com", "password")

# Login with MFA secret
await mm.login(
    email="user@email.com",
    password="password", 
    mfa_secret_key="ABCD1234EFGH5678"
)

# Force fresh login (ignore saved session)
await mm.login(
    email="user@email.com",
    password="password",
    use_saved_session=False
)
```

### `multi_factor_authenticate(email, password, code)`

Complete MFA authentication when required.

**Parameters:**
- `email` (str): User's email address
- `password` (str): User's password  
- `code` (str): 6-8 digit MFA code (email OTP or TOTP)

**Returns:** None

**Raises:**
- `InvalidMFAError`: If MFA code is invalid
- `AuthenticationError`: If authentication fails

**Example:**
```python
try:
    await mm.login("user@email.com", "password")
except MFARequiredError:
    # User will be prompted for MFA code
    mfa_code = input("Enter MFA code: ")
    await mm.multi_factor_authenticate("user@email.com", "password", mfa_code)
```

**Note:** The library automatically detects email OTP (6 digits) vs authenticator TOTP codes and uses the appropriate authentication field.

## 🔄 Session Management

### `validate_session()`

Check if the current session is valid by making a lightweight API call.

**Returns:** bool (True if session is valid)

**Example:**
```python
is_valid = await mm.validate_session()
if not is_valid:
    print("Session expired, need to re-authenticate")
```

### `ensure_valid_session()`

Ensure session is valid, automatically refreshing if necessary.

**Returns:** None

**Raises:**
- `AuthenticationError`: If session cannot be validated or refreshed

**Example:**
```python
# This will automatically refresh session if stale
await mm.ensure_valid_session()
```

### `get_session_info()`

Get information about the current session state.

**Returns:** Dict with session metadata:
```python
{
    "has_token": bool,           # Whether auth token exists
    "has_csrf": bool,            # Whether CSRF token exists  
    "is_authenticated": bool,    # Whether fully authenticated
    "last_used": float,          # Last activity timestamp
    "created": float,            # Session creation timestamp
    "age_seconds": float,        # Current session age
    "is_stale": bool            # Whether session needs validation
}
```

**Example:**
```python
info = await mm.get_session_info()
print(f"Session age: {info['age_seconds']} seconds")
print(f"Is stale: {info['is_stale']}")
```

## 💾 Session Persistence

### `save_session(session_file=None)`

Save the current session to encrypted storage for later use.

**Parameters:**
- `session_file` (str, optional): Custom session file path

**Returns:** None

**Example:**
```python
# Save to default location
await mm.save_session()

# Save to custom location
await mm.save_session("/path/to/my_session.json")
```

### `load_session(session_file=None)`

Load a previously saved session from storage.

**Parameters:**
- `session_file` (str, optional): Custom session file path

**Returns:** None

**Raises:**
- `FileNotFoundError`: If session file doesn't exist
- `AuthenticationError`: If session is invalid or corrupted

**Example:**
```python
# Load from default location
await mm.load_session()

# Load from custom location  
await mm.load_session("/path/to/my_session.json")
```

### `delete_session(session_file=None)`

Delete a saved session file.

**Parameters:**
- `session_file` (str, optional): Custom session file path

**Returns:** None

**Example:**
```python
# Delete default session
await mm.delete_session()

# Delete custom session
await mm.delete_session("/path/to/my_session.json")
```

## 🔒 Security Features

### Session Encryption

Sessions are encrypted using the `cryptography` library with AES encryption:

- **Default**: Uses a default password with AES encryption
- **Custom Password**: Provide custom password for enhanced security
- **Fallback**: Falls back to plain JSON if cryptography unavailable

### Session Security Best Practices

1. **Use MFA**: Enable multi-factor authentication on your Monarch Money account
2. **Secure Storage**: Store session files in secure locations with appropriate permissions
3. **Custom Passwords**: Use custom session passwords for enhanced security
4. **Regular Rotation**: Periodically delete and recreate sessions
5. **Environment Variables**: Store credentials in environment variables, not code

### Rate Limiting Protection

The library includes built-in protection against rate limiting:

- **Exponential Backoff**: Automatic retry with increasing delays (1s, 2s, 4s, etc.)
- **Maximum Retries**: Configurable retry limits (default: 3 attempts)
- **Smart Detection**: Automatic detection of 429 status codes
- **User Guidance**: Clear error messages and retry recommendations

## 🚨 Error Handling

### Common Authentication Errors

```python
from monarchmoney import (
    AuthenticationError,
    MFARequiredError, 
    InvalidMFAError,
    RateLimitError,
    ValidationError
)

try:
    await mm.login("user@email.com", "password")
except ValidationError as e:
    print(f"Invalid credentials: {e}")
except MFARequiredError:
    # Handle MFA requirement
    code = input("Enter MFA code: ")
    await mm.multi_factor_authenticate("user@email.com", "password", code)
except RateLimitError as e:
    print(f"Rate limited: {e}")
    print("Wait 15-30 minutes before trying again")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
```

### Session Error Recovery

```python
async def ensure_authenticated():
    try:
        await mm.ensure_valid_session()
    except AuthenticationError:
        # Session invalid, need fresh login
        await mm.login(email, password, use_saved_session=False)
```

## 🔧 Advanced Configuration

### Custom Session Storage

```python
# Initialize with custom session file
mm = MonarchMoney(session_file="/secure/path/session.json")

# Use custom encryption password
mm = MonarchMoney(session_password="my_secure_password")
```

### Session Validation Settings

```python
# Configure session staleness threshold (default: 1 hour)
mm = MonarchMoney(session_stale_threshold=3600)

# Disable automatic session validation
mm = MonarchMoney(auto_validate_session=False)
```

## 📝 Usage Patterns

### Long-Running Applications

```python
async def long_running_app():
    mm = MonarchMoney()
    
    # Initial authentication
    await mm.login(email, password)
    
    while True:
        try:
            # Ensure session is valid before each operation
            await mm.ensure_valid_session()
            
            # Perform API operations
            accounts = await mm.get_accounts()
            
            await asyncio.sleep(300)  # Wait 5 minutes
            
        except AuthenticationError:
            # Re-authenticate if needed
            await mm.login(email, password, use_saved_session=False)
```

### Batch Processing

```python
async def batch_process():
    mm = MonarchMoney()
    
    # Use saved session for batch jobs
    try:
        await mm.load_session()
        await mm.validate_session()
    except (FileNotFoundError, AuthenticationError):
        # Fresh login if no valid session
        await mm.login(email, password)
        await mm.save_session()
    
    # Process data...
    
    # Clean up
    await mm.close()
```

### Interactive Sessions

```python
async def interactive_session():
    mm = MonarchMoney()
    
    # Interactive login with MFA support
    await mm.interactive_login()
    
    # Save for future use
    await mm.save_session()
    
    # Continue with operations...
```