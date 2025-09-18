# Budget Management

This module provides comprehensive budget management functionality including flexible budget periods, amount tracking, and spending analysis.

## 📊 Budget Overview

### `get_budgets(start_date=None, end_date=None, category_ids=None)`

Get budget data and planning information with spending analysis.

**Parameters:**
- `start_date` (str, optional): Start date for budget period in YYYY-MM-DD format
- `end_date` (str, optional): End date for budget period in YYYY-MM-DD format
- `category_ids` (List[str], optional): Filter by specific category IDs

**Returns:** Dict containing comprehensive budget data:
```python
{
    "budgets": [
        {
            "categoryId": str,           # Category ID
            "category": {
                "id": str,
                "name": str,             # Category name
                "icon": str,             # Category icon
                "color": str,            # Category color
                "group": {               # Category group
                    "id": str,
                    "name": str
                }
            },
            "budgetAmount": float,       # Current budget amount
            "spentAmount": float,        # Amount spent in period
            "remainingAmount": float,    # Remaining budget
            "percentUsed": float,        # Percentage of budget used
            "isOverBudget": bool,        # Whether over budget
            "overBudgetAmount": float,   # Amount over budget (if applicable)
            "budgetType": str,           # "fixed", "flexible", "envelope"
            "period": {
                "type": str,             # "monthly", "weekly", "yearly", "custom"
                "startDate": str,        # Period start date
                "endDate": str,          # Period end date
                "recurrence": str        # Recurrence pattern
            },
            "flexibleSettings": {        # For flexible budgets
                "variability": float,    # Allowed variability (0.0-1.0)
                "rollover": bool,        # Allow rollover to next period
                "rolledOverAmount": float # Amount rolled over from previous
            },
            "history": [                 # Historical budget performance
                {
                    "period": str,       # YYYY-MM format
                    "budgetAmount": float,
                    "spentAmount": float,
                    "percentUsed": float
                }
            ],
            "transactions": [            # Recent transactions in category
                {
                    "id": str,
                    "amount": float,
                    "date": str,
                    "merchant": str
                }
            ]
        }
    ],
    "summary": {
        "totalBudget": float,            # Total budgeted amount
        "totalSpent": float,             # Total amount spent
        "totalRemaining": float,         # Total remaining budget
        "overBudgetCategories": int,     # Number of over-budget categories
        "onTrackCategories": int,        # Number of on-track categories
        "underBudgetCategories": int,    # Number of under-budget categories
        "percentOfBudgetUsed": float     # Overall budget utilization
    },
    "period": {
        "startDate": str,
        "endDate": str,
        "type": str,
        "daysRemaining": int             # Days left in current period
    },
    "trends": {
        "monthOverMonth": float,         # Month-over-month spending change %
        "averageMonthlySpending": float, # Average monthly spending
        "seasonalPatterns": {...}        # Seasonal spending patterns
    }
}
```

**Example:**
```python
# Get current month's budget data
budgets = await mm.get_budgets()

print(f"Total Budget: ${budgets['summary']['totalBudget']:,.2f}")
print(f"Total Spent: ${budgets['summary']['totalSpent']:,.2f}")
print(f"Budget Utilization: {budgets['summary']['percentOfBudgetUsed']:.1f}%")

# Show over-budget categories
for budget in budgets["budgets"]:
    if budget["isOverBudget"]:
        cat_name = budget["category"]["name"]
        over_amount = budget["overBudgetAmount"]
        print(f"⚠️ {cat_name} is ${over_amount:.2f} over budget")

# Show top spending categories
sorted_budgets = sorted(
    budgets["budgets"], 
    key=lambda x: x["spentAmount"], 
    reverse=True
)

print("\nTop 5 Spending Categories:")
for budget in sorted_budgets[:5]:
    cat_name = budget["category"]["name"]
    spent = budget["spentAmount"]
    budget_amount = budget["budgetAmount"]
    print(f"{cat_name}: ${spent:.2f} / ${budget_amount:.2f}")
```

## ✏️ Budget Management

### `set_budget_amount(category_id, amount, period="monthly", start_date=None)`

Update budget amount for a specific category with flexible period support.

