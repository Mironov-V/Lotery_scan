import sys, time
from telebot import TeleBot
sys.path.append('/home/user/Документы/Проекты/')
from AmritaORM.appeal import SELECT_FROM
from AmritaORM.appeal import INSERT_DATA
from models import db_connect


class Main:
    ''' Бот собирает информацию с rapido 100 лото каждые 15 минут и записывает 
        в базу данных. Перед записью сверяет данные с базой. И отправляет пользователю
        те данные которые не совпали с имеющимися в базе.'''
    def __init__(self, token):
        # Инициализация элементов
        self.token = token
        self.rapido = 'https://www.stoloto.ru/rapido/archive'
        self.rapido2 = 'https://www.stoloto.ru/rapido2/archive'
        self.data_list = []

    def app(self):
        # Запись и отправка
        session = TeleBot(token=self.token)

        @session.message_handler(commands='start')
        def message(message):
            # 
            def send_and_select_data(var):
                '''Функция проверяет данные на наличие в базе, если данные
                    не соответствуют то отправляет их пользователю и записывает в базу'''

                for item in var:
                    try:
                        message = f"{item['archive']}\n{item['draw_date']}\n{item['number_circulations']}\n{item['content_circulations']}"
                        INSERT_DATA(
                            db_connect=db_connect,
                            table='RapidoModel',
                            archive = item['archive'],
                            draw_date = item['draw_date'],
                            number_circulations = item['number_circulations'],
                            content_circulations = item['content_circulations'])
                        session.send_message(chat_id='821708906', text=message)
                    except:
                        print('<!ErrorDataSend>')
                # Очищение списка
                del self.data_list[:]


            sys.path.append('/home/user/Документы/Проекты/Lotery_scan/plugins/')
            from rapido.parser import DataScan

            while True:
                # Цикл каждые 15 минут сканирует сайт на наличие новых данных
                send_and_select_data(var=DataScan(data_list=self.data_list).HTML_data(url=self.rapido))
                send_and_select_data(var=DataScan(data_list=self.data_list).HTML_data(url=self.rapido2))


                time.sleep(60)
        # Держать постоянное прослушивание
        session.polling(none_stop=True)
