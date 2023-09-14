import pulumi, variaveis, iam, network
import pulumi_eks as eks

'''------------------------EKS CLUSTER-------------------------'''
eks_cluster = eks.Cluster("cluster",
  name='eks-cluster-gab',
  vpc_id=network.vpc.id,
  version=variaveis.KUBERNETES_VERSION,
  public_subnet_ids=[network.subnet_public.id],
  skip_default_node_group=True,
  instance_roles=[iam.role],
  private_subnet_ids=[network.subnet_private.id],
  tags=variaveis.LABELS
)

managed_node_groups = eks.ManagedNodeGroup("NodeGroups",
  cluster=eks_cluster,
  capacity_type='SPOT', # ON_DEMAND, SPOT
  node_group_name='node-groups-gab',
  subnet_ids=[network.subnet_public.id],
  version=variaveis.KUBERNETES_VERSION,
  disk_size=20,
  node_role_arn=iam.role.arn,
  instance_types=variaveis.NODE_MACHINE_TYPE,
  scaling_config={
      'desiredSize' : f'{variaveis.SIZE[0]}',
      'minSize' : f'{variaveis.SIZE[1]}',
      'maxSize' : f'{variaveis.SIZE[2]}',
  },
  tags=variaveis.LABELS
)
'''------------------------EKS CLUSTER-------------------------'''

pulumi.export(f"connection", 'Run the following code: aws eks --region {REGION} update-kubeconfig --name {eks_cluster.name}')