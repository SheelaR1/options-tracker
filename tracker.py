import json  
import yfinance as yf # implementing live prices 

# trading function running offline rn 

def calculate_pnl(trade):
    #Open position handling
    if trade ["sell_price"] == None:
        sell_price = yf.Ticker(trade["ticker"]).fast_info["last_price"]
    
    #Closed postion handling
    else:
        sell_price = trade["sell_price"]
    #Returns the profit/loss: (sell_price - buy_price) × shares * just set it in a that it can be used later
    return (sell_price - trade["buy_price"]) * trade ["shares"]


def add_trade(trades, ticker, buy_price, shares):
    #Bad ticker handling
    while True:
        price = yf.Ticker(ticker).fast_info["last_price"]
        if price is not None:
            break
        else:
            print ("Invalid ticker")
            ticker = input("Ticker: ")
    # Open/Close positions
    while True:
        status = input("Open/Closed Positon:" ).lower()
        if status == "open":
            sell_price = None
            break
        elif status == "closed":
            try:
                sell_price = float(input("Enter sell price:"))
                break
            except ValueError:
                print("Sell price must only have numbers")
        else:
            print("Invalid choice, only open or closed allowed")
    # Build a new trade dict from the inputs
    new_trade = { "ticker": ticker, "buy_price":buy_price, "sell_price":sell_price, "shares":shares, "status":status}
    # Append to the trades list
    trades.append(new_trade)
    

def view_trades(trades):
    for i , trade in enumerate(trades):
        # What trade I am working with
        number = i + 1
        pnl = calculate_pnl(trade)
        print(f"Trade {number}: {trade["ticker"]} profit/loss ${pnl:.2f}. {trade["status"]}")

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

#user input fixed to handle typing in non ints
def get_user_choice():
    while True:
        try:
            choice = int(input("Enter your choice: "))
            return choice
        except ValueError:
            print("Enter a valid choice!!")


#get_user_choice()


# save trades from memory 
def save_trades(trades):
    with open("trades.json", 'w') as f:
        json.dump(trades, f)

# load trades from the file 
def load_trades():
    try:
        with open("trades.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

trades = load_trades()   # changed to load_trades function for stage 2

while True:
     display_menu()
     choice = get_user_choice()

     if choice == 1:
        ticker = input("Ticker: ")
        buy_price = float(input("Buy price: "))
        shares = int(input("Shares: "))
        add_trade(trades, ticker, buy_price, shares)
        save_trades(trades)
     elif choice == 2:
         view_trades(trades)
     elif choice == 3:
         show_summary(trades)
     elif choice == 4:
         break
     else:
         print("Invalid choice. Pick between 1-4")

    


