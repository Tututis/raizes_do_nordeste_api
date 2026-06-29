# API Raízes do Nordeste

API Back-End desenvolvida em Python com FastAPI para simular o sistema de gestão da rede **Raízes do Nordeste**.

O projeto contempla cadastro de usuários, autenticação JWT, controle de perfis, unidades, produtos, estoque por unidade, pedidos multicanal, pagamento mock, atualização de status de pedidos, auditoria e tratamento padronizado de erros.

## Tecnologias utilizadas

* Python
* FastAPI
* Uvicorn
* SQLAlchemy
* SQLite
* Pydantic
* Passlib
* bcrypt
* python-jose
* Swagger/OpenAPI
* Git e GitHub

## Funcionalidades implementadas

* Cadastro de usuários
* Hash de senha
* Login com JWT
* Controle de acesso por perfil
* Cadastro e consulta de unidades
* Cadastro e consulta de produtos
* Controle de estoque por unidade
* Entrada e saída de estoque
* Criação de pedidos com itens
* Campo obrigatório `canalPedido`
* Validação de estoque na criação do pedido
* Pagamento mock aprovado ou recusado
* Atualização automática do status do pedido após pagamento
* Atualização manual do status operacional do pedido
* Registro de auditoria para alteração de status
* Tratamento padronizado de erros

## Perfis de usuário

O sistema possui os seguintes perfis:

* `CLIENTE`
* `ATENDENTE`
* `COZINHA`
* `GERENTE`
* `ADMIN`

Alguns endpoints exigem autenticação JWT e perfil autorizado. Por exemplo, cadastro de produtos, unidades e estoque são operações restritas a usuários com perfil `ADMIN` ou `GERENTE`.

## Canais de pedido

O pedido possui o campo obrigatório `canalPedido`, usado para registrar a origem do pedido.

Valores aceitos:

* `APP`
* `TOTEM`
* `BALCAO`
* `PICKUP`
* `WEB`

Exemplo:

```json
{
  "cliente_id": 1,
  "unidade_id": 1,
  "canalPedido": "APP",
  "itens": [
    {
      "produto_id": 1,
      "quantidade": 2
    }
  ]
}
```

## Estrutura do projeto

```text
raizes_api/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── security.py
│   ├── exceptions.py
│   │
│   ├── models/
│   │   ├── usuario.py
│   │   ├── unidade.py
│   │   ├── produto.py
│   │   ├── estoque.py
│   │   ├── pedido.py
│   │   ├── pagamento.py
│   │   └── auditoria.py
│   │
│   ├── schemas/
│   │   ├── auth_schema.py
│   │   ├── usuario_schema.py
│   │   ├── unidade_schema.py
│   │   ├── produto_schema.py
│   │   ├── estoque_schema.py
│   │   ├── pedido_schema.py
│   │   ├── pagamento_schema.py
│   │   └── auditoria_schema.py
│   │
│   └── routers/
│       ├── auth_router.py
│       ├── usuarios_router.py
│       ├── unidades_router.py
│       ├── produtos_router.py
│       ├── estoque_router.py
│       ├── pedidos_router.py
│       ├── pagamentos_router.py
│       └── auditoria_router.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/Tututis/raizes_do_nordeste_api.git
cd raizes_do_nordeste_api
```

### 2. Criar ambiente virtual

```bash
python -m venv venv
```

### 3. Ativar ambiente virtual

No PowerShell:

```bash
.\venv\Scripts\Activate.ps1
```

No CMD:

```bash
venv\Scripts\activate
```

### 4. Instalar dependências

```bash
python -m pip install -r requirements.txt
```

### 5. Executar a API

