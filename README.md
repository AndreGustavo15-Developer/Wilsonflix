# Wilsonflix

Wilsonflix é uma aplicação web para exibir filmes, séries e conteúdo infantil populares, consumindo dados de uma API backend que integra informações do The Movie Database (TMDB). O frontend apresenta imagens, sinopses, trailers e avaliações, tudo com uma interface moderna e responsiva.

---

## Tecnologias usadas

- **Backend:** Python, Flask, SQLite, Requests  
- **Frontend:** HTML, CSS, JavaScript, Swiper.js, FontAwesome, Google Fonts  
- **API externa:** The Movie Database (TMDB)

---

## Funcionalidades

- Listagem de mídias por categoria (Populares, Filmes, Séries, Kids).  
- Exibição de detalhes completos (título, sinopse, gêneros, avaliação, trailer).  
- Navegação fácil via menu e sliders com thumbnails.  
- Trailer em overlay e botão “Saiba Mais” para abrir página no TMDB.  
- Atualização periódica dos dados do TMDB para manter a base atualizada.  

---

## Como instalar

### Requisitos

- Python 3.8+  
- pip (gerenciador de pacotes Python)  

### Passos

1. Clone o repositório:
   ```bash
   git clone https://github.com/seuusuario/wilsonflix.git
   cd wilsonflix
   ```
2. Crie e ative um ambiente virtual (opcional, mas recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS  
    venv\Scripts\activate     # Windows
    ```
3. Instale as dependências:
    ```bash
      pip install -r requirements.txt
    ```
4. Configure sua API Key do [TMDB](https://www.themoviedb.org/) (crie uma conta em TMDB e gere a chave).
5. Crie um arquivo .env na raiz do projeto com o conteúdo:
     ```env
     TMDB_API_KEY=your_tmdb_api_key_here
     ```
--- 
## Para executar o backend
1. Atualize a base de dados com os dados do TMDB:
      ```bash
      python cron_update.py
      ```
2. Inicie o servidor Flask:
      ```bash
      python app.py
      ```
O backend estará disponível em `http://localhost:5000/api.`
No arquivo `swiper-configs.js` certifique de modificar a constante `API_URL` para:
      ```bash
      const API_URL = "http://localhost:5000/api";
      ```
      
---
## Como usar o frontend

- Abra o arquivo index.html no navegador (ou sirva via servidor web local).
- A aplicação consumirá automaticamente a API rodando localmente em http://localhost:5000/api.
- Navegue pelas categorias no menu e aproveite os trailers e detalhes.

---
# Descrição do Fluxo

![Wilsonflix diagram](https://github.com/AndreGustavo15-Developer/Wilsonflix/blob/main/assets/Wilsonflix_diagram.jpg)

1. Usuário interage com o Frontend (clicando categorias, trailers, etc).

2. O Frontend envia requisições HTTP (fetch) para o Backend API para obter dados.

3. O Backend API consulta o banco SQLite local para buscar informações já armazenadas.

4. Se os dados não estiverem atualizados ou disponíveis, o Backend consulta o TMDB API para buscar os dados mais recentes.

5. O Backend armazena/atualiza os dados no banco SQLite para futuras requisições.

6. O Backend retorna a resposta JSON para o Frontend.

7. O Frontend atualiza a interface, exibindo imagens, títulos, sinopses, avaliações e trailers.

8. Periodicamente, o script cron_update.py é executado para atualizar a base de dados SQLite, buscando os dados diretamente do TMDB API, garantindo que o sistema tenha informações atualizadas e evitando chamadas diretas frequentes à API externa durante a navegação.













