import os
from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv

load_dotenv()
URL_DISCORD = os.getenv('WEBHOOK_URL')

def discord_mensagem(mensagem,titulo,descricao):
    webhook = DiscordWebhook(
        url=URL_DISCORD, 
        content=mensagem,
    )
    embed = DiscordEmbed(
        title=titulo, 
        description=descricao, 
        color='03b2f8'
    )
    embed.set_author(name='Gabryel Bento')
    webhook.add_embed(embed)
    response = webhook.execute()
    return response, webhook, embed