from urllib.parse import quote_plus

class HtmlCodeGenerator:
    """
    Gera uma página web HTML estática a partir dos dados de uma playlist.
    """
    def __init__(self, playlist_data):
        self.data = playlist_data
        self.title = self.data.get("name", "Playlist Sem Título")
        self.description = self.data.get("description", "")
        self.musicas = self.data.get("musicas", [])

    def _generate_css(self):
        """Gera o CSS embutido para a página, definindo o estilo e o layout de grade."""
        return """
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                background-color: #f0f2f5;
                color: #1c1e21;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 900px;
                margin: 0 auto;
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                padding: 20px;
            }
            h1 {
                color: #1877f2;
                border-bottom: 2px solid #ddd;
                padding-bottom: 10px;
            }
            a {
                text-decoration: none;
                color: inherit;      
            }
            .description {
                color: #606770;
                font-style: italic;
                margin-bottom: 20px;
            }
            .music-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                gap: 20px;
            }
            .music-card {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 8px;
                overflow: hidden;
                text-align: center;
                transition: transform 0.2s, box-shadow 0.2s;
                cursor: pointer;
            }
            .music-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
            }
            .album-art {
                width: 100%;
                height: 200px; 
                object-fit: cover; 
                display: block;
            }
            .placeholder-art {
                width: 100%;
                height: 200px;
                background-color: #e0e0e0;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #999;
                font-size: 3em;
                font-weight: bold;
            }
            .music-info {
                padding: 16px;
            }
            .music-title {
                font-weight: bold;
                font-size: 1em;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                margin-bottom: 6px;
            }
            .music-author {
                color: #606770;
                font-size: 0.9em;
            }
        </style>
        """

    def _generate_music_item_html(self, musica):
        """Gera o HTML para um único 'card' de música."""
        title = musica.get("title", "Título Desconhecido")
        author = musica.get("author", "Autor Desconhecido")
        image_source = musica.get("image_source")

        # CONSTRUIR A URL DE BUSCA DO YOUTUBE
        search_term = f"{author} {title}"
        encoded_search_term = quote_plus(search_term)
        youtube_search_url = f"https://www.youtube.com/results?search_query={encoded_search_term}"

        # Define o conteúdo da imagem: ou a capa ou um placeholder
        if image_source:
            art_html = f'<img src="{image_source}" alt="Capa de {title}" class="album-art">'
        else:
            art_html = '<div class="placeholder-art">?</div>'
        
        return f"""
        <a href="{youtube_search_url}" target="_blank" rel="noopener noreferrer" class="music-card-link">
            <div class="music-card" title="{author} - {title}">
                {art_html}
                <div class="music-info">
                    <div class="music-title">{title}</div>
                    <div class="music-author">{author}</div>
                </div>
            </div>
        </a>
        """

    def generate_html(self):
        """Monta e retorna a string completa do arquivo HTML."""
        music_grid_html = "\n".join([self._generate_music_item_html(m) for m in self.musicas])
        
        return f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Playlist: {self.title}</title>
            {self._generate_css()}
        </head>
        <body>
            <div class="container">
                <h1>{self.title}</h1>
                <p class="description">{self.description}</p>
                <div class="music-grid">
                    {music_grid_html}
                </div>
            </div>
        </body>
        </html>
        """