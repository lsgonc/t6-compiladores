from parser import create_playlist_parser
from transformer import PlaylistTransformer
import json  # Para saída formatada em JSON

def compile_playlist(input_string):
    """
    Compila a string de entrada da playlist, realizando:
    1. Análise sintática (estrutura da linguagem)
    2. Análise semântica (valores válidos e coerentes)
    Retorna os dados da playlist ou uma lista de erros (sintáticos ou semânticos).
    """
    parser = create_playlist_parser()
    transformer = PlaylistTransformer()

    try:
        # Análise Sintática (Parsing)
        print("\nIniciando Análise Sintática...")
        tree = parser.parse(input_string)
        print("Sucesso: Análise Sintática Concluída com Sucesso!")
        
        # Árvore sintática gerada:
        # print("Árvore Sintática (antes da transformação):")
        # print(tree.pretty())

        # Análise Semântica e Transformação da AST 
        print("\nIniciando Análise Semântica e Transformação...")
        transformer.errors.clear()
        playlist_data = transformer.transform(tree)
        print("Sucesso: Análise Semântica e Transformação Concluídas!")

        # Verificação de Erros Semânticos
        if transformer.errors:
            print("\n⚠️ Erros Semânticos Encontrados")
            for error in transformer.errors:
                print(f"- {error}")
            return None, transformer.errors
        else:
            # Sucesso: imprime os dados finais em formato JSON legível
            print("\n✅ Compilação Concluída com Sucesso!")
            print("Dados da Playlist Gerados:")
            
            try:
                # Tenta serializar e imprimir os dados
                json_output = json.dumps(playlist_data, indent=4, ensure_ascii=False)
                print(json_output)
                
                return playlist_data, None

            except TypeError as json_error:
                print("\n❌ Erro ao gerar a saída JSON")
                print(f"Detalhe do erro: {json_error}")
                print(playlist_data)
                
                return playlist_data, [f"Erro de serialização JSON: {json_error}"]

    except Exception as e:
        # Captura erros sintáticos ou de execução
        print("\n❌ Erro na Compilação")
        print(f"Erro: {e}")
        return None, [str(e)]

# Execução direta do script
if __name__ == "__main__":

    # Teste 1: Entrada Válida
    print("COMPILANDO ENTRADA VÁLIDA")
    valid_input = """
    PLAYLIST "Minha Playlist Favorita" DURACAO_MAXIMA 120 min GENERO "Rock" ANO 2023 FAIXA_ETARIA LIVRE
    DESCRICAO "Uma coleção de rock clássico e moderno."
    MUSICA "Stairway to Heaven" AUTOR "Led Zeppelin" DURACAO 8 min
    MUSICA "Bohemian Rhapsody" AUTOR "Queen" DURACAO 6 min
    MUSICA "Hotel California" AUTOR "Eagles" DURACAO 6 min
    """
    compiled_data, errors = compile_playlist(valid_input)
    print("\n" + "="*40 + "\n")

    # Teste 2: Erros Semânticos (ano no futuro, faixa etária inválida, duração negativa)
    print("COMPILANDO ENTRADA COM ERROS SEMÂNTICOS")
    invalid_input_semantic = """
    PLAYLIST "Playlist Problemática" DURACAO_MAXIMA 10 min GENERO "Pop" ANO 2030 FAIXA_ETARIA 20
    MUSICA "Música Longa" AUTOR "Artista X" DURACAO 15 min
    MUSICA "Música Curta" AUTOR "Artista Y" DURACAO 0 min
    """
    compiled_data_invalid, errors_invalid = compile_playlist(invalid_input_semantic)
    print("\n" + "="*40 + "\n")

    # Teste 3: Erro Sintático - falta do token 'min'
    print("COMPILANDO ENTRADA COM ERRO SINTÁTICO (FALTA 'min')")
    invalid_input_syntax_missing_min = """
    PLAYLIST "Playlist Sintaxe Errada" DURACAO_MAXIMA 60 min GENERO "Jazz" ANO 2024 FAIXA_ETARIA LIVRE
    MUSICA "Alguma Coisa" AUTOR "Alguém" DURACAO 4
    """  # Falta o token 'min' após o número 4
    compiled_data_syntax_missing_min, errors_syntax_missing_min = compile_playlist(invalid_input_syntax_missing_min)
    print("\n" + "="*40 + "\n")

    # Teste 4: Erro Sintático - token inesperado (BLABLA não é reconhecido)
    print("COMPILANDO ENTRADA COM ERRO SINTÁTICO (TOKEN INESPERADO)")
    invalid_input_syntax_unexpected_token = """
    PLAYLIST "Playlist Ruim" DURACAO_MAXIMA 60 min GENERO "Rock" ANO 2024 FAIXA_ETARIA LIVRE
    BLABLA "Música Inesperada" AUTOR "Alguém" DURACAO 5 min
    """  # 'BLABLA' não está definido na gramática
    compiled_data_syntax_unexpected_token, errors_syntax_unexpected_token = compile_playlist(invalid_input_syntax_unexpected_token)
