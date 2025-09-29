# 📄 Guia Rápido: Ordenador da Mega-Sena
Este guia mostra como usar o script Python para ordenar os resultados da Mega-Sena de forma rápida e fácil.

### 🎯 O que o projeto faz?
Lê um arquivo .csv com os resultados dos sorteios da Mega-Sena.

Ordena todos os sorteios em ordem crescente, com base nos números sorteados.

Salva o resultado ordenado em um novo arquivo .csv.

O algoritmo de ordenação utilizado é o Radix Sort.

### 📁 O que você precisa?
A estrutura de pastas deve ser a seguinte:

```.
├── draw-data/
│   └── Mega-Sena-Resultados-Randomizados.csv  # Seu arquivo de dados aqui
└── nome_do_seu_projeto.py                    # O script principal
```
- O script: nome_do_seu_projeto.py.
- Uma pasta: chamada draw-data.

Seu arquivo de dados: com o nome Mega-Sena-Resultados-Randomizados.csv, localizado dentro da pasta draw-data. 
Baixar do site oficial da CAIXA: https://loterias.caixa.gov.br/Paginas/mega-sena.aspx?utm_source=chatgpt.com

### ▶️ Como executar
Siga os 3 passos abaixo:

✔️ Pré-requisitos:

- Ter o Python 3 instalado.

📁 Estrutura:

- Garanta que o seu arquivo .csv com os resultados está na pasta draw-data.

🚀 Execução:

- Abra seu terminal, navegue até a pasta do projeto e rode o comando:
```
python nome_do_seu_projeto.py
```
Pronto! Um novo arquivo com os resultados ordenados será criado na pasta draw-data.