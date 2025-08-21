# Teste Prático: API de Gerenciamento de Usuários

Esta é uma API REST desenvolvida em Python com FastAPI para o gerenciamento de usuários.  
O projeto foi estruturado utilizando princípios da **Arquitetura Hexagonal (Ports and Adapters)** para garantir um código limpo, desacoplado e de fácil manutenção.

---

## Funcionalidades

- **Autenticação**: Sistema de login seguro com tokens **JWT**  
- **CRUD de Usuários**: Criação, Leitura, Atualização e Deleção  
- **Paginação**: Listagem paginada para performance eficiente  
- **Proteção de Rotas**: Autenticação obrigatória em operações críticas  
- **Documentação Automática**: Swagger UI e ReDoc gerados automaticamente  

---

## Requisitos Técnicos Atendidos

- **Framework**: FastAPI  
- **Banco de Dados**: SQLite  
- **Arquitetura**: Hexagonal (Ports and Adapters)  
- **Autenticação**: JWT (JSON Web Tokens)  
- **Testes**: Unitários na camada de serviço  
- **Versionamento**: Código organizado para publicação no GitHub  

---

## Instalação e Configuração

### 1. Pré-requisitos

- Python 3.8 ou superior  
- Git  

### 2. Clone o Repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd fastapi-user-manager
```

### 3. Crie e Ative um Ambiente Virtual

```bash
# Criação
python3 -m venv venv

# Ativação
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

> Após ativar, você verá `(venv)` no início da linha do terminal.

### 4. Instale as Dependências

```bash
pip install -r requirements.txt
```

---

## Como Executar a Aplicação

Na raiz do projeto:

```bash
uvicorn src.main:app --reload
```

- `src.main:app`: aponta para o objeto `app` em `src/main.py`  
- `--reload`: reinicia o servidor automaticamente a cada alteração  

O servidor estará disponível em: **<http://127.0.0.1:8000>**

---

## Como Usar a API (Documentação)

- **Swagger UI** → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- **ReDoc** → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)  

### Fluxo de Uso Básico

1. **Crie um usuário** → `POST /users/` (com `username`, `email` e `password`)  
2. **Autentique-se** → Clique em *Authorize* no Swagger e insira:  
   - `username`: seu email  
   - `password`: sua senha  
   - Deixe `client_id` e `client_secret` em branco  
3. **Acesse rotas protegidas** → Endpoints como `GET /users/me` ou `PUT /users/{user_id}` estarão liberados com o token gerado.  

---

## Como Executar os Testes

Na raiz do projeto:

```bash
pytest
```

Os testes verificam a camada de serviço (`UserService`) isoladamente, usando mocks para simular o repositório, em conformidade com os princípios da arquitetura limpa.
