# Transaction Management

This module provides comprehensive transaction management including CRUD operations, bulk operations, filtering, splits, and categorization.

## 📋 Transaction Retrieval

### `get_transactions_summary()`

Get high-level transaction summary with aggregates from the transactions page.

**Returns:** Dict containing:
```python
{
    "summary": {
        "totalIncome": float,         # Total income in period
        "totalExpenses": float,       # Total expenses in period
        "netCashflow": float,         # Income - expenses
        "transactionCount": int,      # Total transaction count
        "averageTransaction": float,  # Average transaction amount
        "largestExpense": float,      # Largest single expense
        "largestIncome": float        # Largest single income
    },
    "categoryBreakdown": [
        {
            "categoryId": str,
            "categoryName": str,
            "amount": float,
            "transactionCount": int,
            "percentage": float       # Percentage of total expenses
        }
    ],
    "timeRange": {
        "startDate": str,            # YYYY-MM-DD
        "endDate": str
    }
}
```

**Example:**
```python
summary = await mm.get_transactions_summary()
print(f"Net Cashflow: ${summary['summary']['netCashflow']:,.2f}")
print(f"Total Transactions: {summary['summary']['transactionCount']}")

for category in summary['categoryBreakdown'][:5]:  # Top 5 categories
    print(f"{category['categoryName']}: ${category['amount']:,.2f}")
```

### `get_transactions_summary_card()`

Get transaction summary card data with total counts and metrics.

**Returns:** Dict with summary card information:
```python
{
    "totalCount": int,               # Total transactions
    "pendingCount": int,             # Pending transactions
    "reviewCount": int,              # Transactions needing review
    "hiddenCount": int,              # Hidden transactions
    "duplicateCount": int,           # Potential duplicates
    "uncategorizedCount": int,       # Uncategorized transactions
    "dateRange": {
        "startDate": str,
        "endDate": str
    }
}
```

### `get_transactions(limit=100, offset=0, start_date=None, end_date=None, category_ids=None, account_ids=None, tag_ids=None, merchant_ids=None, search=None, is_credit=None, abs_amount_range=None)`

Get paginated transactions with comprehensive filtering options.

**Parameters:**
- `limit` (int): Maximum transactions to return (default: 100)
- `offset` (int): Number of transactions to skip (default: 0)
- `start_date` (str): Start date in YYYY-MM-DD format
- `end_date` (str): End date in YYYY-MM-DD format
- `category_ids` (List[str]): Filter by category IDs
- `account_ids` (List[str]): Filter by account IDs
- `tag_ids` (List[str]): Filter by tag IDs
- `merchant_ids` (List[str]): Filter by merchant IDs
- `search` (str): Text search in merchant/notes
- `is_credit` (bool): Filter by transaction type (True=income, False=expense)
- `abs_amount_range` (Dict): Amount range filter `{"min": float, "max": float}`

**Returns:** Dict with paginated transaction data:
```python
{
    "transactions": [
        {
            "id": str,                   # Transaction ID
            "amount": float,             # Transaction amount (negative for expenses)
            "date": str,                 # Transaction date (YYYY-MM-DD)
            "merchant": str,             # Merchant name
            "notes": str,                # Transaction notes
            "isRecurring": bool,         # Whether part of recurring pattern
            "isPending": bool,           # Whether pending
            "isReviewed": bool,          # Whether reviewed
            "hideFromReports": bool,     # Whether hidden from reports
            "needsReview": bool,         # Whether needs manual review
            "account": {
                "id": str,
                "displayName": str,
                "mask": str
            },
            "category": {
                "id": str,
                "name": str,
                "icon": str,
                "color": str
            },
            "tags": [
                {
                    "id": str,
                    "name": str,
                    "color": str
                }
            ],
            "splits": [                  # If transaction has splits
                {
                    "id": str,
                    "amount": float,
                    "category": {...}
                }
            ]
        }
    ],
    "pagination": {
        "hasNextPage": bool,
        "totalCount": int,
        "currentOffset": int,
        "currentLimit": int
    },
    "filters": {                         # Applied filters
        "dateRange": {...},
        "categories": [...],
        "accounts": [...]
    }
}
```

