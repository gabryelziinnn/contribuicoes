# Instruçoes:

Para uso, se cadastre no link: **https://app.pulumi.com/**

Baixe a cli do pulumi: `curl -fsSL https://get.pulumi.com | sh`

Faca o login: `pulumi login` (insira suas credenciais)

Baixe o python, e dentro da pasta raiz rode o comando:

` python -m venv . && source venv/bin/activate && pip install -r requirements.txt`

Escolha a regiao e as duas zonas de disponibilidades desejadas para o deployment do eks(conforme exemplo abaixo):

```
pulumi config set aws:region us-west-1 
pulumi config set --path availability-zones '['us-west-1a','us-west-1c']'
```

Realize o preview e deploy respectivamente com: `pulumi preview / pulumi up -y`
