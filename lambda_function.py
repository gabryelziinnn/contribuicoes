import webhook_cert, ssl

VALIDACOES = webhook_cert.validate_ssl_certificates(webhook_cert.sites)


def lambda_handler(event, context):
    try:
        for result in VALIDACOES:
            if result['valid']:
                print(f"Os certificados: {result['url']} são válidos por 11 dias ou mais.")
            elif not result['valid'] and result['days_left'] == 10:
                webhook_cert.enviar_email(f'Os certificados: https://{result["url"]} somente serão válidos por: {result["days_left"]}, renove-os!','Expiração de certificados')
                webhook_cert.discord_mensagem(f'O certificado: https://{result["url"]} somente é válido por {result["days_left"]}','Certificado acabando a validade!','Atenção para renovação dos certificados!')
            else:
                webhook_cert.discord_mensagem(f'O certificado: https://{result["url"]} somente é válido por {result["days_left"]}','Certificado acabando a validade!','Atenção para renovação dos certificados!')

    except ssl.SSLCertVerificationError as validacao_falha:
        webhook_cert.discord_mensagem(f'Houve um problema: {validacao_falha}(talvez nao seja mais válido)','Problemas nos certificados','erros dos certificados')
    except ssl.SSLError as ssl_erro:
        webhook_cert.discord_mensagem(f'Houve um problema: {ssl_erro}!','Problemas nos certificado','erros dos certificados')
    except Exception as problema_desconhecido:
        webhook_cert.discord_mensagem(f'Houve algum problema desconhecido: {problema_desconhecido}!','Problemas no script','Vá verificar!')
