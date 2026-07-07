import json  
import yfinance as yf # implementing live prices 
from datetime import datetime # expiration dates handling

# trading function running offline rn 

# Helper Function for options(do not want to deal with nested statements)
def get_live_option_price(trade):
    try:
        chain = yf.Ticker(trade["ticker"]).option_chain(trade["expiration"])
        if trade["option_type"] == "call":
            table = chain.calls
        else:
            table = chain.puts
        row = table[table["strike"] == trade["strike_price"]]
        if row.empty:
            return None
        else:
            return row["lastPrice"].iloc[0]
    except Exception:
        return None

# Calculating Profit/Loss
def calculate_pnl(trade):
    #Open position handling
    if trade ["sell_price"] == None:
        if trade["instrument_type"] == "stock":
            sell_price = yf.Ticker(trade["ticker"]).fast_info["last_price"]
        else:
            sell_price = get_live_option_price(trade)
    #Closed postion handling
    else:
        sell_price = trade["sell_price"]
    if sell_price is None:
        return None
    #Returns the profit/loss: (sell_price - buy_price) × shares (This is for shares)
    if trade["instrument_type"] == "stock":
        return (sell_price - trade["buy_price"]) * trade ["shares"]
    #Returns the profit/loss: (sell_price - buy_price) × contracts × 100 (This is for options)
    elif trade["instrument_type"] == "option":
        return (sell_price - trade["buy_price"]) * trade["shares"] * 100
    
# Validator (Helper function)
def get_validated_input(prompt,cast_type,valid_options):
    while True:
        try:
            validated_input = input(prompt)
            result = cast_type(validated_input)
            if valid_options is not None:
                if result in valid_options:
                    return result
                else:
                    print("Please enter a valid option")
            else:
                return result
        except ValueError:
            print("Please input a valid prompt(numbers/alphabets)")

def add_trade(trades, ticker, buy_price, instrument_type, shares, status,
              sell_price, option_type=None, strike_price=None, expiration=None):
    new_trade = {
        "ticker": ticker,
        "buy_price": buy_price,
        "sell_price": sell_price,
        "shares": shares,
        "status": status,
        "instrument_type": instrument_type,
        "option_type": option_type,
        "strike_price": strike_price,
        "expiration": expiration,
    }
    trades.append(new_trade)

# refactoring for web
def add_trade_cli(trades, ticker, buy_price):
    #Stock/Option handling 
    instrument_type = get_validated_input("Stock or Option: ", lambda x: x.strip().lower(), ["stock", "option"])
    option_type = None
    strike_price = None 
    expiration = None
    #Bad ticker handling
    while True:
        try:
            price = yf.Ticker(ticker).fast_info["last_price"]
            if price is not None:
                break
        except Exception:
            print("Invalid ticker")
            ticker = input("Ticker: ")
    # Open/Close positions
    status = get_validated_input("Open or Closed Position:" , lambda x: x.strip().lower(), ["open", "closed"])
    if status == 'closed':
        sell_price = get_validated_input("Enter the sell price: ", float, None)
    else:
        sell_price = None
    if instrument_type == "option":
            option_type = get_validated_input("Call or Put: ", lambda x: x.strip().lower(), ["call", "put"])
            #Strike price 
            strike_price = get_validated_input("Strike price: ", float, None)
            #Expiration 
            valid_expirations = yf.Ticker(ticker).options
            while True:
                expiration = get_validated_input("Enter expiration date(YYYY-MM-DD): ", lambda x: datetime.strptime(x, "%Y-%m-%d"), None)
                if status == "closed":
                    expiration = expiration.strftime("%Y-%m-%d")
                    break
                if expiration < datetime.now():
                    print("Enter a valid expiration(must be in the future)")
                    continue
                expiration = expiration.strftime("%Y-%m-%d")
                if expiration not in valid_expirations:
                    print("Not a valid contract expiration date")
                    continue
                break
    # No shares handling (with a helper now)
    shares = get_validated_input("Enter the number of shares/contracts: ", float, None)
    add_trade(trades, ticker, buy_price, instrument_type, shares, status, sell_price, option_type, strike_price, expiration)
    

def view_trades(trades):
    for i , trade in enumerate(trades):
        # What trade I am working with
        number = i + 1
        pnl = calculate_pnl(trade)
        # need to handle sell price being none
        if trade["sell_price"] is None:
            sell_display = "Live"
        else:
            sell_display = f"${trade['sell_price']:.2f}"
        if pnl is None:
            pnl_display = "Cannot find contract"
        else: 
            pnl_display = f"${pnl:.2f}"
        # Format handling 
        if trade["instrument_type"] == "stock":
            detail = trade ["ticker"]
        else:
            detail = f"{trade['ticker']} {trade['option_type']} ${trade['strike_price']} exp {trade['expiration']}"
        # changed to show buy price/sell price
        print(f"Trade {number}: {detail} | Buy: ${trade['buy_price']:.2f} | Sell: {sell_display} | P&L: {pnl_display} | {trade['status']}")

def get_open_trades(trades):
    return [(i, t) for i, t in enumerate(trades) if t["status"] == "open"]

def close_trade(trades, original_index, sell_price):
    trades[original_index]["sell_price"] = sell_price
    trades[original_index]["status"] = "closed"

# Close open positions
def close_position_cli(trades):
    open_trades = get_open_trades(trades)
    if not open_trades:
        print("No open trades.")
        return
    for i, (index, trade) in enumerate(open_trades):
        number = i + 1
        pnl = calculate_pnl(trade)
        if pnl is None:
            pnl_display = "Cannot find contract"
        else:
            pnl_display = f"${pnl:.2f}"
        print(f"Trade {number}: {trade['ticker']} profit/loss {pnl_display}. {trade['status']}")
    choice = get_validated_input("Enter a choice:", int, list(range(1, len(open_trades) + 1)))
    sell_price = get_validated_input("Enter sell price: ", float, None)
    original_index, _ = open_trades[choice - 1]
    close_trade(trades, original_index, sell_price)

def show_summary(trades):
    # Count total trades
    if not trades:
        print("No trades yet - add some")
        return 
    total_pnl = 0
    winners = 0 
    losers = 0
    for trade in trades:
    #Sum up all the P/Ls
        if trade["status"] != "closed":
            continue
        pnl = calculate_pnl(trade) 
        total_pnl += pnl
    #Count winners (P/L > 0) and losers (P/L <= 0)
        if pnl > 0:
            winners += 1
        else:
            losers += 1
    total_trades = winners + losers
    # Safeguard for zero 
    if total_trades == 0:
        print("No closed trades to summarize")
        return
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

# menu 
def display_menu():
        print('1. Add trade')
        print('2. View trades')
        print('3. Show summary')
        print('4. Close position')
        print('5. Quit')
       
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
     #updated this line once helper was writeen
     choice = get_validated_input("Enter a choice: ", int, list(range(1, 6)))
     if choice == 1:
        ticker = input("Ticker: ")
        buy_price = get_validated_input("Enter a buy price: ", float, None)
        add_trade_cli(trades, ticker, buy_price)
        save_trades(trades)
     elif choice == 2:
         view_trades(trades)
     elif choice == 3:
         show_summary(trades)
     elif choice == 4:
         close_position_cli(trades)
         save_trades(trades)
     elif choice == 5:
         break
    

    