**Example:**
```python
# Get recent transactions for specific account
transactions = await mm.get_transactions(
    limit=50,
    account_ids=["account_123"],
    start_date="2024-01-01",
    end_date="2024-01-31"
)

for txn in transactions["transactions"]:
    print(f"{txn['date']}: {txn['merchant']} - ${abs(txn['amount']):,.2f}")

# Check if more pages available
if transactions["pagination"]["hasNextPage"]:
    next_page = await mm.get_transactions(
        offset=transactions["pagination"]["currentOffset"] + 50
    )
```

## ✏️ Transaction Creation & Updates

### `create_transaction(account_id, merchant, amount, date, category_id=None, notes=None)`

Create a new transaction.

**Parameters:**
- `account_id` (str): Account ID where transaction occurred
- `merchant` (str): Merchant/payee name
- `amount` (float): Transaction amount (positive for income, negative for expenses)
- `date` (str): Transaction date in YYYY-MM-DD format
- `category_id` (str, optional): Transaction category ID
- `notes` (str, optional): Additional notes

**Returns:** Dict with created transaction data

**Example:**
```python
# Create an expense
expense = await mm.create_transaction(
    account_id="checking_123",
    merchant="Coffee Shop",
    amount=-4.50,
    date="2024-01-15",
    category_id="food_dining",
    notes="Morning coffee"
)

# Create income
income = await mm.create_transaction(
    account_id="checking_123", 
    merchant="Employer",
    amount=3000.00,
    date="2024-01-01",
    category_id="salary"
)

print(f"Created transaction: {expense['id']}")
```

### `update_transaction(transaction_id, merchant=None, amount=None, date=None, category_id=None, notes=None, hide_from_reports=None)`

Update an existing transaction.

**Parameters:**
- `transaction_id` (str): Transaction ID to update
- `merchant` (str, optional): New merchant name
- `amount` (float, optional): New transaction amount
- `date` (str, optional): New transaction date
- `category_id` (str, optional): New category ID
- `notes` (str, optional): New notes
- `hide_from_reports` (bool, optional): Whether to hide from reports

**Returns:** Dict with updated transaction data

**Example:**
```python
# Update transaction category and notes
updated = await mm.update_transaction(
    transaction_id="txn_123",
    category_id="entertainment",
    notes="Updated category after review"
)

# Hide transaction from reports
await mm.update_transaction(
    transaction_id="txn_123",
    hide_from_reports=True
)
```

### `delete_transaction(transaction_id)`

Delete a transaction permanently.

**Parameters:**
- `transaction_id` (str): Transaction ID to delete

**Returns:** bool (True if successful)

**Example:**
```python
success = await mm.delete_transaction("txn_123")
if success:
    print("Transaction deleted successfully")
```

## 📄 Transaction Details & Splits

### `get_transaction_details(transaction_id)`

Get detailed information for a specific transaction including splits and tags.

**Parameters:**
- `transaction_id` (str): Transaction ID

**Returns:** Dict with detailed transaction data:
```python
{
    "transaction": {
        "id": str,
        "amount": float,
        "date": str,
        "merchant": str,
        "notes": str,
        "account": {...},
        "category": {...},
        "tags": [...],
        "splits": [...],
        "attachments": [...],        # Receipt attachments
        "recurring": {              # Recurring info if applicable
            "streamId": str,
            "frequency": str,
            "nextDate": str
        }
    },
    "relatedTransactions": [...],   # Similar transactions
    "suggestions": {                # AI suggestions
        "categories": [...],
        "merchants": [...],
        "tags": [...]
    }
}
```

### `get_transaction_splits(transaction_id)`

Get split information for a transaction.

**Parameters:**
- `transaction_id` (str): Transaction ID

**Returns:** Dict with transaction splits:
```python
{
    "splits": [
        {
            "id": str,
            "amount": float,
            "category": {
                "id": str,
                "name": str
            },
            "notes": str
        }
    ],
    "totalAmount": float,
    "remainingAmount": float
}
```

### `update_transaction_splits(transaction_id, splits)`

Update splits for a transaction.

