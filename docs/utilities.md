# Utility Methods

This module provides utility functions for GraphQL execution, debugging, session management, and library information.

## 🔧 GraphQL Operations

### `gql_call(operation, graphql_query, variables=None)`

Execute a GraphQL query with comprehensive error handling and optimization.

**Parameters:**
- `operation` (str): The GraphQL operation name for logging and debugging
- `graphql_query` (DocumentNode): The GraphQL query object (from `gql()`)
- `variables` (Dict, optional): Variables to pass to the GraphQL query

**Returns:** Dict with GraphQL response data

**Raises:**
- `GraphQLError`: If GraphQL operation fails
- `AuthenticationError`: If session is invalid
- `NetworkError`: If network request fails
- `RateLimitError`: If rate limited

**Example:**
```python
from gql import gql

# Define GraphQL query
query = gql("""
    query GetAccountSummary($accountId: ID!) {
        account(id: $accountId) {
            id
            displayName
            currentBalance
            type {
                name
                display
            }
        }
    }
""")

# Execute query
result = await mm.gql_call(
    operation="GetAccountSummary",
    graphql_query=query,
    variables={"accountId": "account_123"}
)

account = result["account"]
print(f"Account: {account['displayName']}")
print(f"Balance: ${account['currentBalance']:,.2f}")
```

## 🔍 Session Utilities

### `validate_session()`

Validate current session by making a lightweight API call.

**Returns:** bool (True if session is valid)

**Example:**
```python
if await mm.validate_session():
    print("Session is valid")
else:
    print("Session expired, need to re-authenticate")
    await mm.login(email, password)
```

### `get_session_info()`

Get comprehensive information about the current session state.

**Returns:** Dict with session metadata:
```python
{
    "authenticated": bool,           # Whether user is authenticated
    "session_age_seconds": float,    # Age of current session
    "last_activity": str,            # Last activity timestamp
    "csrf_token": bool,              # Whether CSRF token is present
    "auth_token": bool,              # Whether auth token is present
    "session_file": str,             # Session file path
    "encrypted": bool,               # Whether session is encrypted
    "user_agent": str,               # User agent being used
    "device_uuid": str               # Device UUID for session
}
```

**Example:**
```python
session_info = await mm.get_session_info()

print(f"Authenticated: {session_info['authenticated']}")
print(f"Session age: {session_info['session_age_seconds']:.0f} seconds")
print(f"Session file: {session_info['session_file']}")

# Check if session needs refresh
if session_info['session_age_seconds'] > 3600:  # 1 hour
    print("Session is getting old, consider refreshing")
```

## 🧹 Resource Management

### `close()`

Close HTTP session and cleanup resources properly.

**Returns:** None

**Example:**
```python
try:
    # Perform API operations
    accounts = await mm.get_accounts()
    transactions = await mm.get_transactions()
    
finally:
    # Always cleanup resources
    await mm.close()
```

### Context Manager Usage

The MonarchMoney client can be used as an async context manager for automatic resource cleanup:

```python
async with MonarchMoney() as mm:
    await mm.login(email, password)
    accounts = await mm.get_accounts()
    # Resources are automatically cleaned up when exiting context
```

## 📋 Library Information

### `get_version()`

Get version and build information for the library.

**Returns:** Dict with version information:
```python
{
    "version": str,                  # Library version (e.g., "0.9.9")
    "build_date": str,               # Build date
    "python_version": str,           # Python version used
    "dependencies": {                # Key dependency versions
        "aiohttp": str,
        "gql": str,
        "oathtool": str,
        "cryptography": str
    },
    "features": {                    # Available features
        "optimizations": bool,       # GraphQL optimizations available
        "encryption": bool,          # Session encryption available
        "caching": bool              # Query caching available
    },
    "commit_hash": str,              # Git commit hash (if available)
    "author": str                    # Library author
}
```

**Example:**
```python
version_info = await mm.get_version()

print(f"MonarchMoney Enhanced v{version_info['version']}")
print(f"Python: {version_info['python_version']}")
print(f"Features: {', '.join(k for k, v in version_info['features'].items() if v)}")

# Check if optimizations are available
if version_info['features']['optimizations']:
    print("✅ GraphQL optimizations enabled")
else:
    print("⚠️ GraphQL optimizations not available")
```

## 🐛 Debug & Diagnostics

### Debug Mode

Enable debug mode for detailed logging and troubleshooting:

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

