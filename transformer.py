from lark import Transformer, v_args, Token

# Decorador que permite passar os argumentos inline (sem lista)
@v_args(inline=True)
class PlaylistTransformer(Transformer):
    def __init__(self):
        # Lista para armazenar erros semânticos detectados durante a transformação
        self.errors = []

    # === Terminais (Tokens) ===
    # Transforma uma string com aspas escapadas para seu valor literal
    ESCAPED_STRING = lambda self, s: s[1:-1].replace('\\"', '"')

    # Converte o token INT em um número inteiro
    INT = lambda self, n: int(n)

    # === Regras Sintáticas (Não-terminais) ===
    # Regra inicial da gramática: retorna o resultado ou os erros detectados
    def start(self, playlist):
        if self.errors:
            return {"status": "falha", "erros": self.errors}
        return {"status": "sucesso", "playlist": playlist}

    # Trata o cabeçalho da playlist: nome, duração máxima, gênero, ano, faixa etária
    def playlist_cabecalho(self, nome, duracao_max, genero, ano, faixa_etaria):
        return {
            "nome": nome,
            "duracao_max": duracao_max,
            "genero": genero,
            "ano": ano,
            "faixa_etaria": faixa_etaria,
        }

    # Constrói a estrutura principal da playlist, validando regras semânticas
    def playlist(self, cabecalho, descricao, *musicas):
        lista_musicas = list(musicas)
        
        # Monta o dicionário final da playlist com base nos dados capturados
        playlist_final = {
            "nome": cabecalho["nome"],
            "duracao_maxima": cabecalho["duracao_max"],
            "genero": cabecalho["genero"],
            "ano": cabecalho["ano"],
            "faixa_etaria": cabecalho["faixa_etaria"],
            "descricao": descricao if descricao is not None else "", 
            "musicas": lista_musicas,
            "duracao_total": sum(m['duracao'] for m in lista_musicas)
        }

        # === Validações Semânticas para a Playlist ===
        # Verifica se a duração máxima é positiva
        if playlist_final["duracao_maxima"] <= 0:
            self.errors.append(f"Erro Semântico: Duração máxima da playlist '{playlist_final['nome']}' deve ser positiva.")

        # Verifica se o ano da playlist não está no futuro
        if playlist_final["ano"] > 2025: 
            self.errors.append(f"Erro Semântico: Ano da playlist '{playlist_final['nome']}' ({playlist_final['ano']}) não pode ser no futuro.")

        # Validação da faixa etária: deve ser "LIVRE" ou um valor de 0 a 18
        faixa = playlist_final["faixa_etaria"]
        if isinstance(faixa, int) and not (0 <= faixa <= 18):
            self.errors.append(f"Erro Semântico: Faixa etária '{faixa}' para '{playlist_final['nome']}' inválida. Deve ser LIVRE ou entre 0 e 18.")

        # Validação da duração total das músicas em relação à duração máxima
        if playlist_final["duracao_total"] > playlist_final["duracao_maxima"]:
            self.errors.append(f"Erro Semântico: Duração total das músicas ({playlist_final['duracao_total']} min) excede a duração máxima da playlist '{playlist_final['nome']}' ({playlist_final['duracao_maxima']} min).")

        return playlist_final

    # Captura o texto da descrição da playlist
    def descricao(self, texto):
        return texto

    # Trata a faixa etária, que pode ser um número (ex: 12) ou o token 'LIVRE'
    def faixa_etaria(self, valor):
        if isinstance(valor, Token) and valor.type == 'LIVRE':
            return valor.value  
        return valor 

    # Constrói o dicionário de uma música, com validação semântica da duração
    def musica(self, titulo, autor, duracao):
        if duracao <= 0:
            self.errors.append(f"Erro Semântico: Duração da música '{titulo}' por '{autor}' ({duracao} min) deve ser positiva.")

        return {
            "titulo": titulo,
            "autor": autor,
            "duracao": duracao
        }
