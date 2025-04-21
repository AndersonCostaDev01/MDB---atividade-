# Multithreading

Código para atividade educacional.

Ao executar este código, ele realiza web scraping no site IMDB e armazena informações de filmes como título, data de lançamento, avaliação e sinopse em um arquivo `.csv`.

---

## Passos para execução

### 1. Criação do Ambiente Virtual

```bash
python -m venv .venv
```

### 2. Ativação do Ambiente Virtual

```bash
.venv\Scripts\activate
```

### 3. Instalação das dependências

```bash
pip install -r requirements.txt
```

Se for necessário adicionar novas bibliotecas, utilize:

```bash
pip freeze > requirements.txt
```

---

## Estrutura e Funcionamento

- **Importações**:

  - Bibliotecas nativas do Python para requisições, tempo, escrita de arquivos e paralelismo.
  - Biblioteca externa `BeautifulSoup` para leitura e navegação em HTML.

- **Headers**:

  - Simulam um navegador real para evitar bloqueios no site.

- **Multithreading**:

  - Utiliza até 8 threads para acelerar o processo de scraping.

- **Funções**:

  - `extract_movie_details(link)`: acessa cada página de filme individualmente e coleta os dados necessários.
  - `extract_movies(soup)`: coleta os links dos filmes populares a partir da página principal.
  - `main()`: coordena todo o processo de scraping e salva os dados no arquivo CSV.

- **Saída**:
  - Um arquivo chamado `movies.csv` contendo:
    - Nome do filme
    - Data de lançamento
    - Nota/avaliação
    - Sinopse

---

## Observações importantes

- O site pode mudar a estrutura HTML a qualquer momento, o que pode quebrar o scraper.
- A execução de múltiplas threads simula atrasos aleatórios para parecer mais natural e evitar bloqueios.
- Certifique-se de ter conexão com a internet ativa durante a execução.
