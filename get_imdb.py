# Importação das bibliotecas do python
import requests # Para requisições em HTTP
import time # Para cálculo de tempo e simular atrasos (delays)
import csv # Para salvar os resultados em formato de texto .CSV
import random # Para adicionar o recurso de aleatoriedade
import concurrent.futures # Para conseguir rodar threads em paralelo

# Importação de bibliotecas de terceiros
from bs4 import BeautifulSoup # Para conseguir "navegar" no arquivo HTML

# --------------------------------------------------------------------------------------------------------------------------

# Criação do header para burlar alguns mecanismos de proteção do site IMDB e acessar ele pelo python
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Define o máximo de THREADS que podem ser utilizadas ao mesmo tempo
MAX_THREADS = 8

# --------------------------------------------------------------------------------------------------------------------------

# Criação das funções que serão executadas

# =========================

# Função para ler o HTML do site IMDB e extrair as informações, será executada uma vez por filme
def extract_movie_details(movie_link):
    time.sleep(random.uniform(0, 0.2))  # Simula um atraso aleatório entre 0 e 0.2 segundos

    response = requests.get(movie_link, headers=header) # Faz uma requisição HTTP para o link do filme
    movie_soup = BeautifulSoup(response.content, 'html.parser') # Analisa o HTML da resposta da requisição

    if movie_soup is not None: # Verifica se o HTML foi analisado corretamente
        title = None
        date = None

        page_section = movie_soup.find('section', attrs={'class': 'ipc-page-section'})

        if page_section is not None: # Encontra o cabeçalho da página que contém as informações do filme
            divs = page_section.find_all('div', recursive=False)

            if len(divs) > 1:
                target_div = divs[1]

                title_tag = target_div.find('h1')
                if title_tag:
                    title = title_tag.find('span').get_text()

                date_tag = target_div.find('a', href=lambda href: href and 'releaseinfo' in href)
                if date_tag:
                    date = date_tag.get_text().strip()

                rating_tag = movie_soup.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'})
                rating = rating_tag.get_text() if rating_tag else None

                plot_tag = movie_soup.find('span', attrs={'data-testid': 'plot-xs_to_m'})
                plot_text = plot_tag.get_text().strip() if plot_tag else None

                with open('movies.csv', mode='a', newline='', encoding='utf-8') as file:
                    movie_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    if all([title, date, rating, plot_text]):
                        print(title, date, rating, plot_text)
                        movie_writer.writerow([title, date, rating, plot_text])

# =========================

# Função para extrair os filmes da página inicial de filmes populares do IMDB
def extract_movies(soup):
    movies_table = soup.find('div', attrs={'data-testid': 'chart-layout-main-column'}).find('ul')
    movies_table_rows = movies_table.find_all('li')

    # Pega os links dos filmes
    movie_links = ['https://imdb.com' + movie.find('a')['href'] for movie in movies_table_rows]

    # Usa multithreading para acelerar o processo
    threads = min(MAX_THREADS, len(movie_links))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(extract_movie_details, movie_links)

# =========================

# Função principal para coordenar todo o processo
def main():
    start_time = time.time()

    popular_movies_url = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'
    response = requests.get(popular_movies_url, headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')

    extract_movies(soup)

    end_time = time.time()
    print('Total time taken: ', end_time - start_time)

# =========================

if __name__ == '__main__':
    main()