import logging, os, boto3 
from botocore.exceptions import ClientError

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

ec2 = boto3.client('ec2')

class chave_publica:
    def chave(self,nome,tipo):
        try:
            self.key = ec2.create_key_pair(
                KeyName= nome,    
                KeyType= tipo,
                TagSpecifications=[
                    {
                        'ResourceType': 'key-pair',
                        'Tags': [
                            {
                                'Key': 'Gabryel',
                                'Value': 'Empresa'
                            },
                        ]
                    },
                ],
                KeyFormat='pem'
            )
        except ClientError as erro:
            return f'Ocorreu um erro {self.key} na criação da chave'
        private_key_file=open('./chave_privada',"w") # Salva a chave privada em um arquivo no local
        private_key_file.write(self.key['KeyMaterial'])
        private_key_file.close

chave = chave_publica()

logger.info(f'Gerando chave, e inserindo as permissões corretas...')
chave.chave('gabryel','rsa') # Nome da chave e o tipo de chave
os.system('chmod 066 ./chave_privada')
logger.info(f'Chave gerada: \n {chave.key})')