**Parameters:**
- `category_id` (str): Category ID to set budget for
- `amount` (float): Budget amount to set
- `period` (str): Budget period ("monthly", "weekly", "yearly", "custom")
- `start_date` (str, optional): Start date for custom periods in YYYY-MM-DD format

**Returns:** Dict with updated budget information:
```python
{
    "budget": {
        "categoryId": str,
        "category": {...},
        "budgetAmount": float,       # New budget amount
        "period": {...},             # Budget period info
        "effectiveDate": str,        # When the budget takes effect
        "previousAmount": float      # Previous budget amount
    },
    "impact": {
        "totalBudgetChange": float,  # Change to total budget
        "percentChange": float,      # Percentage change from previous
        "projectedSpending": float   # Projected spending for period
    }
}
```

**Example:**
```python
# Set monthly grocery budget
grocery_budget = await mm.set_budget_amount(
    category_id="groceries",
    amount=600.00,
    period="monthly"
)

print(f"Set grocery budget to ${grocery_budget['budget']['budgetAmount']:.2f}/month")

# Set weekly entertainment budget
entertainment_budget = await mm.set_budget_amount(
    category_id="entertainment", 
    amount=100.00,
    period="weekly"
)

# Set custom period budget (quarterly)
quarterly_budget = await mm.set_budget_amount(
    category_id="clothing",
    amount=300.00,
    period="custom",
    start_date="2024-01-01"  # Will create 3-month budget period
)
```

## 📈 Budget Analysis & Insights

### Budget Performance Tracking

```python
async def analyze_budget_performance(months_back=6):
    """Analyze budget performance over multiple months."""
    from datetime import datetime, timedelta
    
    performance_data = []
    
    for i in range(months_back):
        # Calculate date range for each month
        end_date = datetime.now().replace(day=1) - timedelta(days=i*30)
        start_date = end_date.replace(day=1)
        
        # Get budget data for the month
        budgets = await mm.get_budgets(
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d")
        )
        
        performance_data.append({
            'month': start_date.strftime("%Y-%m"),
            'total_budget': budgets['summary']['totalBudget'],
            'total_spent': budgets['summary']['totalSpent'],
            'utilization': budgets['summary']['percentOfBudgetUsed'],
            'over_budget_count': budgets['summary']['overBudgetCategories']
        })
    
    return performance_data
```

### Category Budget Recommendations

```python
async def suggest_budget_adjustments():
    """Suggest budget adjustments based on spending patterns."""
    # Get last 3 months of data
    from datetime import datetime, timedelta
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    budgets = await mm.get_budgets(
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d")
    )
    
    suggestions = []
    
    for budget in budgets["budgets"]:
        category_name = budget["category"]["name"]
        avg_spending = budget["spentAmount"] / 3  # 3-month average
        current_budget = budget["budgetAmount"]
        
        # Suggest adjustments based on patterns
        if budget["isOverBudget"]:
            # Consistently over budget - suggest increase
            suggested_amount = avg_spending * 1.1  # 10% buffer
            suggestions.append({
                'category': category_name,
                'current_budget': current_budget,
                'suggested_budget': suggested_amount,
                'reason': 'Consistently over budget',
                'action': 'increase'
            })
        elif budget["percentUsed"] < 50:
            # Consistently under budget - suggest decrease
            suggested_amount = avg_spending * 1.05  # 5% buffer
            suggestions.append({
                'category': category_name,
                'current_budget': current_budget,
                'suggested_budget': suggested_amount,
                'reason': 'Consistently under budget',
                'action': 'decrease'
            })
    
    return suggestions
```

## 💰 Flexible Budget Features

### Envelope Budgeting

```python
async def setup_envelope_budget(category_id, monthly_amount):
    """Set up envelope-style budgeting for a category."""
    # Set budget with rollover enabled
    budget = await mm.set_budget_amount(
        category_id=category_id,
        amount=monthly_amount,
        period="monthly"
    )
    
    # Note: Envelope budgeting typically involves:
    # - Strict limits (no overspending)
    # - Rollover of unused amounts
    # - Visual indicators of remaining funds
    
    return budget
```

### Variable Budget Management

