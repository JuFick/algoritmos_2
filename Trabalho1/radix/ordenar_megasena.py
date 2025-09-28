"""
Trabalho: Ordenação de Resultados da Mega-Sena usando Radix Sort
Disciplina: Algoritmos e Estrutura de Dados II
Data: Setembro/2025

Descrição:
- Este script lê um arquivo CSV com sorteios da Mega-Sena em ordem aleatória
- Ordena os resultados usando o algoritmo Radix Sort
- Salva os resultados organizados em um novo arquivo CSV
- Exibe estatísticas e alguns exemplos no terminal
"""

import csv
import os


# ------------------ ALGORITMOS ------------------

def counting_sort_por_digito(vetor, exp):
    """Ordena vetor de inteiros com base em um dígito específico (exp)."""
    tamanho = len(vetor)
    saida = [0] * tamanho
    contagem = [0] * 10

    for valor in vetor:
        digito = (valor // exp) % 10
        contagem[digito] += 1

    for i in range(1, 10):
        contagem[i] += contagem[i - 1]

    for i in range(tamanho - 1, -1, -1):
        digito = (vetor[i] // exp) % 10
        saida[contagem[digito] - 1] = vetor[i]
        contagem[digito] -= 1

    for i in range(tamanho):
        vetor[i] = saida[i]


def radix_sort(vetor):
    """Implementa o algoritmo Radix Sort para inteiros não-negativos."""
    if not vetor:
        return vetor

    maior = max(vetor)
    exp = 1
    while maior // exp > 0:
        counting_sort_por_digito(vetor, exp)
        exp *= 10
    return vetor


# ------------------ PROCESSAMENTO ------------------

def gerar_chave_hash(numeros):
    """
    Gera uma chave numérica única a partir da combinação de dezenas.
    Multiplica cada número por uma potência de 100 para preservar ordem.
    """
    chave = 0
    for i, valor in enumerate(sorted(numeros)):
        chave += valor * (100 ** (len(numeros) - 1 - i))
    return chave


def ordenar_resultados(arquivo_entrada, arquivo_saida):
    if not os.path.exists(arquivo_entrada):
        print(f"❌ Arquivo não encontrado: {arquivo_entrada}")
        return

    sorteios = []

    with open(arquivo_entrada, "r", encoding="utf-8") as f:
        leitor = csv.reader(f, delimiter=";")
        cabecalho = next(leitor, None)

        for linha in leitor:
            try:
                concurso = int(linha[0])
                dezenas = list(map(int, linha[2:8]))
                chave = gerar_chave_hash(dezenas)

                sorteios.append({
                    "concurso": concurso,
                    "numeros": sorted(dezenas),
                    "chave": chave
                })
            except Exception as e:
                print(f"⚠️ Erro ao processar linha: {linha} -> {e}")

    print(f"Total de sorteios lidos: {len(sorteios)}")

    # Ordenação com Radix Sort
    chaves = [s["chave"] for s in sorteios]
    radix_sort(chaves)

    sorteios_ordenados = []
    usadas = set()
    for chave in chaves:
        for idx, s in enumerate(sorteios):
            if idx not in usadas and s["chave"] == chave:
                sorteios_ordenados.append(s)
                usadas.add(idx)
                break

    # Salvando em CSV
    with open(arquivo_saida, "w", encoding="utf-8", newline="") as f:
        escritor = csv.writer(f)
        escritor.writerow(["Números Sorteados", "Sorteio"])
        for s in sorteios_ordenados:
            dezenas_fmt = "[" + ",".join(f"{n:02d}" for n in s["numeros"]) + "]"
            escritor.writerow([dezenas_fmt, s["concurso"]])

    print(f"✅ Arquivo salvo: {arquivo_saida}")

    # Estatísticas
    print("\n=== EXEMPLOS DE RESULTADOS ORDENADOS ===")
    for s in sorteios_ordenados[:5]:
        dezenas_fmt = "[" + ",".join(f"{n:02d}" for n in s["numeros"]) + "]"
        print(f"{dezenas_fmt} - {s['concurso']}")
    print("...")
    for s in sorteios_ordenados[-5:]:
        dezenas_fmt = "[" + ",".join(f"{n:02d}" for n in s["numeros"]) + "]"
        print(f"{dezenas_fmt} - {s['concurso']}")


# ------------------ MAIN ------------------

if __name__ == "__main__":
    print("=" * 60)
    print("ORDENAÇÃO DE RESULTADOS DA MEGA-SENA COM RADIX SORT")
    print("=" * 60)

    entrada = "./data/resultados_randomizados.csv"
    saida = "./data/resultados_ordenados.csv"

    ordenar_resultados(entrada, saida)
