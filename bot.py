import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bem-vindo ao Bot Gratuito de Consultas!\n\n"
        "Comandos disponíveis:\n"
        "/cnpj <número>\n"
        "/cep <número>"
    )

# /cnpj - usa a API gratuita publica.cnpjs.dev
async def consulta_cnpj(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /cnpj 12345678000195")
        return
    cnpj = context.args[0]
    try:
        response = requests.get(f"https://publica.cnpjs.dev/cnpj/{cnpj}")
        if response.status_code == 200:
            dados = response.json()
            msg = (
                f"🏢 Empresa: {dados.get('razao_social', 'N/A')}\n"
                f"🔢 CNPJ: {cnpj}\n"
                f"📍 Endereço: {dados.get('descricao_logradouro', '')}, "
                f"{dados.get('numero', '')} - {dados.get('municipio', '')}/{dados.get('uf', '')}"
            )
        else:
            msg = f"Erro {response.status_code}: {response.text}"
    except Exception as e:
        msg = f"Erro inesperado: {e}"
    await update.message.reply_text(msg)

# /cep - usa API gratuita do ViaCEP
async def consulta_cep(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /cep 01001000")
        return
    cep = context.args[0]
    try:
        response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        if response.status_code == 200:
            dados = response.json()
            if 'erro' in dados:
                msg = "CEP não encontrado."
            else:
                msg = (
                    f"📍 Logradouro: {dados.get('logradouro')}\n"
                    f"🏙️ Bairro: {dados.get('bairro')}\n"
                    f"🗺️ Cidade: {dados.get('localidade')}/{dados.get('uf')}"
                )
        else:
            msg = f"Erro {response.status_code}: {response.text}"
    except Exception as e:
        msg = f"Erro inesperado: {e}"
    await update.message.reply_text(msg)


# Inicialização
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("cnpj", consulta_cnpj))
app.add_handler(CommandHandler("cep", consulta_cep))

app.run_polling()
