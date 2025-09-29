import os
import sys

def counting_sort_custom(data_list, exponent, get_key_func):
    """
    Função auxiliar do Radix Sort (Counting Sort) que ordena uma lista de objetos
    (dicionários, neste caso) com base em um dígito específico da chave de ordenação.
    """
    n = len(data_list)
    output = [None] * n
    count = [0] * 10

    # Conta a ocorrência de cada dígito (0-9)
    for item in data_list:
        key_value = get_key_func(item)
        digit = (key_value // exponent) % 10
        count[digit] += 1

    # Transforma 'count' para que contenha as posições finais de cada dígito
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Constrói a lista de saída ordenada
    i = n - 1
    while i >= 0:
        item = data_list[i]
        key_value = get_key_func(item)
        digit = (key_value // exponent) % 10
        output_index = count[digit] - 1
        output[output_index] = item
        count[digit] -= 1
        i -= 1

    # Copia o resultado de volta para a lista original
    for i in range(n):
        data_list[i] = output[i]

def radix_sort_custom(data_list, get_key_func):
    """
    Implementação do Radix Sort que ordena uma lista de objetos (dicionários)
    com base em uma chave numérica extraída por 'get_key_func'.
    """
    if not data_list:
        return []

    # Encontra o valor máximo da chave para determinar o número de dígitos
    max_key = 0
    for item in data_list:
        key_value = get_key_func(item)
        if key_value > max_key:
            max_key = key_value

    # Aplica o Counting Sort para cada dígito, do menos para o mais significativo
    exponent = 1
    while max_key // exponent > 0:
        counting_sort_custom(data_list, exponent, get_key_func)
        exponent *= 10
    
    return data_list

def generate_sort_key(numbers):
    """
    Cria uma chave de ordenação numérica única a partir de uma lista de números.
    Os números são primeiro ordenados e depois combinados em um grande inteiro
    para permitir a ordenação lexicográfica.
    Ex: [1, 2, 3] -> 100020003
    """
    sorted_numbers = sorted(numbers)
    key = 0
    # Usamos 100 como base, pois os números da Mega-Sena vão de 1 a 60.
    base = 100 
    for num in sorted_numbers:
        key = key * base + num
    return key

def load_and_process_data(file_path):
    """
    Lê o arquivo CSV com os resultados, processa cada linha e prepara os dados
    para a ordenação.
    """
    draw_data = []
    print(f"Lendo o arquivo de dados: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # Pula o cabeçalho
            next(f) 
            for line_num, line in enumerate(f, 2):
                try:
                    parts = line.strip().split(";")
                    if len(parts) < 8:
                        print(f"Aviso: Linha {line_num} ignorada (formato inválido).")
                        continue
                    
                    contest = int(parts[0])
                    numbers = [int(n) for n in parts[2:8]]
                    
                    draw_data.append({
                        "concurso": contest,
                        "numeros": sorted(numbers),
                        "chave_ordenacao": generate_sort_key(numbers)
                    })
                except (ValueError, IndexError) as e:
                    print(f"Aviso: Erro ao processar linha {line_num}: {e}. Linha ignorada.")
    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao ler o arquivo: {e}")
        return None
        
    print(f"{len(draw_data)} sorteios carregados com sucesso.")
    return draw_data

def save_sorted_results(sorted_data, file_path):
    """
    Salva os dados ordenados em um novo arquivo CSV no formato solicitado.
    """
    print(f"Salvando resultados ordenados em: {file_path}")
    try:
        # Garante que o diretório de saída exista
        output_dir = os.path.dirname(file_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(file_path, "w", encoding="utf-8", newline="") as f:
            f.write("Numeros Sorteados,Sorteio\n")
            for draw in sorted_data:
                # Formata os números com dois dígitos (ex: 01, 09, 10)
                formatted_numbers = "[" + ",".join(f"{num:02d}" for num in draw["numeros"]) + "]"
                f.write(f"\"{formatted_numbers}\",{draw['concurso']}\n")
        print("Arquivo salvo com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")

def display_results_sample(sorted_data, count=10):
    """
    Exibe uma amostra dos resultados ordenados no console.
    """
    print("\n" + "="*40)
    print("  Amostra dos Primeiros Resultados Ordenados")
    print("="*40)
    print("Números Sorteados   - Sorteio")
    
    # Limita a exibição ao número de resultados disponíveis
    display_count = min(count, len(sorted_data))
    
    for i in range(display_count):
        draw = sorted_data[i]
        formatted_numbers = "[" + ",".join(f"{num:02d}" for num in draw["numeros"]) + "]"
        print(f"{formatted_numbers} - {draw['concurso']}")
    print("="*40)


def main():
    """
    Função principal que orquestra a execução do script.
    """
    print("\n--- Ordenador de Resultados da Mega-Sena com Radix Sort ---")
    
    # Define os caminhos dos arquivos de entrada e saída.
    # Certifique-se de que o arquivo de entrada está no local correto.
    input_file = os.path.join("draw-data", "Mega-Sena-Resultados-Randomizados.csv")
    output_file = os.path.join("draw-data", "Mega-Sena-Resultados-Ordenados-RadixSort.csv")

    # 1. Carregar e processar os dados
    all_draws = load_and_process_data(input_file)
    
    if all_draws is None:
        sys.exit(1) # Encerra o script se houver erro na leitura do arquivo

    # 2. Ordenar os dados usando Radix Sort
    print("\nIniciando a ordenação com Radix Sort...")
    sorted_draws = radix_sort_custom(all_draws, lambda item: item['chave_ordenacao'])
    print("Ordenação concluída.")

    # 3. Salvar os resultados em um novo arquivo
    save_sorted_results(sorted_draws, output_file)

    # 4. Exibir uma amostra no console
    display_results_sample(sorted_draws)

    print("\nProcesso finalizado com sucesso!")


if __name__ == "__main__":
    main()