from lark import Transformer, v_args, Token
from urllib.parse import urlparse

class PlaylistTransformer(Transformer):
    def __init__(self):
        # Lista para acumular erros semânticos encontrados durante a transformação
        self.errors = []

    # === Terminais (Tokens) ===
    # Trata strings escapadas: remove as aspas externas e interpreta \" como "
    ESCAPED_STRING = lambda self, s: s[1:-1].replace('\\"', '"')

    # Converte token de número inteiro em inteiro Python
    INT = lambda self, n: int(n)

    # === Regras Sintáticas ===
    def start(self, playlist):
        return playlist[0]

    def playlist(self, items):
        musicas = items[-1]
        
        # Verificamos se a descrição opcional está presente pelo número de itens.
        if len(items) > 6:
            name, max_duration, genre, year, age_rating, description, _ = items
        else:
            name, max_duration, genre, year, age_rating, _ = items
            description = None
            
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

        # Valida se o nome da playlist é válido
        if not name.strip():
            self.errors.append(
                "Erro Semântico: O nome da playlist não pode ser vazio ou conter apenas espaços."
            )

        # Valida o tamanho das descrições
        if description and len(description) > 500:
            self.errors.append(
                f"Aviso Semântico: A descrição da playlist '{name}' é muito longa ({len(description)} caracteres). Considere resumi-la."
            )

        # Validações complexas que dependem de dados das músicas
        total_duration = 0
        if isinstance(musicas, list):
            # Calcula a duração total de forma segura
            total_duration = sum(m.get('duration', 0) for m in musicas if isinstance(m, dict))

            if total_duration > max_duration:
                self.errors.append(
                    f"Erro Semântico: Duração total das músicas ({total_duration} min) excede a duração máxima da playlist '{name}' ({max_duration} min)."
                )

            # Validação de duplicidade e de capas
            seen_songs = set()
            for musica in musicas:
                if not isinstance(musica, dict):
                    continue
                
                # Validação de duplicidade
                title = musica.get('title', '').lower()
                author = musica.get('author', '').lower()
                song_id = (title, author)

                if song_id in seen_songs:
                    self.errors.append(
                        f"Erro Semântico: A música '{musica.get('title')}' por '{musica.get('author')}' está duplicada na playlist '{name}'."
                    )
                seen_songs.add(song_id)
                
                # Validação de formato de URL/Caminho da Capa (segura)
                image_source = musica.get('image_source')
                if image_source:
                    try:
                        result = urlparse(image_source)
                        is_url = all([result.scheme, result.netloc])
                        is_path = not result.scheme and not result.netloc
                        if not is_url and not is_path:
                            self.errors.append(
                                f"Aviso Semântico: A capa '{image_source}' para a música '{musica.get('title')}' não parece ser uma URL válida ou um caminho de arquivo."
                            )
                    except (ValueError, TypeError):
                        self.errors.append(
                            f"Aviso Semântico: Formato de capa inválido para a música '{musica.get('title')}'."
                        )
                        
        # Construção do dicionário
        playlist_data = {
            "name": name,
            "max_duration": max_duration,
            "genre": genre,
            "year": year,
            "age_rating": age_rating,
            "description": description,
            "musicas": musicas,
            "total_duration": total_duration 
        }

        return playlist_data

    def descricao(self, text):
        # A descrição é uma string simples, já processada no terminal ESCAPED_STRING
        return text[0]
    
    def faixa_etaria(self, valor):
        # A regra que chama `faixa_etaria` não tem `v_args`, então recebe uma lista.
        val = valor[0]
        if isinstance(val, Token):
            # Se for um Token, seu valor é "LIVRE". Retornamos a string.
            return val.value
        else:
            # Caso contrário, já é o inteiro que queremos.
            return val

    def capa(self, image_source):
        return image_source[0]
    
    @v_args(inline=True)
    def musicas(self, *musica_list):
        # Coleta a lista de músicas (cada uma já transformada em dicionário)
        return list(musica_list)

    @v_args(inline=True)
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