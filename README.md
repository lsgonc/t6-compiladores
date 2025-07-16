# Playlist Language Compiler

Linguagem criada como parte do trabalho final da disciplina de Compiladores, destinada à definição e validação de playlists musicais com suporte a metadados estruturados.

### Como funciona?
A linguagem permite definir uma playlist através de um arquivo de texto com uma estrutura clara e obrigatória. O compilador lê este arquivo, valida sua sintaxe e semântica, e gera uma página representativa da playlist.

A estrutura de uma playlist é composta por três partes principais:
- **Cabeçalho da Playlist (Obrigatório)**: Define os metadados principais.
- **Descrição (Opcional)**: Um texto livre para descrever a playlist.
- **Músicas (Obrigatório, pelo menos uma)**: A lista de faixas que compõem a playlist. A imagem de capa é opcional.

<br>

Modelo básico de utilização da linguagem:
```
PLAYLIST "nome-da-playlist"
DURACAO_MAXIMA {número} min
GENERO "genero-da-playlist"
ANO {número}
FAIXA_ETARIA {"LIVRE" || número}

DESCRICAO "descricao-da-playlist"

MUSICA "musica1" AUTOR "autor1" DURACAO {número} min CAPA "url-da-imagem1"
MUSICA "musica2" AUTOR "autor2" DURACAO {número} min CAPA "url-da-imagem2"
```
<br>

> Cada arquivo passado pelo compilador é capaz de definir uma única playlist.

<br>

## 📦 Arquivos

Este projeto está organizado nos seguintes arquivos:

- `gramatica.lark` → Gramática da linguagem. Define todas as regras sintáticas e léxicas da nossa linguagem de playlists.
- `parser.py` → Cria o analisador sintático a partir da gramática. Sua única função é gerar um parser do Lark pronto para uso.
- `transformer.py` → Realiza a análise semântica. Valida a lógica do código e transforma os dados em uma estrutura Python.
- `html_generator.py` → Realiza a criação da página HTML.
- `main.py` → Fluxo principal do compilador.
- `requirements.txt` → Dependências do projeto.

<br>

## 📑 Exemplos de uso

O projeto também inclui arquivos contendo casos de teste utilizados para validar a linguagem desenvolvida, abrangendo diferentes cenários de uso e possíveis erros.

- `caso-teste-01.txt` → Exemplo correto
- `caso-teste-02.txt` → Exemplo com erros léxicos
- `caso-teste-03.txt` → Exemplo com erros sintáticos
- `caso-teste-[04-10].txt` → Exemplo com erros semânticos

<br>

## 🛠 Guia de uso

```bash
git clone (https://github.com/lsgonc/t6-compiladores.git)
cd t6-compiladores
pip install -r requirements.txt
python main.py casos-de-teste/caso-teste-01.txt nome-da-playlist
