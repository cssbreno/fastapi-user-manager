````markdown
# Teste Prático: API de Gerenciamento de Usuários

Esta é uma API REST desenvolvida em Python com FastAPI para o gerenciamento de usuários. O projeto foi estruturado utilizando princípios da **Arquitetura Hexagonal (Ports and Adapters)** para garantir um código limpo, desacoplado e de fácil manutenção.

## Funcionalidades

* **Autenticação**: Sistema de login seguro com tokens **JWT**.
* **CRUD de Usuários**: Operações completas de Criação, Leitura, Atualização e Deleção de usuários.
* **Paginação**: A listagem de usuários é paginada para uma performance eficiente.
* **Proteção de Rotas**: Rotas críticas (como update e delete) exigem autenticação.
* **Documentação Automática**: A API possui documentação interativa gerada automaticamente pelo Swagger UI e ReDoc.

## Requisitos Técnicos Atendidos

* **Framework**: FastAPI
* **Banco de Dados**: SQLite
* **Arquitetura**: Hexagonal (Ports and Adapters)
* **Autenticação**: JWT (JSON Web Tokens)
* **Testes**: Testes unitários para a camada de serviço.
* **Versionamento**: O código foi organizado para ser publicado no GitHub.

## Instalação e Configuração

Siga os passos abaixo para configurar e executar o projeto localmente.

### 1. Pré-requisitos

* Python 3.8 ou superior
* Git

### 2. Clone o Repositório

Clone este repositório para a sua máquina local:

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd fastapi-user-manager
````

### 3\. Crie e Ative um Ambiente Virtual

É uma boa prática usar um ambiente virtual para isolar as dependências do projeto.

```bash
# Crie o ambiente virtual (a pasta se chamará venv)
python -m venv venv

# Ative o ambiente virtual
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate
```

Após ativar, você verá `(venv)` no início da linha do seu terminal.

### 4\. Instale as Dependências

Com o ambiente virtual ativado, instale todas as bibliotecas necessárias de uma só vez:

```bash
pip install -r requirements.txt
```

## Como Executar a Aplicação

Para iniciar o servidor da API, execute o seguinte comando na raiz do projeto:

```bash
uvicorn src.main:app --reload
```

* `src.main:app` informa ao Uvicorn para encontrar o objeto `app` no arquivo `src/main.py`.
* `--reload` faz com que o servidor reinicie automaticamente após qualquer alteração no código.

O servidor estará rodando em `http://127.0.0.1:8000`.

## Como Usar a API (Documentação)

Após iniciar a aplicação, você pode acessar a documentação interativa gerada pelo FastAPI em seu navegador:

* **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Fluxo de Uso Básico

1. **Crie um usuário**: Use o endpoint `POST /users/`. Forneça um `username`, `email` e `password`.
2. **Autentique-se na documentação**:
      * No topo direito da página, clique no botão verde "Authorize".
      * Na janela que abrir, na seção "OAuth2PasswordBearer", digite o `email` do seu usuário no campo `username` e a sua senha no campo `password`.
      * Deixe os campos `client_id` e `client_secret` em branco.
      * Clique no botão "Authorize" dentro da janela. Se as credenciais estiverem corretas, a janela fechará e um ícone de cadeado aparecerá no botão principal.
3. **Acesse rotas protegidas**: Agora que você está autenticado, pode testar os endpoints que exigem login, como `GET /users/me` ou `PUT /users/{user_id}`. O Swagger irá anexar seu token a essas requisições automaticamente.

## Como Executar os Testes

Para garantir a qualidade e o funcionamento da lógica de negócio, você pode executar os testes unitários. Na raiz do projeto, execute:

```bash
pytest
```

Os testes verificarão a camada de serviço (`UserService`) de forma isolada, utilizando mocks para simular o repositório, conforme os princípios da arquitetura limpa.

```
```
