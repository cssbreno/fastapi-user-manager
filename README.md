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
git clone https://github.com/cssbreno/fastapi-user-manager.git
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

### 4. Configure as Variáveis de Ambiente

**IMPORTANTE:** Este projeto requer configuração de variáveis de ambiente para funcionar corretamente.

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Gere uma chave secreta única
# Python (recomendado, pois já é um pré-requisito)
python -c "import secrets; print(secrets.token_hex(32))"

# Ou use o comando abaixo para gerar uma chave secreta única
# Windows:
powershell -Command "openssl rand -hex 32"
# Linux/Mac:
openssl rand -hex 32

# Copie a chave secreta gerada para o arquivo .env
echo "SECRET_KEY=sua_chave_secreta_aqui" >> .env

# Edite o arquivo .env com suas configurações (opcional)
nano .env  # ou use seu editor preferido
```

**Configurações no .env:**

- **`SECRET_KEY`**: Chave secreta para JWT (obrigatória para produção)
- **`ACCESS_TOKEN_EXPIRE_MINUTES`**: Tempo de expiração do token (padrão: 30 min)
- **`DATABASE_URL`**: URL do banco de dados (padrão: SQLite local)
- **`ALGORITHM`**: Algoritmo de criptografia JWT (padrão: HS256)

**Exemplo de .env preenchido:**

```bash
SECRET_KEY=sua_chave_secreta_gerada_aqui_com_64_caracteres
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./database.db
ALGORITHM=HS256
```

**Nota:** O projeto funcionará com os valores padrão, mas é **altamente recomendado** configurar uma `SECRET_KEY` única em produção.

### 5. Instale as Dependências

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
2. **Crie um token de acesso** → `POST /token` (com `email` e `password`)
3. **Autentique-se** → Clique em *Authorize* no Swagger e insira:  
   - `email`: seu email (não username)  
   - `password`: sua senha  
   - Deixe `client_id` e `client_secret` em branco  
4. **Acesse rotas protegidas** → Endpoints como `GET /users/me` ou `PUT /users/{user_id}` estarão liberados com o token gerado.

**Nota:** O sistema usa **email** (não username) para autenticação, conforme implementado na API.

### Exemplos de Uso com cURL (Postman)

**1. Criar usuário:**

```bash
curl -X POST "http://127.0.0.1:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario_teste",
    "email": "teste@exemplo.com",
    "password": "senha123"
  }'
```

**2. Obter token de acesso:**

```bash
curl -X POST "http://127.0.0.1:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=teste@exemplo.com&password=senha123"
```

**Nota:** O endpoint `/token` espera `email` e `password` como form data, não JSON.

**3. Acessar rota protegida:**

```bash
curl -X GET "http://127.0.0.1:8000/users/me" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```  

**4. Listar usuários:**

```bash
curl -X GET "http://127.0.0.1:8000/users/" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

**5. Atualizar usuário:**

```bash
curl -X PUT "http://127.0.0.1:8000/users/1" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario_teste_atualizado",
    "email": "teste@exemplo.com",
    "password": "senha123"
  }'
```

**6. Deletar usuário:**

```bash
curl -X DELETE "http://127.0.0.1:8000/users/1" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

---

## Como Executar os Testes

Na raiz do projeto:

```bash
# Executar todos os testes
pytest

# Executar com mais detalhes
pytest -v

# Executar com cobertura de código
pytest --cov=src --cov-report=html

# Após executar, abra o relatório HTML:
# Abra o arquivo htmlcov/index.html no seu navegador

