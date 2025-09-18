# Insights & Analytics

This module provides comprehensive financial insights, analytics, and recommendations including cash flow analysis, spending insights, and bill tracking.

## 💡 Financial Insights

### `get_insights(start_date=None, end_date=None, insight_types=None)`

Get AI-powered financial insights and recommendations.

**Parameters:**
- `start_date` (str, optional): Start date for analysis in YYYY-MM-DD format
- `end_date` (str, optional): End date for analysis in YYYY-MM-DD format
- `insight_types` (List[str], optional): Specific insight types to retrieve

**Returns:** Dict containing insights and analysis:
```python
{
    "insights": [
        {
            "id": str,                   # Insight ID
            "type": str,                 # Insight type ("spending", "saving", "budget", etc.)
            "title": str,                # Insight title
            "description": str,          # Detailed description
            "severity": str,             # "info", "warning", "critical"
            "category": str,             # Related category
            "amount": float,             # Related amount (if applicable)
            "trend": str,                # "increasing", "decreasing", "stable"
            "confidence": float,         # Confidence score (0-1)
            "actionable": bool,          # Whether insight has actionable recommendations
            "recommendations": [         # Specific recommendations
                {
                    "action": str,       # Recommended action
                    "impact": str,       # Expected impact
                    "difficulty": str,   # Implementation difficulty
                    "timeframe": str     # Expected timeframe for results
                }
            ],
            "relatedData": {             # Supporting data
                "transactions": [...],
                "trends": [...],
                "comparisons": [...]
            },
            "createdDate": str,          # When insight was generated
            "priority": int              # Priority ranking (1-10)
        }
    ],
    "summary": {
        "totalInsights": int,
        "criticalInsights": int,
        "actionableInsights": int,
        "potentialSavings": float,       # Total potential savings identified
        "implementationScore": float     # How many recommendations are implemented
    },
    "categories": {                      # Insights grouped by category
        "spending": [...],
        "saving": [...],
        "budgeting": [...],
        "investing": [...],
        "debt": [...]
    }
}
```

**Example:**
```python
# Get all financial insights for the last 3 months
from datetime import datetime, timedelta

end_date = datetime.now()
start_date = end_date - timedelta(days=90)

insights = await mm.get_insights(
    start_date=start_date.strftime("%Y-%m-%d"),
    end_date=end_date.strftime("%Y-%m-%d")
)

print(f"Found {insights['summary']['totalInsights']} insights")
print(f"Potential savings: ${insights['summary']['potentialSavings']:,.2f}")

# Show critical insights
for insight in insights['insights']:
    if insight['severity'] == 'critical':
        print(f"🚨 {insight['title']}")
        print(f"   {insight['description']}")
        for rec in insight['recommendations']:
            print(f"   💡 {rec['action']}")
```

## 💰 Cash Flow Analysis

### `get_cashflow(start_date=None, end_date=None, group_by="month")`

Get detailed cash flow analysis with income/expense breakdown over time.

**Parameters:**
- `start_date` (str, optional): Start date for analysis
- `end_date` (str, optional): End date for analysis
- `group_by` (str): Time grouping ("day", "week", "month", "quarter", "year")

**Returns:** Dict with cash flow data:
```python
{
    "cashflow": [
        {
            "period": str,               # Time period (e.g., "2024-01")
            "startDate": str,            # Period start date
            "endDate": str,              # Period end date
            "income": {
                "total": float,          # Total income for period
                "byCategory": {
                    "salary": float,
                    "freelance": float,
                    "investment": float,
                    "other": float
                },
                "bySource": [            # Income sources
                    {
                        "source": str,
                        "amount": float,
                        "percentage": float
                    }
                ]
            },
            "expenses": {
                "total": float,          # Total expenses for period
                "byCategory": {
                    "housing": float,
                    "transportation": float,
                    "food": float,
                    "utilities": float,
                    "entertainment": float,
                    "other": float
                },
                "essential": float,      # Essential expenses
                "discretionary": float,  # Discretionary expenses
                "variableExpenses": float, # Variable expenses
                "fixedExpenses": float    # Fixed expenses
            },
            "netCashflow": float,        # Income - expenses
            "savingsRate": float,        # Savings rate percentage
            "runway": float,             # Months of expenses covered by savings
            "trends": {
                "incomeGrowth": float,   # Income growth vs previous period
                "expenseGrowth": float,  # Expense growth vs previous period
                "savingsGrowth": float   # Savings growth vs previous period
            }
        }
    ],
    "summary": {
        "averageMonthlyIncome": float,
        "averageMonthlyExpenses": float,
        "averageMonthlySavings": float,
        "averageSavingsRate": float,
        "incomeStability": float,        # Income consistency score
        "expenseStability": float,       # Expense consistency score
        "projectedAnnualSavings": float
    },
    "insights": {
        "strongestIncomeMonth": {...},
        "highestExpenseMonth": {...},
        "bestSavingsMonth": {...},
        "seasonalPatterns": [...],
        "recommendations": [...]
    }
}
```

