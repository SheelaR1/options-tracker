# trading function running offline rn 

def calculate_pnl(trade):
    #Returns the profit/loss: (sell_price - buy_price) × shares * just set it in a that it can be used later
    return (trade["sell_price"] - trade["buy_price"]) * trade ["shares"]

# sample = {"ticker": "AAPL", "buy_price": 140.0, "sell_price": 175.0, "shares": 10}
# print(calculate_pnl(sample))   # should print 250.0

# loss_sample = {"ticker": "TSLA", "buy_price": 200.0, "sell_price": 180.0, "shares": 5}
# print(calculate_pnl(loss_sample))   # should print -100.0

def add_trade(trades, ticker, buy_price, sell_price, shares):
    # Build a new trade dict from the inputs
    new_trade = { "ticker": ticker, "buy_price":buy_price, "sell_price": sell_price, "shares":shares}
    # Append to the trades list
    trades.append(new_trade)


trades = []   # start with empty list

add_trade(trades, "AAPL", 150.0, 175.0, 10)
add_trade(trades, "TSLA", 200.0, 180.0, 5)



def view_trades(trades):
    for i , trade in enumerate(trades):
        # What trade I am working with
        number = i + 1
        pnl = calculate_pnl(trade)
        print(f"Trade {number}: {trade["ticker"]} profit/loss ${pnl:.2f}")

#view_trades(trades)


def show_summary(trades):
    # Count total trades
    if not trades:
        print("No trades yet - add some")
        return 
    total_trades = len(trades)
    total_pnl = 0
    winners = 0 
    losers = 0
    for trade in trades:
    #Sum up all the P/Ls
        pnl = calculate_pnl(trade)
        total_pnl += pnl
    #Count winners (P/L > 0) and losers (P/L <= 0)
        if pnl > 0:
            winners += 1
        else:
            losers += 1
    # Calculate win rate as a percentage
    win_percent = (winners/ total_trades) * 100
    # Blank print 
    print()
    # Print everything
    print(f"Total trades: {total_trades}")
    print(f"Winning trades: {winners}")
    print(f"Losing trades: {losers}") 
    print(f"Total profit/loss: ${total_pnl:.2f}")
    print(f"Win rate: {win_percent:.2f}%:")

# show_summary(trades)

# menu 
def display_menu():
        print('1. Add trade')
        print('2. View trades')
        print('3. Show summary')
        print('4. Quit')

#display_menu()

#user input 
def get_user_choice():
    choice = int(input("Enter your choice: "))
    return choice

#get_user_choice()

while True:
     display_menu()
     choice = get_user_choice()

     if choice == 1:
        ticker = input("Ticker: ")
        buy_price = float(input("Buy price: "))
        sell_price = float(input("Sell price: "))
        shares = int(input("Shares: "))
        add_trade(trades, ticker, buy_price, sell_price, shares)
     elif choice == 2:
         view_trades(trades)
     elif choice == 3:
         show_summary(trades)
     elif choice == 4:
         break
     else:
         print("Invalid choice. Pick between 1-4")