# Executar testes específicos
pytest tests/test_user_service.py -v
```

**Cobertura Atual dos Testes:**

- ✅ **UserService**: Testes unitários completos com mocks
- ✅ **SQLiteUserRepository**: Testes de persistência com mocks
- ✅ **Autenticação**: Sistema JWT e hash de senhas testado
- ✅ **Configuração**: Validação de variáveis de ambiente
- ✅ **Validação**: Schemas e validações testados
- ✅ **Rotas da API**: Endpoints testados com TestClient

**Estrutura de Testes:**

- **`tests/test_user_service.py`**: Testes unitários da camada de serviço
- **`tests/test_sqlite_repository.py`**: Testes do repositório de dados
- **`tests/test_auth.py`**: Testes de autenticação e JWT
- **`tests/test_config.py`**: Testes de configuração
- **`tests/test_api_endpoints.py`**: Testes de integração dos endpoints da API

**Tipos de Testes Implementados:**

- **Testes Unitários**: `tests/test_user_service.py` - Testa a lógica de negócio isoladamente
- **Testes de Repositório**: `tests/test_sqlite_repository.py` - Testa a camada de persistência
- **Testes de Autenticação**: `tests/test_auth.py` - Testa JWT, hash de senhas e validação de tokens
- **Testes de Configuração**: `tests/test_config.py` - Testa carregamento de variáveis de ambiente
- **Testes de API**: `tests/test_api_endpoints.py` - Testa os endpoints com TestClient
- **Mocks**: Uso de `unittest.mock` para isolamento de dependências
- **Fixtures**: Reutilização de dados de teste entre diferentes testes

---

## Desenvolvimento

### Estrutura do Projeto

```
fastapi-user-manager/
├── src/
│   ├── core/                    # Lógica de negócio (domínio)
│   │   ├── models.py           # Modelos de domínio (Pydantic)
│   │   ├── ports/              # Interfaces (contratos)
│   │   │   └── user_repository.py
│   │   └── services/           # Serviços de negócio
│   │       └── user_service.py
│   ├── infrastructure/          # Implementações concretas
│   │   ├── database/           # Camada de persistência
│   │   │   ├── models.py       # Modelos SQLAlchemy
│   │   │   ├── database.py     # Configuração do banco
│   │   │   └── sqlite_user_repository.py
│   │   └── web/                # Camada de apresentação
│   │       ├── api.py          # Controllers/rotas
│   │       ├── auth.py         # Autenticação JWT
│   │       ├── schemas.py      # Validação de entrada/saída
│   │       └── dependencies.py # Injeção de dependências
│   ├── config.py               # Configurações e variáveis de ambiente
│   └── main.py                 # Ponto de entrada da aplicação
├── tests/                      # Testes automatizados
│   ├── test_user_service.py   # Testes unitários
│   └── test_api_endpoints.py  # Testes de integração
├── requirements.txt            # Dependências Python
├── pytest.ini                 # Configuração do pytest
└── .env.example               # Exemplo de variáveis de ambiente
```

### Arquitetura e Separação de Responsabilidades

**Core (Domínio):**

- **`models.py`**: Entidades de negócio (User) usando Pydantic
- **`ports/`**: Interfaces que definem contratos (UserRepository)
- **`services/`**: Lógica de negócio (UserService)

**Infrastructure (Implementação):**

- **`database/`**: Persistência de dados com SQLAlchemy
- **`web/`**: API REST com FastAPI, autenticação e validação

**Schemas vs Models:**

- **`core/models.py`**: Modelos de domínio para lógica de negócio
- **`infrastructure/web/schemas.py`**: Schemas para validação de entrada/saída da API
- **`infrastructure/database/models.py`**: Modelos SQLAlchemy para persistência

### Adicionando Novos Testes

Para adicionar novos testes:

1. **Testes Unitários**: Crie arquivos em `tests/test_*.py`
2. **Use Mocks**: Para isolar dependências externas
3. **Fixtures**: Para reutilizar dados de teste
4. **Cobertura**: Execute `pytest --cov=src --cov-report=html`

### Padrões de Código

- **Arquitetura Hexagonal**: Separação clara entre domínio e infraestrutura
- **Dependency Injection**: Uso de `Depends()` para injeção de dependências
- **Validação**: Schemas Pydantic para entrada/saída da API
- **Tratamento de Erros**: HTTP status codes apropriados
- **Separação de Modelos**:
  - Modelos de domínio (core) para lógica de negócio
  - Schemas (web) para validação de API
  - Modelos de persistência (database) para SQLAlchemy

---

## Troubleshooting

### Problemas Comuns

**1. Erro "Module not found":**

```bash
# Certifique-se de estar no diretório raiz do projeto
cd fastapi-user-manager

# Ative o ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

**2. Erro de banco de dados:**

```bash
# Verifique se o arquivo .env está configurado
cat .env

# Certifique-se de que o DATABASE_URL está correto
```

**3. Erro de autenticação:**

- Verifique se `SECRET_KEY` está configurada no .env
- Certifique-se de que o token não expirou
- Use o endpoint `/token` para obter um novo token
- **IMPORTANTE**: Use **email** (não username) para autenticação

**4. Porta já em uso:**

```bash
# Use uma porta diferente
uvicorn src.main:app --reload --port 8001
```
