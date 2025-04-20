import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "https://api.arcadiancenter.com/token/20e8019d-7165-48a9-aac1-63063c71f727/CpfData/"

# Consulta de CPF
async def consulta_cpf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /cpf 12345678900")
        return
    cpf = context.args[0]
    try:
        response = requests.get(f"https://api.arcadiancenter.com/token/20e8019d-7165-48a9-aac1-63063c71f727/CpfData/", headers={
            "Authorization": "Bearer SEU_TOKEN_API"
        })
        if response.status_code == 200:
            dados = response.json()
            msg = (
                f"👤 Nome: {dados.get('nome')}"
                f"🔢 CPF: {cpf}"
                f"📍 Endereço: {dados.get('endereco', 'N/A')}"
            )
        else:
            msg = f"Erro {response.status_code}: {response.text}"
    except Exception as e:
        msg = f"Erro inesperado: {e}"
    await update.message.reply_text(msg)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bem-vindo! Use /cpf <número> para consultar.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("cpf", consulta_cpf))
app.run_polling()
