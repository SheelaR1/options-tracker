from fastapi import FastAPI, Request, Form 
from fastapi.templating import Jinja2Templates
from tracker import load_trades, save_trades, calculate_pnl, get_summary, add_trade
from fastapi.responses import RedirectResponse


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home():
    return {"message": "Options tracker web frontend"}

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
    trades = load_trades()
    add_trade(trades, ticker, buy_price, instrument_type, shares, status,
              sell_price, option_type, strike_price, expiration)
    save_trades(trades)
    return RedirectResponse(url="/trades", status_code=303)