import os
import telebot
import logging
import nmap
import asyncio
from dotenv import load_dotenv

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = telebot.TeleBot(BOT_TOKEN)

async def scan_host(nm, alvo, portas):
    nm.scan(alvo, portas)
    open_ports = [int(porta) for porta in nm[alvo]['tcp'] if nm[alvo]['tcp'][porta]['state'] == 'open']
    if open_ports == []:
        message = (f'Não foram encontradas possíveis ameaças no host {alvo}.')
    else:
        message = (f'Atenção: foram encontradas possíveis ameaças no host {alvo}! Portas abertas: {", ".join(map(str, open_ports))}')
    await bot.send_message(chat_id=CHAT_ID, text=message)

async def main():
    nm = nmap.PortScanner()
    alvos = ['192.168.1.107', '192.168.1.104'] # A list of hosts to scan
    portas = '22-443'
    tasks = []
    for alvo in alvos:
        task = asyncio.create_task(scan_host(nm, alvo, portas))
        tasks.append(task)
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())