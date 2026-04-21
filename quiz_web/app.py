"""
Aplicação Flask do Quiz de Estruturas de Dados.

Rotas:

    GET  /                -> página inicial (iniciar jogo / admin)
    POST /iniciar         -> monta a FILA da partida e vai para /jogar
    GET  /jogar           -> mostra a pergunta da frente da fila
    POST /responder       -> valida resposta via DICIONÁRIO e empilha na PILHA
    GET  /resultado       -> pontuação + histórico (PILHA, topo primeiro)
    GET  /admin           -> formulário de cadastro de perguntas
    POST /admin           -> salva nova pergunta na LISTA global

Estruturas aplicadas (em comentários no código):

    * LISTA      -> ``dados.PERGUNTAS``
    * FILA       -> ``estado.fila``        (ordem das perguntas do jogo)
    * PILHA      -> ``estado.historico``   (histórico de respostas)
    * DICIONÁRIO -> ``dados.RESPOSTAS_CORRETAS`` (ID -> resposta correta)
"""

from __future__ import annotations

from typing import List

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from . import dados
from .estado import obter_estado


PONTOS_POR_ACERTO = 10


def criar_app() -> Flask:
    """Factory do app Flask."""
    app = Flask(__name__)
    app.secret_key = "oficina-git-quiz-estruturas"  # apenas para flash messages

    # -------------------------------------------------------------------
    # Página inicial
    # -------------------------------------------------------------------
    @app.route("/")
    def home() -> str:
        return render_template(
            "index.html",
            total_perguntas=len(dados.PERGUNTAS),
        )

    
    # Iniciar jogo
    
    @app.route("/iniciar", methods=["POST"])
    def iniciar():
        estado = obter_estado()
        # LISTA global -> FILA da partida (cópia para não mutar a lista).
        estado.reiniciar(dados.snapshot_perguntas())
        if estado.fila.esta_vazia():
            flash("Nenhuma pergunta cadastrada. Cadastre ao menos uma em /admin.", "warning")
            return redirect(url_for("home"))
        return redirect(url_for("jogar"))

  
    # Tela de jogo
    -
    @app.route("/jogar")
    def jogar():
        estado = obter_estado()
        if not estado.iniciada:
            flash("Inicie o jogo pela página principal.", "info")
            return redirect(url_for("home"))
        if estado.terminou():
            return redirect(url_for("resultado"))

        pergunta = estado.pergunta_atual()  # FRENTE da fila
        numero_atual = estado.total_inicial - estado.fila.tamanho() + 1
        feedback = estado.feedback_ultimo
        estado.feedback_ultimo = None  # feedback é one-shot
        return render_template(
            "jogar.html",
            pergunta=pergunta,
            numero=numero_atual,
            total=estado.total_inicial,
            pontuacao=estado.pontuacao,
            feedback=feedback,
        )

    
    # Processar resposta
    
    @app.route("/responder", methods=["POST"])
    def responder():
        estado = obter_estado()
        if not estado.iniciada or estado.fila.esta_vazia():
            return redirect(url_for("home"))

        try:
            escolha = int(request.form.get("opcao", "-1"))
        except ValueError:
            escolha = -1

        # Validação usando o DICIONÁRIO ``RESPOSTAS_CORRETAS`` e
        # empilhando o registro na PILHA ``estado.historico``.
        estado.responder(escolha, pontos_por_acerto=PONTOS_POR_ACERTO)

        if estado.terminou():
            return redirect(url_for("resultado"))
        return redirect(url_for("jogar"))

    # -------------------------------------------------------------------
    # Resultado final
    # -------------------------------------------------------------------
    @app.route("/resultado")
    def resultado():
        estado = obter_estado()
        if not estado.iniciada:
            return redirect(url_for("home"))
        total = estado.acertos + estado.erros
        aproveitamento = (estado.acertos / total * 100) if total else 0.0
        # Percorre a PILHA do topo para a base (ordem inversa da resposta).
        historico = estado.historico_topo_primeiro()
        return render_template(
            "resultado.html",
            pontuacao=estado.pontuacao,
            acertos=estado.acertos,
            erros=estado.erros,
            total=total,
            aproveitamento=aproveitamento,
            historico=historico,
        )

    # -------------------------------------------------------------------
    # Área administrativa
    # -------------------------------------------------------------------
    @app.route("/admin", methods=["GET", "POST"])
    def admin():
        if request.method == "POST":
            enunciado = request.form.get("enunciado", "").strip()
            # Coleta alternativas (até 6 campos opcionais).
            opcoes: List[str] = []
            for i in range(1, 7):
                valor = request.form.get(f"opcao_{i}", "").strip()
                if valor:
                    opcoes.append(valor)
            try:
                correta = int(request.form.get("correta", "-1"))
            except ValueError:
                correta = -1

            try:
                # Atualiza a LISTA global e o DICIONÁRIO de respostas.
                pergunta = dados.adicionar_pergunta(enunciado, opcoes, correta)
            except ValueError as exc:
                flash(f"Erro ao cadastrar pergunta: {exc}", "danger")
                return render_template(
                    "admin.html",
                    perguntas=dados.PERGUNTAS,
                    form={
                        "enunciado": enunciado,
                        "opcoes": opcoes,
                        "correta": correta,
                    },
                )

            flash(
                f'Pergunta #{pergunta["id"]} cadastrada com sucesso. '
                "Ela entrará na fila do próximo jogo.",
                "success",
            )
            return redirect(url_for("admin"))

        return render_template("admin.html", perguntas=dados.PERGUNTAS, form=None)

    return app


app = criar_app()


if __name__ == "__main__":  # pragma: no cover
    app.run(host="0.0.0.0", port=5000, debug=True)
