# trading function running offline rn 

def calculate_pnl(trade):
    #Returns the profit/loss: (sell_price - buy_price) × shares * just set it in a that it can be used later
    return (trade["sell_price"] - trade["buy_price"]) * trade ["shares"]

# sample = {"ticker": "AAPL", "buy_price": 140.0, "sell_price": 175.0, "shares": 10}
# print(calculate_pnl(sample))   # should print 250.0

# loss_sample = {"ticker": "TSLA", "buy_price": 200.0, "sell_price": 180.0, "shares": 5}
# print(calculate_pnl(loss_sample))   # should print -100.0

def add_trade(trades, ticker, buy_price, sell_price, shares):
    # 1. Build a new trade dict from the inputs
    new_trade = { "ticker": ticker, "buy_price":buy_price, "sell_price": sell_price, "shares":shares}
    # 2. Append to the trades list
    trades.append(new_trade)


trades = []   # start with empty list

add_trade(trades, "AAPL", 150.0, 175.0, 10)
add_trade(trades, "TSLA", 200.0, 180.0, 5)



def view_trades(trades):
    for i , trade in enumerate(trades):
        # What trade I am working with
        number = i + 1
        pnl = calculate_pnl(trade)
        print(f"Trade {number}: {trade["ticker"]} profit/loss ${pnl}")

view_trades(trades)


def show_summary(trades):
    # 1. Count total trades
    total_trades = len(trades)
    total_pnl = 0
    winners = 0 
    losers = 0
    for trade in trades:
    #2. Sum up all the P/Ls
        pnl = calculate_pnl(trade)
        total_pnl += pnl
    # 3. Count winners (P/L > 0) and losers (P/L <= 0)
        if pnl > 0:
            winners += 1
        else:
            losers += 1
    # 4. Calculate win rate as a percentage
    win_percent = (winners/ total_trades) * 100
    # Blank print 
    print()
    # 5. Print everything
    print(f"Total trades: {total_trades}, Winning trades:{winners}, Losing trades:{losers}, Total profit/loss:{total_pnl}, Win rate: {win_percent}%:")

show_summary(trades)


       