```bash
python -m uvicorn app.main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

## Documentação Swagger/OpenAPI

Com a API rodando, acesse:

```text
http://127.0.0.1:8000/docs
```

Documentação alternativa:

```text
http://127.0.0.1:8000/redoc
```

## Banco de dados

O projeto utiliza SQLite para execução local.

O banco é criado automaticamente na raiz do projeto:

```text
raizes.db
```

As tabelas são criadas automaticamente na inicialização da aplicação via SQLAlchemy.

## Principais endpoints

### Autenticação

| Método | Rota          | Descrição                               |
| ------ | ------------- | --------------------------------------- |
| POST   | `/auth/login` | Realiza login e retorna token JWT       |
| GET    | `/auth/me`    | Retorna os dados do usuário autenticado |

### Usuários

| Método | Rota                     | Descrição            |
| ------ | ------------------------ | -------------------- |
| POST   | `/usuarios`              | Cadastra usuário     |
| GET    | `/usuarios`              | Lista usuários       |
| GET    | `/usuarios/{usuario_id}` | Busca usuário por ID |

### Unidades

| Método | Rota                     | Descrição            |
| ------ | ------------------------ | -------------------- |
| POST   | `/unidades`              | Cadastra unidade     |
| GET    | `/unidades`              | Lista unidades       |
| GET    | `/unidades/{unidade_id}` | Busca unidade por ID |

### Produtos

| Método | Rota                     | Descrição            |
| ------ | ------------------------ | -------------------- |
| POST   | `/produtos`              | Cadastra produto     |
| GET    | `/produtos`              | Lista produtos       |
| GET    | `/produtos/{produto_id}` | Busca produto por ID |

### Estoque

| Método | Rota                            | Descrição                               |
| ------ | ------------------------------- | --------------------------------------- |
| POST   | `/estoque`                      | Cadastra estoque de produto por unidade |
| GET    | `/estoque/unidade/{unidade_id}` | Lista estoque de uma unidade            |
| PATCH  | `/estoque/{estoque_id}/entrada` | Registra entrada no estoque             |
| PATCH  | `/estoque/{estoque_id}/saida`   | Registra saída do estoque               |

### Pedidos

| Método | Rota                          | Descrição                             |
| ------ | ----------------------------- | ------------------------------------- |
| POST   | `/pedidos`                    | Cria pedido                           |
| GET    | `/pedidos`                    | Lista pedidos com filtros             |
| GET    | `/pedidos/{pedido_id}`        | Busca pedido por ID                   |
| PATCH  | `/pedidos/{pedido_id}/status` | Atualiza status operacional do pedido |

### Pagamentos

| Método | Rota                         | Descrição                             |
| ------ | ---------------------------- | ------------------------------------- |
| POST   | `/pagamentos/mock`           | Simula pagamento aprovado ou recusado |
| GET    | `/pagamentos/{pagamento_id}` | Busca pagamento por ID                |

### Auditoria

| Método | Rota         | Descrição                    |
| ------ | ------------ | ---------------------------- |
| GET    | `/auditoria` | Lista registros de auditoria |

## Fluxo principal implementado

O fluxo principal da API é:

```text
Pedido → Pagamento mock → Atualização de status
```

### Etapas do fluxo

1. Criar usuário.
2. Fazer login.
3. Autorizar no Swagger usando o token JWT.
4. Criar unidade.
5. Criar produto.
6. Cadastrar estoque do produto na unidade.
7. Criar pedido informando cliente, unidade, canal e itens.
8. A API valida se existe estoque suficiente.
9. A API baixa o estoque.
10. O pedido é criado com status `AGUARDANDO_PAGAMENTO`.
11. O pagamento mock é processado.
12. Se aprovado, o pedido muda para `PAGO`.
13. Se recusado, o pedido muda para `PAGAMENTO_RECUSADO`.
14. Após pagamento aprovado, o pedido pode avançar para `EM_PREPARO`, `PRONTO` e `ENTREGUE`.

## Exemplos de uso

### Criar usuário administrador

Endpoint:

```text
POST /usuarios
```

Body:

```json
{
  "nome": "Admin Teste",
  "email": "admin@teste.com",
  "senha": "123456",
  "perfil": "ADMIN",
  "consentimento_lgpd": true
}
```

### Criar usuário cliente

Endpoint:

```text
POST /usuarios
```

Body:

```json
{
  "nome": "Cliente Teste",
  "email": "cliente@teste.com",
  "senha": "123456",
  "perfil": "CLIENTE",
  "consentimento_lgpd": true
}
```

### Login

Endpoint:

```text
POST /auth/login
```

Body:

```json
{
  "email": "admin@teste.com",
  "senha": "123456"
}
```

Resposta esperada:

```json
{
  "access_token": "token_jwt_gerado",
  "token_type": "bearer",
  "usuario_id": 1,
  "nome": "Admin Teste",
  "perfil": "ADMIN"
}
```

Para acessar rotas protegidas no Swagger:

1. Copie o valor de `access_token`.
2. Clique em **Authorize**.
3. Informe o token no formato:

```text
Bearer token_jwt_gerado
```

### Criar unidade

Endpoint:

```text
POST /unidades
```

Body:

```json
{
  "nome": "Raízes Recife Centro",
  "cidade": "Recife",
  "estado": "PE",
  "ativa": true
}
```

### Criar produto

Endpoint:

```text
POST /produtos
```

Body:

```json
{
  "nome": "Tapioca de Carne Seca",
  "descricao": "Tapioca recheada com carne seca e queijo coalho",
  "preco": 18.90,
  "ativo": true,
  "sazonal": false
}
```

### Cadastrar estoque

Endpoint:

```text
POST /estoque
```

Body:

```json
{
  "unidade_id": 1,
  "produto_id": 1,
  "quantidade": 20
}
```

### Criar pedido

Endpoint:

```text
POST /pedidos
```

Body:

```json
{
  "cliente_id": 2,
  "unidade_id": 1,
  "canalPedido": "APP",
  "itens": [
    {
      "produto_id": 1,
      "quantidade": 2
    }
  ]
}
```

Resposta esperada:

```json
{
  "id": 1,
  "cliente_id": 2,
  "unidade_id": 1,
  "canal_pedido": "APP",
  "status": "AGUARDANDO_PAGAMENTO",
  "valor_total": 37.80,
  "itens": [
    {
      "produto_id": 1,
      "quantidade": 2,
      "preco_unitario": 18.90,
      "subtotal": 37.80
    }
  ]
}
```

### Pagamento mock aprovado

Endpoint:

```text
POST /pagamentos/mock
```

Body:

```json
{
  "pedido_id": 1,
  "aprovado": true
}
```

Resposta esperada:

```json
{
  "pedido_id": 1,
  "status": "APROVADO",
  "mensagem": "Pagamento mock aprovado"
}
```

Após o pagamento aprovado, o pedido muda para:

```text
PAGO
```

### Pagamento mock recusado

Endpoint:

```text
POST /pagamentos/mock
```

Body:

```json
{
  "pedido_id": 2,
  "aprovado": false
}
```

Após o pagamento recusado, o pedido muda para:

```text
PAGAMENTO_RECUSADO
```

### Atualizar status do pedido

Após o pedido estar pago, o status pode seguir o fluxo:

```text
PAGO → EM_PREPARO → PRONTO → ENTREGUE
```

Endpoint:

```text
PATCH /pedidos/1/status
```

Body:

```json
{
  "status": "EM_PREPARO"
}
```

## Padrão de erro da API

A API possui resposta padronizada para erros.

Exemplo de erro 404:

```json
{
  "erro": true,
  "codigo": "HTTP_ERROR",
  "mensagem": "Produto não encontrado",
  "status": 404,
  "path": "/produtos/999",
  "timestamp": "2026-06-28T19:30:00Z"
}
```

Exemplo de erro de validação:

```json
{
  "erro": true,
  "codigo": "VALIDATION_ERROR",
  "mensagem": "Erro de validação dos dados enviados",
  "status": 422,
  "path": "/produtos",
  "timestamp": "2026-06-28T19:30:00Z",
  "detalhes": [
    {
      "campo": "body.preco",
      "mensagem": "Input should be greater than 0",
      "tipo": "greater_than"
    }
  ]
}
```

## Segurança e LGPD

O projeto aplica controles básicos de segurança e privacidade:

* Senhas são armazenadas com hash.
* A senha original não é retornada nas respostas.
* O campo `senha_hash` não é exposto pela API.
* Autenticação via JWT.
* Controle de acesso por perfil.
* Campo `consentimento_lgpd` no cadastro de usuários.
* Auditoria para ações sensíveis, como alteração de status de pedidos.

## Auditoria

A API registra auditoria para alterações de status de pedidos.

Endpoint:

```text
GET /auditoria
```

Exemplo de resposta:

```json
{
  "id": 1,
  "usuario_id": 1,
  "acao": "ATUALIZACAO_STATUS_PEDIDO",
  "entidade": "Pedido",
  "entidade_id": 1,
  "detalhes": "Status alterado de PAGO para EM_PREPARO",
  "criado_em": "2026-06-28T19:30:00"
}
```

## Testes manuais sugeridos

| ID  | Cenário                               | Endpoint                     | Resultado esperado                        |
| --- | ------------------------------------- | ---------------------------- | ----------------------------------------- |
| T01 | Criar usuário administrador           | POST `/usuarios`             | 201 Created                               |
| T02 | Login válido                          | POST `/auth/login`           | 200 OK com token                          |
| T03 | Login inválido                        | POST `/auth/login`           | 401 Unauthorized                          |
| T04 | Criar unidade com ADMIN               | POST `/unidades`             | 201 Created                               |
| T05 | Criar produto com ADMIN               | POST `/produtos`             | 201 Created                               |
| T06 | Criar estoque                         | POST `/estoque`              | 201 Created                               |
| T07 | Criar pedido com estoque suficiente   | POST `/pedidos`              | 201 Created                               |
| T08 | Criar pedido com estoque insuficiente | POST `/pedidos`              | 409 Conflict                              |
| T09 | Pagamento mock aprovado               | POST `/pagamentos/mock`      | 201 Created e pedido `PAGO`               |
| T10 | Pagamento mock recusado               | POST `/pagamentos/mock`      | 201 Created e pedido `PAGAMENTO_RECUSADO` |
| T11 | Atualizar status do pedido            | PATCH `/pedidos/{id}/status` | 200 OK                                    |
| T12 | Acessar rota protegida sem token      | GET `/auth/me`               | 401 ou 403                                |
| T13 | Consultar auditoria                   | GET `/auditoria`             | 200 OK                                    |

## Ordem recomendada para testar

1. Executar a API.
2. Acessar `http://127.0.0.1:8000/docs`.
3. Criar usuário `ADMIN`.
4. Fazer login com o usuário `ADMIN`.
5. Autorizar no Swagger usando o token JWT.
6. Criar unidade.
7. Criar produto.
8. Criar estoque.
9. Criar usuário `CLIENTE`.
10. Fazer login como `CLIENTE`.
11. Autorizar no Swagger com o token do cliente.
12. Criar pedido.
13. Fazer pagamento mock.
14. Fazer login novamente como `ADMIN`, `GERENTE`, `ATENDENTE` ou `COZINHA`.
15. Atualizar status do pedido.
16. Consultar auditoria.

## Histórico de commits

O projeto utiliza Git para versionamento e possui commits organizados por etapa de desenvolvimento, como estrutura inicial, endpoints, estoque, pedidos, autenticação, autorização, pagamento mock, auditoria e documentação.

## Observações finais

Este projeto foi desenvolvido como uma simulação de Back-End para uma rede de lanchonetes, com foco em API REST, modelagem de domínio, persistência em banco, segurança, integração simulada com pagamento externo e rastreabilidade operacional.

## Autor

Arthur de Santana Magri 
RU: 4763786
