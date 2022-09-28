# Documentação oficial utilizada:

Criação de uma VPC:

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_vpc

Criação de um internet gateway:

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.create_internet_gateway

Atachar o gateway a vpc:

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.attach_internet_gateway

Criar uma routing table:

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_route_table

Cria uma rota:

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.create_route

Cria uma subnet:

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.create_subnet

Associação com a subnet:

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.RouteTable.associate_with_subnet

# Acesso a máquina:

ssh -o "IdentitiesOnly=yes" -i my_key ec2-user@54.87.202.110
