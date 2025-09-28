"""
Trabalho: Randomizador de Resultados da Mega-Sena
Disciplina: Algoritmos e Estrutura de Dados II
Autor: Estudante
Data: Setembro/2025

Descrição:
- Este script lê um arquivo CSV com resultados já ordenados
- Embaralha a ordem das linhas de forma aleatória
- Salva em um novo arquivo CSV sem alterar os dados originais
"""

import csv
import random
import os


def embaralhar_csv(entrada, saida):
    if not os.path.exists(entrada):
        print(f"❌ Arquivo não encontrado: {entrada}")
        return

    with open(entrada, "r", encoding="utf-8") as f:
        leitor = csv.reader(f)
        cabecalho = next(leitor)
        linhas = list(leitor)

    random.shuffle(linhas)

    with open(saida, "w", encoding="utf-8", newline="") as f:
        escritor = csv.writer(f)
        escritor.writerow(cabecalho)
        escritor.writerows(linhas)

    print(f"✅ Arquivo embaralhado salvo em: {saida}")
    print(f"Total de sorteios processados: {len(linhas)}")
    print("Exemplo (primeiras 2 linhas após embaralhar):")
    for l in linhas[:2]:
        print(l)


if __name__ == "__main__":
    print("=== RANDOMIZADOR DE RESULTADOS DA MEGA-SENA ===")

    entrada = "./data/resultados_ordenados.csv"
    saida = "./data/resultados_randomizados.csv"

    embaralhar_csv(entrada, saida)
    print("🎉 Processo concluído com sucesso!")