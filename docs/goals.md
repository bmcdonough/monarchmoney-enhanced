# Goals Management

This module provides comprehensive financial goal management including goal creation, progress tracking, and achievement monitoring.

## 🎯 Goal Overview

### `get_goals()`

Get all financial goals with progress tracking and target information.

**Returns:** Dict containing goals data:
```python
{
    "goals": [
        {
            "id": str,                   # Goal ID
            "name": str,                 # Goal name
            "description": str,          # Goal description
            "targetAmount": float,       # Target amount to achieve
            "currentAmount": float,      # Current progress amount
            "remainingAmount": float,    # Amount remaining to reach target
            "progressPercent": float,    # Progress percentage (0-100)
            "targetDate": str,           # Target completion date (YYYY-MM-DD)
            "createdDate": str,          # Goal creation date
            "lastUpdatedDate": str,      # Last update date
            "status": str,               # "active", "completed", "paused", "archived"
            "priority": str,             # "high", "medium", "low"
            "category": {
                "id": str,
                "name": str,             # Goal category (e.g., "Emergency Fund")
                "icon": str,
                "color": str
            },
            "goalType": str,             # "savings", "debt_payoff", "investment", "purchase"
            "linkedAccounts": [          # Associated accounts
                {
                    "id": str,
                    "name": str,
                    "type": str,
                    "balance": float
                }
            ],
            "timeline": {
                "startDate": str,
                "endDate": str,
                "daysRemaining": int,
                "monthsRemaining": float,
                "isOverdue": bool
            },
            "projections": {
                "monthlyContributionNeeded": float,  # To reach target on time
                "projectedCompletionDate": str,     # Based on current pace
                "onTrackToMeetTarget": bool,        # Whether goal is achievable
                "recommendedMonthlyAmount": float   # Suggested contribution
            },
            "milestones": [              # Progress milestones
                {
                    "percentage": int,   # Milestone percentage (25, 50, 75, 100)
                    "amount": float,     # Dollar amount for milestone
                    "achieved": bool,    # Whether milestone reached
                    "achievedDate": str  # Date milestone was reached
                }
            ],
            "insights": {
                "averageMonthlyProgress": float,
                "bestMonth": {
                    "month": str,
                    "amount": float
                },
                "consistency": float     # Progress consistency score (0-1)
            }
        }
    ],
    "summary": {
        "totalGoals": int,               # Total number of goals
        "activeGoals": int,              # Number of active goals
        "completedGoals": int,           # Number of completed goals
        "totalTargetAmount": float,      # Sum of all target amounts
        "totalCurrentAmount": float,     # Sum of all current amounts
        "totalRemainingAmount": float,   # Sum of all remaining amounts
        "overallProgressPercent": float, # Overall progress across all goals
        "goalsOnTrack": int,            # Number of goals on track
        "goalsNeedingAttention": int     # Number of goals behind schedule
    },
    "recommendations": [               # AI-powered recommendations
        {
            "goalId": str,
            "type": str,               # "increase_contribution", "adjust_target", etc.
            "message": str,
            "suggestedAmount": float
        }
    ]
}
```

**Example:**
```python
goals_data = await mm.get_goals()

print(f"Active Goals: {goals_data['summary']['activeGoals']}")
print(f"Overall Progress: {goals_data['summary']['overallProgressPercent']:.1f}%")

for goal in goals_data["goals"]:
    if goal["status"] == "active":
        name = goal["name"]
        progress = goal["progressPercent"]
        remaining = goal["remainingAmount"]
        print(f"{name}: {progress:.1f}% complete (${remaining:,.2f} remaining)")
        
        # Check if goal needs attention
        if not goal["projections"]["onTrackToMeetTarget"]:
            needed = goal["projections"]["monthlyContributionNeeded"]
            print(f"  ⚠️ Need ${needed:.2f}/month to stay on track")
```

## ✏️ Goal Creation & Management

### `create_goal(name, target_amount, target_date=None, description=None, category_id=None, account_ids=None)`

Create a new financial goal with tracking and progress monitoring.

**Parameters:**
- `name` (str): Goal name/title
- `target_amount` (float): Target amount to achieve
- `target_date` (str, optional): Target completion date in YYYY-MM-DD format
- `description` (str, optional): Detailed goal description
- `category_id` (str, optional): Goal category ID
- `account_ids` (List[str], optional): Associated account IDs for tracking

**Returns:** Dict with created goal data

