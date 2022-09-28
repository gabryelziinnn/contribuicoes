# Regras:

Insira um arquivo com nome: "config"" dentro da pasta para ser buildado no container, com sua regiao e credenciais conforme exemplo do conteúdo dele abaixo:

[default]
aws_access_key_id =
aws_secret_access_key =
region =

# Então builde a imagem:

docker build -t *qualquer_nome:qualquer_versao* .

Ao rodar o container, tudo que está definido nos python serão criados

docker run -it --rm  *nome_definido*:*versao_definida*

# ISSUES:

Por algum motivo desconhecido o arquivo: vpc2.py

A rota para o routing table, não está sendo criada com o sed, pois o mesmo da um espacamento indevido, somente neste bloco.
