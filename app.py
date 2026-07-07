from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from tracker import load_trades, calculate_pnl

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home():
    return {"message": "Options tracker web frontend"}

@app.get("/trades")
def get_trades(request: Request):
    trades = load_trades()
    result = []
    for trade in trades:
        pnl = calculate_pnl(trade)
        result.append({**trade, "pnl": round(pnl, 2) if pnl is not None else None})
    return templates.TemplateResponse(request, "trades.html", {"trades": result})