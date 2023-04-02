import variaveis
import pulumi_aws as aws

def vpc_asg(descricao):
    vpc = aws.ec2.Vpc(
        descricao,
        cidr_block="172.16.0.0/16",
        tags=variaveis.minhas_tags,
    )
    return vpc

def sub_rede_asg(descricao,associacao_vpc,rede,zona):
    subnet = aws.ec2.Subnet(
        descricao,
        vpc_id=associacao_vpc,
        availability_zone=zona,
        cidr_block=rede,
        tags=variaveis.minhas_tags,
        map_public_ip_on_launch=True,
    )
    return subnet

def gateway_asg(descricao,associacao_vpc):
    gw = aws.ec2.InternetGateway(descricao,
        vpc_id=associacao_vpc,
        tags=variaveis.minhas_tags
    )
    return gw

def tabela_rotas(descricao,associacao_vpc,associacao_gw):
    routing_table = aws.ec2.RouteTable(descricao,
        vpc_id=associacao_vpc,
        routes=[
            aws.ec2.RouteTableRouteArgs(
                cidr_block="0.0.0.0/0",
                gateway_id=associacao_gw,
            ),
        ],
        tags=variaveis.minhas_tags
    )
    return routing_table

def associacao_rb(descricao,associacao_sb,associacao_rb):
    route_table_assoc = aws.ec2.RouteTableAssociation(descricao,
        subnet_id=associacao_sb,
        route_table_id=associacao_rb,
    )
    return route_table_assoc

def grupo_seguranca(referencia,nome,descricao,associacao_vpc):
    security_group = aws.ec2.SecurityGroup(referencia,
                name=nome,
                description=descricao,
                vpc_id=associacao_vpc,
                ingress=[{
                        "protocol": "tcp",
                        "from_port": 80,
                        "to_port": 80,
                        "cidr_blocks": ["0.0.0.0/0"],
                    },
                {
                    "protocol": "tcp",
                    "from_port": 443,
                    "to_port": 443,
                    "cidr_blocks": ["0.0.0.0/0"],
                },
                {
                    "protocol": "udp",
                    "from_port": 51821,
                    "to_port": 51821,
                    "cidr_blocks": ["0.0.0.0/0"],
                },
                {
                    "protocol": "tcp",
                    "from_port": 6443,
                    "to_port": 6443,
                    "cidr_blocks": ["0.0.0.0/0"],
                },
                {
                    "protocol": "udp",
                    "from_port": 8472,
                    "to_port": 8472,
                    "cidr_blocks": ["0.0.0.0/0"],
                },
                {
                    "protocol": "udp",
                    "from_port": 10250,
                    "to_port": 10250,
                    "cidr_blocks": ["0.0.0.0/0"],
                },
                {
                    "protocol": "tcp",
                    "from_port": 3021,
                    "to_port": 3021,
                    "cidr_blocks": ["0.0.0.0/0"],
                },
                {
                    "protocol": "tcp",
                    "from_port": 3022,
                    "to_port": 3022,
                    "cidr_blocks": ["0.0.0.0/0"],
                },
                {
                    "protocol": "tcp",
                    "from_port": 3025,
                    "to_port": 3025,
                    "cidr_blocks": ["0.0.0.0/0"],
                },
                {
                    "protocol": "tcp",
                    "from_port": 3028,
                    "to_port": 3028,
                    "cidr_blocks": ["0.0.0.0/0"],
                },
                {
                    "protocol": "tcp",
                    "from_port": 22,
                    "to_port": 22,
                    "cidr_blocks": ["0.0.0.0/0"],
                }
                ],
                egress=[
                    {
                        "protocol": "-1",
                        "from_port": 0,
                        "to_port": 0,
                        "cidr_blocks": ["0.0.0.0/0"],
                    },
                    {
                        "protocol": "tcp",
                        "from_port": 22,
                        "to_port": 22,
                        "cidr_blocks": ["0.0.0.0/0"],
                    },
                    {
                        "protocol": "tcp",
                        "from_port": 2376,
                        "to_port": 2376,
                        "cidr_blocks": ["0.0.0.0/0"],
                    },
                    {
                        "protocol": "tcp",
                        "from_port": 6443,
                        "to_port": 6443,
                        "cidr_blocks": ["0.0.0.0/0"],
                    }
                ],
                tags=variaveis.minhas_tags,
            )
    return security_group

def rota(descricao,associacao_rb,associacao_gw):
    route = aws.ec2.Route(
        descricao,
        route_table_id=associacao_rb,
        destination_cidr_block="0.0.0.0/0",
        gateway_id=associacao_gw,
    )
    return route

'''Insira uma descricao nesta funcao para criar a vpc'''
cria_vpc_1 = vpc_asg("vpc-asg")

'''Insira uma descricao para as sub-redes que serão criadas, insira a ID que esta sub-rede estará, insira a faixa de IP, 
insira a zona de disponibilidade que a sub-rede estará'''
sub_rede_1 = sub_rede_asg("sug-rede-asg-1",cria_vpc_1.id,"172.16.10.0/24",variaveis.zona_disponibilidade1)
sub_rede_2 = sub_rede_asg("sug-rede-asg-2",cria_vpc_1.id,"172.16.20.0/24",variaveis.zona_disponibilidade2)

'''Insira uma descrição do gateway que será criado, insira a ID da vpc'''
gw_asg_1 = gateway_asg("asg-gw",cria_vpc_1.id)

'''Insira uma descrição do routing table que será criado, insira a ID da vpc, insira o ID do gateway'''
rb_1 = tabela_rotas("rb-asg",cria_vpc_1.id,gw_asg_1.id)

'''Insira uma descrição das associações para os routing table que serão criados, 
insira a ID das sub-redes que estarão, e a ID das routing tables'''
associa_rb_1 = associacao_rb("associacairb1",sub_rede_1.id,rb_1.id)
associa_rb_1 = associacao_rb("associacairb2",sub_rede_2.id,rb_1.id)

'''Insira uma descrição para o grupo de segurança para o ASG, o nome do mesmo,
uma descrição(esta aparecerá no console da AWS), e a ID da VPC'''
sg_1 = grupo_seguranca("sg-asg","teleport_k3s","Regras de seguranca para k3s e Teleport",cria_vpc_1.id)

'''Insira uma descrição para criar uma EC2 route, ID da RB, ID do gateway'''
rota_1 = rota("rota-para-asg",rb_1.id,gw_asg_1.id)