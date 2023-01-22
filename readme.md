# CLUSTER HA K3S with pulumi and ansible (AWS)

In this project i'm using gitlab-ci pipeline to deploy all the instances on AWS, and provision all the configuration required to deploy a cluster HA with K3S.

To IAC i'm using pulumi (python version), and to configure Ansible.

This project will deploy 6 EC2 instances (with ubuntu 22.04) on AWS, where 3 are master nodes and 3 are worker nodes.

This project is still on progress, any problem you see contact me please.

# Notes:

In the k3s.yml playbook, the user chosen, is the ubuntu (which is the default for ubuntu machines), if you like to use another version of system, you need to define there, the default user for that system.

You need to define all the fqdn variables and secrets, please read carefully all the vars/ folders and all.yml, from the main playbook.

On the function to create all the instances, you have to define your key_name = variaveis.nome_da_chave, of your aws existing key.

### To use the ***pipeline on GITLAB,*** you need to define 3 VARIABLES:

PROJETO: insert here your project name

STACK: insert here your stack name

PULUMI_ACESS_TOKEN: insert on gitlab variables(secret), your pulumi token

You also need to export 2 credentials from AWS which is:

AWS_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY

(which is capable of creating EC2 instances and all of requirements to use it online, like subnets, ig, and so on)
