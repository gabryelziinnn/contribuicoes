import json,pulumi
from pulumi_aws import iam

# Define the IAM Role
role = iam.Role("cluster-eks-role",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Effect": "Allow",
        }]
    }))

# Define the list of policy ARNs
policy_arns = [
    "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy",
    "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy",
    "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly",
]

# Attach the policies to the role
for counter, policy_arn in enumerate(policy_arns):
    iam.RolePolicyAttachment(f"my-cluster-ng-role-policy-{counter}",
                             role=role.name,
                             policy_arn=policy_arn)