**Example:**
```python
# Get 12 months of cash flow data
cashflow = await mm.get_cashflow(
    start_date="2023-01-01",
    end_date="2023-12-31",
    group_by="month"
)

print(f"Average Monthly Income: ${cashflow['summary']['averageMonthlyIncome']:,.2f}")
print(f"Average Monthly Expenses: ${cashflow['summary']['averageMonthlyExpenses']:,.2f}")
print(f"Average Savings Rate: {cashflow['summary']['averageSavingsRate']:.1f}%")

# Show monthly breakdown
for month in cashflow['cashflow']:
    period = month['period']
    net = month['netCashflow']
    savings_rate = month['savingsRate']
    print(f"{period}: ${net:+,.2f} ({savings_rate:.1f}% savings rate)")

# Show spending categories for latest month
latest = cashflow['cashflow'][-1]
print(f"\nTop expenses for {latest['period']}:")
expenses_sorted = sorted(
    latest['expenses']['byCategory'].items(),
    key=lambda x: x[1],
    reverse=True
)
for category, amount in expenses_sorted[:5]:
    print(f"  {category}: ${amount:,.2f}")
```

### `get_cashflow_summary(start_date=None, end_date=None)`

Get high-level cash flow summary with key metrics.

**Parameters:**
- `start_date` (str, optional): Start date for summary
- `end_date` (str, optional): End date for summary

**Returns:** Dict with cash flow summary:
```python
{
    "summary": {
        "totalIncome": float,
        "totalExpenses": float,
        "netCashflow": float,
        "savingsRate": float,
        "monthsCovered": int         # Months in analysis
    },
    "trends": {
        "incomeDirection": str,      # "increasing", "decreasing", "stable"
        "expenseDirection": str,
        "savingsDirection": str,
        "volatility": float          # Cash flow volatility score
    },
    "projections": {
        "annualIncome": float,
        "annualExpenses": float,
        "annualSavings": float,
        "emergencyFundMonths": float # Months of expenses in emergency fund
    }
}
```

## 📊 Spending & Income Analysis

### `get_spending_analysis(start_date, end_date, group_by="category", compare_period=False)`

Get detailed spending analysis and trends.

**Parameters:**
- `start_date` (str): Start date for analysis
- `end_date` (str): End date for analysis
- `group_by` (str): Analysis grouping ("category", "merchant", "account", "time")
- `compare_period` (bool): Whether to include comparison with previous period

**Returns:** Dict with spending analysis:
```python
{
    "spending": {
        "total": float,
        "byCategory": [
            {
                "categoryId": str,
                "categoryName": str,
                "amount": float,
                "percentage": float,
                "transactionCount": int,
                "averageTransaction": float,
                "trend": str,            # vs previous period
                "changePercent": float   # if compare_period=True
            }
        ],
        "byMerchant": [...],             # Top merchants
        "byAccount": [...],              # Spending by account
        "dailyAverage": float,
        "weeklyAverage": float,
        "monthlyAverage": float
    },
    "patterns": {
        "dayOfWeek": {...},              # Spending by day of week
        "timeOfDay": {...},              # Spending by time of day
        "seasonal": {...},               # Seasonal patterns
        "recurring": {                   # Recurring spending
            "subscriptions": [...],
            "utilities": [...],
            "other": [...]
        }
    },
    "insights": {
        "largestCategory": {...},
        "fastestGrowingCategory": {...},
        "mostFrequentMerchant": {...},
        "unusualSpending": [...],        # Anomalies detected
        "optimizationOpportunities": [...]
    },
    "comparison": {                      # If compare_period=True
        "previousPeriod": {...},
        "totalChange": float,
        "categoryChanges": [...],
        "significantChanges": [...]
    }
}
```

