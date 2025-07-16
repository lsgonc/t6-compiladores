from lark import Transformer, v_args, Token

@v_args(inline=True) 
class PlaylistTransformer(Transformer):
    def __init__(self):
        # Armazena os dados da playlist sendo processada (usado para validações cruzadas)
        self.current_playlist_data = {}
        # Lista para acumular erros semânticos encontrados durante a transformação
        self.errors = []

    # === Terminais (Tokens) ===

    # Trata strings escapadas: remove as aspas externas e interpreta \" como "
    ESCAPED_STRING = lambda self, s: s[1:-1].replace('\\"', '"')

    # Converte token de número inteiro em inteiro Python
    INT = lambda self, n: int(n)

    # === Regras Sintáticas ===
    def start(self, playlist):
        # A regra 'start' apenas retorna o dicionário da playlist transformada
        return playlist

    def playlist(self, name, max_duration, genre, year, age_rating, description, musicas):
        # Monta o dicionário da playlist com todos os campos coletados
        self.current_playlist_data = {
            "name": name,
            "max_duration": max_duration,
            "genre": genre,
            "year": year,
            "age_rating": age_rating,
            "description": description,
            "musicas": musicas,
            "total_duration": sum(m['duration'] for m in musicas) 
        }

        # === Validações Semânticas da Playlist ===

        # Valida se a duração máxima da playlist é positiva
        if max_duration <= 0:
            self.errors.append(
                f"Erro Semântico: Duração máxima da playlist '{name}' deve ser positiva."
            )

        # Impede que o ano da playlist seja no futuro
        if year > 2025: 
            self.errors.append(
                f"Erro Semântico: Ano da playlist '{name}' ({year}) não pode ser no futuro."
            )

        # Valida faixa etária numérica (se for int, deve estar entre 0 e 18)
        if isinstance(age_rating, int) and (age_rating < 0 or age_rating > 18):
            self.errors.append(
                f"Erro Semântico: Faixa etária '{age_rating}' para '{name}' inválida. Deve ser 'LIVRE' ou entre 0 e 18."
            )

        # Valida se a soma das músicas excede o tempo máximo da playlist
        if self.current_playlist_data["total_duration"] > max_duration:
            self.errors.append(
                f"Erro Semântico: Duração total das músicas ({self.current_playlist_data['total_duration']} min) excede a duração máxima da playlist '{name}' ({max_duration} min)."
            )

        return self.current_playlist_data

    def descricao(self, text):
        # A descrição é uma string simples, já processada no terminal ESCAPED_STRING
        return text
    
    def faixa_etaria(self, valor):
        if isinstance(valor, Token):
            # Se for um Token, seu valor é "LIVRE". Retornamos a string.
            return valor.value
        else:
            # Caso contrário, já é o inteiro que queremos.
            return valor

    def capa(self, image_source):
        return image_source
    
    def musicas(self, *musica_list):
        # Coleta a lista de músicas (cada uma já transformada em dicionário)
        return list(musica_list)

    def musica(self, title, author, duration, capa=None):

        # === Validações Semânticas da Música ===
        # Verifica se a duração da música é positiva
        if duration <= 0:
            self.errors.append(
                f"Erro Semântico: Duração da música '{title}' por '{author}' ({duration} min) deve ser positiva."
            )

        # Retorna os dados da música em formato de dicionário
        return {
            "title": title,
            "author": author,
            "duration": duration,
            "image_source": capa 
        }
