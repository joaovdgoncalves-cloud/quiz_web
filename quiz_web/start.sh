#!/usr/bin/env bash
# Inicia o Quiz Web em um clique (macOS / Linux).
# 1) Descobre um Python 3 instalado
# 2) Instala o Flask (modo usuário, sem sudo e sem venv)
# 3) Sobe o servidor em http://localhost:5000

set -e

# Este script mora dentro da pasta "quiz_web". Queremos rodar a partir do pai,
# porque o comando é `python -m quiz_web.app`.
cd "$(dirname "$0")/.."

if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "Nao encontrei Python 3 no PATH."
  echo "Instale em https://www.python.org/downloads/ e rode de novo."
  exit 1
fi

echo ">> Instalando Flask (so se ainda nao tiver)..."
"$PY" -m pip install --user --quiet --disable-pip-version-check flask

echo ">> Abrindo http://localhost:5000  (Ctrl+C para parar)"
exec "$PY" -m quiz_web.app
