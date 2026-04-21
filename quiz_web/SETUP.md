# Quiz Web · Passo-a-passo para rodar do zero

Este é o caminho **mais curto possível**, **sem virtualenv**: só Python instalado e um duplo clique.

---

## 1) Instalar o Python 3 (uma vez só)

### Windows
1. Baixe em https://www.python.org/downloads/windows/
2. Execute o instalador e **marque a caixinha "Add python.exe to PATH"** antes de clicar em *Install Now*.
3. Abra o **Prompt de Comando** e confira:
   ```
   py -V
   ```
   Deve aparecer algo como `Python 3.12.x`.

### macOS
1. Baixe em https://www.python.org/downloads/macos/ e instale o `.pkg`.
   *(ou, se já usa Homebrew: `brew install python`)*
2. Confira no Terminal:
   ```
   python3 -V
   ```

### Linux (Ubuntu / Debian / Mint)
```
sudo apt update && sudo apt install -y python3 python3-pip
python3 -V
```

---

## 2) Baixar este projeto

- Se recebeu `quiz_web.zip`: descompacte em qualquer lugar (ex.: Área de Trabalho).
- Se clonou do Git: entre na pasta `oficina-git` normalmente.

Você deve ver uma pasta chamada `quiz_web/` com vários arquivos `.py`.

---

## 3) Rodar (um clique)

### Windows
Dê **duplo clique** em `quiz_web/start.bat`.

Uma janela preta vai abrir, instalar o Flask (só na primeira vez) e mostrar:
```
* Running on http://127.0.0.1:5000
```

### macOS / Linux
No Terminal, dentro da pasta do projeto:
```
bash quiz_web/start.sh
```
*(Se preferir duplo clique: clique com botão direito em `start.sh` → "Executar como programa" / "Abrir com Terminal".)*

O script instala o Flask automaticamente na primeira execução — **você não precisa criar venv**.

---

## 4) Abrir o jogo

Abra o navegador em:

> **http://localhost:5000**

Pronto. Clique em **Jogar agora**.

Para parar o servidor, volte na janela do terminal e aperte **Ctrl + C**.

---

## 5) Cadastrar novas perguntas
No próprio site, clique em **Gerenciar** (ou acesse `http://localhost:5000/admin`), preencha enunciado, alternativas (pelo menos 2) e marque a correta. A nova pergunta entra na **Lista** global e vai aparecer no próximo jogo.

---

## 6) Rodar os testes automáticos (opcional)
Na mesma pasta do projeto:
```
python3 -m unittest quiz_web.test_app -v     # macOS/Linux
py -m unittest quiz_web.test_app -v          # Windows
```
Deve mostrar `Ran 9 tests ... OK`.

---

## 7) Mostrar para outra pessoa na mesma rede (opcional)
Enquanto o servidor está rodando, descubra seu IP local:
- **Windows**: `ipconfig` → procure "Endereço IPv4".
- **macOS**: `ipconfig getifaddr en0`.
- **Linux**: `hostname -I`.

A outra pessoa acessa `http://SEU_IP:5000` pelo navegador (precisa estar no mesmo Wi-Fi e, no Windows, pode ser preciso liberar o firewall).

---

## 8) Se der errado

| Problema | O que fazer |
|---|---|
| `py` ou `python3` "não é reconhecido" | Reinstale o Python marcando "Add to PATH" e reinicie o terminal. |
| `ModuleNotFoundError: flask` | Rode de novo o `start.sh` / `start.bat` — ele instala o Flask. |
| "Port 5000 already in use" | Outro app já usa a porta. Feche-o, ou edite `quiz_web/app.py` e troque `port=5000` por `port=5050`. |
| Página abre sem estilo ou sem confetti | Verifique que tem internet (o Bootstrap, Animate.css e o canvas-confetti vêm de CDN). |
| Timer "travado" na tela de jogo | Atualize a aba (F5). |

---

Feito. Qualquer dúvida, manda print.