**Example:**
```python
# Create emergency fund goal
emergency_fund = await mm.create_goal(
    name="Emergency Fund",
    target_amount=10000.00,
    target_date="2024-12-31",
    description="Save 6 months of expenses for emergencies",
    category_id="emergency_savings"
)

# Create vacation goal
vacation_goal = await mm.create_goal(
    name="Europe Vacation",
    target_amount=5000.00,
    target_date="2024-06-15",
    description="Family trip to Europe summer 2024",
    account_ids=["savings_account_123"]
)

# Create debt payoff goal
debt_goal = await mm.create_goal(
    name="Pay Off Credit Card",
    target_amount=3500.00,
    target_date="2024-08-01",
    description="Pay off high-interest credit card debt"
)

print(f"Created goal: {emergency_fund['name']}")
print(f"Goal ID: {emergency_fund['id']}")
```

### `update_goal(goal_id, name=None, target_amount=None, target_date=None, description=None, is_completed=None)`

Update an existing financial goal.

**Parameters:**
- `goal_id` (str): Goal ID to update
- `name` (str, optional): New goal name
- `target_amount` (float, optional): New target amount
- `target_date` (str, optional): New target date
- `description` (str, optional): New description
- `is_completed` (bool, optional): Mark goal as completed

**Returns:** Dict with updated goal data

**Example:**
```python
# Update target amount and date
updated_goal = await mm.update_goal(
    goal_id="goal_123",
    target_amount=12000.00,  # Increased from $10,000
    target_date="2025-03-31" # Extended deadline
)

# Mark goal as completed
completed_goal = await mm.update_goal(
    goal_id="goal_456",
    is_completed=True
)

print(f"Updated goal: {updated_goal['name']}")
print(f"New target: ${updated_goal['targetAmount']:,.2f}")
```

### `delete_goal(goal_id)`

Delete a financial goal permanently.

**Parameters:**
- `goal_id` (str): Goal ID to delete

**Returns:** bool (True if successful)

**Example:**
```python
success = await mm.delete_goal("goal_789")
if success:
    print("Goal deleted successfully")
```

## 📊 Goal Progress Tracking

### Manual Progress Updates

```python
async def update_goal_progress(goal_id, new_amount):
    """Update goal progress with new current amount."""
    # Note: This would typically be done through account linking
    # or manual contribution tracking in the Monarch Money interface
    
    goal = await mm.get_goal_details(goal_id)
    progress_percent = (new_amount / goal['targetAmount']) * 100
    
    # Log progress milestone if reached
    milestones = [25, 50, 75, 100]
    current_milestone = max([m for m in milestones if m <= progress_percent], default=0)
    
    return {
        'goal_id': goal_id,
        'current_amount': new_amount,
        'progress_percent': progress_percent,
        'milestone_reached': current_milestone,
        'remaining_amount': goal['targetAmount'] - new_amount
    }
```

### Goal Performance Analytics

```python
async def analyze_goal_performance():
    """Analyze goal performance and provide insights."""
    goals = await mm.get_goals()
    
    analysis = {
        'total_goals': len(goals['goals']),
        'performance_by_type': {},
        'at_risk_goals': [],
        'ahead_of_schedule': [],
        'completion_projections': {}
    }
    
    for goal in goals['goals']:
        if goal['status'] != 'active':
            continue
            
        goal_type = goal['goalType']
        progress = goal['progressPercent']
        on_track = goal['projections']['onTrackToMeetTarget']
        
        # Group by goal type
        if goal_type not in analysis['performance_by_type']:
            analysis['performance_by_type'][goal_type] = {
                'count': 0,
                'average_progress': 0,
                'on_track_count': 0
            }
        
        type_stats = analysis['performance_by_type'][goal_type]
        type_stats['count'] += 1
        type_stats['average_progress'] += progress
        if on_track:
            type_stats['on_track_count'] += 1
        
        # Identify at-risk goals
        if not on_track and progress < 75:
            analysis['at_risk_goals'].append({
                'id': goal['id'],
                'name': goal['name'],
                'progress': progress,
                'needed_monthly': goal['projections']['monthlyContributionNeeded']
            })
        
        # Identify ahead-of-schedule goals
        if progress > 80 and goal['timeline']['daysRemaining'] > 30:
            analysis['ahead_of_schedule'].append({
                'id': goal['id'],
                'name': goal['name'],
                'progress': progress,
                'projected_completion': goal['projections']['projectedCompletionDate']
            })
    
    # Calculate averages
    for goal_type in analysis['performance_by_type']:
        type_stats = analysis['performance_by_type'][goal_type]
        type_stats['average_progress'] /= type_stats['count']
        type_stats['success_rate'] = type_stats['on_track_count'] / type_stats['count']
    
    return analysis
```