mm = MonarchMoney(debug=True)
```

### Connection Diagnostics

```python
async def diagnose_connection():
    """Diagnose connection and authentication issues."""
    diagnostics = {
        'network': await test_network_connectivity(),
        'authentication': await test_authentication(),
        'session': await test_session_validity(),
        'graphql': await test_graphql_endpoint()
    }
    
    return diagnostics

async def test_network_connectivity():
    """Test basic network connectivity to Monarch Money."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://monarchmoney.com") as response:
                return {
                    'status': 'success',
                    'status_code': response.status,
                    'response_time_ms': response.headers.get('X-Response-Time', 'unknown')
                }
    except Exception as e:
        return {
            'status': 'failed',
            'error': str(e)
        }

async def test_authentication():
    """Test authentication status."""
    try:
        is_valid = await mm.validate_session()
        return {
            'status': 'success' if is_valid else 'invalid',
            'session_valid': is_valid
        }
    except Exception as e:
        return {
            'status': 'failed',
            'error': str(e)
        }

async def test_session_validity():
    """Test session validity and metadata."""
    try:
        session_info = await mm.get_session_info()
        return {
            'status': 'success',
            'session_info': session_info
        }
    except Exception as e:
        return {
            'status': 'failed',
            'error': str(e)
        }

async def test_graphql_endpoint():
    """Test GraphQL endpoint connectivity."""
    try:
        # Simple query to test GraphQL
        from gql import gql
        
        query = gql("""
            query TestQuery {
                me {
                    id
                }
            }
        """)
        
        result = await mm.gql_call("TestQuery", query)
        return {
            'status': 'success',
            'graphql_working': True,
            'user_id': result.get('me', {}).get('id', 'unknown')
        }
    except Exception as e:
        return {
            'status': 'failed',
            'error': str(e)
        }
```

### Performance Monitoring

```python
async def monitor_api_performance(operations):
    """Monitor API performance for multiple operations."""
    import time
    
    performance_data = []
    
    for operation_name, operation_func in operations.items():
        start_time = time.time()
        
        try:
            result = await operation_func()
            end_time = time.time()
            
            performance_data.append({
                'operation': operation_name,
                'status': 'success',
                'duration_ms': (end_time - start_time) * 1000,
                'result_size': len(str(result)) if result else 0
            })
            
        except Exception as e:
            end_time = time.time()
            
            performance_data.append({
                'operation': operation_name,
                'status': 'failed',
                'duration_ms': (end_time - start_time) * 1000,
                'error': str(e)
            })
    
    return performance_data

# Example usage
operations = {
    'get_accounts': lambda: mm.get_accounts(),
    'get_transactions': lambda: mm.get_transactions(limit=10),
    'get_budgets': lambda: mm.get_budgets()
}

performance = await monitor_api_performance(operations)
for perf in performance:
    print(f"{perf['operation']}: {perf['duration_ms']:.1f}ms ({perf['status']})")
```

## 🔧 Configuration Utilities

### Environment Configuration

```python
def get_optimal_configuration():
    """Get optimal configuration based on environment."""
    import os
    import platform
    
    config = {
        'session_timeout': 3600,        # 1 hour default
        'max_retries': 3,
        'request_timeout': 30,
        'use_compression': True,
        'enable_caching': True
    }
    
    # Adjust for production environments
    if os.getenv('ENVIRONMENT') == 'production':
        config.update({
            'session_timeout': 7200,    # 2 hours for production
            'max_retries': 5,
            'enable_detailed_logging': False
        })
    
    # Adjust for development
    elif os.getenv('ENVIRONMENT') == 'development':
        config.update({
            'session_timeout': 1800,    # 30 minutes for dev
            'enable_detailed_logging': True,
            'debug_mode': True
        })
    
    # Platform-specific adjustments
    if platform.system() == 'Windows':
        config['session_file_extension'] = '.json'  # Better Windows compatibility
    
    return config

# Apply optimal configuration
config = get_optimal_configuration()
mm = MonarchMoney(
    session_timeout=config['session_timeout'],
    max_retries=config['max_retries'],
    debug=config.get('debug_mode', False)
)
```

### Batch Operation Utilities

```python
async def batch_operation_with_progress(operations, batch_size=5, show_progress=True):
    """Execute operations in batches with progress tracking."""
    import asyncio
    
    results = []
    total_operations = len(operations)
    
    for i in range(0, total_operations, batch_size):
        batch = operations[i:i + batch_size]
        
        if show_progress:
            print(f"Processing batch {i//batch_size + 1}/{(total_operations + batch_size - 1)//batch_size}")
        
        # Execute batch concurrently
        batch_results = await asyncio.gather(*batch, return_exceptions=True)
        results.extend(batch_results)
        
        # Small delay between batches to avoid rate limiting
        if i + batch_size < total_operations:
            await asyncio.sleep(1)
    
    # Separate successful results from errors
    successful = [r for r in results if not isinstance(r, Exception)]
    errors = [r for r in results if isinstance(r, Exception)]
    
    return {
        'successful': successful,
        'errors': errors,
        'success_rate': len(successful) / len(results) * 100 if results else 0
    }

# Example: Batch update multiple transactions
transaction_updates = [
    mm.update_transaction(txn_id, category_id="groceries")
    for txn_id in ["txn_1", "txn_2", "txn_3", "txn_4", "txn_5"]
]

results = await batch_operation_with_progress(transaction_updates, batch_size=2)
print(f"Success rate: {results['success_rate']:.1f}%")
```

## 🚨 Error Handling Utilities

### Comprehensive Error Handler

```python
from monarchmoney import (
    MonarchMoneyError, AuthenticationError, NetworkError, 
    RateLimitError, ValidationError, ServerError
)

async def robust_api_call(api_function, max_retries=3, retry_delay=1):
    """Make API call with comprehensive error handling and retries."""
    import asyncio
    
    for attempt in range(max_retries + 1):
        try:
            return await api_function()
            
        except RateLimitError as e:
            if attempt < max_retries:
                delay = retry_delay * (2 ** attempt)  # Exponential backoff
                print(f"Rate limited, waiting {delay}s before retry {attempt + 1}/{max_retries}")
                await asyncio.sleep(delay)
                continue
            raise
            
        except NetworkError as e:
            if attempt < max_retries:
                print(f"Network error, retrying {attempt + 1}/{max_retries}: {e}")
                await asyncio.sleep(retry_delay)
                continue
            raise
            
        except AuthenticationError as e:
            print(f"Authentication error: {e}")
            # Try to re-authenticate once
            if attempt == 0:
                await mm.ensure_valid_session()
                continue
            raise
            
        except ValidationError as e:
            print(f"Validation error: {e}")
            # Don't retry validation errors
            raise
            
        except ServerError as e:
            if attempt < max_retries:
                print(f"Server error, retrying {attempt + 1}/{max_retries}: {e}")
                await asyncio.sleep(retry_delay * 2)  # Longer delay for server errors
                continue
            raise
            
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

# Example usage
try:
    accounts = await robust_api_call(
        lambda: mm.get_accounts(),
        max_retries=3,
        retry_delay=2
    )
except MonarchMoneyError as e:
    print(f"API call failed after retries: {e}")
```

## 💡 Best Practices

### Resource Management Pattern

```python
class MonarchMoneyManager:
    """Context manager for MonarchMoney operations."""
    
    def __init__(self, email=None, password=None, session_file=None):
        self.email = email
        self.password = password
        self.session_file = session_file
        self.mm = None
    
    async def __aenter__(self):
        self.mm = MonarchMoney(session_file=self.session_file)
        
        if self.email and self.password:
            await self.mm.login(self.email, self.password)
        else:
            await self.mm.load_session()
        
        return self.mm
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.mm:
            await self.mm.close()

# Usage
async with MonarchMoneyManager(email, password) as mm:
    accounts = await mm.get_accounts()
    transactions = await mm.get_transactions()
    # Automatic cleanup on exit
```

### Configuration Management

```python
def create_client_with_config(config_file=None):
    """Create MonarchMoney client with configuration file."""
    import json
    import os
    
    # Default configuration
    config = {
        'session_file': '.mm/session.json',
        'max_retries': 3,
        'timeout': 30,
        'debug': False
    }
    
    # Load from config file
    if config_file and os.path.exists(config_file):
        with open(config_file, 'r') as f:
            file_config = json.load(f)
            config.update(file_config)
    
    # Override with environment variables
    config.update({
        k.lower().replace('MM_', ''): v 
        for k, v in os.environ.items() 
        if k.startswith('MM_')
    })
    
    return MonarchMoney(**config)

# Example usage with config file
mm = create_client_with_config('config/monarchmoney.json')
```