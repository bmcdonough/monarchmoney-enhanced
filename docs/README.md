# MonarchMoney Enhanced API Documentation

This directory contains comprehensive documentation for all API methods available in the MonarchMoney Enhanced library.

## 📚 API Reference

The API is organized into functional categories:

### 🔐 [Authentication & Session Management](authentication.md)
- Login, MFA, and session persistence
- Session validation and management
- Security features and best practices

### 🏦 [Account Management](accounts.md)
- Account operations, balances, and institution data
- Account creation, updates, and deletion
- Account refresh and synchronization

### 💳 [Transaction Management](transactions.md)
- Transaction CRUD operations
- Bulk operations and filtering
- Transaction splits and categorization

### 📝 [Transaction Rules](transaction-rules.md)
- Automated transaction rules and conditions
- Rule creation, updates, and management
- Preview and testing functionality

### 🏷️ [Categories & Tags](categories-tags.md)
- Transaction categorization system
- Tag management and organization
- Category groups and hierarchies

### 🔄 [Recurring Transactions](recurring-transactions.md)
- Recurring transaction streams
- Stream management and reviews
- Future transaction predictions

### 🛍️ [Merchants](merchants.md)
- Merchant data and transaction history
- Merchant editing and recurring settings
- Search and filtering capabilities

### 📊 [Budget Management](budgets.md)
- Budget creation and management
- Flexible budget periods and amounts
- Budget tracking and analysis

### 🎯 [Goals Management](goals.md)
- Financial goal creation and tracking
- Progress monitoring and updates
- Goal categories and timelines

### 💼 [Investment Management](investments.md)
- Investment holdings and portfolio data
- Manual holding management
- Security details and performance metrics

### 📈 [Insights & Analytics](insights.md)
- Financial insights and recommendations
- Spending and income analysis
- Cash flow and bill tracking

### ⚙️ [Settings & User Management](settings.md)
- User profile and preferences
- Account settings and notifications
- Subscription and billing information

### 🔧 [Utility Methods](utilities.md)
- GraphQL execution and debugging
- Version information and diagnostics
- Session cleanup and resource management

## 🚀 Quick Start

```python
from monarchmoney import MonarchMoney

# Initialize client
mm = MonarchMoney()

# Login (will use saved session if available)
await mm.login(email="your@email.com", password="password")

# Get account data
accounts = await mm.get_accounts()
transactions = await mm.get_transactions(limit=50)

# Clean up
await mm.close()
```

## 📖 Additional Resources

- [GRAPHQL.md](../GRAPHQL.md) - GraphQL operation mappings
- [README.md](../README.md) - Main project documentation
- [CHANGELOG.md](../CHANGELOG.md) - Version history and changes
- [Examples](../examples/) - Working code examples

## 🔍 Error Handling

All API methods may raise the following exceptions:

- `AuthenticationError` - Authentication/session issues
- `ValidationError` - Invalid input parameters
- `RateLimitError` - API rate limiting
- `NetworkError` - Network connectivity issues
- `ServerError` - Monarch Money server errors
- `GraphQLError` - GraphQL-specific errors

See individual method documentation for specific error conditions and handling recommendations.

## 📝 Return Format

Most API methods return dictionaries containing:
- **Data**: The requested information
- **Metadata**: Additional context (pagination, timestamps, etc.)
- **Status**: Success/error indicators

Example response structure:
```python
{
    "data": {...},           # Main response data
    "pagination": {...},     # Pagination info (if applicable)
    "meta": {                # Additional metadata
        "timestamp": "...",
        "version": "...",
        "query_time_ms": 123
    }
}
```