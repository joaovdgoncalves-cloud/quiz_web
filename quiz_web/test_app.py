"""Testes do app Flask do Quiz.

Executar:

    python -m unittest quiz_web.test_app -v
"""

from __future__ import annotations

import unittest

from . import dados, estado
from .app import criar_app
from .estruturas import Fila, Pilha


class TestEstruturas(unittest.TestCase):
    def test_fila_fifo(self) -> None:
        f = Fila()
        self.assertTrue(f.esta_vazia())
        f.enqueue("a")
        f.enqueue("b")
        self.assertEqual(f.frente(), "a")
        self.assertEqual(f.dequeue(), "a")
        self.assertEqual(f.dequeue(), "b")
        self.assertIsNone(f.dequeue())

    def test_pilha_lifo(self) -> None:
        p = Pilha()
        for x in [1, 2, 3]:
            p.push(x)
        self.assertEqual(p.topo(), 3)
        self.assertEqual(p.como_lista_topo_primeiro(), [3, 2, 1])
        self.assertEqual(p.pop(), 3)
        self.assertEqual(p.pop(), 2)
        self.assertEqual(p.pop(), 1)
        self.assertIsNone(p.pop())


class TestDados(unittest.TestCase):
    def setUp(self) -> None:
        dados.resetar_para_padrao()

    def test_adicionar_pergunta_valida(self) -> None:
        tamanho_inicial = len(dados.PERGUNTAS)
        p = dados.adicionar_pergunta(
            "Qual estrutura usa hashing?",
            ["Lista", "Hash Map", "Heap"],
            1,
        )
        self.assertEqual(len(dados.PERGUNTAS), tamanho_inicial + 1)
        self.assertEqual(dados.RESPOSTAS_CORRETAS[p["id"]], 1)

    def test_adicionar_pergunta_invalida(self) -> None:
        with self.assertRaises(ValueError):
            dados.adicionar_pergunta("", ["a", "b"], 0)
        with self.assertRaises(ValueError):
            dados.adicionar_pergunta("?", ["a"], 0)
        with self.assertRaises(ValueError):
            dados.adicionar_pergunta("?", ["a", "b"], 5)


class TestRotasFlask(unittest.TestCase):
    def setUp(self) -> None:
        dados.resetar_para_padrao()
        estado.resetar_estado()
        self.app = criar_app()
        self.app.testing = True
        self.client = self.app.test_client()

    def test_home_carrega(self) -> None:
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Quiz de Estruturas".encode("utf-8"), resp.data)

    def test_iniciar_redireciona_para_jogar(self) -> None:
        resp = self.client.post("/iniciar", follow_redirects=False)
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/jogar", resp.headers["Location"])

    def test_fluxo_completo_acerta_tudo(self) -> None:
        self.client.post("/iniciar")
        total = len(dados.PERGUNTAS)
        for _ in range(total):
            resp = self.client.get("/jogar")
            self.assertEqual(resp.status_code, 200)
            st = estado.obter_estado()
            pergunta_atual = st.pergunta_atual()
            self.assertIsNotNone(pergunta_atual)
            resp = self.client.post(
                "/responder",
                data={"opcao": str(pergunta_atual["correta"])},
                follow_redirects=False,
            )
            self.assertEqual(resp.status_code, 302)

        resp = self.client.get("/resultado")
        self.assertEqual(resp.status_code, 200)
        st = estado.obter_estado()
        self.assertEqual(st.acertos, total)
        self.assertEqual(st.erros, 0)
        self.assertEqual(st.pontuacao, total * 10)
        # pilha deve conter todos os registros
        self.assertEqual(st.historico.tamanho(), total)

    def test_admin_cadastra_pergunta(self) -> None:
        tamanho_inicial = len(dados.PERGUNTAS)
        resp = self.client.post(
            "/admin",
            data={
                "enunciado": "Nova pergunta de teste?",
                "opcao_1": "Alt A",
                "opcao_2": "Alt B",
                "opcao_3": "Alt C",
                "correta": "2",
            },
            follow_redirects=True,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(dados.PERGUNTAS), tamanho_inicial + 1)
        nova = dados.PERGUNTAS[-1]
        self.assertEqual(nova["enunciado"], "Nova pergunta de teste?")
        self.assertEqual(nova["correta"], 2)
        self.assertEqual(dados.RESPOSTAS_CORRETAS[nova["id"]], 2)

    def test_admin_rejeita_invalido(self) -> None:
        resp = self.client.post(
            "/admin",
            data={
                "enunciado": "",
                "opcao_1": "",
                "correta": "0",
            },
            follow_redirects=True,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Erro".encode("utf-8"), resp.data)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
