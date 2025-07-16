from parser import create_playlist_parser
from transformer import PlaylistTransformer
from html_generator import HtmlCodeGenerator
import sys
import os
import json

def compile_playlist(input_string, source_filename="playlist"):
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
            print("\n⚠️  Erros Semânticos Encontrados")
            for error in transformer.errors:
                print(f"{error}")
            return None, transformer.errors
        
        # FASE DE GERAÇÃO DE CÓDIGO
        print("\n✅ Compilação Concluída com Sucesso!")

        # 1. Instancia o gerador com os dados da playlist
        generator = HtmlCodeGenerator(playlist_data)
        
        # 2. Gera o conteúdo HTML
        html_content = generator.generate_html()

        # 3. Define o nome do arquivo de saída
        # Ex: se o entrada for 'minha_playlist.pldef', a saída será 'minha_playlist.html'
        output_filename = os.path.splitext(source_filename)[0] + ".html"
        
        # 4. Escreve o arquivo HTML
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"Sucesso: Página da web gerada em '{output_filename}'")
        print("Abra este arquivo em seu navegador para ver o resultado!")

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
        html = sys.argv[2] if len(sys.argv) > 2 else "playlist"

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                # Lê todo o conteúdo do arquivo
                input_code = f.read()
            
            # Chama o compilador com o conteúdo do arquivo
            compile_playlist(input_code, source_filename=html)

        except FileNotFoundError:
            print(f"❌ Erro: Arquivo não encontrado em '{filepath}'")
        except Exception as e:
            print(f"❌ Erro ao ler o arquivo: {e}")

    else:
        print("Insira um arquivo de texto: python main.py <caminho_para_o_arquivo.txt>")