```python
async def create_variable_budget(category_id, base_amount, variability_percent=20):
    """Create a flexible budget with variable spending allowance."""
    # Calculate flexible range
    min_amount = base_amount * (1 - variability_percent / 100)
    max_amount = base_amount * (1 + variability_percent / 100)
    
    # Set base budget
    budget = await mm.set_budget_amount(
        category_id=category_id,
        amount=base_amount,
        period="monthly"
    )
    
    return {
        'base_budget': base_amount,
        'min_acceptable': min_amount,
        'max_acceptable': max_amount,
        'variability': variability_percent,
        'budget_info': budget
    }
```

## 📊 Budget Reporting

### Monthly Budget Report

```python
async def generate_monthly_budget_report(year, month):
    """Generate comprehensive monthly budget report."""
    from datetime import datetime
    
    # Calculate date range
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    
    budgets = await mm.get_budgets(
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d")
    )
    
    report = {
        'period': f"{year}-{month:02d}",
        'summary': budgets['summary'],
        'performance': {
            'on_track': [],
            'over_budget': [],
            'under_budget': []
        },
        'top_categories': [],
        'recommendations': []
    }
    
    # Categorize performance
    for budget in budgets['budgets']:
        category_info = {
            'name': budget['category']['name'],
            'budgeted': budget['budgetAmount'],
            'spent': budget['spentAmount'],
            'remaining': budget['remainingAmount'],
            'percent_used': budget['percentUsed']
        }
        
        if budget['isOverBudget']:
            report['performance']['over_budget'].append(category_info)
        elif budget['percentUsed'] < 50:
            report['performance']['under_budget'].append(category_info)
        else:
            report['performance']['on_track'].append(category_info)
    
    # Top spending categories
    report['top_categories'] = sorted(
        budgets['budgets'],
        key=lambda x: x['spentAmount'],
        reverse=True
    )[:10]
    
    return report
```

### Budget vs Actual Analysis

```python
async def budget_vs_actual_analysis(start_date, end_date):
    """Compare budgeted vs actual spending over a period."""
    budgets = await mm.get_budgets(
        start_date=start_date,
        end_date=end_date
    )
    
    analysis = {
        'period': f"{start_date} to {end_date}",
        'total_variance': 0,
        'categories': []
    }
    
    for budget in budgets['budgets']:
        variance = budget['spentAmount'] - budget['budgetAmount']
        variance_percent = (variance / budget['budgetAmount']) * 100 if budget['budgetAmount'] > 0 else 0
        
        category_analysis = {
            'category': budget['category']['name'],
            'budgeted': budget['budgetAmount'],
            'actual': budget['spentAmount'],
            'variance': variance,
            'variance_percent': variance_percent,
            'status': 'over' if variance > 0 else 'under' if variance < 0 else 'on_target'
        }
        
        analysis['categories'].append(category_analysis)
        analysis['total_variance'] += variance
    
    # Sort by largest variances
    analysis['categories'].sort(key=lambda x: abs(x['variance']), reverse=True)
    
    return analysis
```

## 🎯 Budget Goal Setting

### Smart Budget Allocation

```python
async def smart_budget_allocation(monthly_income, savings_goal_percent=20):
    """Automatically allocate budget based on income and savings goals."""
    
    # Get current spending patterns
    budgets = await mm.get_budgets()
    
    # Calculate allocation
    savings_amount = monthly_income * (savings_goal_percent / 100)
    available_for_spending = monthly_income - savings_amount
    
    # Get historical spending to inform allocations
    total_historical_spending = sum(b['spentAmount'] for b in budgets['budgets'])
    
    allocations = {}
    
    for budget in budgets['budgets']:
        category_name = budget['category']['name']
        historical_percent = budget['spentAmount'] / total_historical_spending
        suggested_amount = available_for_spending * historical_percent
        
        allocations[category_name] = {
            'suggested_budget': suggested_amount,
            'historical_spending': budget['spentAmount'],
            'historical_percent': historical_percent * 100
        }
    
    return {
        'monthly_income': monthly_income,
        'savings_goal': savings_amount,
        'available_for_spending': available_for_spending,
        'category_allocations': allocations
    }
```

### Zero-Based Budget Setup

