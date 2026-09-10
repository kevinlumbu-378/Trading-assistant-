import json, os, yfinance as yf
from datetime import datetime
from telegram.ext import Application, CommandHandler

TOKEN = os.environ.get("8694303363:AAFf4Q92KZZs9FgFEPe8Eqck2-JBIBdWykA")
CHAT_ID = int(os.environ.get("8946872265"))
F_ZONES = "zones.json"
F_JOURNAL = "journal.json"

def load(f):
    try:
        with open(f,'r') as file: return json.load(file)
    except: return []
def save(f, d):
    with open(f,'w') as file: json.dump(file, d) if False else json.dump(d, file)

zones = load(F_ZONES)
trades = load(F_JOURNAL)

def get_price():
    try:
        p=yf.Ticker("EURUSD=X").fast_info['lastPrice']
        if p: return float(p)
    except: pass
    return float(yf.Ticker("EURUSD=X").history(period="1d",interval="1m")['Close'].iloc[-1])

async def start(u,c):
    await u.message.reply_text(
        "🤖 TRADING ASSISTANT EURUSD\n\n"
        "📍 ZONES:\n/setob 1.0850 1.0865\n/listob\n\n"
        "📊 CALCUL:\n/risk 50 20\n/tp 1.0850 1.0830 buy\n\n"
        "📓 JOURNAL:\n/trade buy 1.0850 1.0830 1.0890\n/journal\n/stats\n/win 0\n/loss 0"
    )

# --- ZONES ---
async def setob(u,c):
    try:
        low=float(c.args[0]);high=float(c.args[1])
        zones.append({"low":min(low,high),"high":max(low,high)});save(F_ZONES,zones)
        await u.message.reply_text(f"✅ OB {min(low,high)}-{max(low,high)}")
    except: await u.message.reply_text("/setob 1.0850 1.0865")
async def listob(u,c):
    if not zones: await u.message.reply_text("Aucune zone"); return
    await u.message.reply_text("\n".join([f"{i}: {z['low']}-{z['high']}" for i,z in enumerate(zones)]))
async def clearob(u,c): zones.clear();save(F_ZONES,zones);await u.message.reply_text("Effacé")
async def delob(u,c):
    try: zones.pop(int(c.args[0]));save(F_ZONES,zones);await u.message.reply_text("Supprimé")
    except: await u.message.reply_text("/delob 0")

# --- CALCUL ---
async def risk(u,c):
    try:
        r=float(c.args[0]);sl=float(c.args[1]);lot=round(r/(sl*10),2)
        await u.message.reply_text(f"📊 RISQUE {r}$ SL {sl} pips\n👉 LOT: {lot}")
    except: await u.message.reply_text("/risk 50 20")
async def tp(u,c):
    try:
        e=float(c.args[0]);s=float(c.args[1]);d=c.args[2].lower();ri=abs(e-s)
        tp1=e+ri*2 if d=="buy" else e-ri*2;tp2=e+ri*3 if d=="buy" else e-ri*3
        await u.message.reply_text(f"🎯 TP {d.upper()} E:{e} SL:{s}\nTP1 1:2 {tp1:.5f}\nTP2 1:3 {tp2:.5f}")
    except: await u.message.reply_text("/tp 1.0850 1.0830 buy")

# --- JOURNAL ---
async def trade(u,c):
    try:
        direction=c.args[0].lower();entry=float(c.args[1]);sl=float(c.args[2]);tp_val=float(c.args[3])
        trades.append({"date":datetime.now().strftime("%d/%m %H:%M"),"dir":direction,"entry":entry,"sl":sl,"tp":tp_val,"result":None})
        save(F_JOURNAL,trades)
        await u.message.reply_text(f"📓 Trade enregistré:\n{direction.upper()} {entry} SL {sl} TP {tp_val}\nTape /win 0 si TP touché")
    except: await u.message.reply_text("/trade buy 1.0850 1.0830 1.0890")

async def journal(u,c):
    if not trades: await u.message.reply_text("Journal vide"); return
    msg="📓 10 Derniers trades:\n"
    for i,t in enumerate(trades[-10:]):
        res = f" {t['result']}" if t['result'] else " ⏳"
        msg+=f"{i}: {t['date']} {t['dir'].upper()} {t['entry']}{res}\n"
    await u.message.reply_text(msg)

async def win(u,c):
    try:
        idx=int(c.args[0]);trades[idx]['result']="WIN";save(F_JOURNAL,trades)
        await u.message.reply_text(f"✅ Trade {idx} marqué WIN")
    except: await u.message.reply_text("/win 0 (numéro du trade)")

async def loss(u,c):
    try:
        idx=int(c.args[0]);trades[idx]['result']="LOSS";save(F_JOURNAL,trades)
        await u.message.reply_text(f"❌ Trade {idx} marqué LOSS")
    except: await u.message.reply_text("/loss 0")

async def stats(u,c):
    if not trades: await u.message.reply_text("Pas de trades"); return
    wins=len([t for t in trades if t['result']=="WIN"])
    losses=len([t for t in trades if t['result']=="LOSS"])
    total=wins+losses
    wr= round(wins/total*100,1) if total>0 else 0
    await u.message.reply_text(f"📈 STATS EURUSD\nTotal: {len(trades)} trades\nClôturés: {total}\nWIN: {wins} | LOSS: {losses}\nWinrate: {wr}%\n\nContinue, c'est comme ça qu'on s'améliore.")

async def job(c):
    if not zones: return
    try:
        p=get_price()
        for z in zones:
            if z['low']<=p<=z['high']:
                await c.bot.send_message(chat_id=CHAT_ID,text=f"🔥 EURUSD DANS OB! {p:.5f} Zone {z['low']}-{z['high']}")
    except: pass

def main():
    app=Application.builder().token(TOKEN).build()
    for cmd,fn in [("start",start),("setob",setob),("listob",listob),("clearob",clearob),("delob",delob),("risk",risk),("tp",tp),("trade",trade),("journal",journal),("win",win),("loss",loss),("stats",stats)]:
        app.add_handler(CommandHandler(cmd,fn))
    app.job_queue.run_repeating(job,interval=30,first=10,chat_id=CHAT_ID)
    app.run_polling()

if __name__=="__main__": main()-
