# 🎲 Mega-Sena - Ordenação com Radix Sort

Este projeto foi desenvolvido como parte de um estudo em **Algoritmos e Estrutura de Dados II**.
O objetivo é **ordenar resultados da Mega-Sena** utilizando o algoritmo **Radix Sort**, garantindo uma ordenação eficiente dos sorteios em ordem crescente.

---

## 📌 Objetivos do Projeto

- Ler resultados da Mega-Sena a partir de um arquivo CSV.
- Ordenar os números sorteados utilizando **Radix Sort**.
- Apresentar os resultados no formato:
```
Números Sorteados - Sorteio
[01,03,23,27,47,57] - 2683
[01,04,08,21,46,51] - 2667
[01,11,19,20,28,48] - 2700
```

- Salvar os resultados ordenados em um novo arquivo CSV.
- Criar um **randomizador** que embaralha os resultados para simular uma base desordenada.

---

## 📂 Estrutura do Projeto
```
mega-sena-radixsort/
├── data/
│   ├── resultados_ordenados.csv      # resultados finais já ordenados
│   └── resultados_randomizados.csv   # resultados embaralhados
├── ordenar_megasena.py               # script principal (Radix Sort)
└── embaralhar_megasena.py            # script randomizador
```

---

## ⚙️ Como Executar
1️⃣ Clonar o repositório
```
cd seu-diretorio
git clone https://github.com/usuario/mega-sena-radixsort.git
```
2️⃣ Gerar resultados embaralhados
Antes de ordenar, precisamos simular um CSV desordenado:
```
python embaralhar_megasena.py
```
Isso irá gerar o arquivo: ./data/resultados_randomizados.csv

3️⃣ Ordenar com Radix Sort
```
python ordenar_megasena.py
```
Será criado o arquivo final: ./data/resultados_ordenados.csv

🧩 Estrutura dos Arquivos CSV
Arquivo resultados_randomizados.csv (entrada):
```
Concurso;Data;N1;N2;N3;N4;N5;N6
2683;2023-08-15;01;03;23;27;47;57
2667;2023-07-22;01;04;08;21;46;51
```
Arquivo resultados_ordenados.csv (saída):
```
Números Sorteados,Sorteio
"[01,03,23,27,47,57]",2683
"[01,04,08,21,46,51]",2667
```

📊 Exemplo de Execução no Terminal
```
============================================================
ORDENAÇÃO DE RESULTADOS DA MEGA-SENA COM RADIX SORT
============================================================
Total de sorteios lidos: 60
✅ Arquivo salvo: ./data/resultados_ordenados.csv

=== EXEMPLOS DE RESULTADOS ORDENADOS ===
[01,03,23,27,47,57] - 2683
[01,04,08,21,46,51] - 2667
[01,11,19,20,28,48] - 2700
```
📚 Algoritmo Utilizado

O Radix Sort é um algoritmo de ordenação não-comparativo que ordena inteiros processando seus dígitos individuais.