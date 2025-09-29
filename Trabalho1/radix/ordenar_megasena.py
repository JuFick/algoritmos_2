# -*- coding: utf-8 -*-
import os

def counting_sort(lista_de_sorteios, expoente, obter_chave_func):
    """
    Função auxiliar do Radix Sort que ordena a lista de sorteios
    com base em um dígito específico da chave de ordenação.
    """
    tamanho = len(lista_de_sorteios)
    lista_saida = [None] * tamanho
    contagem = [0] * 10

    # Conta a ocorrência de cada dígito (0 a 9)
    for i in range(tamanho):
        chave = obter_chave_func(lista_de_sorteios[i])
        indice_digito = (chave // expoente) % 10
        contagem[indice_digito] += 1

    # Soma cumulativa para obter as posições finais
    for i in range(1, 10):
        contagem[i] += contagem[i - 1]

    # Constrói a lista de saída de forma estável
    i = tamanho - 1
    while i >= 0:
        sorteio_atual = lista_de_sorteios[i]
        chave = obter_chave_func(sorteio_atual)
        indice_digito = (chave // expoente) % 10
        posicao_final = contagem[indice_digito] - 1
        lista_saida[posicao_final] = sorteio_atual
        contagem[indice_digito] -= 1
        i -= 1

    # Copia a lista ordenada de volta para a lista original
    for i in range(tamanho):
        lista_de_sorteios[i] = lista_saida[i]

def radix_sort(lista_de_sorteios, obter_chave_func):
    """
    Implementa o Radix Sort, ordenando os números dígito por dígito,
    do menos significativo para o mais significativo.
    """
    if not lista_de_sorteios:
        return []

    chave_maxima = max(obter_chave_func(item) for item in lista_de_sorteios)

    expoente = 1
    while chave_maxima // expoente > 0:
        counting_sort(lista_de_sorteios, expoente, obter_chave_func)
        expoente *= 10
    
    return lista_de_sorteios

def gerar_chave_ordenacao(numeros):
    """
    Cria uma chave numérica única para cada sorteio a partir da lista de números.
    Ex: [4, 8, 15] se torna 40815.
    """
    numeros_ordenados = sorted(numeros)
    chave = 0
    base = 100
    for num in numeros_ordenados:
        chave = chave * base + num
    return chave

def carregar_e_processar_dados(caminho_arquivo):
    """
    Lê o arquivo CSV, linha por linha, e transforma os dados em uma
    lista de dicionários para manipulação.
    """
    dados_sorteios = []
    print(f"Lendo o arquivo de dados: {caminho_arquivo}")
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()[1:] # Pula o cabeçalho
            
            for i, linha in enumerate(linhas, 1):
                try:
                    colunas = linha.strip().split(',')

                    if len(colunas) < 8:
                        print(f"Aviso: Linha {i+1} ignorada (formato inválido).")
                        continue
                    
                    concurso = int(colunas[0])
                    numeros = [int(n) for n in colunas[2:8]]
                    chave_ordenacao = gerar_chave_ordenacao(numeros)

                    dados_sorteios.append({
                        "concurso": concurso,
                        "numeros": sorted(numeros),
                        "chave_ordenacao": chave_ordenacao,
                    })
                except (ValueError, IndexError):
                    print(f"Aviso: Linha {i+1} ignorada (dados inválidos).")
                    continue
        
        print(f"-> {len(dados_sorteios)} sorteios carregados com sucesso.")
        return dados_sorteios

    except FileNotFoundError:
        print(f"ERRO: O arquivo '{caminho_arquivo}' não foi encontrado.")
        return []
    except Exception as e:
        print(f"ERRO: Ocorreu um erro inesperado ao ler o arquivo: {e}")
        return []

def salvar_resultados_ordenados(dados, caminho_saida):
    """
    Salva a lista de sorteios ordenada em um novo arquivo CSV.
    """
    print(f"Salvando resultados ordenados em: {caminho_saida}")
    try:
        os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
        with open(caminho_saida, "w", encoding="utf-8", newline="") as arquivo:
            arquivo.write("Números Sorteados,Sorteio\n")
            for sorteio in dados:
                numeros_formatados = f"\"[{','.join([f'{num:02d}' for num in sorteio['numeros']])}]\""
                arquivo.write(f"{numeros_formatados},{sorteio['concurso']}\n")
        print("-> Arquivo salvo com sucesso!")
    except Exception as e:
        print(f"ERRO: Ocorreu um erro ao salvar o arquivo: {e}")

def main():
    """
    Função principal que orquestra todo o processo.
    """
    print("=====================================================")
    print("   Ordenador de Resultados da Mega-Sena com Radix Sort   ")
    print("=====================================================")

    arquivo_entrada = os.path.join("draw-data", "Mega-Sena-Resultados-Randomizados.csv")
    arquivo_saida = os.path.join("draw-data", "Mega-Sena-Resultados-Ordenados-RadixSort.csv")

    todos_os_sorteios = carregar_e_processar_dados(arquivo_entrada)

    if not todos_os_sorteios:
        print("\nNenhum dado foi carregado. O programa será encerrado.")
        return

    print("\nIniciando a ordenação com Radix Sort...")
    sorteios_ordenados = radix_sort(todos_os_sorteios, lambda item: item['chave_ordenacao'])
    print("-> Ordenação concluída.")

    salvar_resultados_ordenados(sorteios_ordenados, arquivo_saida)

    print("\n=====================================================")
    print("     Amostra dos 10 Primeiros Resultados Ordenados    ")
    print("=====================================================")
    print("Números Sorteados   - Concurso")
    print("-----------------------------------------------------")
    for sorteio in sorteios_ordenados[:10]:
        numeros_str = str(sorteio['numeros']).replace(" ", "")
        print(f"{numeros_str} - {sorteio['concurso']}")
    
    print("\nProcesso finalizado com sucesso!")

if __name__ == "__main__":
    main()