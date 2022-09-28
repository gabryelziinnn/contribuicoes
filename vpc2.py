import logging, os, boto3, json 
from botocore.exceptions import ClientError


logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

class comandos:
    def __init__(self,execucao):
        import subprocess
        self.execucao = execucao
        sp=subprocess.Popen(execucao,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
        self.rc=sp.wait()
        self.out,self.err=sp.communicate() 

tabela_de_rotas_id = comandos("sed -n '/rtb/p' output.txt")
subnet_id = comandos("sed -n '/subnet/p' output.txt")
internet_gateway_id = comandos("sed -n '/igw/p' output.txt")
id_vpc = comandos("sed -n '/vpc/p' output.txt")



ec2 = boto3.resource('ec2')
route_table = ec2.RouteTable(f'{tabela_de_rotas_id.out}') # Insira aqui o RouteTableId
vpc_resources = boto3.client("ec2")



route_table_association = route_table.associate_with_subnet(
    SubnetId = f'{subnet_id.out}' # insira aqui SubnetID
)


# # Atacha o IG a vpc
atachar = vpc_resources.attach_internet_gateway( 
    InternetGatewayId=f'{internet_gateway_id.out}', # Insira aqui o InternetGatewayId
    VpcId = f'{id_vpc.out}' # insira o VpcId
)

# Cria rota para acesso externo a internet | por algum motivo o sed nao funciona neste
#route = route_table.create_route(
#    DestinationCidrBlock = '0.0.0.0/0', # rota para acesso externo a internet
#    GatewayId = f'{internet_gateway_id.out}' # Aponte para o InternetGatewayId
#)

import security_group3