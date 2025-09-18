# Investment Management

This module provides comprehensive investment and portfolio management functionality including holdings management, securities data, and performance analytics.

## 💼 Investment Holdings

### `get_account_holdings(account_id, start_date=None)`

Get investment holdings for a specific investment account.

**Parameters:**
- `account_id` (str): Investment account ID
- `start_date` (str, optional): Start date for historical data in YYYY-MM-DD format

**Returns:** Dict containing holdings data:
```python
{
    "holdings": [
        {
            "id": str,                   # Holding ID
            "security": {
                "id": str,               # Security ID
                "symbol": str,           # Stock ticker symbol
                "name": str,             # Security name
                "type": str,             # Security type (stock, bond, etc.)
                "cusip": str,            # CUSIP identifier
                "exchange": str          # Exchange (NYSE, NASDAQ, etc.)
            },
            "quantity": float,           # Number of shares/units
            "basisPerShare": float,      # Cost basis per share
            "totalBasis": float,         # Total cost basis
            "currentPrice": float,       # Current market price
            "marketValue": float,        # Current market value
            "unrealizedGain": float,     # Unrealized gain/loss
            "unrealizedGainPercent": float,  # Unrealized gain/loss %
            "acquisitionDate": str,      # Date acquired (YYYY-MM-DD)
            "isManual": bool,            # Whether manually entered
            "lastUpdated": str           # Last price update timestamp
        }
    ],
    "summary": {
        "totalValue": float,         # Total portfolio value
        "totalBasis": float,         # Total cost basis
        "totalGain": float,          # Total unrealized gain/loss
        "totalGainPercent": float,   # Total gain/loss percentage
        "holdingCount": int,         # Number of holdings
        "diversification": {         # Portfolio diversification
            "bySecurityType": {...},
            "bySector": {...},
            "byAllocation": {...}
        }
    },
    "account": {                     # Account information
        "id": str,
        "displayName": str,
        "type": str
    }
}
```

**Example:**
```python
# Get holdings for investment account
holdings_data = await mm.get_account_holdings("investment_account_123")

print(f"Portfolio Value: ${holdings_data['summary']['totalValue']:,.2f}")
print(f"Total Gain: ${holdings_data['summary']['totalGain']:,.2f} ({holdings_data['summary']['totalGainPercent']:.1f}%)")

for holding in holdings_data["holdings"]:
    security = holding["security"]
    gain_pct = holding["unrealizedGainPercent"]
    print(f"{security['symbol']}: {holding['quantity']} shares @ ${holding['currentPrice']:.2f} ({gain_pct:+.1f}%)")
```

## ✏️ Manual Holdings Management

### `create_manual_holding(account_id, symbol, quantity, basis_per_share=None, acquisition_date=None)`

Create a manual investment holding by security symbol.

**Parameters:**
- `account_id` (str): Investment account ID
- `symbol` (str): Stock ticker symbol (e.g., "AAPL", "MSFT")
- `quantity` (float): Number of shares/units
- `basis_per_share` (float, optional): Cost basis per share
- `acquisition_date` (str, optional): Acquisition date in YYYY-MM-DD format

**Returns:** Dict with created holding data

**Example:**
```python
# Add Apple stock to portfolio
holding = await mm.create_manual_holding(
    account_id="investment_123",
    symbol="AAPL",
    quantity=100.0,
    basis_per_share=150.00,
    acquisition_date="2024-01-15"
)

print(f"Added holding: {holding['security']['name']}")
print(f"Holding ID: {holding['id']}")
```

### `create_manual_holding_by_ticker(account_id, ticker, quantity, basis_per_share=None)`

Alias method for creating manual holdings by ticker symbol.

**Parameters:**
- `account_id` (str): Investment account ID
- `ticker` (str): Stock ticker symbol
- `quantity` (float): Number of shares
- `basis_per_share` (float, optional): Cost basis per share

**Returns:** Dict with created holding data

### `update_holding_quantity(holding_id, new_quantity, new_basis_per_share=None)`

Update the quantity and cost basis of an existing manual holding.

**Parameters:**
- `holding_id` (str): Holding ID to update
- `new_quantity` (float): New quantity of shares/units
- `new_basis_per_share` (float, optional): New cost basis per share

**Returns:** Dict with updated holding data

**Example:**
```python
# Update holding after buying more shares
updated_holding = await mm.update_holding_quantity(
    holding_id="holding_123",
    new_quantity=150.0,        # Increased from 100 to 150 shares
    new_basis_per_share=155.00 # New average cost basis
)

print(f"Updated to {updated_holding['quantity']} shares")
```

