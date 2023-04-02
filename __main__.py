import variaveis, pulumi
import pulumi_aws as aws

get_ami = aws.ec2.get_ami_ids(filters=[aws.ec2.GetAmiIdsFilterArgs(
        name="description",
        values=["Canonical, Ubuntu, 22.04 LTS, amd64 jammy image build on 2022-12-06"],
    )],
    owners=["amazon"]
)

launch_template = aws.ec2.LaunchTemplate(
    "template-gab-for-asg",
    block_device_mappings=[aws.ec2.LaunchTemplateBlockDeviceMappingArgs(
        device_name="/dev/sda1",
        ebs=aws.ec2.LaunchTemplateBlockDeviceMappingEbsArgs(
            volume_size=50, # em GB
            delete_on_termination=True,
            iops=3000, # para volumes io1/io2/gp3
            throughput=125, # velocidade do volume em MB/s
            volume_type='gp3',
        ),
    )],
    capacity_reservation_specification=aws.ec2.LaunchTemplateCapacityReservationSpecificationArgs(
        capacity_reservation_preference="none",
    ),
    credit_specification=aws.ec2.LaunchTemplateCreditSpecificationArgs(
        cpu_credits="unlimited",
    ),
    disable_api_stop=False,
    disable_api_termination=False,
    ebs_optimized="false",
    image_id=get_ami.ids[0],
    instance_initiated_shutdown_behavior="terminate",
    instance_market_options=aws.ec2.LaunchTemplateInstanceMarketOptionsArgs(
        market_type="spot", # Utiliza instancias spot
    ),
    instance_type="t2.medium",
    key_name=variaveis.nome_da_chave, # Esta chave deve existir em sua cloud
    monitoring=aws.ec2.LaunchTemplateMonitoringArgs(
        enabled=False,
    ),
    network_interfaces=[aws.ec2.LaunchTemplateNetworkInterfaceArgs(
        associate_public_ip_address="true",
        delete_on_termination="true",
        description="nic-for-asgs",
        security_groups=[variaveis.sg_1.id],
        subnet_id=variaveis.sub_rede_1.id,
    )],
    placement=aws.ec2.LaunchTemplatePlacementArgs(
        availability_zone=variaveis.zona_disponibilidade1,
    ),
    tag_specifications=[aws.ec2.LaunchTemplateTagSpecificationArgs(
        resource_type="instance",
        tags=variaveis.minhas_tags,
    )],
)



asg = aws.autoscaling.Group(
    "asg-teleport",
    capacity_rebalance=True,
    name='asg-teleport-k3s',
    desired_capacity=3,
    max_size=10,
    min_size=2,
    health_check_grace_period=300, # em segundos
    health_check_type="ELB",
    vpc_zone_identifiers=[
        variaveis.sub_rede_1.id,
    ],
    launch_template=aws.autoscaling.GroupLaunchTemplateArgs(
        id=launch_template.id,
        version="$Latest",
    ))


target_group = aws.lb.TargetGroup('alvo-asg',
    target_type="alb",                                  
    port=80,
    protocol='TCP',
    vpc_id=variaveis.cria_vpc_1.id,
    tags=variaveis.minhas_tags,
)

# create a new ALB
alb = aws.lb.LoadBalancer('alb-asg',
    name="alb-asg-teleport",
    internal=False,
    load_balancer_type='application', # application, gateway, or network
    security_groups=[variaveis.sg_1.id],
    enable_deletion_protection=False,
    subnets=[variaveis.sub_rede_1.id,variaveis.sub_rede_2.id],
    tags=variaveis.minhas_tags,
)

# redireciona para pagina movida caso tente na porta 80
listener = aws.lb.Listener("redirecionador-lb",
    load_balancer_arn=alb.arn,
    tags=variaveis.minhas_tags,
    port=80,
    protocol="HTTP",
    default_actions=[aws.lb.ListenerDefaultActionArgs(
        type="redirect",
        redirect=aws.lb.ListenerDefaultActionRedirectArgs(
            port="443",
            protocol="HTTPS",
            path="/",
            status_code="HTTP_301",
        ),
    )])


# export the ALB endpoint URL
pulumi.export('alb_url', alb.dns_name)