import logging, boto3, json
from botocore.exceptions import ClientError

class comandos:
    def __init__(self,execucao):
        import subprocess
        self.execucao = execucao
        sp=subprocess.Popen(execucao,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
        self.rc=sp.wait()
        self.out,self.err=sp.communicate() 

id_vpc = comandos("sed -n '/vpc/p' output.txt")


# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

vpc_resource = boto3.resource("ec2")

class seguranca:
        def __init__(self,descricao, groupname, vpc_id):
            try:
                self.descricao = descricao
                self.groupname = groupname
                self.vpc_id = vpc_id
                self.security_group = vpc_resource.create_security_group(
                    Description=descricao,
                    GroupName=groupname,
                    VpcId=vpc_id,
                    TagSpecifications=[
                        {
                            'ResourceType': 'security-group',
                            'Tags': [
                                {
                                    'Key': 'Name',
                                    'Value': 'sg_gabryel'
                                },
                            ]
                        },
                    ],
                )
            except ClientError:
                logger.exception(f'Não pode ser criado o grupo de seguranca: {self.groupname}')
                raise


logger.info(f'Criando grupo de segurança...')
grupo_de_seguranca = seguranca('Grupo de seguranca do Gab', 'Grupo Gab', id_vpc.out)
logger.info(f'Grupo de segurança criado: {grupo_de_seguranca.security_group.id}')

# Insere o ID do SG em um arquivo separado
conteudo2=open('sg_id.txt','w')
conteudo2.write(grupo_de_seguranca.security_group.id)
conteudo2.close()

import ingress_rule4