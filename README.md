# Playlist Language Compiler

Linguagem para criação de playlists musicais com metadados.

---

## 📦 Arquivos

- `playlist.lark` → gramática da linguagem
- `compilador.py` → parser, semântica, interpretação
- `requirements.txt` → dependências
- `exemplo_valido.txt` → exemplo correto
- `exemplo_erro.txt` → exemplo com erros semânticos

---

## ▶️ Como usar

```bash
git clone <URL_DO_SEU_REPO>
cd playlist_compilador
pip install -r requirements.txt
python compilador.py casos-de-teste/caso-teste-01.txt
