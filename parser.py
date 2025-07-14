from lark import Lark

def create_playlist_parser():
    """Cria e retorna uma instância do parser Lark para a gramática da playlist."""
    with open('gramatica.lark', 'r') as f:
        grammar = f.read()
    # Usamos propagate_positions=False pois não precisamos das posições dos tokens para este compilador simples.
    return Lark(grammar, start='start', parser='lalr', propagate_positions=False)

if __name__ == "__main__":
    # Exemplo de uso para testar o parser
    parser = create_playlist_parser()
    test_input = """
    PLAYLIST "Minha Playlist Favorita" DURACAO_MAXIMA 120 min GENERO "Rock" ANO 2023 FAIXA_ETARIA LIVRE
    DESCRICAO "Uma coleção de rock clássico e moderno."
    MUSICA "Stairway to Heaven" AUTOR "Led Zeppelin" DURACAO 8 min
    MUSICA "Bohemian Rhapsody" AUTOR "Queen" DURACAO 6 min
    """
    try:
        tree = parser.parse(test_input)
        print("Parse Tree gerada com sucesso:")
        print(tree.pretty())
    except Exception as e:
        print(f"Erro ao fazer o parse: {e}")