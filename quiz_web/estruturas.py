"""
Estruturas de dados utilizadas pelo Quiz Web.

Implementações didáticas e comentadas:

    * Fila (Queue)  - FIFO - usada para a ordem das perguntas.
    * Pilha (Stack) - LIFO - usada para o histórico de respostas.

As estruturas são propositalmente simples (baseadas em `list`) para que
sirvam como material de estudo, deixando claro onde cada operação
acontece no código do sistema.
"""

from __future__ import annotations

from typing import Any, Iterator, List, Optional


class Fila:
    """Fila (FIFO - First In, First Out).

    Aplicada em ``quiz_web/estado.py`` para gerenciar a **ordem das
    perguntas** que serão apresentadas ao jogador durante a partida.
    """

    def __init__(self, itens: Optional[List[Any]] = None) -> None:
        # A fila é mantida em uma lista Python. `enqueue` adiciona ao
        # final; `dequeue` remove do início (FIFO).
        self.itens: List[Any] = list(itens) if itens else []

    def enqueue(self, elemento: Any) -> None:
        """Enfileira um elemento (adiciona ao final da fila)."""
        self.itens.append(elemento)

    def dequeue(self) -> Optional[Any]:
        """Desenfileira o primeiro elemento. Retorna ``None`` se vazia."""
        if self.esta_vazia():
            return None
        return self.itens.pop(0)

    def frente(self) -> Optional[Any]:
        """Retorna (sem remover) o elemento à frente da fila."""
        if self.esta_vazia():
            return None
        return self.itens[0]

    def esta_vazia(self) -> bool:
        return len(self.itens) == 0

    def tamanho(self) -> int:
        return len(self.itens)

    def __iter__(self) -> Iterator[Any]:
        return iter(self.itens)

    def __len__(self) -> int:
        return len(self.itens)


class Pilha:
    """Pilha (LIFO - Last In, First Out).

    Aplicada em ``quiz_web/estado.py`` para armazenar o **histórico de
    respostas** do jogador. Ao final da partida, a tela de resultado
    percorre a pilha (do topo para a base) para exibir as respostas na
    ordem inversa da resposta.
    """

    def __init__(self) -> None:
        self.itens: List[Any] = []

    def push(self, elemento: Any) -> None:
        """Empilha um elemento (adiciona ao topo)."""
        self.itens.append(elemento)

    def pop(self) -> Optional[Any]:
        """Desempilha o elemento do topo. Retorna ``None`` se vazia."""
        if self.is_empty():
            return None
        return self.itens.pop()

    def topo(self) -> Optional[Any]:
        if self.is_empty():
            return None
        return self.itens[-1]

    def is_empty(self) -> bool:
        return len(self.itens) == 0

    def tamanho(self) -> int:
        return len(self.itens)

    def como_lista_topo_primeiro(self) -> List[Any]:
        """Retorna a pilha como lista, do topo para a base."""
        return list(reversed(self.itens))

    def __iter__(self) -> Iterator[Any]:
        # Itera do topo para a base (LIFO).
        return iter(reversed(self.itens))

    def __len__(self) -> int:
        return len(self.itens)