### `get_income_analysis(start_date, end_date, group_by="source", include_projections=False)`

Get detailed income analysis and trends.

**Parameters:**
- `start_date` (str): Start date for analysis
- `end_date` (str): End date for analysis
- `group_by` (str): Analysis grouping ("source", "category", "account", "time")
- `include_projections` (bool): Whether to include future income projections

**Returns:** Dict with income analysis:
```python
{
    "income": {
        "total": float,
        "bySource": [
            {
                "source": str,           # Income source
                "amount": float,
                "percentage": float,
                "frequency": str,        # "monthly", "bi-weekly", etc.
                "stability": float,      # Consistency score (0-1)
                "growth": float          # Growth rate
            }
        ],
        "byCategory": [...],
        "byAccount": [...],
        "monthlyAverage": float,
        "stability": float,              # Overall income stability
        "diversification": float         # Income source diversification
    },
    "patterns": {
        "paymentFrequency": {...},       # Payment timing patterns
        "seasonal": {...},               # Seasonal income variations
        "recurring": [...],              # Regular income sources
        "irregular": [...]               # One-time or irregular income
    },
    "projections": {                     # If include_projections=True
        "nextMonth": float,
        "nextQuarter": float,
        "annualProjection": float,
        "confidence": float              # Projection confidence
    },
    "insights": {
        "primaryIncomeSource": {...},
        "mostStableSource": {...},
        "fastestGrowingSource": {...},
        "riskFactors": [...],            # Income risk analysis
        "opportunities": [...]           # Income optimization opportunities
    }
}
```

## 📈 Financial Health & Scoring

### `get_financial_health_score()`

Get comprehensive financial health score and component breakdowns.

**Returns:** Dict with financial health assessment:
```python
{
    "overallScore": int,                 # Overall score (0-100)
    "grade": str,                        # Letter grade (A, B, C, D, F)
    "components": {
        "emergencyFund": {
            "score": int,
            "status": str,               # "excellent", "good", "fair", "poor"
            "target": float,             # Target amount
            "current": float,            # Current amount
            "monthsCovered": float       # Months of expenses covered
        },
        "debtToIncome": {
            "score": int,
            "ratio": float,              # Current debt-to-income ratio
            "target": float,             # Target ratio
            "status": str
        },
        "savingsRate": {
            "score": int,
            "currentRate": float,        # Current savings rate %
            "target": float,             # Target savings rate %
            "status": str
        },
        "investmentDiversification": {
            "score": int,
            "diversificationIndex": float,
            "status": str
        },
        "creditUtilization": {
            "score": int,
            "utilizationRate": float,    # Credit utilization %
            "status": str
        },
        "budgetAdherence": {
            "score": int,
            "adherenceRate": float,      # Budget adherence %
            "status": str
        }
    },
    "trends": {
        "scoreChange": int,              # Change from last assessment
        "improvingAreas": [...],         # Areas showing improvement
        "decliningAreas": [...]          # Areas needing attention
    },
    "recommendations": [
        {
            "area": str,                 # Component area
            "priority": str,             # "high", "medium", "low"
            "action": str,               # Recommended action
            "impact": int,               # Potential score improvement
            "timeframe": str             # Expected timeframe
        }
    ],
    "benchmarks": {
        "ageGroup": {...},               # Comparison to age group
        "incomeLevel": {...},            # Comparison to income level
        "region": {...}                  # Regional comparisons
    }
}
```

**Example:**
```python
health = await mm.get_financial_health_score()

print(f"Financial Health Score: {health['overallScore']}/100 (Grade: {health['grade']})")

# Show component scores
for component, data in health['components'].items():
    print(f"{component.replace('_', ' ').title()}: {data['score']}/100 ({data['status']})")

# Show top recommendations
print("\nTop Recommendations:")
for rec in sorted(health['recommendations'], key=lambda x: x['impact'], reverse=True)[:3]:
    print(f"• {rec['action']} (Impact: +{rec['impact']} points)")
```