### `delete_manual_holding(holding_id)`

Delete a manual investment holding.

**Parameters:**
- `holding_id` (str): Holding ID to delete

**Returns:** bool (True if successful)

**Example:**
```python
success = await mm.delete_manual_holding("holding_123")
if success:
    print("Holding deleted successfully")
```

## 🔍 Holdings Lookup & Search

### `get_holding_by_ticker(ticker, account_id=None)`

Find holding information by ticker symbol.

**Parameters:**
- `ticker` (str): Stock ticker symbol
- `account_id` (str, optional): Specific account to search (all accounts if None)

**Returns:** Dict with holding info or None if not found

**Example:**
```python
# Find Apple holdings across all accounts
apple_holding = await mm.get_holding_by_ticker("AAPL")

if apple_holding:
    print(f"Found AAPL: {apple_holding['quantity']} shares")
    print(f"Current value: ${apple_holding['marketValue']:,.2f}")
else:
    print("No AAPL holdings found")
```

### `add_holding_by_ticker(account_id, ticker, quantity, basis_per_share=None)`

Add a new holding by ticker (convenience method).

**Parameters:**
- `account_id` (str): Investment account ID
- `ticker` (str): Stock ticker symbol
- `quantity` (float): Number of shares
- `basis_per_share` (float, optional): Cost basis per share

**Returns:** Dict with created holding info

### `remove_holding_by_ticker(ticker, account_id=None)`

Remove holding by ticker symbol.

**Parameters:**
- `ticker` (str): Stock ticker symbol to remove
- `account_id` (str, optional): Specific account (all accounts if None)

**Returns:** bool (True if successful)

## 📈 Securities & Market Data

### `get_security_details(ticker=None, cusip=None)`

Get detailed security information by ticker or CUSIP.

**Parameters:**
- `ticker` (str, optional): Stock ticker symbol
- `cusip` (str, optional): CUSIP identifier

**Returns:** Dict with security information:
```python
{
    "security": {
        "id": str,
        "symbol": str,               # Ticker symbol
        "name": str,                 # Company/security name
        "type": str,                 # Security type
        "cusip": str,                # CUSIP identifier
        "exchange": str,             # Exchange
        "sector": str,               # Business sector
        "industry": str,             # Industry classification
        "marketCap": float,          # Market capitalization
        "description": str           # Company description
    },
    "pricing": {
        "currentPrice": float,       # Current market price
        "previousClose": float,      # Previous day's close
        "dayChange": float,          # Change from previous close
        "dayChangePercent": float,   # Percentage change
        "volume": int,               # Trading volume
        "averageVolume": int,        # Average daily volume
        "high52Week": float,         # 52-week high
        "low52Week": float,          # 52-week low
        "lastUpdated": str           # Price timestamp
    },
    "fundamentals": {               # Fundamental data (if available)
        "peRatio": float,
        "dividendYield": float,
        "eps": float,
        "beta": float
    }
}
```

**Example:**
```python
# Get Apple stock details
security = await mm.get_security_details(ticker="AAPL")

print(f"Company: {security['security']['name']}")
print(f"Sector: {security['security']['sector']}")
print(f"Current Price: ${security['pricing']['currentPrice']:.2f}")
print(f"Day Change: {security['pricing']['dayChangePercent']:+.2f}%")
```

### `get_security_price_history(symbol, start_date, end_date)`

Get historical price data for a security.

**Parameters:**
- `symbol` (str): Stock ticker symbol
- `start_date` (str): Start date in YYYY-MM-DD format
- `end_date` (str): End date in YYYY-MM-DD format

**Returns:** Dict with historical OHLCV data:
```python
{
    "priceHistory": [
        {
            "date": str,             # YYYY-MM-DD
            "open": float,           # Opening price
            "high": float,           # Day's high
            "low": float,            # Day's low
            "close": float,          # Closing price
            "volume": int,           # Trading volume
            "adjustedClose": float   # Dividend-adjusted close
        }
    ],
    "symbol": str,
    "dateRange": {
        "startDate": str,
        "endDate": str
    },
    "summary": {
        "totalReturn": float,        # Total return over period
        "totalReturnPercent": float, # Total return percentage
        "volatility": float,         # Price volatility
        "averageVolume": int         # Average daily volume
    }
}
```

