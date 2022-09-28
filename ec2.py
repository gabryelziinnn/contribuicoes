import logging, os, boto3, datetime, json
from botocore.exceptions import ClientError

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

class ids:
    def __init__(self,execucao):
        import subprocess
        self.execucao = execucao
        sp=subprocess.Popen(execucao,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
        self.rc=sp.wait()
        self.out,self.err=sp.communicate() 
# Insere a ID do grupo de segurança criada anteriormente
security_group_id = ids("sed -n '/sg/p' sg_id.txt")
subnet_id = ids("sed -n '/subnet/p' output.txt")
id_vpc = ids("sed -n '/vpc/p' output.txt")

ec2 = boto3.resource('ec2')

class maquinas:
    def __init__(self):
        self.instance = ec2.create_instances(
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/sdc', 
                    'VirtualName': 'ephemeral0',
                    'Ebs': {
                        'DeleteOnTermination': True, 
                        'Iops': 3000, 
                        'VolumeSize': 50, # Tamanho do disco em gigabytes
                        'VolumeType': 'gp3', 
                        #'KmsKeyId': 'string', # utilizado em encriptações de disco
                        #'Throughput': 123, # inválido para volumes gp3
                        #'OutpostArn': 'string', # necessário somente para snapshots
                        'Encrypted': False 
                    },
                },
            ],
            ImageId='ami-026b57f3c383c2eec',
            InstanceType='t2.micro',
            KeyName='gabryel', # APONTE PARA UMA CHAVE JÁ CRIADA
            MaxCount=1, # número máximo de instância a subir
            MinCount=1, # número mínimo de instância a subir
            Monitoring={
                'Enabled': False # monitoramento da instancia
            },
            #Placement={
            #    'AvailabilityZone': 'us-east-1a', # Lista de zonas disponíveis
            #    'Tenancy': 'default'
            #},
            UserData='apt update -y && apt upgrade -y', # script de inicialização
            EbsOptimized=False, 
            #IamInstanceProfile={
            #    'Arn': 'string',   # Opcional
            #    'Name': 'string'
            #},
            NetworkInterfaces=[
                {
                    'AssociatePublicIpAddress': True,
                    'SubnetId' : subnet_id.out,
                    'DeleteOnTermination': True,
                    'Description': 'maquina para testes de acesso',
                    'DeviceIndex': 0,
                    'Groups': [
                        security_group_id.out,
                    ],
                },
            ],
            #ElasticInferenceAccelerators=[
            #    {
            #        'Type': 'string',
            #        'Count': 123
            #    },
            #],
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'gabryel-maquina'
                        },
                    ]
                },
            ],
            CreditSpecification={
                'CpuCredits': 'standard'
            },
            #CpuOptions={
            #    'CoreCount': 4,
            #    'ThreadsPerCore': 2 # habilita multithreading (1 desabilita multithreading)
            #},
            #PrivateDnsNameOptions={
            #    'HostnameType': 'ip-name'|'resource-name',
            #    'EnableResourceNameDnsARecord': True|False,
            #    'EnableResourceNameDnsAAAARecord': True|False
            #},
        )


logger.info('Criando serviço EC2...')
criacao = maquinas()
logger.info(f'Servico ec2 criado: \n{criacao.instance}')

# limpa os arquivos de config deste script, para permitir a criação de novas regras
os.system('rm -rf *.txt')


#ssh -o "IdentitiesOnly=yes" -i my_key ec2-user@54.87.202.110