### `get_net_worth_insights(time_period="1Y", include_projections=False)`

Get net worth insights and growth analysis.

**Parameters:**
- `time_period` (str): Analysis period ("1M", "3M", "6M", "1Y", "3Y", "5Y")
- `include_projections` (bool): Whether to include future projections

**Returns:** Dict with net worth insights and trends

## 📋 Bills & Payment Tracking

### `get_bills(start_date=None, end_date=None, include_completed=False)`

Get upcoming bills and payment tracking information.

**Parameters:**
- `start_date` (str, optional): Start date for bill lookup
- `end_date` (str, optional): End date for bill lookup
- `include_completed` (bool): Whether to include already paid bills

**Returns:** Dict containing bills and payment information:
```python
{
    "bills": [
        {
            "id": str,                   # Bill ID
            "name": str,                 # Bill name/description
            "merchant": str,             # Payee/merchant
            "amount": float,             # Bill amount
            "dueDate": str,              # Due date (YYYY-MM-DD)
            "status": str,               # "upcoming", "overdue", "paid"
            "category": {
                "id": str,
                "name": str              # Bill category
            },
            "account": {                 # Account to be charged
                "id": str,
                "name": str
            },
            "isRecurring": bool,         # Whether this is a recurring bill
            "frequency": str,            # "monthly", "quarterly", etc.
            "nextDueDate": str,          # Next occurrence if recurring
            "averageAmount": float,      # Average amount for variable bills
            "lastPaidDate": str,         # When last paid
            "lastPaidAmount": float,     # Last payment amount
            "isAutoPay": bool,           # Whether auto-pay is enabled
            "daysUntilDue": int,         # Days until due
            "isOverdue": bool,           # Whether bill is overdue
            "priority": str,             # "high", "medium", "low"
            "estimatedAmount": float,    # Estimated amount (for variable bills)
            "paymentHistory": [          # Recent payment history
                {
                    "date": str,
                    "amount": float,
                    "status": str
                }
            ]
        }
    ],
    "summary": {
        "totalUpcoming": float,          # Total upcoming bills amount
        "totalOverdue": float,           # Total overdue amount
        "billCount": int,                # Number of bills
        "overdueCount": int,             # Number of overdue bills
        "nextWeekTotal": float,          # Bills due in next 7 days
        "nextMonthTotal": float,         # Bills due in next 30 days
        "averageMonthlyBills": float     # Average monthly bill amount
    },
    "schedule": {                        # Payment schedule
        "thisWeek": [...],               # Bills due this week
        "nextWeek": [...],               # Bills due next week
        "thisMonth": [...],              # Bills due this month
        "nextMonth": [...]               # Bills due next month
    },
    "insights": {
        "seasonalPatterns": {...},       # Seasonal bill patterns
        "variableBills": [...],          # Bills with varying amounts
        "newBills": [...],               # Recently added bills
        "recommendations": [...]         # Bill management recommendations
    }
}
```

**Example:**
```python
# Get upcoming bills for next 30 days
from datetime import datetime, timedelta

end_date = datetime.now() + timedelta(days=30)
bills = await mm.get_bills(
    end_date=end_date.strftime("%Y-%m-%d"),
    include_completed=False
)

print(f"Upcoming bills: ${bills['summary']['totalUpcoming']:,.2f}")
print(f"Overdue bills: {bills['summary']['overdueCount']}")

# Show bills due this week
if bills['schedule']['thisWeek']:
    print("\nBills due this week:")
    for bill in bills['schedule']['thisWeek']:
        status_emoji = "⚠️" if bill['isOverdue'] else "📅"
        print(f"{status_emoji} {bill['name']}: ${bill['amount']:.2f} due {bill['dueDate']}")

# Show overdue bills
overdue_bills = [b for b in bills['bills'] if b['isOverdue']]
if overdue_bills:
    print("\n🚨 Overdue bills:")
    for bill in overdue_bills:
        days_overdue = abs(bill['daysUntilDue'])
        print(f"  {bill['name']}: ${bill['amount']:.2f} ({days_overdue} days overdue)")
```

## 📊 Comprehensive Financial Reports

### `generate_financial_report(start_date, end_date, report_type="comprehensive", include_charts=True)`

Generate comprehensive financial report with analysis and insights.

