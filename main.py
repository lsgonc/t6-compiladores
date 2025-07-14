from parser import create_playlist_parser
from transformer import PlaylistTransformer
import json # Para output bonito

def compile_playlist(input_string):
    """
    Compila a string de entrada da playlist, realizando análise sintática e semântica.
    Retorna os dados da playlist ou uma lista de erros.
    """
    parser = create_playlist_parser()
    transformer = PlaylistTransformer()

    try:
        # 1. Análise Sintática (Parsing)
        print("\n--- Iniciando Análise Sintática ---")
        tree = parser.parse(input_string)
        print("Análise Sintática Concluída.")
        # print("Árvore Sintática (antes da transformação):")
        # print(tree.pretty()) # Descomente para ver a árvore antes da transformação

        # 2. Análise Semântica e Construção da AST Final
        print("\n--- Iniciando Análise Semântica e Transformação ---")
        playlist_data = transformer.transform(tree)
        print("Análise Semântica e Transformação Concluídas.")

        if transformer.errors:
            print("\n--- Erros Semânticos Encontrados ---")
            for error in transformer.errors:
                print(f"- {error}")
            return None, transformer.errors
        else:
            print("\n--- Compilação Concluída com Sucesso! ---")
            print("Dados da Playlist Gerados:")
            print(json.dumps(playlist_data, indent=4, ensure_ascii=False))
            return playlist_data, None

    except Exception as e:
        print(f"\n--- Erro na Compilação ---")
        print(f"Erro: {e}")
        return None, [str(e)]

if __name__ == "__main__":
    print("= COMPILANDO ENTRADA VÁLIDA =")
    valid_input = """
    PLAYLIST "Minha Playlist Favorita" DURACAO_MAXIMA 120 min GENERO "Rock" ANO 2023 FAIXA_ETARIA LIVRE
    DESCRICAO "Uma coleção de rock clássico e moderno."
    MUSICA "Stairway to Heaven" AUTOR "Led Zeppelin" DURACAO 8 min
    MUSICA "Bohemian Rhapsody" AUTOR "Queen" DURACAO 6 min
    MUSICA "Hotel California" AUTOR "Eagles" DURACAO 6 min
    """
    compiled_data, errors = compile_playlist(valid_input)
    print("\n" + "="*40 + "\n")

    print("\n= COMPILANDO ENTRADA COM ERROS SEMÂNTICOS =")
    invalid_input_semantic = """
    PLAYLIST "Playlist Problemática" DURACAO_MAXIMA 10 min GENERO "Pop" ANO 2030 FAIXA_ETARIA 20
    MUSICA "Música Longa" AUTOR "Artista X" DURACAO 15 min
    MUSICA "Música Curta" AUTOR "Artista Y" DURACAO 0 min
    """
    compiled_data_invalid, errors_invalid = compile_playlist(invalid_input_semantic)
    print("\n" + "="*40 + "\n")

    # Exemplo para demonstrar um ERRO SINTÁTICO REAL (falta 'min')
    print("\n= COMPILANDO ENTRADA COM ERRO SINTÁTICO (FALTA 'min') =")
    invalid_input_syntax_missing_min = """
    PLAYLIST "Playlist Sintaxe Errada" DURACAO_MAXIMA 60 min GENERO "Jazz" ANO 2024 FAIXA_ETARIA LIVRE
    MUSICA "Alguma Coisa" AUTOR "Alguém" DURACAO 4
    """ # Falta o 'min' após a duração
    compiled_data_syntax_missing_min, errors_syntax_missing_min = compile_playlist(invalid_input_syntax_missing_min)
    print("\n" + "="*40 + "\n")

    # Exemplo para demonstrar um ERRO SINTÁTICO REAL (token inesperado)
    print("\n= COMPILANDO ENTRADA COM ERRO SINTÁTICO (TOKEN INESPERADO) =")
    invalid_input_syntax_unexpected_token = """
    PLAYLIST "Playlist Ruim" DURACAO_MAXIMA 60 min GENERO "Rock" ANO 2024 FAIXA_ETARIA LIVRE
    BLABLA "Música Inesperada" AUTOR "Alguém" DURACAO 5 min
    """ # BLABLA não é um token esperado
    compiled_data_syntax_unexpected_token, errors_syntax_unexpected_token = compile_playlist(invalid_input_syntax_unexpected_token)
    print("\n" + "="*40 + "\n")