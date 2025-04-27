Instalar o minikube
Instalar o istio via istioctl
Criar o novo namespace: `teste` e realizar tudo dentro dele.

# Realizar tudo dentro deste namespace:
Subir o nginx teste e verificar que o istio nao esta inserido
Realizar o label no namespace e logo após restartar os pods para ativar o istio e verifiar os pods
Criar o gateway
Criar o virtual service
Expor a aplicacao no nome `labgab.local` e verificar acesso
Criar o PeerAuthEntication com MTLS Strict
Deletar os Gateway e VS antigos

# Subindo canary
Realizar o deployment em canary da aplicação lendo todos os manifestos
Acesse a aplicacao em: [http://labgab.local:/home/](http://labgab.local/home/)
Veja que o tráfego está sendo dividido em 50%