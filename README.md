# UPIA - API de Conexão entre Empregados e Empregadores

Esta é uma API REST que gerencia conexões entre candidatos e empresas, permitindo o cadastro de candidatos, empresas, vagas e candidaturas.

## Tecnologias Utilizadas

- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker e Docker Compose

## Como Executar

1. Certifique-se de ter o Docker e o Docker Compose instalados em sua máquina.

2. Clone o repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd upia
```

3. Inicie os containers:
```bash
docker-compose up --build
```

A API estará disponível em `http://localhost:8000`

## Documentação da API

Após iniciar a aplicação, você pode acessar:

- Documentação Swagger UI: `http://localhost:8000/docs`
- Documentação ReDoc: `http://localhost:8000/redoc`

## Endpoints Principais

### Candidatos
- `POST /candidatos/` - Criar novo candidato
- `GET /candidatos/` - Listar todos os candidatos
- `GET /candidatos/{id}` - Obter candidato específico

### Candidaturas
- `POST /candidatos/{candidato_id}/candidaturas/` - Criar nova candidatura

### Empresas
- `POST /empresas/` - Criar nova empresa
- `GET /empresas/` - Listar todas as empresas
- `GET /empresas/{id}` - Obter empresa específica

### Vagas
- `POST /empresas/{empresa_id}/vagas/` - Criar nova vaga
- `GET /vagas/` - Listar todas as vagas

## Estrutura do Banco de Dados

- **Candidatos**: Armazena informações dos candidatos
- **Candidaturas**: Registra as candidaturas dos candidatos
- **Empresas**: Armazena informações das empresas
- **Vagas**: Registra as vagas disponibilizadas pelas empresas 