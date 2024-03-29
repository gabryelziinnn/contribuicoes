<<<<<<< HEAD
import logging
import nmap
import telebot
import ipaddress
from dotenv import load_dotenv
import os
=======
import os, telebot, logging, nmap
from dotenv import load_dotenv

>>>>>>> origin/telegram_bot

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = telebot.TeleBot(BOT_TOKEN)

nm = nmap.PortScanner()

<<<<<<< HEAD
# Define o intervalo de IPs a serem escaneados
ip_range = ipaddress.IPv4Network('192.168.23.0/24')
portas = '22-443'

# Percorre a lista de IPs e realiza o scan de portas
for alvo in ip_range:
    nm.scan(str(alvo), portas)

    # Verifica se há alguma porta aberta
    try:
        threats = []
        for porta in nm[str(alvo)]['tcp']:
            if nm[str(alvo)]['tcp'][porta]['state'] == 'open':
                vulneraveis = threats.append(f'{porta}')

        if threats == []:
            message = (f'Não foram encontradas possíveis ameaças no host {alvo}.')
        else:
            message = (f'Atenção: foram encontradas possíveis ameaças no host {alvo}! Portas abertas: {", ".join(threats)}')
        bot.send_message(chat_id=CHAT_ID, text=message)
    except telebot.apihelper.ApiTelegramException as erro_tele:
        message = (f'Houve algum erro com a API do telegram: {erro_tele}')
        bot.send_message(chat_id=CHAT_ID, text=message)
    except nmap.nmap.PortScannerError as erro_nmap:
        message = (f'Houve algum problema com o nmap: {erro_nmap}')
        bot.send_message(chat_id=CHAT_ID, text=message)
    except KeyError as erro_key:
        message = (f'Os hosts definidos não são válidos!')
        bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as erro:
        message = (f'Houve um erro não identificado: {erro}')
        bot.send_message(chat_id=CHAT_ID, text=message)
=======
alvos = ['192.168.1.107', '192.168.1.104']
portas = '22-443'

try:
    for alvo in alvos:
        nm.scan(alvo, portas)
        open_ports = [int(porta) for porta in nm[alvo]['tcp'] if nm[alvo]['tcp'][porta]['state'] == 'open']

        if open_ports == []:
            message = (f'Não foram encontradas possíveis ameaças no host {alvo}.')
        else:
            message = (f'Atenção: foram encontradas possíveis ameaças no host {alvo}! Portas abertas: {", ".join(map(str, open_ports))}')
        bot.send_message(chat_id=CHAT_ID, text=message)
except telebot.apihelper.ApiTelegramException as erro_tele:
    message = (f'Houve algum erro com a API do telegram: {erro_tele}')
    bot.send_message(chat_id=CHAT_ID, text=message)
except nmap.nmap.PortScannerError as erro_nmap:
    message = (f'Houve algum problema com o nmap: {erro_nmap}')
    bot.send_message(chat_id=CHAT_ID, text=message)
except KeyError as erro_key:
    message = (f'Os hosts definidos não são válidos!')
    bot.send_message(chat_id=CHAT_ID, text=message)
except Exception as erro:
    message = (f'Houve algum erro no script: {erro}')
    bot.send_message(chat_id=CHAT_ID, text=message)
>>>>>>> origin/telegram_bot
