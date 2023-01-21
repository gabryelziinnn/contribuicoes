import pulumi, variaveis, logging
import pulumi_command as command
import pulumi_aws as aws

log = logging.getLogger(__name__)
# def refresh_stack(stackd):
#     try:
#         log.info("Refreshing stack...")
#         stackd.refresh(on_output=print)
#         log.info("Successfully refreshed stack")
#     except Exception as e:
#         log.error("Failure when trying to refresh stack:")
#         raise e







vpc = aws.ec2.Vpc(
    "vpc-instancia-teste",
    cidr_block="172.16.0.0/16",
    tags=variaveis.minhas_tags,
)

subnet = aws.ec2.Subnet(
    "subnet-gabryel",
    vpc_id=vpc.id,
    availability_zone=variaveis.zona_de_disponibilidade,
    cidr_block="172.16.10.0/24",
    tags=variaveis.minhas_tags,
    map_public_ip_on_launch=True,
)

gw = aws.ec2.InternetGateway("ig-gateway",
    vpc_id=vpc.id,
    tags=variaveis.minhas_tags
)

routing_table = aws.ec2.RouteTable("routing-table",
    vpc_id=vpc.id,
    routes=[
        aws.ec2.RouteTableRouteArgs(
            cidr_block="0.0.0.0/0",
            gateway_id=gw.id,
        ),
    ],
    tags=variaveis.minhas_tags
)

security_group = aws.ec2.SecurityGroup('Liberacoes de portas',
            name='Liberacoes',
            description='Liberacoes de varias portas',
            vpc_id=vpc.id,
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

interface_de_rede = aws.ec2.NetworkInterface(
    "ni-gab",
    subnet_id=subnet.id,
    private_ips=["172.16.10.100"],
    tags=variaveis.minhas_tags,
    description='Interface de rede para ec2',
)

# Adquire o AMI da aws baseado na descrição da imagem
adquire_ami = aws.ec2.get_ami_ids(filters=[aws.ec2.GetAmiIdsFilterArgs(
        name="description",
        values=["Canonical, Ubuntu, 22.04 LTS, amd64 jammy image build on 2022-12-06"],
    )],
    owners=["amazon"]
)

# Insere o usuário do UBUNTU na lista de sudoers sem password (não esqueça de deletar este usuário)
user_data = f"""
!/bin/bash
sed -i '/User privilege specification/i ubuntu ALL=(ALL) NOPASSWD:ALL' /etc/sudoers
"""

'''Instância, triplicada'''
def instancias(nome,tipo_instancia,volume_root):
    instancia_aws = aws.ec2.Instance(
    nome,
    ami=adquire_ami.ids[0],
    vpc_security_group_ids = [security_group.id],
    subnet_id = subnet.id,
    key_name = variaveis.nome_da_chave,
    associate_public_ip_address = True,
    availability_zone=variaveis.zona_de_disponibilidade,
    instance_type=tipo_instancia,
    credit_specification=aws.ec2.InstanceCreditSpecificationArgs(
    cpu_credits="unlimited",
),
    root_block_device=aws.ec2.InstanceRootBlockDeviceArgs(
    delete_on_termination=True,
    volume_size=volume_root,
    volume_type='gp3',
))
    return instancia_aws

instancia_1 = instancias("instancia_1","t2.xlarge",50)
instancia_2 = instancias("instancia_2","t2.xlarge",50)
instancia_3 = instancias("instancia_3","t2.xlarge",50)
instancia_4 = instancias("instancia_4","t2.xlarge",50)
instancia_5 = instancias("instancia_5","t2.xlarge",50)
instancia_6 = instancias("instancia_6","t2.xlarge",50)

public_ips = [
    instancia_1.public_ip, 
    instancia_2.public_ip, 
    instancia_3.public_ip,
    instancia_4.public_ip,
    instancia_5.public_ip,
    instancia_6.public_ip,
]

# Envia o IP FIXO para nossas máquinas
ip_fixo_1 = aws.ec2.Eip("k3s_cluster_master", instance=instancia_1.id)
ip_fixo_2 = aws.ec2.Eip("k3s_cluster_master_2", instance=instancia_2.id)
ip_fixo_3 = aws.ec2.Eip("k3s_cluster_master_3", instance=instancia_3.id)
ip_fixo_4 = aws.ec2.Eip("k3s_cluster_node_1", instance=instancia_4.id)
ip_fixo_5 = aws.ec2.Eip("k3s_cluster_node_2", instance=instancia_5.id)
ip_fixo_6 = aws.ec2.Eip("k3s_cluster_node_3", instance=instancia_6.id)


'''Associações'''
vpc_endpoint = aws.ec2.VpcEndpoint("ec2",
    vpc_id=vpc.id,
    ip_address_type='ipv4',
    service_name="com.amazonaws.us-east-1.ec2",
    vpc_endpoint_type="Interface",
    security_group_ids=[security_group.id],
)

sn_ec2 = aws.ec2.VpcEndpointSubnetAssociation(
    "associacao_vpc_subnet",
    vpc_endpoint_id=vpc_endpoint.id,
    subnet_id=subnet.id
)

sg_ec2 = aws.ec2.SecurityGroupAssociation(
    "associa_sg",
    vpc_endpoint_id=vpc_endpoint.id,
    security_group_id=security_group.id
)

route_table_assoc = aws.ec2.RouteTableAssociation("routeTableAssociation",
    subnet_id=subnet.id,
    route_table_id=routing_table.id,
)

# Realiza o export dos IPS das máquinas
exporta_ips = pulumi.export('ips das maquinas', public_ips)


# Renderiza o inventário, somente após o ip ser conhecido
render_playbook_inventory = command.local.Command("renderiza_inventario_playbook",
    create="cat inventory.conf | envsubst > inventario",
    environment={
        "EC2_IP_1": instancia_1.public_ip,
        "EC2_IP_2": instancia_1.public_ip,
        "EC2_IP_3": instancia_1.public_ip,
        "EC2_IP_4": instancia_1.public_ip,
        "EC2_IP_5": instancia_1.public_ip,
        "EC2_IP_6": instancia_1.public_ip,
})

# Define o primeiro servidor como master
render_playbook_all = command.local.Command("renderiza_arquivo_all",
    create="cat ./group_vars/all | envsubst > ./group_vars/all.yml",
    environment={
        "EC2_MASTER": instancia_1.public_ip,
})