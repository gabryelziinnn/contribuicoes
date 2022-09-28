import logging, os, boto3, json 
from botocore.exceptions import ClientError


logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

ec2 = boto3.resource('ec2')
vpc_resources = boto3.client("ec2")

# Cria uma vpc
class recursos: 
    def main(self,vpc_name,ig_name,route_table_name,subnet_name,cidr_vpc,cidr_subnet):
        try:
            self.vpc = ec2.create_vpc(
                CidrBlock=cidr_vpc,
                TagSpecifications=[
                    {
                        'ResourceType': 'vpc',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': vpc_name
                            },
                        ]
                    },
                ]
            )
            logger.info('Criando a vpc...')
            logger.info(f'VPC criada: {self.vpc.id}')

            # Cria o internet gateway
            self.ig = vpc_resources.create_internet_gateway(
                TagSpecifications=[
                    {
                        'ResourceType': 'internet-gateway',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': ig_name
                            },
                        ]
                    },
                ],
            )
            logger.info('Cria o gateway de internet...')
            logger.info(f'Gateway criado: {json.dumps(self.ig, indent=4)}')


            # Cria route table e uma rota publica para o IG
            self.route_table = vpc_resources.create_route_table(
                VpcId = self.vpc.id, 
                TagSpecifications=[
                    {
                        'ResourceType': 'route-table',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': route_table_name
                            },
                        ]
                    },
                ]
            )
            logger.info('Criando a routing table...')
            logger.info(f'Routing table criada: {json.dumps(self.route_table, indent=4)}')

            # Cria uma subnet
            self.subnet = vpc_resources.create_subnet(
                #AvailabilityZone='string',
                #AvailabilityZoneId='string',
                CidrBlock=cidr_subnet, # Deve estar numa rede diferente da VPC
                VpcId = self.vpc.id, # ID da VPC
                TagSpecifications=[
                    {
                        'ResourceType': 'subnet',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': subnet_name
                            },
                        ]
                    },
                ]                            
            )
            logger.info('Criando subnet...')
            logger.info(f'Subnet criada: {json.dumps(self.subnet, indent=4)}')
        except ClientError as erro:
            logger.exception(f"Não foi possível criar a vpc e seus recursos devido ao erro:{erro}")
    def exibir(self):
        print(f'exibe a info: {self.subnet}')

vpc_recursos = recursos()

# Insira respectivamente: 
# nome da vpc, nome do internet gateway, nome da route table, nome da subnet, cidr da vpc, cidr da subnet
if __name__ == "__main__":
    vpc_recursos.main('gab_vpc','gateway_gab','table_gab','subnet_gab','10.0.0.0/16','10.0.1.0/16')
    
    # Insere todo o conteudo que foi criado para um arquivo de texto
    conteudo1 = [json.dumps(vpc_recursos.subnet, indent=4),json.dumps(vpc_recursos.route_table, indent=4),json.dumps(vpc_recursos.ig, indent=4)]
    arquivo = open('info.txt','a') 
    for cada_linha in conteudo1: 
        arquivo.write(cada_linha + '\n')
    arquivo.close()
    
    # Insere o ID da VPC em um arquivo separado
    conteudo2=open('vpc_id.txt','w')
    conteudo2.write(vpc_recursos.vpc.id)
    conteudo2.close()

os.system('./atualiza.sh')

# Realiza os attach
import vpc2