**Example:**
```python
# Get 1 year of Apple price history
from datetime import datetime, timedelta

end_date = datetime.now()
start_date = end_date - timedelta(days=365)

history = await mm.get_security_price_history(
    symbol="AAPL",
    start_date=start_date.strftime("%Y-%m-%d"),
    end_date=end_date.strftime("%Y-%m-%d")
)

print(f"1-year return: {history['summary']['totalReturnPercent']:.1f}%")
for day in history['priceHistory'][-5:]:  # Last 5 days
    print(f"{day['date']}: ${day['close']:.2f}")
```

## 📊 Investment Performance & Analytics

### `get_investment_performance(account_id=None, start_date=None, end_date=None, time_period="1Y")`

Get comprehensive investment performance metrics.

**Parameters:**
- `account_id` (str, optional): Specific account (all investment accounts if None)
- `start_date` (str, optional): Start date for analysis
- `end_date` (str, optional): End date for analysis
- `time_period` (str): Predefined period ("1M", "3M", "6M", "1Y", "3Y", "5Y")

**Returns:** Dict with performance analytics:
```python
{
    "performance": {
        "totalReturn": float,            # Total return amount
        "totalReturnPercent": float,     # Total return percentage
        "annualizedReturn": float,       # Annualized return percentage
        "volatility": float,             # Portfolio volatility
        "sharpeRatio": float,            # Risk-adjusted return
        "maxDrawdown": float,            # Maximum drawdown
        "beta": float,                   # Market beta
        "alpha": float                   # Alpha vs benchmark
    },
    "attribution": {                     # Performance attribution
        "byHolding": [
            {
                "symbol": str,
                "contribution": float,   # Contribution to total return
                "weight": float,         # Portfolio weight
                "return": float          # Individual holding return
            }
        ],
        "bySector": {...},              # Sector attribution
        "byAssetClass": {...}           # Asset class attribution
    },
    "benchmark": {                      # Benchmark comparison
        "name": str,                    # Benchmark name (e.g., "S&P 500")
        "return": float,                # Benchmark return
        "outperformance": float         # Portfolio vs benchmark
    },
    "riskMetrics": {
        "valueAtRisk": float,           # 95% VaR
        "conditionalVaR": float,        # Expected shortfall
        "trackingError": float,         # Tracking error vs benchmark
        "informationRatio": float       # Information ratio
    }
}
```

**Example:**
```python
# Get 1-year performance for all investment accounts
performance = await mm.get_investment_performance(time_period="1Y")

print(f"Annual Return: {performance['performance']['annualizedReturn']:.1f}%")
print(f"Volatility: {performance['performance']['volatility']:.1f}%")
print(f"Sharpe Ratio: {performance['performance']['sharpeRatio']:.2f}")

# Top performers
for holding in performance['attribution']['byHolding'][:5]:
    print(f"{holding['symbol']}: {holding['return']:+.1f}% contribution")
```

## 📋 Portfolio Analysis Tools

### Portfolio Composition Analysis

```python
async def analyze_portfolio_composition(account_id):
    """Analyze portfolio composition and diversification."""
    holdings = await mm.get_account_holdings(account_id)
    
    # Sector diversification
    sector_allocation = {}
    total_value = holdings['summary']['totalValue']
    
    for holding in holdings['holdings']:
        security_details = await mm.get_security_details(
            ticker=holding['security']['symbol']
        )
        
        sector = security_details['security']['sector']
        holding_value = holding['marketValue']
        weight = (holding_value / total_value) * 100
        
        sector_allocation[sector] = sector_allocation.get(sector, 0) + weight
    
    return sector_allocation
```

### Performance Tracking

```python
async def track_holding_performance(symbol, period_days=30):
    """Track individual holding performance over time."""
    from datetime import datetime, timedelta
    
    # Get current holding
    holding = await mm.get_holding_by_ticker(symbol)
    if not holding:
        return None
    
    # Get price history
    end_date = datetime.now()
    start_date = end_date - timedelta(days=period_days)
    
    history = await mm.get_security_price_history(
        symbol=symbol,
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d")
    )
    
    # Calculate metrics
    current_price = holding['currentPrice']
    basis_price = holding['basisPerShare']
    period_start_price = history['priceHistory'][0]['close']
    
    return {
        'symbol': symbol,
        'total_return_pct': ((current_price - basis_price) / basis_price) * 100,
        'period_return_pct': ((current_price - period_start_price) / period_start_price) * 100,
        'current_value': holding['marketValue'],
        'unrealized_gain': holding['unrealizedGain']
    }
```

### Rebalancing Analysis