## 🎯 Goal Types & Categories

### Savings Goals

```python
async def create_savings_goal(name, target_amount, months_to_achieve):
    """Create a savings-type goal with automatic calculations."""
    from datetime import datetime, timedelta
    
    target_date = (datetime.now() + timedelta(days=30 * months_to_achieve))
    
    goal = await mm.create_goal(
        name=name,
        target_amount=target_amount,
        target_date=target_date.strftime("%Y-%m-%d"),
        description=f"Save ${target_amount:,.2f} over {months_to_achieve} months"
    )
    
    monthly_needed = target_amount / months_to_achieve
    
    return {
        'goal': goal,
        'monthly_contribution_needed': monthly_needed,
        'weekly_contribution_needed': monthly_needed / 4.33,
        'daily_contribution_needed': monthly_needed / 30
    }

# Examples of different savings goals
emergency_fund = await create_savings_goal("Emergency Fund", 15000, 18)
vacation_fund = await create_savings_goal("Japan Trip", 8000, 12)
house_down_payment = await create_savings_goal("House Down Payment", 50000, 36)
```

### Debt Payoff Goals

```python
async def create_debt_payoff_goal(debt_name, current_balance, interest_rate, target_months):
    """Create a debt payoff goal with payment calculations."""
    # Calculate monthly payment needed
    monthly_rate = interest_rate / 12 / 100
    
    if monthly_rate > 0:
        # Use loan payment formula
        monthly_payment = current_balance * (monthly_rate * (1 + monthly_rate)**target_months) / ((1 + monthly_rate)**target_months - 1)
    else:
        # No interest case
        monthly_payment = current_balance / target_months
    
    total_payments = monthly_payment * target_months
    total_interest = total_payments - current_balance
    
    from datetime import datetime, timedelta
    target_date = (datetime.now() + timedelta(days=30 * target_months))
    
    goal = await mm.create_goal(
        name=f"Pay Off {debt_name}",
        target_amount=current_balance,
        target_date=target_date.strftime("%Y-%m-%d"),
        description=f"Pay off ${current_balance:,.2f} debt in {target_months} months"
    )
    
    return {
        'goal': goal,
        'monthly_payment_needed': monthly_payment,
        'total_payments': total_payments,
        'total_interest': total_interest,
        'payoff_date': target_date.strftime("%Y-%m-%d")
    }

# Example debt payoff goals
credit_card = await create_debt_payoff_goal("Visa Credit Card", 5000, 18.99, 24)
student_loan = await create_debt_payoff_goal("Student Loan", 25000, 4.5, 120)
```

### Investment Goals

```python
async def create_investment_goal(name, target_amount, years, expected_return_rate):
    """Create an investment goal with compound growth calculations."""
    from datetime import datetime, timedelta
    import math
    
    # Calculate required monthly contribution with compound interest
    months = years * 12
    monthly_rate = expected_return_rate / 12 / 100
    
    if monthly_rate > 0:
        # Future value of annuity formula solved for payment
        monthly_contribution = target_amount * monthly_rate / ((1 + monthly_rate)**months - 1)
    else:
        monthly_contribution = target_amount / months
    
    target_date = (datetime.now() + timedelta(days=365 * years))
    
    goal = await mm.create_goal(
        name=name,
        target_amount=target_amount,
        target_date=target_date.strftime("%Y-%m-%d"),
        description=f"Invest to reach ${target_amount:,.2f} in {years} years at {expected_return_rate}% return"
    )
    
    total_contributions = monthly_contribution * months
    investment_growth = target_amount - total_contributions
    
    return {
        'goal': goal,
        'monthly_contribution_needed': monthly_contribution,
        'total_contributions': total_contributions,
        'expected_growth': investment_growth,
        'expected_annual_return': expected_return_rate
    }

# Example investment goals
retirement_goal = await create_investment_goal("Retirement Fund", 1000000, 30, 7.0)
college_fund = await create_investment_goal("Kids College Fund", 200000, 18, 6.0)
```

## 📈 Goal Automation & Smart Features

### Automatic Goal Progress Tracking