**Parameters:**
- `transaction_id` (str): Transaction ID
- `splits` (List[Dict]): Split configurations:
  ```python
  [
      {
          "amount": float,
          "category_id": str,
          "notes": str
      }
  ]
  ```

**Returns:** Dict with updated transaction and splits

**Example:**
```python
# Split a grocery transaction
splits = [
    {"amount": -50.00, "category_id": "groceries", "notes": "Food items"},
    {"amount": -15.00, "category_id": "household", "notes": "Cleaning supplies"},
    {"amount": -10.00, "category_id": "personal_care", "notes": "Toiletries"}
]

updated = await mm.update_transaction_splits(
    transaction_id="txn_123",
    splits=splits
)

print(f"Split transaction into {len(splits)} categories")
```

## 📦 Bulk Operations

### `bulk_update_transactions(transaction_ids, updates, excluded_transaction_ids=None, all_selected=False, filters=None)`

Perform bulk updates on multiple transactions.

**Parameters:**
- `transaction_ids` (List[str]): Transaction IDs to update
- `updates` (Dict): Updates to apply:
  ```python
  {
      "category_id": str,           # New category
      "hide_from_reports": bool,    # Hide/show status
      "tags": List[str],            # Tag IDs to set
      "notes": str                  # Notes to set
  }
  ```
- `excluded_transaction_ids` (List[str], optional): IDs to exclude from bulk operation
- `all_selected` (bool): Whether operation applies to all matching transactions
- `filters` (Dict, optional): Filters that define "all" transactions

**Returns:** Dict with bulk operation results:
```python
{
    "updated": int,                 # Number of transactions updated
    "skipped": int,                 # Number of transactions skipped
    "errors": [str],                # Any error messages
    "affectedTransactions": [str]   # IDs of updated transactions
}
```

**Example:**
```python
# Bulk categorize coffee shop transactions
transaction_ids = ["txn_1", "txn_2", "txn_3"]
updates = {
    "category_id": "food_dining",
    "notes": "Coffee expenses"
}

result = await mm.bulk_update_transactions(
    transaction_ids=transaction_ids,
    updates=updates
)

print(f"Updated {result['updated']} transactions")
```

### `bulk_unhide_transactions(transaction_ids, filters=None)`

Convenience method to bulk unhide transactions.

**Parameters:**
- `transaction_ids` (List[str]): Transaction IDs to unhide
- `filters` (Dict, optional): Additional filters

**Returns:** Dict with bulk operation results

### `bulk_hide_transactions(transaction_ids, filters=None)`

Convenience method to bulk hide transactions.

**Parameters:**
- `transaction_ids` (List[str]): Transaction IDs to hide
- `filters` (Dict, optional): Additional filters

**Returns:** Dict with bulk operation results

**Example:**
```python
# Hide all transactions from a specific merchant
merchant_transactions = await mm.get_transactions(
    merchant_ids=["merchant_123"]
)

transaction_ids = [t["id"] for t in merchant_transactions["transactions"]]
result = await mm.bulk_hide_transactions(transaction_ids)

print(f"Hidden {result['updated']} transactions")
```

### `get_hidden_transactions(limit=100, offset=0, order_by="date")`

Get transactions that are hidden from reports.

**Parameters:**
- `limit` (int): Maximum transactions to return
- `offset` (int): Number to skip for pagination
- `order_by` (str): Sort order ("date", "amount", "merchant")

**Returns:** Dict with hidden transactions (same format as `get_transactions`)

## 🔍 Advanced Filtering

### Date Range Filtering

```python
# Get transactions for specific month
transactions = await mm.get_transactions(
    start_date="2024-01-01",
    end_date="2024-01-31"
)

# Get transactions for last 30 days
from datetime import datetime, timedelta
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

transactions = await mm.get_transactions(
    start_date=start_date.strftime("%Y-%m-%d"),
    end_date=end_date.strftime("%Y-%m-%d")
)
```

### Amount Filtering

```python
# Get large expenses (over $500)
large_expenses = await mm.get_transactions(
    abs_amount_range={"min": 500.0},
    is_credit=False  # Expenses only
)

# Get transactions in specific amount range
moderate_expenses = await mm.get_transactions(
    abs_amount_range={"min": 50.0, "max": 200.0}
)
```

