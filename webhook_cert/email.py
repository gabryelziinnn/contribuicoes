import smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from dotenv import load_dotenv

load_dotenv()
SENHA = os.getenv('PASSWORD')
SENDER = seu email
RECEIVERS = [emails a enviar]


'''Email configurations'''
def enviar_email(corpo_email,titulo):
  subject = titulo
  caminho_foto = escolha o caminho de uma foto qualquer
  body = f"""
  <html>
    <head></head>
    <body>
      <p><strong>Chamados do Let's Encrypt!</strong></p>
      <p>{corpo_email}</p>
      <p><img src="cid:image1"></p>
    </body>
  </html>
  """
  msg = MIMEMultipart()
  msg['From'] = SENDER
  msg['To'] = ', '.join(RECEIVERS)
  msg['Subject'] = subject

  '''Adiciona o corpo e a imagem ao email'''
  msg.attach(MIMEText(body, 'html'))
  # if you want a photo, just point the path here.
  # with open(caminho_foto, 'rb') as f:
  #     img_data = f.read()
  # img = MIMEImage(img_data, name='python.png')
  # img.add_header('Content-ID', '<image1>')
  # msg.attach(img)


  '''Configurações do email'''
  server = smtplib.SMTP('smtp.zoho.com', 587)
  server.starttls()
  server.login(SENDER, SENHA)

  '''Envio de mensagens'''
  text = msg.as_string()
  server.sendmail(SENDER, RECEIVERS, text)
  server.quit()