# Account Management

This module provides comprehensive account management functionality including account operations, balances, institution data, and account synchronization.

## 🏦 Account Information

### `get_accounts()`

Retrieve all linked accounts with balances, types, and institution information.

**Parameters:** None

**Returns:** Dict containing:
```python
{
    "accounts": [
        {
            "id": str,                    # Account ID
            "displayName": str,           # Account display name
            "type": {                     # Account type info
                "name": str,              # Type name (e.g., "checking")
                "display": str            # Display name
            },
            "subtype": {                  # Account subtype
                "name": str,
                "display": str
            },
            "currentBalance": float,      # Current balance
            "availableBalance": float,    # Available balance (if applicable)
            "institution": {              # Financial institution
                "name": str,
                "logoUrl": str,
                "primaryColor": str
            },
            "isHidden": bool,            # Whether hidden from reports
            "syncDisabled": bool,        # Whether sync is disabled
            "includeInNetWorth": bool,   # Include in net worth calculations
            "mask": str,                 # Last 4 digits of account number
            "createdAt": str,            # Account creation date
            "updatedAt": str             # Last update date
        }
    ],
    "summary": {
        "totalAssets": float,
        "totalLiabilities": float,
        "netWorth": float,
        "accountCount": int
    }
}
```

**Example:**
```python
accounts_data = await mm.get_accounts()
for account in accounts_data["accounts"]:
    print(f"{account['displayName']}: ${account['currentBalance']:,.2f}")
    
print(f"Net Worth: ${accounts_data['summary']['netWorth']:,.2f}")
```

### `get_account_type_options()`

Get available account types and subtypes for creating new accounts.

**Returns:** Dict containing available account types:
```python
{
    "accountTypes": [
        {
            "name": str,              # Type identifier (e.g., "depository")
            "display": str,           # Display name (e.g., "Bank Account")
            "subtypes": [
                {
                    "name": str,      # Subtype identifier
                    "display": str    # Subtype display name
                }
            ]
        }
    ]
}
```

**Example:**
```python
options = await mm.get_account_type_options()
for account_type in options["accountTypes"]:
    print(f"Type: {account_type['display']}")
    for subtype in account_type["subtypes"]:
        print(f"  - {subtype['display']}")
```

## 📊 Account History & Balances

### `get_recent_account_balances(account_id=None, start_date=None, end_date=None)`

Get recent balance history for accounts with daily snapshots.

**Parameters:**
- `account_id` (str, optional): Specific account ID (all accounts if None)
- `start_date` (str, optional): Start date in YYYY-MM-DD format
- `end_date` (str, optional): End date in YYYY-MM-DD format

**Returns:** Dict with balance history:
```python
{
    "balances": [
        {
            "accountId": str,
            "date": str,              # YYYY-MM-DD
            "balance": float,
            "availableBalance": float
        }
    ],
    "accounts": [...],            # Account metadata
    "dateRange": {
        "startDate": str,
        "endDate": str
    }
}
```

**Example:**
```python
# Get last 30 days of balance history
from datetime import datetime, timedelta

end_date = datetime.now()
start_date = end_date - timedelta(days=30)

balances = await mm.get_recent_account_balances(
    start_date=start_date.strftime("%Y-%m-%d"),
    end_date=end_date.strftime("%Y-%m-%d")
)

for balance in balances["balances"]:
    print(f"{balance['date']}: ${balance['balance']:,.2f}")
```

### `get_account_history(account_id, start_date=None, end_date=None)`

Get detailed account information with transaction history.

**Parameters:**
- `account_id` (str): Account ID to retrieve history for
- `start_date` (str, optional): Start date for transaction history
- `end_date` (str, optional): End date for transaction history

**Returns:** Dict with account details and transactions:
```python
{
    "account": {...},             # Full account details
    "transactions": [...],        # Recent transactions
    "balanceHistory": [...],      # Balance snapshots
    "summary": {
        "totalTransactions": int,
        "averageBalance": float,
        "highestBalance": float,
        "lowestBalance": float
    }
}
```

**Example:**
```python
account_id = "account_123"
history = await mm.get_account_history(account_id)

print(f"Account: {history['account']['displayName']}")
print(f"Transactions: {history['summary']['totalTransactions']}")
print(f"Average Balance: ${history['summary']['averageBalance']:,.2f}")
```

## ✏️ Account Creation & Management

### `create_manual_account(name, type_name, subtype_name=None, balance=None)`

Create a new manual account.