**Parameters:**
- `start_date` (str): Report start date
- `end_date` (str): Report end date
- `report_type` (str): Report type ("comprehensive", "summary", "cash_flow", "spending")
- `include_charts` (bool): Whether to include chart data

**Returns:** Dict with comprehensive financial report

**Example:**
```python
# Generate quarterly financial report
report = await mm.generate_financial_report(
    start_date="2024-01-01",
    end_date="2024-03-31",
    report_type="comprehensive",
    include_charts=True
)

print(f"Financial Report: Q1 2024")
print(f"Net Worth Change: ${report['summary']['netWorthChange']:+,.2f}")
print(f"Savings Rate: {report['summary']['savingsRate']:.1f}%")
print(f"Top Spending Category: {report['insights']['topSpendingCategory']['name']}")
```

## 🚨 Error Handling

### Insights API Errors

```python
from monarchmoney import ValidationError, AuthenticationError

try:
    insights = await mm.get_insights(
        start_date="invalid-date"
    )
except ValidationError as e:
    print(f"Invalid date format: {e}")
    print("Use YYYY-MM-DD format for dates")
```

### Analysis Period Errors

```python
try:
    cashflow = await mm.get_cashflow(
        start_date="2024-01-01",
        end_date="2023-12-31"  # End before start
    )
except ValidationError as e:
    print(f"Invalid date range: {e}")
    print("End date must be after start date")
```

## 💡 Best Practices

### Regular Financial Health Monitoring

```python
async def monthly_financial_checkup():
    """Perform monthly financial health assessment."""
    health = await mm.get_financial_health_score()
    cashflow = await mm.get_cashflow_summary()
    bills = await mm.get_bills()
    
    checkup = {
        'health_score': health['overallScore'],
        'savings_rate': cashflow['summary']['savingsRate'],
        'upcoming_bills': bills['summary']['totalUpcoming'],
        'overdue_bills': bills['summary']['overdueCount'],
        'action_items': []
    }
    
    # Generate action items
    if health['overallScore'] < 70:
        checkup['action_items'].append("Focus on improving financial health score")
    
    if cashflow['summary']['savingsRate'] < 10:
        checkup['action_items'].append("Increase savings rate to at least 10%")
    
    if bills['summary']['overdueCount'] > 0:
        checkup['action_items'].append("Pay overdue bills immediately")
    
    return checkup
```

### Spending Optimization

```python
async def identify_spending_optimization():
    """Identify opportunities to optimize spending."""
    spending = await mm.get_spending_analysis(
        start_date="2024-01-01",
        end_date="2024-03-31",
        group_by="category",
        compare_period=True
    )
    
    optimizations = []
    
    for category in spending['spending']['byCategory']:
        # Look for categories with high spending and positive trends
        if category['amount'] > 500 and category['changePercent'] > 20:
            optimizations.append({
                'category': category['categoryName'],
                'current_spending': category['amount'],
                'growth_rate': category['changePercent'],
                'optimization_potential': category['amount'] * 0.1,  # 10% reduction target
                'recommendation': f"Review {category['categoryName']} spending - increased {category['changePercent']:.1f}%"
            })
    
    return optimizations
```

### Cash Flow Forecasting

```python
async def forecast_cash_flow(months_ahead=6):
    """Forecast cash flow for upcoming months."""
    # Get historical data
    historical_cashflow = await mm.get_cashflow(
        start_date="2023-01-01",
        end_date="2024-03-31",
        group_by="month"
    )
    
    # Get scheduled bills
    bills = await mm.get_bills(include_completed=False)
    
    # Calculate averages
    avg_income = historical_cashflow['summary']['averageMonthlyIncome']
    avg_expenses = historical_cashflow['summary']['averageMonthlyExpenses']
    
    # Forecast future months
    forecast = []
    for month in range(1, months_ahead + 1):
        projected_month = {
            'month': month,
            'projected_income': avg_income,
            'projected_expenses': avg_expenses,
            'scheduled_bills': sum(b['amount'] for b in bills['bills'] if b['isRecurring']),
            'projected_savings': avg_income - avg_expenses,
            'confidence': 0.8 - (month * 0.1)  # Decreasing confidence over time
        }
        forecast.append(projected_month)
    
    return forecast
```