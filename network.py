import variaveis
from pulumi_aws import ec2

vpc = ec2.Vpc("vpc",
  cidr_block="10.0.0.0/16")

subnet_public = ec2.Subnet("subnet_public",
  vpc_id=vpc.id,
  availability_zone=variaveis.ZONES[0],
  map_public_ip_on_launch=True,
  cidr_block="10.0.1.0/24")

subnet_private = ec2.Subnet("subnet_private",
  vpc_id=vpc.id,
  availability_zone=variaveis.ZONES[1],
  map_public_ip_on_launch=False,
  cidr_block="10.0.2.0/24")

igw = ec2.InternetGateway(
    'vpc-ig',
    vpc_id=vpc.id,
    tags={
        'Name': 'pulumi-vpc-ig',
    },
)


rtb = ec2.RouteTable("RoutingTable",
    vpc_id=vpc.id,
    routes=[
        ec2.RouteTableRouteArgs(
            cidr_block='0.0.0.0/0',
            gateway_id=igw.id,
        ),
    ],
    tags={
        'Name': 'pulumi-vpc-rt',
    })

def rtb_assoc(name,id_sub,rtb_id):
  route_table_assoc = ec2.RouteTableAssociation(name,
      subnet_id=id_sub,
      route_table_id=rtb_id,
  )
  return route_table_assoc
assoc_1 = rtb_assoc('routingtable1',subnet_public.id,rtb.id)
assoc_2 = rtb_assoc('routingtable2',subnet_private.id,rtb.id)