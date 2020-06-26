import requests, sys
from bs4 import BeautifulSoup


class Connect:
    # Класс подключения к серверу
    def __init__(self):
        # Инициализация элементов подключения
        self.headers = {
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
            }
    
    def query(self, url):
        query = requests.get(url=url, headers=self.headers)

        if query.status_code == 200:
            return query.text
        else:
            return f'Error: status - {query.status_code}'

class DataScan(Connect):
    # Класс DataScan наследуется от класса Connect и забирает данные со страницы
    def __init__(self, data_list):
        # Инициализация элементов класса родителя
        super().__init__()
        self.data = data_list

    def HTML_data(self, url):
        soup = BeautifulSoup(self.query(url=url), 'lxml')
        items_data = soup.find_all(class_='elem')

        for item in items_data:
            draw_date = str(item.find(class_='draw_date').text).split()
            number_circulations = item.find('a').text
            content_circulations = str(item.find_all('b')).replace('<b>', '').replace('</b>', '').replace(',', '').replace('<b class="extra">', '').replace('[', '').replace(']', '')
            
            # Проверка на версию архивов Rapido
            urls = url.split('/')
            if urls[-2] == 'rapido2':
                archive = 'Rapido 2.0'
            elif urls[-2] == 'rapido':
                archive = 'Rapido'
            # Если в content_circulations присутствуют числа [5, 10, 15, 20] ничего не делаем
            if '5' in content_circulations and '10' in content_circulations and '15' or content_circulations and '20' in content_circulations:
                pass
            else:   # иначе записываем данные в список
                self.data.append({
                    'archive': archive.strip(),
                    'draw_date': f'Информация о тираже от - {draw_date[0]} время - {draw_date[1]}'.strip(),
                    'number_circulations': f'Номер тиража: {number_circulations}'.strip(),
                    'content_circulations': f'Выпадающие цифры: {content_circulations}'.replace('\xa0', '')
                    })

        return self.data