```python
async def setup_automatic_goal_tracking(goal_id, account_ids, tracking_method="balance_growth"):
    """Set up automatic goal progress tracking based on account balances."""
    # This would integrate with account monitoring
    # Different tracking methods:
    # - balance_growth: Track increases in linked account balances
    # - contribution_tracking: Track specific contributions/transfers
    # - category_spending: Track spending reductions in specific categories
    
    goal = await mm.get_goal_details(goal_id)
    
    tracking_config = {
        'goal_id': goal_id,
        'method': tracking_method,
        'linked_accounts': account_ids,
        'update_frequency': 'daily',
        'baseline_amount': goal.get('currentAmount', 0)
    }
    
    return tracking_config

# Example: Track emergency fund through savings account growth
emergency_tracking = await setup_automatic_goal_tracking(
    goal_id="emergency_fund_goal",
    account_ids=["high_yield_savings_123"],
    tracking_method="balance_growth"
)
```

### Goal Milestone Celebrations

```python
async def check_goal_milestones():
    """Check for newly achieved goal milestones and celebrate progress."""
    goals = await mm.get_goals()
    
    celebrations = []
    
    for goal in goals['goals']:
        if goal['status'] != 'active':
            continue
            
        progress = goal['progressPercent']
        milestones = goal['milestones']
        
        # Check for newly achieved milestones
        for milestone in milestones:
            if milestone['achieved'] and not milestone.get('celebrated', False):
                celebrations.append({
                    'goal_name': goal['name'],
                    'milestone_percent': milestone['percentage'],
                    'milestone_amount': milestone['amount'],
                    'achievement_date': milestone['achievedDate'],
                    'message': f"🎉 Congratulations! You've reached {milestone['percentage']}% of your {goal['name']} goal!"
                })
    
    return celebrations

# Example usage
milestones = await check_goal_milestones()
for celebration in milestones:
    print(celebration['message'])
```

### Smart Goal Recommendations

```python
async def generate_goal_recommendations():
    """Generate smart recommendations for new goals based on financial situation."""
    # Get financial overview
    accounts = await mm.get_accounts()
    budgets = await mm.get_budgets()
    existing_goals = await mm.get_goals()
    
    net_worth = accounts['summary']['netWorth']
    monthly_income = sum(b['spentAmount'] for b in budgets['budgets'] if b['category']['name'] == 'income')
    monthly_expenses = sum(b['spentAmount'] for b in budgets['budgets'] if b['category']['name'] != 'income')
    monthly_surplus = monthly_income - monthly_expenses
    
    recommendations = []
    
    # Emergency fund recommendation
    emergency_fund_exists = any(g['category']['name'] == 'Emergency Fund' for g in existing_goals['goals'])
    if not emergency_fund_exists:
        emergency_target = monthly_expenses * 6  # 6 months of expenses
        recommendations.append({
            'type': 'emergency_fund',
            'priority': 'high',
            'name': 'Emergency Fund',
            'target_amount': emergency_target,
            'reasoning': 'Build 6 months of expenses for financial security',
            'monthly_contribution': min(monthly_surplus * 0.3, emergency_target / 12)
        })
    
    # Retirement recommendation
    retirement_exists = any('retirement' in g['name'].lower() for g in existing_goals['goals'])
    if not retirement_exists and monthly_surplus > 500:
        retirement_target = monthly_income * 12 * 25  # 25x annual income rule
        recommendations.append({
            'type': 'retirement',
            'priority': 'high',
            'name': 'Retirement Savings',
            'target_amount': retirement_target,
            'reasoning': 'Save 25x annual income for comfortable retirement',
            'monthly_contribution': monthly_surplus * 0.15  # 15% of surplus
        })
    
    # Debt payoff recommendation
    credit_accounts = [acc for acc in accounts['accounts'] if acc['type']['name'] == 'credit']
    high_interest_debt = [acc for acc in credit_accounts if acc.get('interestRate', 0) > 15]
    
    if high_interest_debt:
        total_debt = sum(abs(acc['currentBalance']) for acc in high_interest_debt)
        recommendations.append({
            'type': 'debt_payoff',
            'priority': 'high',
            'name': 'High-Interest Debt Payoff',
            'target_amount': total_debt,
            'reasoning': 'Pay off high-interest debt to save on interest charges',
            'monthly_contribution': monthly_surplus * 0.4  # 40% of surplus
        })
    
    return recommendations

# Example usage
recommendations = await generate_goal_recommendations()
for rec in recommendations:
    print(f"💡 {rec['priority'].upper()} PRIORITY: {rec['name']}")
    print(f"   Target: ${rec['target_amount']:,.2f}")
    print(f"   Suggested monthly: ${rec['monthly_contribution']:,.2f}")
    print(f"   Reason: {rec['reasoning']}")
```

