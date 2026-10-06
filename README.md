# Sistema de Estoque

Projeto "DevOps para projetos web" da turma Aponti FAP DevOps 5 (2026), Grupo 4.

Sistema web simples de estoque: o usuario se cadastra, faz login e, depois de logado, cadastra e consulta produtos.

> Em desenvolvimento (parte 1). Este README vai sendo completado por cada area.

## Stack

| Camada | Tecnologia |
| --- | --- |
| Backend e API | Python 3.12+ com FastAPI |
| Banco de dados | PostgreSQL |
| Frontend | HTML, CSS e JavaScript |
| Testes | pytest |

## Como rodar (base atual)

```bash
git clone https://github.com/Fililpe/Projeto-DevOps-para-projetos-web.git
cd Projeto-DevOps-para-projetos-web
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Abrir http://localhost:8000/api/health. Tem que responder `{"status":"ok"}`.

TODO (Dados e Backend): passos do banco e do arquivo `.env`.

## Testes

```bash
pytest
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