### Text Search

```python
# Search for specific merchant or notes
coffee_transactions = await mm.get_transactions(
    search="coffee",
    limit=50
)

# Search for transactions with specific notes
business_expenses = await mm.get_transactions(
    search="business expense"
)
```

### Multiple Filter Combination

```python
# Complex filtering example
filtered_transactions = await mm.get_transactions(
    start_date="2024-01-01",
    end_date="2024-03-31",
    category_ids=["dining", "entertainment"],
    account_ids=["checking_123"],
    abs_amount_range={"min": 20.0, "max": 100.0},
    is_credit=False,
    limit=100
)
```

## 📊 Transaction Analysis

### Spending by Category

```python
async def analyze_spending_by_category(start_date, end_date):
    transactions = await mm.get_transactions(
        start_date=start_date,
        end_date=end_date,
        is_credit=False,  # Expenses only
        limit=1000
    )
    
    category_totals = {}
    for txn in transactions["transactions"]:
        cat_name = txn["category"]["name"]
        amount = abs(txn["amount"])
        category_totals[cat_name] = category_totals.get(cat_name, 0) + amount
    
    # Sort by spending amount
    sorted_categories = sorted(
        category_totals.items(), 
        key=lambda x: x[1], 
        reverse=True
    )
    
    return sorted_categories
```

### Monthly Spending Trends

```python
async def monthly_spending_trend(year):
    monthly_totals = {}
    
    for month in range(1, 13):
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year + 1}-01-01"
        else:
            end_date = f"{year}-{month + 1:02d}-01"
        
        transactions = await mm.get_transactions(
            start_date=start_date,
            end_date=end_date,
            is_credit=False
        )
        
        total = sum(abs(t["amount"]) for t in transactions["transactions"])
        monthly_totals[f"{year}-{month:02d}"] = total
    
    return monthly_totals
```

## 🚨 Error Handling

### Transaction Operation Errors

```python
from monarchmoney import ValidationError, AuthenticationError

try:
    transaction = await mm.create_transaction(
        account_id="invalid_account",
        merchant="Test",
        amount=100.0,
        date="2024-01-01"
    )
except ValidationError as e:
    print(f"Invalid transaction data: {e}")
except AuthenticationError:
    print("Authentication required")
```

### Bulk Operation Error Handling

```python
result = await mm.bulk_update_transactions(
    transaction_ids=["txn_1", "txn_2", "invalid_txn"],
    updates={"category_id": "food_dining"}
)

if result["errors"]:
    print(f"Bulk operation had {len(result['errors'])} errors:")
    for error in result["errors"]:
        print(f"  - {error}")

print(f"Successfully updated {result['updated']} transactions")
```

## 💡 Best Practices

### Efficient Pagination

```python
async def get_all_transactions(start_date, end_date):
    all_transactions = []
    offset = 0
    limit = 100
    
    while True:
        batch = await mm.get_transactions(
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            offset=offset
        )
        
        all_transactions.extend(batch["transactions"])
        
        if not batch["pagination"]["hasNextPage"]:
            break
            
        offset += limit
    
    return all_transactions
```

### Transaction Categorization

```python
async def auto_categorize_transactions():
    # Get uncategorized transactions
    uncategorized = await mm.get_transactions(
        category_ids=["uncategorized"],
        limit=100
    )
    
    # Apply simple rules
    for txn in uncategorized["transactions"]:
        merchant = txn["merchant"].lower()
        new_category = None
        
        if "coffee" in merchant or "starbucks" in merchant:
            new_category = "food_dining"
        elif "gas" in merchant or "shell" in merchant:
            new_category = "transportation"
        elif "grocery" in merchant or "safeway" in merchant:
            new_category = "groceries"
        
        if new_category:
            await mm.update_transaction(
                transaction_id=txn["id"],
                category_id=new_category
            )
```

### Data Validation

```python
def validate_transaction_data(merchant, amount, date):
    if not merchant or len(merchant.strip()) == 0:
        raise ValueError("Merchant name is required")
    
    if amount == 0:
        raise ValueError("Transaction amount cannot be zero")
    
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format")
```