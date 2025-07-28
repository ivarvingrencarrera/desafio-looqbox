# Desafio Looqbox

Bem-vindo ao meu repositório! Este é um guia rápido para ajudá-lo a começar a usar o projeto.

## Pré-requisitos

Certifique-se de ter instaladas as seguintes ferramentas em seu sistema:

- [Python 3.13 ou Superior](https://www.python.org/downloads/)
- [UV] (https://docs.astral.sh/uv/getting-started/installation/) (Gerenciador de Dependências) 
- [Make](https://www.gnu.org/software/make/) (Automação de Tarefas)

## Configuração

Siga as etapas abaixo para configurar e executar o projeto:

1. Clone o repositório:
    ```git clone -b main https://github.com/ivarvingrencarrera/desafio-looqbox.git```
#####
2. Navegue até o diretório do projeto:
    ```cd desafio-looqbox```
#####
3. Instale as dependências do projeto:
    ```uv sync```
#####
4. Crie e ative um ambiente virtual usando o uv:
    ```source .venv/bin/activate```
#####
5. Validar variáveis de ambiente e caso não exista, preencher os valores da env:
    ```make check_env```
#####
6. Execute a aplicação:
    ```make local/start```
#####

## Testes

Para executar os testes, utilize o seguinte comando:
    ```make test```


## Documentação

Para visualizar a documentação com os endpoints, acesse [http://localhost:8008/docs](http://localhost:8008/docs/) e obtenha todos os detalhes.