```python
async def setup_zero_based_budget(monthly_income):
    """Set up a zero-based budget where every dollar is allocated."""
    
    # Essential categories and their typical percentages
    essential_categories = {
        'housing': 0.30,      # 30% for housing
        'transportation': 0.15, # 15% for transportation  
        'groceries': 0.12,    # 12% for groceries
        'utilities': 0.08,    # 8% for utilities
        'insurance': 0.05,    # 5% for insurance
        'savings': 0.20,      # 20% for savings
        'debt_payment': 0.10  # 10% for debt payments
    }
    
    budget_plan = {}
    allocated_total = 0
    
    for category, percentage in essential_categories.items():
        amount = monthly_income * percentage
        budget_plan[category] = amount
        allocated_total += amount
    
    # Remaining amount for discretionary spending
    remaining = monthly_income - allocated_total
    
    return {
        'monthly_income': monthly_income,
        'essential_allocations': budget_plan,
        'discretionary_amount': remaining,
        'total_allocated': allocated_total,
        'verification': allocated_total + remaining == monthly_income
    }
```

## 🚨 Error Handling

### Budget Operation Errors

```python
from monarchmoney import ValidationError, AuthenticationError

try:
    budget = await mm.set_budget_amount(
        category_id="invalid_category",
        amount=500.00
    )
except ValidationError as e:
    print(f"Invalid budget data: {e}")
    # Get valid categories
    categories = await mm.get_transaction_categories()
    print("Available categories:", [cat['name'] for cat in categories['categories']])
```

### Budget Analysis Errors

```python
try:
    budgets = await mm.get_budgets(
        start_date="invalid-date",
        end_date="2024-01-31"
    )
except ValidationError as e:
    print(f"Invalid date format: {e}")
    print("Use YYYY-MM-DD format for dates")
```

## 💡 Best Practices

### Budget Monitoring

```python
async def monitor_budget_alerts(alert_threshold=0.8):
    """Monitor budgets and alert when approaching limits."""
    budgets = await mm.get_budgets()
    
    alerts = []
    
    for budget in budgets['budgets']:
        if budget['percentUsed'] >= alert_threshold:
            alert = {
                'category': budget['category']['name'],
                'percent_used': budget['percentUsed'],
                'remaining': budget['remainingAmount'],
                'days_remaining': budgets['period']['daysRemaining']
            }
            alerts.append(alert)
    
    return alerts
```

### Seasonal Budget Adjustments

```python
async def adjust_seasonal_budgets(season):
    """Adjust budgets based on seasonal patterns."""
    seasonal_adjustments = {
        'winter': {
            'utilities': 1.3,      # 30% increase for heating
            'clothing': 1.2,       # 20% increase for winter clothes
            'entertainment': 0.8   # 20% decrease for outdoor activities
        },
        'summer': {
            'utilities': 1.2,      # 20% increase for cooling
            'travel': 1.5,         # 50% increase for vacation
            'entertainment': 1.3   # 30% increase for activities
        }
    }
    
    if season not in seasonal_adjustments:
        return None
    
    adjustments = seasonal_adjustments[season]
    current_budgets = await mm.get_budgets()
    
    recommendations = []
    
    for budget in current_budgets['budgets']:
        category_name = budget['category']['name']
        if category_name in adjustments:
            current_amount = budget['budgetAmount']
            suggested_amount = current_amount * adjustments[category_name]
            
            recommendations.append({
                'category': category_name,
                'current_budget': current_amount,
                'suggested_budget': suggested_amount,
                'adjustment_factor': adjustments[category_name]
            })
    
    return recommendations
```

### Budget Reconciliation

```python
async def reconcile_budgets_with_actual():
    """Reconcile budget allocations with actual spending patterns."""
    budgets = await mm.get_budgets()
    
    reconciliation = {
        'total_variance': 0,
        'accuracy_score': 0,
        'categories_needing_adjustment': []
    }
    
    total_categories = len(budgets['budgets'])
    accurate_categories = 0
    
    for budget in budgets['budgets']:
        variance_percent = abs(budget['percentUsed'] - 100)
        
        if variance_percent <= 10:  # Within 10% is considered accurate
            accurate_categories += 1
        else:
            reconciliation['categories_needing_adjustment'].append({
                'category': budget['category']['name'],
                'variance_percent': variance_percent,
                'recommendation': 'increase' if budget['percentUsed'] > 110 else 'decrease'
            })
    
    reconciliation['accuracy_score'] = (accurate_categories / total_categories) * 100
    
    return reconciliation
```