```python
async def analyze_rebalancing_needs(account_id, target_allocation):
    """
    Analyze portfolio rebalancing needs.
    
    target_allocation: Dict mapping sectors to target percentages
    Example: {"Technology": 30, "Healthcare": 20, "Finance": 15, ...}
    """
    holdings = await mm.get_account_holdings(account_id)
    total_value = holdings['summary']['totalValue']
    
    # Calculate current allocation
    current_allocation = {}
    for holding in holdings['holdings']:
        security = await mm.get_security_details(
            ticker=holding['security']['symbol']
        )
        sector = security['security']['sector']
        weight = (holding['marketValue'] / total_value) * 100
        current_allocation[sector] = current_allocation.get(sector, 0) + weight
    
    # Calculate rebalancing needs
    rebalancing_needs = {}
    for sector, target_pct in target_allocation.items():
        current_pct = current_allocation.get(sector, 0)
        difference = target_pct - current_pct
        dollar_amount = (difference / 100) * total_value
        
        rebalancing_needs[sector] = {
            'current_percent': current_pct,
            'target_percent': target_pct,
            'difference_percent': difference,
            'dollar_amount': dollar_amount,
            'action': 'buy' if difference > 0 else 'sell' if difference < 0 else 'hold'
        }
    
    return rebalancing_needs
```

## 🚨 Error Handling

### Investment Operation Errors

```python
from monarchmoney import ValidationError, AuthenticationError

try:
    holding = await mm.create_manual_holding(
        account_id="invalid_account",
        symbol="AAPL", 
        quantity=100
    )
except ValidationError as e:
    print(f"Invalid holding data: {e}")
    # Check if account exists and is investment type
    accounts = await mm.get_accounts()
    investment_accounts = [
        acc for acc in accounts['accounts'] 
        if acc['type']['name'] == 'investment'
    ]
    print(f"Available investment accounts: {[acc['id'] for acc in investment_accounts]}")
```

### Security Lookup Errors

```python
try:
    security = await mm.get_security_details(ticker="INVALID_SYMBOL")
except ValidationError as e:
    print(f"Security not found: {e}")
    # Suggest similar symbols or search
```

### Holdings Management Errors

```python
# Handle missing holdings gracefully
holding = await mm.get_holding_by_ticker("AAPL")
if holding is None:
    print("No AAPL holdings found")
    # Create new holding or suggest adding
else:
    # Update existing holding
    await mm.update_holding_quantity(
        holding_id=holding['id'],
        new_quantity=holding['quantity'] + 10
    )
```

## 💡 Best Practices

### Portfolio Monitoring

```python
async def daily_portfolio_check():
    """Daily portfolio monitoring routine."""
    accounts = await mm.get_accounts()
    
    for account in accounts['accounts']:
        if account['type']['name'] == 'investment':
            holdings = await mm.get_account_holdings(account['id'])
            
            # Check for significant moves
            for holding in holdings['holdings']:
                if abs(holding['unrealizedGainPercent']) > 5:  # 5% threshold
                    print(f"Alert: {holding['security']['symbol']} moved {holding['unrealizedGainPercent']:+.1f}%")
```

### Data Consistency

```python
async def validate_portfolio_data():
    """Validate portfolio data consistency."""
    accounts = await mm.get_accounts()
    
    for account in accounts['accounts']:
        if account['type']['name'] == 'investment':
            holdings = await mm.get_account_holdings(account['id'])
            
            # Verify market values are current
            for holding in holdings['holdings']:
                security = await mm.get_security_details(
                    ticker=holding['security']['symbol']
                )
                
                current_price = security['pricing']['currentPrice']
                calculated_value = holding['quantity'] * current_price
                
                if abs(calculated_value - holding['marketValue']) > 0.01:
                    print(f"Price discrepancy for {holding['security']['symbol']}")
```

### Cost Basis Tracking

```python
async def update_cost_basis_after_trade(symbol, trade_quantity, trade_price, trade_type):
    """Update cost basis after buying/selling shares."""
    holding = await mm.get_holding_by_ticker(symbol)
    
    if trade_type == 'buy':
        # Calculate new average cost basis
        old_value = holding['quantity'] * holding['basisPerShare']
        new_value = trade_quantity * trade_price
        
        new_quantity = holding['quantity'] + trade_quantity
        new_basis = (old_value + new_value) / new_quantity
        
        await mm.update_holding_quantity(
            holding_id=holding['id'],
            new_quantity=new_quantity,
            new_basis_per_share=new_basis
        )
    
    elif trade_type == 'sell':
        new_quantity = holding['quantity'] - trade_quantity
        # Basis per share stays the same for FIFO accounting
        
        await mm.update_holding_quantity(
            holding_id=holding['id'],
            new_quantity=new_quantity
        )
```