## 🚨 Error Handling

### Goal Operation Errors

```python
from monarchmoney import ValidationError, AuthenticationError

try:
    goal = await mm.create_goal(
        name="",  # Empty name
        target_amount=-1000  # Negative amount
    )
except ValidationError as e:
    print(f"Invalid goal data: {e}")
    print("Goal name cannot be empty and target amount must be positive")
```

### Goal Update Errors

```python
try:
    updated_goal = await mm.update_goal(
        goal_id="nonexistent_goal",
        target_amount=5000
    )
except ValidationError as e:
    print(f"Goal not found: {e}")
    # List existing goals
    goals = await mm.get_goals()
    print("Available goals:", [g['name'] for g in goals['goals']])
```

## 💡 Best Practices

### Goal Setting Strategy

```python
async def implement_smart_goal_strategy():
    """Implement SMART (Specific, Measurable, Achievable, Relevant, Time-bound) goals."""
    
    smart_goals = [
        {
            'name': 'Emergency Fund - 6 Months Expenses',  # Specific
            'target_amount': 18000,  # Measurable
            'target_date': '2024-12-31',  # Time-bound
            'description': 'Save enough to cover 6 months of living expenses for financial security',  # Relevant
            'monthly_needed': 1000  # Achievable based on income
        },
        {
            'name': 'Vacation to Italy',
            'target_amount': 4000,
            'target_date': '2024-08-15',
            'description': 'Family vacation to Italy including flights, hotels, and activities',
            'monthly_needed': 500
        }
    ]
    
    for goal_plan in smart_goals:
        goal = await mm.create_goal(
            name=goal_plan['name'],
            target_amount=goal_plan['target_amount'],
            target_date=goal_plan['target_date'],
            description=goal_plan['description']
        )
        print(f"Created SMART goal: {goal['name']}")
    
    return smart_goals
```

### Goal Prioritization

```python
async def prioritize_goals_by_urgency():
    """Prioritize goals based on urgency and importance."""
    goals = await mm.get_goals()
    
    prioritized = {
        'urgent_important': [],    # Emergency fund, high-interest debt
        'important_not_urgent': [], # Retirement, education
        'urgent_not_important': [], # Short-term wants
        'neither': []              # Nice-to-have goals
    }
    
    for goal in goals['goals']:
        if goal['status'] != 'active':
            continue
            
        # Determine priority based on goal type and timeline
        days_remaining = goal['timeline']['daysRemaining']
        goal_type = goal['goalType']
        
        if goal_type == 'debt_payoff' or 'emergency' in goal['name'].lower():
            prioritized['urgent_important'].append(goal)
        elif goal_type == 'investment' or 'retirement' in goal['name'].lower():
            prioritized['important_not_urgent'].append(goal)
        elif days_remaining < 180:  # Less than 6 months
            prioritized['urgent_not_important'].append(goal)
        else:
            prioritized['neither'].append(goal)
    
    return prioritized
```

### Progress Momentum Building

```python
async def build_goal_momentum():
    """Create strategies to build and maintain goal momentum."""
    goals = await mm.get_goals()
    
    momentum_strategies = []
    
    for goal in goals['goals']:
        if goal['status'] != 'active':
            continue
            
        progress = goal['progressPercent']
        
        if progress < 25:
            # Early stage - focus on building habit
            strategy = {
                'goal_id': goal['id'],
                'stage': 'building_habit',
                'recommendation': 'Start with small, consistent contributions',
                'action': f"Set up automatic ${goal['projections']['monthlyContributionNeeded']/4:.0f} weekly transfers"
            }
        elif progress < 75:
            # Middle stage - maintain momentum
            strategy = {
                'goal_id': goal['id'],
                'stage': 'maintaining_momentum', 
                'recommendation': 'Track progress weekly and celebrate milestones',
                'action': 'Review progress every Friday and adjust if needed'
            }
        else:
            # Final push - accelerate to finish
            strategy = {
                'goal_id': goal['id'],
                'stage': 'final_push',
                'recommendation': 'Consider increasing contributions to finish strong',
                'action': f"Add extra ${goal['remainingAmount']/6:.0f} monthly to finish 6 months early"
            }
        
        momentum_strategies.append(strategy)
    
    return momentum_strategies
```