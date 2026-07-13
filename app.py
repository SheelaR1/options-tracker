from fastapi import FastAPI, Request, Form 
from fastapi.templating import Jinja2Templates
from tracker import load_trades, save_trades, calculate_pnl, get_summary, add_trade, get_open_trades, close_trade
from fastapi.responses import RedirectResponse
import yfinance as yf
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home():
    return RedirectResponse(url="/trades")

@app.get("/summary")
def summary(request: Request):
    trades = load_trades()
    stats = get_summary(trades)
    return templates.TemplateResponse(request, "summary.html", {"stats": stats})

@app.get("/trades")
def get_trades(request: Request):
    trades = load_trades()
    result = []
    for trade in trades:
        pnl = calculate_pnl(trade)
        result.append({**trade, "pnl": round(pnl, 2) if pnl is not None else None})
    return templates.TemplateResponse(request, "trades.html", {"trades": result})

@app.get("/add")
def add_trade_form(request: Request):
    return templates.TemplateResponse(request, "add.html", {})

@app.post("/add")
def add_trade_submit(
    request: Request,
    ticker: str = Form(...),
    buy_price: float = Form(...),
    instrument_type: str = Form(...),
    shares: float = Form(...),
    status: str = Form(...),
    sell_price: float = Form(None),
    option_type: str = Form(None),
    strike_price: float = Form(None),
    expiration: str = Form(None),
):
    form_data = {
        "ticker": ticker, "buy_price": buy_price, "instrument_type": instrument_type,
        "shares": shares, "status": status, "sell_price": sell_price,
        "option_type": option_type, "strike_price": strike_price, "expiration": expiration,
    }

    try:
        price = yf.Ticker(ticker).fast_info["last_price"]
        if price is None:
            raise ValueError
    except Exception:
        return templates.TemplateResponse(request, "add.html", {"error": f"Invalid ticker: {ticker}", "form_data": form_data})

    if instrument_type == "option":
        try:
            exp_dt = datetime.strptime(expiration, "%Y-%m-%d")
        except (ValueError, TypeError):
            return templates.TemplateResponse(request, "add.html", {"error": "Invalid expiration date format. Use YYYY-MM-DD.", "form_data": form_data})

        if status != "closed" and exp_dt < datetime.now():
            return templates.TemplateResponse(request, "add.html", {"error": "Expiration must be in the future for open positions.", "form_data": form_data})

    trades = load_trades()
    add_trade(trades, ticker, buy_price, instrument_type, shares, status,
              sell_price, option_type, strike_price, expiration)
    save_trades(trades)
    return RedirectResponse(url="/trades", status_code=303)

@app.get("/close")
def close_position_form(request: Request):
    trades = load_trades()
    open_trades = get_open_trades(trades)
    result = []
    for index, trade in open_trades:
        pnl = calculate_pnl(trade)
        result.append({**trade, "pnl": round(pnl, 2) if pnl is not None else None, "index": index})
    return templates.TemplateResponse(request, "close.html", {"open_trades": result})

@app.post("/close")
def close_position_submit(index: int = Form(...), sell_price: float = Form(...)):
    trades = load_trades()
    close_trade(trades, index, sell_price)
    save_trades(trades)
    return RedirectResponse(url="/trades", status_code=303)