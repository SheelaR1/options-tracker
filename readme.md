# Options Tracker

A command-line Python application for tracking stock trades and calculating profit/loss.

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

## Roadmap

- [x] Stage 1: Core P/L logic (in progress)
- [x] Stage 2: Save/load trades to disk
- [x] Stage 3: Live prices via yfinance API
- [ ] Stage 4: Options support / web frontend

## Future Plans
- Live options pricing via yfinance option chains
- Automated trading via broker API integration

## Tech

Python 3
yfinance

## Run it

```python
pip install yfinance
python tracker.py
```

## Status

Active development. Built as a personal portfolio project.