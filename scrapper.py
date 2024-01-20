import requests
from bs4 import BeautifulSoup

class GameInfo:
    def __init__(self, titulo, nome_jogo, brasao_src, nome_campeonato, data_jogo, horario_jogo):
        self.titulo = titulo
        self.nome_jogo = nome_jogo
        self.brasao_src = brasao_src
        self.nome_campeonato = nome_campeonato
        self.data_jogo = data_jogo
        self.horario_jogo = horario_jogo

def get_games():
    url = 'https://www.espn.com.br/futebol/time/calendario/_/id/2026/bra.sao_paulo'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        div_tables = soup.select('div.ResponsiveTable')

        game_info_list = {}  # Move the dictionary outside the loop

        for table in div_tables:
            title_element = table.find(class_='Table__Title')
            titulo = title_element.text.strip()

            tbody = table.find(class_='Table__TBODY')
            jogos = tbody.find_all(class_='Table__TR')


            for jogo in jogos:
                tables_td = jogo.select('.Table__TD')

                try:
                    adversario_element = tables_td[3].find('div')
                    nome_adversario = adversario_element.find('a').get_text(strip=True)
                    if nome_adversario == 'São Paulo':
                        adversario_element = tables_td[1].find('div')
                        nome_adversario = adversario_element.find('a').get_text(strip=True)
                    nome_jogo = "São Paulo X " + nome_adversario
                except:
                    nome_jogo = 'Erro ao obter nome do jogo'

                try:
                    brasao_element = tables_td[2]
                    element_a = brasao_element.find_all('a', class_='AnchorLink')
                    a_valid = [element_a[0], element_a[2]]
                    
                    for a in a_valid:
                        if 'sao-paulo' not in a.get('href'):
                            element_img = a.find('img')
                            brasao_src = element_img.get('src')
                            break
                    else:
                        brasao_src = 'Brasão do adversário não encontrado'
                except:
                    brasao_src = 'Erro ao obter brasão do adversário'

                try:
                    nome_campeonato = tables_td[5].find('span').get_text(strip=True)
                except:
                    nome_campeonato = 'Erro ao obter nome do campeonato'

                try:
                    data_element = tables_td[0]
                    data_jogo = data_element.find('div').get_text(strip=True)
                except:
                    data_jogo = 'Erro ao obter data'

                try:
                    horario_element = tables_td[4]
                    horario_jogo = horario_element.find('a').get_text(strip=True)
                except:
                    horario_jogo = 'Erro ao obter horário'

                game_info = GameInfo(titulo, nome_jogo, brasao_src, nome_campeonato, data_jogo, horario_jogo)

                if titulo not in game_info_list:
                    game_info_list[titulo] = []
                game_info_list[titulo].append(game_info)

        for title, games in game_info_list.items():
            print(title)
            for game in games:
                print(f"Nome do Jogo: {game.nome_jogo}")
                print(f"Brasão do Adversário: {game.brasao_src}")
                print(f"Nome do Campeonato: {game.nome_campeonato}")
                print(f"Data do Jogo: {game.data_jogo}")
                print(f"Horário do Jogo: {game.horario_jogo}")
                print("-" * 20)

    else:
        print("Erro ao acessar a página:", response.status_code)

get_games()
