import logging, boto3, json, os
from botocore.exceptions import ClientError

class comandos:
    def __init__(self,execucao):
        import subprocess
        self.execucao = execucao
        sp=subprocess.Popen(execucao,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
        self.rc=sp.wait()
        self.out,self.err=sp.communicate() 
# Insere a ID do grupo de segurança criada anteriormente
security_group_id = comandos("sed -n '/sg/p' sg_id.txt")


# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

vpc_client = boto3.client("ec2")


class ingress:
        def __init__(self):
            """
            Cria as regras abaixo no grupo de segurança criado anteriormente
            """
            try:
                self.regras = vpc_client.authorize_security_group_ingress(
                    GroupId=security_group_id.out,
                    IpPermissions=[{
                        'IpProtocol': 'tcp',
                        'FromPort': 80,
                        'ToPort': 80,
                        'IpRanges': [{
                            'CidrIp': '0.0.0.0/0'
                        }]
                    }, {
                        'IpProtocol': 'tcp',
                        'FromPort': 22,
                        'ToPort': 22,
                        'IpRanges': [{
                            'CidrIp': '0.0.0.0/0'
                        }]
                    }])
            except ClientError:
                logger.exception('Regra de ingresso não criada.')
                raise




logger.info(f'Criando as regras de ingress definidas...')
regras_ingress = ingress()
logger.info(f'Regras de ingress criadas: \n{json.dumps(regras_ingress.regras, indent=4)}')

import ec2