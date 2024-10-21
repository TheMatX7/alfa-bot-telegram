import requests
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler


# Stan, w którym bot oczekuje na adres IP
IP_ADDRESS = 1

# Funkcja startowa
async def start(update: Update, context):
    await update.message.reply_text('Cześć! Jestem Alfa robot h^k3RSKI. Pomogę ci, ale pamiętaj używaj mnie z głową.')

# Funkcja dla komendy /ip
async def ip(update: Update, context):
    ip = ' '.join(context.args)  # Odczytujemy IP, które użytkownik podał po komendzie
    if not ip:
        await update.message.reply_text("Proszę podaj adres IP w formacie: /ip <adres_ip>")
        return
    
    try:
        # Używamy ipinfo.io do pobrania danych o IP
        response = requests.get(f'http://ipinfo.io/{ip}/json')
        data = response.json()

        if response.status_code == 200:
            info = f"Informacje o IP {ip}:\n"
            info += f"IP: {data.get('ip', 'Brak informacji')}\n"
            info += f"Miasto: {data.get('city', 'Brak informacji')}\n"
            info += f"Kraj: {data.get('country', 'Brak informacji')}\n"
            info += f"Region: {data.get('region', 'Brak informacji')}\n"
            info += f"Organizacja: {data.get('org', 'Brak informacji')}\n"
            info += f"Typ połączenia (hostname): {data.get('hostname', 'Brak informacji')}\n"
            info += f"Strefa czasowa: {data.get('timezone', 'Brak informacji')}\n"
            info += f"Szerokość geograficzna: {data.get('loc', 'Brak informacji').split(',')[0]}\n"
            info += f"Długość geograficzna: {data.get('loc', 'Brak informacji').split(',')[1]}\n"
            
            # Dodatkowe informacje o ISP
            isp_info = f"ISP: {data.get('org', 'Brak informacji')}\n"
            await update.message.reply_text(info + isp_info)
        else:
            await update.message.reply_text(f"Nie udało się pobrać danych dla adresu IP {ip}.")
    
    except Exception as e:
        await update.message.reply_text(f"Coś poszło nie tak: {e}")




async def help_info(update: Update, context):
    info = """
    /start - podstawowa komenda startowa
    /ip - pokaz informacje o ip (/ip xxx.xxx.xx.xx)
    """
    await update.message.reply_text(info)

# Funkcja, która odpowiada na wiadomości tekstowe
async def echo(update: Update, context):
    await update.message.reply_text(update.message.text)

# Główna funkcja
def main():
    # Twój token od BotFather
    TOKEN = '7364368147:AAGi0xYKqLxeDIuhmRo_VgbOqerqyY2wWSw'
    
    # Tworzenie obiektu Application
    application = Application.builder().token(TOKEN).build()
    
    # Dodanie obsługi komendy /start
    application.add_handler(CommandHandler('start', start))
    
    # Dodanie obsługi wszystkich innych wiadomości (echowanie wiadomości)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Dodanie komend informatycznych
    application.add_handler(CommandHandler('help', help_info))
    application.add_handler(CommandHandler('ip', ip))
    
    # Uruchomienie bota
    application.run_polling()

if __name__ == '__main__':
    main()
