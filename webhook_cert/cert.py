import ssl, socket
from datetime import datetime
from pytz import timezone

FORMATO = '%b %d %H:%M:%S %Y %Z'
HORA_ATUAL = datetime.now(timezone('America/Fortaleza'))

def validate_ssl_certificates(urls):
    results = []
    for url in urls:
        '''Divide a URL entre site e PORTA'''
        parts = url.split(':')
        if len(parts) == 1:
            hostname, port = parts[0], 443
        else:
            hostname, port = parts[0], int(parts[1])
        
        '''Realiza a conexão SSH e adquire o certificado'''
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        '''Realiza a comparação da data de expiração do cert com a data de hoje'''
        expiration_date = datetime.strptime(cert['notAfter'], FORMATO).replace(tzinfo=timezone('UTC'))


        '''Cria a variável com a data de expiração'''
        days_left = (expiration_date - HORA_ATUAL).days
        is_valid = days_left >= 11

        '''Realiza o append dos dados em um dic para acesso fora da função'''
        results.append({
            'url': url,
            'subject': cert['subject'],
            'issuer': cert['issuer'],
            'not_before': cert['notBefore'],
            'not_after': cert['notAfter'],
            'days_left': days_left,
            'valid': is_valid
        })
    return results