**Parameters:**
- `name` (str): Display name for the account
- `type_name` (str): Account type identifier (e.g., "depository", "investment")
- `subtype_name` (str, optional): Account subtype identifier
- `balance` (float, optional): Initial account balance

**Returns:** Dict with created account data

**Example:**
```python
# Create a savings account
new_account = await mm.create_manual_account(
    name="Emergency Fund",
    type_name="depository", 
    subtype_name="savings",
    balance=5000.00
)

print(f"Created account: {new_account['displayName']}")
print(f"Account ID: {new_account['id']}")
```

### `update_account(account_id, display_name=None, is_hidden=None, sync_disabled=None)`

Update existing account properties.

**Parameters:**
- `account_id` (str): Account ID to update
- `display_name` (str, optional): New display name
- `is_hidden` (bool, optional): Whether to hide from reports
- `sync_disabled` (bool, optional): Whether to disable automatic sync

**Returns:** Dict with updated account data

**Example:**
```python
# Rename an account and hide it from reports
updated = await mm.update_account(
    account_id="account_123",
    display_name="Old Credit Card",
    is_hidden=True
)

print(f"Updated account: {updated['displayName']}")
```

### `delete_account(account_id)`

Delete an account permanently.

**Parameters:**
- `account_id` (str): Account ID to delete

**Returns:** bool (True if successful)

**Warning:** This permanently deletes all account data including transaction history.

**Example:**
```python
success = await mm.delete_account("account_123")
if success:
    print("Account deleted successfully")
```

## 🔄 Account Synchronization

### `request_accounts_refresh()`

Request refresh of account data from financial institutions.

**Returns:** Dict with refresh status:
```python
{
    "refreshId": str,             # Refresh operation ID
    "status": str,                # Current status
    "startedAt": str,             # Start timestamp
    "accountIds": [str],          # Accounts being refreshed
    "estimatedDuration": int      # Estimated seconds to complete
}
```

**Example:**
```python
refresh = await mm.request_accounts_refresh()
print(f"Refresh started: {refresh['refreshId']}")
print(f"Estimated duration: {refresh['estimatedDuration']} seconds")
```

### `is_accounts_refresh_complete(refresh_id=None, account_ids=None)`

Check if account refresh operation is complete.

**Parameters:**
- `refresh_id` (str, optional): Specific refresh operation ID
- `account_ids` (List[str], optional): Check specific accounts

**Returns:** bool (True if refresh is complete)

**Example:**
```python
# Check specific refresh operation
is_complete = await mm.is_accounts_refresh_complete(refresh_id="refresh_123")

# Check if any account refresh is in progress
is_complete = await mm.is_accounts_refresh_complete()

print(f"Refresh complete: {is_complete}")
```

### `request_accounts_refresh_and_wait(timeout=60, poll_interval=5)`

Request account refresh and wait for completion.

**Parameters:**
- `timeout` (int): Maximum seconds to wait (default: 60)
- `poll_interval` (int): Seconds between status checks (default: 5)

**Returns:** Dict with final refresh status

**Example:**
```python
try:
    result = await mm.request_accounts_refresh_and_wait(timeout=120)
    print(f"Refresh completed: {result['status']}")
except TimeoutError:
    print("Refresh is taking longer than expected")
```

## 📈 Net Worth & Snapshots

### `get_net_worth_history(start_date=None, end_date=None, interval="monthly")`

Get net worth history with account type breakdown.

**Parameters:**
- `start_date` (str, optional): Start date in YYYY-MM-DD format
- `end_date` (str, optional): End date in YYYY-MM-DD format  
- `interval` (str): Data interval ("daily", "weekly", "monthly")

**Returns:** Dict with net worth tracking:
```python
{
    "netWorthHistory": [
        {
            "date": str,              # YYYY-MM-DD
            "netWorth": float,
            "assets": float,
            "liabilities": float,
            "byAccountType": {
                "depository": float,
                "investment": float,
                "credit": float,
                "loan": float
            }
        }
    ],
    "summary": {
        "currentNetWorth": float,
        "previousNetWorth": float,
        "change": float,
        "changePercent": float
    }
}
```

**Example:**
```python
# Get 1 year of net worth history
net_worth = await mm.get_net_worth_history(
    start_date="2023-01-01",
    end_date="2023-12-31",
    interval="monthly"
)

for point in net_worth["netWorthHistory"]:
    print(f"{point['date']}: ${point['netWorth']:,.2f}")
    
change = net_worth["summary"]["changePercent"]
print(f"Net worth change: {change:.1f}%")
```

