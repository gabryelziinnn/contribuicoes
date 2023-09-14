from pulumi import Config
'''--------------------VARIAVEIS---------------------------------'''
config = Config(None)
ZONES = config.get_int('availability-zones') or ['us-west-1a','us-west-1c'] # caso nao exista algo definido, sera west por padrao
KUBERNETES_VERSION = '1.27'
REGION = "us-west-1"


LABELS = {
    "environment" : "production", # homologation / production / dev
    "app" : "cluster",
    "team": "devops",
    "project" : "testing-purposes",
    "version" : "1-0-0",
    "service" : "web-service",
    "location" : REGION,
}

if LABELS.get('environment') == 'production':
    NODE_MACHINE_TYPE = ['t3.xlarge']
    SIZE = [2,1,2]
elif LABELS.get('environment') == 'homologation':
    NODE_MACHINE_TYPE = ['e2-medium']
    SIZE = [1,1,2]
else:
    NODE_MACHINE_TYPE = ['e2-small']
    SIZE = [1,1,1]
'''--------------------VARIAVEIS---------------------------------'''