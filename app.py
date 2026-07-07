from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from tracker import load_trades, calculate_pnl, get_summary

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