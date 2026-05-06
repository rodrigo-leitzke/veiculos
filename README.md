# 🚗 Cadastro de Veículos API

API REST em Python/Flask para cadastro e consulta de veículos, com pipeline de CI/CD completo via GitHub Actions.

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Linguagem | Python 3.11 / 3.12 |
| Framework | Flask 3.1 |
| Banco de dados | SQLite |
| Testes | pytest + pytest-cov |
| Container | Docker / Docker Compose |
| CI/CD | GitHub Actions |

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/veiculos/` | Cadastrar novo veículo |
| `GET` | `/veiculos/<placa>` | Buscar veículo por placa |
| `GET` | `/veiculos/` | Listar todos os veículos |

### Exemplo — Cadastrar

```bash
curl -X POST http://localhost:5000/veiculos/ \
  -H "Content-Type: application/json" \
  -d '{"placa":"ABC1234","marca":"Toyota","modelo":"Corolla","ano":2022,"cor":"Prata","dono":"João Silva"}'
```

### Exemplo — Buscar

```bash
curl http://localhost:5000/veiculos/ABC1234
```

## Como executar localmente

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar a aplicação
python run.py
```

## Como executar com Docker

```bash
# Usando docker-compose (imagem do Docker Hub)
docker-compose up

# Ou build local
docker build -t cadastro-veiculos .
docker run -p 5000:5000 cadastro-veiculos
```

## Imagem Docker

```
docker pull seuusuario/cadastro-veiculos:latest
```

> 🔗 [Docker Hub — cadastro-veiculos](https://hub.docker.com/r/seuusuario/cadastro-veiculos)

## Testes

```bash
pytest tests/ -v --cov=app
```

10 testes cobrindo: cadastro válido, placa duplicada, placa inválida, ano inválido, campos ausentes, busca existente, busca inexistente, placa Mercosul, listagem vazia e listagem após cadastro.

## Pipeline CI/CD

```
push / PR  →  build-and-test (py3.11 + py3.12)
           →  lint (paralelo)
                  ↓
              package (artefato zip)
                  ↓
              docker push (somente main)
```

### Secrets necessários no repositório

| Secret | Descrição |
|--------|-----------|
| `API_KEY` | Chave de API fictícia |
| `DOCKERHUB_USERNAME` | Usuário Docker Hub |
| `DOCKERHUB_TOKEN` | Access Token Docker Hub |

## Respostas às perguntas do trabalho

**O que acontece se um teste falhar?**
O step `pytest` retorna código de saída diferente de zero, fazendo o job falhar imediatamente. Os jobs seguintes (`package`, `docker`) não são executados graças ao `needs`.

**Em que cenário real o upload de artefato é útil?**
Em deploys manuais, auditoria de versão ou quando a equipe precisa baixar o binário gerado sem precisar fazer checkout e buildar localmente.

**Por que não commitar credenciais no código?**
Qualquer pessoa com acesso ao repositório (presente ou futuro, via histórico git) teria acesso às credenciais. Secrets do GitHub são armazenados de forma criptografada e nunca expostos nos logs.

**Diferença entre tag `latest` e tag por SHA?**
`latest` sempre aponta para a versão mais recente — útil em ambientes de desenvolvimento. A tag por SHA (ex: `abc1234...`) é imutável e identifica exatamente qual commit gerou aquela imagem — essencial em produção para rollback e rastreabilidade.

## Integrantes

- _Nome 1_
- _Nome 2_
- _Nome 3_
