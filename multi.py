import os
import telebot
import logging
import nmap
from dotenv import load_dotenv
from multiprocessing import Pool

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = telebot.TeleBot(BOT_TOKEN)

nm = nmap.PortScanner()

alvos = ['192.168.1.107', '192.168.1.104'] # A list of hosts to scan
portas = '22-443'

def scan_host(alvo):
    nm.scan(alvo, portas)

    try:
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

if __name__ == '__main__':
    with Pool(processes=len(alvos)) as pool:
        pool.map(scan_host, alvos)