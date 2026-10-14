# Sistema de Estoque

Projeto "DevOps para projetos web" da turma Aponti FAP DevOps 5 (2026), Grupo 4.

Sistema web simples de estoque: o usuario se cadastra, faz login e, depois de logado, cadastra e consulta produtos.

> Em desenvolvimento (parte 1). Este README vai sendo completado por cada area.

## Stack

| Camada | Tecnologia |
| --- | --- |
| Backend e API | Python 3.12+ com FastAPI (validado no Python 3.14.7) |
| Banco de dados | PostgreSQL |
| Frontend | HTML, CSS e JavaScript |
| Testes | pytest |

## Como obter o projeto

```bash
git clone https://github.com/Fililpe/Projeto-DevOps-para-projetos-web.git
cd Projeto-DevOps-para-projetos-web
```

## Como instalar as dependencias

As dependencias diretas do projeto possuem versoes fixas no arquivo
`requirements.txt`.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Linux e macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Como configurar e executar

1. Copie `.env.example` para `.env`.
2. Preencha as variaveis do PostgreSQL e defina uma `SECRET_KEY` com pelo
   menos 32 caracteres.
3. Crie as tabelas utilizando `backend/db.sql`.
4. Inicie a API:

```powershell
python -m uvicorn backend.main:app --reload
```

Abra http://localhost:8000/api/health. A resposta deve ser
`{"status":"ok"}`.

## Testes

```powershell
python -m pytest -v
```

## Como contribuir

1. Ninguem faz push direto na `main`. Todo codigo entra por Pull Request.
2. Uma branch por card do Trello, saindo da `main` atualizada:

| Tipo | Exemplo de branch |
| --- | --- |
| Funcionalidade | `feat/login` |
| Correcao | `fix/validacao-email` |
| Documentacao | `docs/rotas-api` |
| Ajuste de estrutura | `chore/dependencias` |

3. Commits no padrao Conventional Commits, em portugues:

```
feat: adiciona rota de login
fix: corrige senha sem hash no cadastro
docs: documenta rotas de produtos
test: adiciona testes do cadastro
```

4. Antes de abrir o PR: rodar `pytest` e conferir que passou.
5. O Tech Lead revisa e faz o merge.

## Documentacao

- [Arquitetura](docs/arquitetura.md)

## Equipe

| Papel | Pessoa |
| --- | --- |
| Tech Lead | Filipe |
| Scrum Master | Pedro |
| Backend | Vitor, Otavio |
| Dados | Felipe Gomes |
| Frontend | Nelson |
