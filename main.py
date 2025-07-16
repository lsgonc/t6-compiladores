from parser import create_playlist_parser
from transformer import PlaylistTransformer
import sys
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
            print("Dados da Playlist Gerados: \n")
            
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
    # Verifica se um nome de arquivo foi passado como argumento na linha de comando
    if len(sys.argv) > 1:
        # Pega o nome do arquivo do primeiro argumento (índice 1)
        filepath = sys.argv[1]

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                # Lê todo o conteúdo do arquivo
                input_code = f.read()
            
            # Chama o compilador com o conteúdo do arquivo
            compile_playlist(input_code)

        except FileNotFoundError:
            print(f"❌ Erro: Arquivo não encontrado em '{filepath}'")
        except Exception as e:
            print(f"❌ Erro ao ler o arquivo: {e}")

    else:
        print("Insira um arquivo de texto: python main.py <caminho_para_o_arquivo.txt>")