import os

def counting_sort_custom(data_list, exp, get_key_func):
    """
    Função auxiliar do Radix Sort que ordena a lista de sorteios
    com base em um dígito específico da chave de ordenação.
    """
    n = len(data_list)
    output = [None] * n
    count = [0] * 10

    # Conta a ocorrência de cada dígito (0 a 9)
    for i in range(n):
        key = get_key_func(data_list[i])
        index = (key // exp) % 10
        count[index] += 1

    # Soma cumulativa para obter as posições corretas
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Constrói a lista de saída de forma estável (de trás para frente)
    i = n - 1
    while i >= 0:
        key = get_key_func(data_list[i])
        index = (key // exp) % 10
        output[count[index] - 1] = data_list[i]
        count[index] -= 1
        i -= 1

    # Copia a lista ordenada de volta para a lista original
    for i in range(n):
        data_list[i] = output[i]

def radix_sort_custom(data_list, get_key_func):
    """
    Ordena uma lista de dicionários (sorteios) usando o Radix Sort.
    A ordenação é baseada em uma chave numérica extraída de cada item.
    """
    if not data_list:
        return []

    # Encontra a maior chave para determinar o número de dígitos
    max_key = 0
    for item in data_list:
        key = get_key_func(item)
        if key > max_key:
            max_key = key

    # Aplica o Counting Sort para cada dígito, da direita para a esquerda
    exp = 1
    while max_key // exp > 0:
        counting_sort_custom(data_list, exp, get_key_func)
        exp *= 10
    
    return data_list

def generate_sort_key(numbers):
    """
    Gera uma chave numérica única e grande a partir de uma lista de números.
    A chave garante que a ordenação numérica corresponda à ordenação correta
    dos conjuntos de números.
    Ex: [1, 2, 3] -> 10203
    """
    sorted_numbers = sorted(numbers)
    key = 0
    base = 100
    for num in sorted_numbers:
        key = key * base + num
    return key

def load_and_process_data(file_path):
    """
    Lê os dados de um arquivo CSV, processa cada linha e gera as chaves de ordenação.
    """
    draw_data = []
    print(f"Lendo o arquivo de dados: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            
            # Pula o cabeçalho
            for i, line in enumerate(lines[1:], 1):
                try:
                    # CORREÇÃO: Altera o separador de ';' para ','
                    fields = line.strip().split(',')

                    if len(fields) < 8:
                        print(f"Aviso: Linha {i+1} ignorada (formato inválido, poucas colunas).")
                        continue
                    
                    contest = int(fields[0])
                    # As dezenas estão nas colunas de índice 2 a 7
                    numbers = [int(n) for n in fields[2:8]]
                    
                    sort_key = generate_sort_key(numbers)

                    draw_data.append({
                        "concurso": contest,
                        "numeros": sorted(numbers),
                        "chave_ordenacao": sort_key,
                    })
                except (ValueError, IndexError) as e:
                    print(f"Aviso: Linha {i+1} ignorada (formato inválido). Erro: {e}")
                    continue
        
        print(f"{len(draw_data)} sorteios carregados com sucesso.")
        return draw_data

    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        return []
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao ler o arquivo: {e}")
        return []

def save_sorted_results(data, output_path):
    """
    Salva os dados ordenados em um novo arquivo CSV.
    """
    print(f"Salvando resultados ordenados em: {output_path}")
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8", newline="") as file:
            file.write("Números Sorteados,Sorteio\n")
            for draw in data:
                # Formata os números com zero à esquerda e como uma lista de strings
                formatted_numbers = f"\"[{','.join([f'{num:02d}' for num in draw['numeros']])}]\""
                file.write(f"{formatted_numbers},{draw['concurso']}\n")
        print("Arquivo salvo com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro ao salvar o arquivo: {e}")

def main():
    """
    Função principal que orquestra todo o processo.
    """
    print("========================================")
    print("  Ordenador de Resultados da Mega-Sena  ")
    print("========================================")

    input_file = os.path.join("draw-data", "Mega-Sena-Resultados-Randomizados.csv")
    output_file = os.path.join("draw-data", "Mega-Sena-Resultados-Ordenados-RadixSort.csv")

    # 1. Carregar e processar dados
    all_draws = load_and_process_data(input_file)

    if not all_draws:
        print("Nenhum dado foi carregado. O programa será encerrado.")
        return

    # 2. Ordenar com Radix Sort
    print("\nIniciando a ordenação com Radix Sort...")
    sorted_draws = radix_sort_custom(all_draws, lambda item: item['chave_ordenacao'])
    print("Ordenação concluída.")

    # 3. Salvar os resultados
    save_sorted_results(sorted_draws, output_file)

    # 4. Exibir uma amostra
    print("\n========================================")
    print("  Amostra dos Primeiros Resultados Ordenados")
    print("========================================")
    print("Números Sorteados   - Sorteio")
    print("========================================")
    for draw in sorted_draws[:10]:
        numbers_str = str(draw['numeros']).replace(" ", "")
        print(f"{numbers_str} - {draw['concurso']}")
    
    print("\nProcesso finalizado com sucesso!")

if __name__ == "__main__":
    main()

