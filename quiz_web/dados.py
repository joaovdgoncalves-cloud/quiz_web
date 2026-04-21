"""
Repositório global de perguntas do sistema.

- ``PERGUNTAS`` é uma **Lista** Python (requisito do desafio: "Lista para
  manter o repositório global de perguntas cadastradas").
- ``RESPOSTAS_CORRETAS`` é um **Dicionário / Hash Map** que associa o ID
  de cada pergunta à sua resposta correta (acesso O(1) durante a
  validação, requisito do desafio).

Ambas as estruturas são reconstruídas em conjunto pelas funções
``adicionar_pergunta`` e ``remover_pergunta``, garantindo consistência.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


# ESTRUTURA DE DADOS: LISTA

# Repositório global de perguntas cadastradas. Cada pergunta é um dict
# com as chaves: id, enunciado, opcoes (lista), correta (índice 0-based).
PERGUNTAS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "enunciado": "Qual estrutura segue o princípio FIFO?",
        "opcoes": ["Pilha", "Fila", "Árvore", "Grafo"],
        "correta": 1,
    },
    {
        "id": 2,
        "enunciado": "Qual estrutura segue o princípio LIFO?",
        "opcoes": ["Fila", "Lista ligada", "Pilha", "Hash Map"],
        "correta": 2,
    },
    {
        "id": 3,
        "enunciado": "Qual estrutura mapeia chaves a valores com acesso médio O(1)?",
        "opcoes": ["Árvore binária", "Dicionário / Hash Map", "Fila", "Lista"],
        "correta": 1,
    },
    {
        "id": 4,
        "enunciado": "Qual estrutura é usada naturalmente no algoritmo BFS?",
        "opcoes": ["Pilha", "Fila", "Heap", "Árvore AVL"],
        "correta": 1,
    },
    {
        "id": 5,
        "enunciado": "Qual estrutura é usada naturalmente em DFS iterativo?",
        "opcoes": ["Fila", "Pilha", "Conjunto", "Hash Map"],
        "correta": 1,
    },
]



# ESTRUTURA DE DADOS: DICIONÁRIO (HASH MAP)
# Mapeia id_pergunta -> índice da resposta correta. Permite validação
# O(1) quando o usuário envia uma resposta a partir do formulário.

RESPOSTAS_CORRETAS: Dict[int, int] = {p["id"]: p["correta"] for p in PERGUNTAS}


def proximo_id() -> int:
    """Retorna o próximo ID disponível para cadastro."""
    if not PERGUNTAS:
        return 1
    return max(p["id"] for p in PERGUNTAS) + 1


def adicionar_pergunta(
    enunciado: str, opcoes: List[str], correta: int
) -> Dict[str, Any]:
    """Cadastra uma nova pergunta na lista global e atualiza o dicionário.

    Levanta ``ValueError`` se os dados forem inválidos.
    """
    enunciado = (enunciado or "").strip()
    opcoes = [o.strip() for o in opcoes if o and o.strip()]

    if not enunciado:
        raise ValueError("O enunciado não pode ser vazio.")
    if len(opcoes) < 2:
        raise ValueError("É necessário pelo menos 2 alternativas.")
    if not (0 <= correta < len(opcoes)):
        raise ValueError("Índice da resposta correta fora do intervalo.")

    pergunta = {
        "id": proximo_id(),
        "enunciado": enunciado,
        "opcoes": opcoes,
        "correta": correta,
    }
    PERGUNTAS.append(pergunta)             # LISTA global atualizada
    RESPOSTAS_CORRETAS[pergunta["id"]] = correta  # HASH MAP atualizado
    return pergunta


def buscar_pergunta(id_: int) -> Optional[Dict[str, Any]]:
    """Busca linear na lista global (simples e suficiente para o demo)."""
    for p in PERGUNTAS:
        if p["id"] == id_:
            return p
    return None


def snapshot_perguntas() -> List[Dict[str, Any]]:
    """Cópia rasa da lista (usada para construir a fila do jogo)."""
    return [dict(p) for p in PERGUNTAS]


def resetar_para_padrao() -> None:
    """Restaura o repositório para o conjunto inicial (usado em testes)."""
    PERGUNTAS.clear()
    RESPOSTAS_CORRETAS.clear()
    PERGUNTAS.extend(
        [
            {
                "id": 1,
                "enunciado": "Qual estrutura segue o princípio FIFO?",
                "opcoes": ["Pilha", "Fila", "Árvore", "Grafo"],
                "correta": 1,
            },
            {
                "id": 2,
                "enunciado": "Qual estrutura segue o princípio LIFO?",
                "opcoes": ["Fila", "Lista ligada", "Pilha", "Hash Map"],
                "correta": 2,
            },
            {
                "id": 3,
                "enunciado": "Qual estrutura mapeia chaves a valores com acesso médio O(1)?",
                "opcoes": ["Árvore binária", "Dicionário / Hash Map", "Fila", "Lista"],
                "correta": 1,
            },
            {
                "id": 4,
                "enunciado": "Qual estrutura é usada naturalmente no algoritmo BFS?",
                "opcoes": ["Pilha", "Fila", "Heap", "Árvore AVL"],
                "correta": 1,
            },
            {
                "id": 5,
                "enunciado": "Qual estrutura é usada naturalmente em DFS iterativo?",
                "opcoes": ["Fila", "Pilha", "Conjunto", "Hash Map"],
                "correta": 1,
            },
        ]
    )
    for p in PERGUNTAS:
        RESPOSTAS_CORRETAS[p["id"]] = p["correta"]