### `get_account_snapshots_by_type(start_date=None, end_date=None)`

Get balance snapshots grouped by account type.

**Parameters:**
- `start_date` (str, optional): Start date in YYYY-MM-DD format
- `end_date` (str, optional): End date in YYYY-MM-DD format

**Returns:** Dict with snapshots by account type:
```python
{
    "snapshots": {
        "depository": [
            {
                "date": str,
                "balance": float,
                "accountCount": int
            }
        ],
        "investment": [...],
        "credit": [...],
        "loan": [...]
    },
    "totals": {
        "assets": float,
        "liabilities": float,
        "netWorth": float
    }
}
```

### `get_aggregate_snapshots(start_date=None, end_date=None, group_by="month")`

Get aggregated balance snapshots across timeframes.

**Parameters:**
- `start_date` (str, optional): Start date
- `end_date` (str, optional): End date
- `group_by` (str): Grouping period ("day", "week", "month", "quarter", "year")

**Returns:** Dict with aggregated snapshot data

**Example:**
```python
snapshots = await mm.get_aggregate_snapshots(
    start_date="2023-01-01",
    group_by="quarter"
)

for period, data in snapshots["snapshots"].items():
    print(f"Q{period}: ${data['netWorth']:,.2f}")
```

## 📤 Data Import/Export

### `upload_account_balance_history(account_id, balance_data)`

Upload historical balance data for manual accounts.

**Parameters:**
- `account_id` (str): Target account ID
- `balance_data` (List[Dict]): Balance history entries:
  ```python
  [
      {
          "date": "YYYY-MM-DD",
          "balance": float,
          "availableBalance": float  # Optional
      }
  ]
  ```

**Returns:** Dict with upload results:
```python
{
    "imported": int,              # Number of records imported
    "skipped": int,               # Number of records skipped  
    "errors": [str],              # Error messages if any
    "dateRange": {
        "start": str,
        "end": str
    }
}
```

**Example:**
```python
# Upload 6 months of balance history
balance_history = [
    {"date": "2023-01-01", "balance": 1000.00},
    {"date": "2023-02-01", "balance": 1150.00},
    {"date": "2023-03-01", "balance": 1200.00},
    # ... more entries
]

result = await mm.upload_account_balance_history(
    account_id="account_123",
    balance_data=balance_history
)

print(f"Imported {result['imported']} balance records")
```

## 🚨 Error Handling

### Common Account Errors

```python
from monarchmoney import ValidationError, AuthenticationError

try:
    accounts = await mm.get_accounts()
except AuthenticationError:
    print("Session expired, please re-authenticate")
except ValidationError as e:
    print(f"Invalid request: {e}")
```

### Account Creation Errors

```python
try:
    account = await mm.create_manual_account(
        name="Test Account",
        type_name="invalid_type"
    )
except ValidationError as e:
    print(f"Invalid account type: {e}")
    # Get valid types
    options = await mm.get_account_type_options()
    print("Available types:", [t['name'] for t in options['accountTypes']])
```

### Refresh Timeout Handling

```python
try:
    result = await mm.request_accounts_refresh_and_wait(timeout=30)
except asyncio.TimeoutError:
    print("Account refresh is taking longer than expected")
    print("Check refresh status manually with is_accounts_refresh_complete()")
```

## 💡 Best Practices

### Account Organization

```python
# Hide old/inactive accounts
await mm.update_account(
    account_id="old_account",
    is_hidden=True,
    sync_disabled=True
)

# Organize accounts with clear naming
await mm.update_account(
    account_id="checking_123",
    display_name="Primary Checking (Bank of Example)"
)
```

### Efficient Data Retrieval

```python
# Get accounts once and cache the result
accounts_cache = await mm.get_accounts()

# Use account IDs from cache for subsequent operations
for account in accounts_cache["accounts"]:
    if account["type"]["name"] == "investment":
        holdings = await mm.get_account_holdings(account["id"])
```

### Balance Monitoring

```python
async def check_low_balances(threshold=100.0):
    accounts = await mm.get_accounts()
    
    low_balance_accounts = [
        acc for acc in accounts["accounts"] 
        if acc["currentBalance"] < threshold
        and acc["type"]["name"] in ["depository"]
    ]
    
    for account in low_balance_accounts:
        print(f"⚠️ Low balance: {account['displayName']} - ${account['currentBalance']:.2f}")
```