"""
Estado da partida atual (singleton em memória).

Este módulo concentra o **estado mutável** do jogo: a fila de perguntas
a serem apresentadas e a pilha de histórico de respostas. Como o sistema
é um demo local de usuário único, o estado é mantido em nível de módulo
(in-memory) — em produção usaríamos sessões persistentes ou banco de
dados.

Estruturas aplicadas aqui:

    * **Fila (Queue)**  -> ordem das perguntas da partida atual.
    * **Pilha (Stack)** -> histórico de respostas do jogador.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from . import dados
from .estruturas import Fila, Pilha


@dataclass
class RegistroResposta:
    """Entrada empilhada na pilha de histórico."""

    pergunta_id: int
    enunciado: str
    opcao_escolhida: str
    opcao_correta: str
    acertou: bool


@dataclass
class EstadoPartida:
    """Singleton com o estado do jogo em andamento."""

    fila: Fila = field(default_factory=Fila)
    historico: Pilha = field(default_factory=Pilha)
    pontuacao: int = 0
    acertos: int = 0
    erros: int = 0
    total_inicial: int = 0
    iniciada: bool = False
    feedback_ultimo: Optional[Dict[str, Any]] = None

    def reiniciar(self, perguntas: List[Dict[str, Any]]) -> None:
        """Monta uma nova partida a partir da lista global de perguntas."""
        self.fila = Fila(list(perguntas))    # FILA: ordem de apresentação
        self.historico = Pilha()             # PILHA: histórico zerado
        self.pontuacao = 0
        self.acertos = 0
        self.erros = 0
        self.total_inicial = self.fila.tamanho()
        self.iniciada = True
        self.feedback_ultimo = None

    def pergunta_atual(self) -> Optional[Dict[str, Any]]:
        """Retorna a pergunta no topo da fila sem removê-la."""
        return self.fila.frente()

    def responder(self, indice_escolhido: int, pontos_por_acerto: int = 10) -> RegistroResposta:
        """Consome a pergunta da fila, empilha o registro e atualiza o placar.

        Usa o **dicionário** ``dados.RESPOSTAS_CORRETAS`` para validar em
        tempo O(1).
        """
        pergunta = self.fila.dequeue()
        if pergunta is None:
            raise RuntimeError("Nenhuma pergunta disponível na fila.")

        correta_idx = dados.RESPOSTAS_CORRETAS.get(pergunta["id"], pergunta["correta"])
        acertou = indice_escolhido == correta_idx

        if acertou:
            self.pontuacao += pontos_por_acerto
            self.acertos += 1
        else:
            self.erros += 1

        opcao_escolhida = (
            pergunta["opcoes"][indice_escolhido]
            if 0 <= indice_escolhido < len(pergunta["opcoes"])
            else "<inválida>"
        )
        registro = RegistroResposta(
            pergunta_id=pergunta["id"],
            enunciado=pergunta["enunciado"],
            opcao_escolhida=opcao_escolhida,
            opcao_correta=pergunta["opcoes"][correta_idx],
            acertou=acertou,
        )
        self.historico.push(registro)       # PILHA de histórico
        self.feedback_ultimo = {
            "acertou": acertou,
            "opcao_correta": registro.opcao_correta,
            "enunciado": pergunta["enunciado"],
        }
        return registro

    def terminou(self) -> bool:
        return self.iniciada and self.fila.esta_vazia()

    def historico_topo_primeiro(self) -> List[RegistroResposta]:
        """Retorna o histórico do topo para a base (última resposta primeiro)."""
        return self.historico.como_lista_topo_primeiro()


# Singleton acessado pelas rotas do Flask.
_estado = EstadoPartida()


def obter_estado() -> EstadoPartida:
    return _estado


def resetar_estado() -> None:
    """Usado em testes para limpar entre cenários."""
    global _estado
    _estado = EstadoPartida()
