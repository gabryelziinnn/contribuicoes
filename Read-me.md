# Teleport with AUTO-SCALING Group on AWS:

This pulumi code will deploy a AUTO-SCALING Group on AWS with a load balancer on the front of the ASG with listener and target groups poiting to the ASG.

You will just need to export your IAM credentials, or use one already configured in the folder: `.aws/credentials`

(your credentials need to have access to deploy EC2 instances, Auto scaling groups, and Target Groups).

See the code to view more details about your deployment.

# Deploying:

Connect to your account on pulumi (if you have questions see: `https://www.pulumi.com/docs/get-started/aws/`)

Insert the regions that you want to deploy your infra, on the files: `Pulumi.dev.yaml - variaveis/vars.py`

**And just run:**

```
pulumi preview (to see what this code will deploy)
pulumi up -y (actually deploy the infra to AWS)
```

# Changing the infra:

You can change the infra as you like, on the folder `variaveis/redes` contains all the network creation to your ASG. On the `variaveis/vars` contains variables that you can modify as you like it.

# Extra:

In the folder you have a ansible playbook called: teleport-k8s-install.yml, you can run it to deploy the Teleport Kubernetes Server, assuming you already have a kubernetes cluster installed on yours ASG deployment.
