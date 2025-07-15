from lark import Transformer, v_args, Token

@v_args(inline=True)    # Faz com que os filhos das regras sejam passados diretamente
class PlaylistTransformer(Transformer):
    def __init__(self):
        self.current_playlist_data = {} # Armazena dados da playlist atual para validações
        self.errors = [] # Lista para coletar erros semânticos

    # --- Terminais (Tokens) ---
    ESCAPED_STRING = lambda self, s: s[1:-1].replace('\\"', '"') # Remove aspas e trata escapes
    INT = lambda self, n: int(n)

    # --- Regras Sintáticas ---

    def start(self, playlist):
        # A regra 'start' apenas passa a playlist
        return playlist

    def playlist(self, name, max_duration, genre, year, age_rating, description, musicas):
        self.current_playlist_data = {
            "name": name,
            "max_duration": max_duration,
            "genre": genre,
            "year": year,
            "age_rating": age_rating,
            "description": description,
            "musicas": musicas,
            "total_duration": sum(m['duration'] for m in musicas) # Soma as durações das músicas
        }

        # --- Validações Semânticas para Playlist ---

        if max_duration <= 0:
            self.errors.append(f"Erro Semântico: Duração máxima da playlist '{name}' deve ser positiva.")

        if year > 2025: # Ajuste o ano conforme a necessidade
            self.errors.append(f"Erro Semântico: Ano da playlist '{name}' ({year}) não pode ser no futuro.")

        if isinstance(age_rating, int) and (age_rating < 0 or age_rating > 18):
            self.errors.append(f"Erro Semântico: Faixa etária '{age_rating}' para '{name}' inválida. Deve ser LIVRE ou entre 0 e 18.")

        if self.current_playlist_data["total_duration"] > max_duration:
             self.errors.append(f"Erro Semântico: Duração total das músicas ({self.current_playlist_data['total_duration']} min) excede a duração máxima da playlist '{name}' ({max_duration} min).")

        return self.current_playlist_data

    def descricao(self, text):
        return text

    def idade(self, age):
        if isinstance(age, Token):
            return age.value
        return age

    def musicas(self, *musica_list):
        # music_list é uma tupla de dicionários de músicas
        return list(musica_list)

    def musica(self, title, author, duration):
        # --- Validações Semânticas para Música ---
        if duration <= 0:
            self.errors.append(f"Erro Semântico: Duração da música '{title}' por '{author}' ({duration} min) deve ser positiva.")

        # Retorna um dicionário para facilitar o acesso aos dados da música
        return {
            "title": title,
            "author": author,
            "duration": duration
        }