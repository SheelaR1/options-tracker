# Options Tracker

A command-line Python application for tracking stock options/trades and calculating profit/loss.

## Features

- Add trades with ticker validation against live market data
- Open and closed position tracking
- Live price fetching for open positions via yfinance
- Realized P/L for closed trades, unrealized P/L for open positions
- Close open positions with actual sell price entry
- View all trades with detailed breakdown (buy, sell, P/L, status)
- Summary stats: total P/L, win rate, winners/losers count
- Persistent storage via JSON
- Input validation across all user-facing prompts
- Options support 

## Roadmap

- [x] Stage 1: Core P/L logic
- [x] Stage 2: Save/load trades to disk
- [x] Stage 3: Live prices via yfinance API
- [x] Stage 4: Options support (calls/puts, strike, expiration, live option pricing)
- [ ] Stage 5: Web frontend (in progress)

## Future Plans
- Automated trading via broker API integration

## Tech

- Python 3
- yfinance

## Run it

```bash
pip install yfinance
python tracker.py
```
## Example Output

```
Enter a choice: 2
Trade 1: NVDA call $240.0 exp 2026-06-22 | Buy: $210.00 | Sell: $240.00 | P&L: $15000.00 | closed
Trade 2: AAPL | Buy: $180.00 | Sell: Live | P&L: $1164.20 | open
```

## Status

Active development. Built as a personal portfolio project.