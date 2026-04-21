# Quiz Web - Estruturas de Dados (Flask)

Aplicação web em **Python + Flask** para um quiz interativo sobre
Estruturas de Dados, com área de **gerenciamento de perguntas**.

## Estruturas aplicadas (back-end)

| Estrutura | Papel | Onde no código |
|-----------|-------|----------------|
| **Lista** | Repositório global de perguntas cadastradas. | `dados.PERGUNTAS` |
| **Fila (Queue)** | Ordem das perguntas apresentadas no jogo. | `estruturas.Fila` / `estado.fila` |
| **Pilha (Stack)** | Histórico de respostas (exibido ao final). | `estruturas.Pilha` / `estado.historico` |
| **Dicionário (Hash Map)** | Mapeia `id da pergunta -> resposta correta` (acesso O(1)). | `dados.RESPOSTAS_CORRETAS` |

## Como rodar

```bash
# instalar dependências (apenas Flask)
pip install -r quiz_web/requirements.txt

# rodar o servidor
python -m quiz_web.app
# -> acesse http://localhost:5000

# rodar testes
python -m unittest quiz_web.test_app -v
```

## Páginas

- `/` **Início** - botão para iniciar o quiz e acessar o gerenciamento.
- `/jogar` **Área de Jogo** - uma pergunta por vez (FILA), feedback
  imediato (Correto/Incorreto) e pontuação.
- `/resultado` - pontuação total e histórico (PILHA, topo primeiro).
- `/admin` **Gerenciamento** - formulário para cadastrar novas
  perguntas, que entram na LISTA global e na FILA do próximo jogo.

## Requisitos funcionais atendidos

- [x] Página inicial com botões para iniciar e gerenciar.
- [x] Pergunta por vez consumindo a **Fila**.
- [x] Feedback imediato + pontuação acumulada.
- [x] Formulário no `/admin` para cadastrar perguntas que alimentam a
      **Lista** global e entram na **Fila** do próximo jogo.
- [x] Tela final com pontuação e histórico via **Pilha**.
- [x] Validação das respostas via **Dicionário** (`id -> correta`).
- [x] Interface responsiva (Bootstrap 5 via CDN).
