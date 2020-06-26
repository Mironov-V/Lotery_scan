import sys
sys.path.append('/home/user/Документы/Проекты/')
from AmritaORM.SettingsConnect.connect import data_session_connection
from AmritaORM.SettingsMigrations.migrations import Migration
from AmritaORM.engineer import Models


db_connect = data_session_connection(SUBD='sqlite', dbname='rapido_db.sql')

class RapidoModel(Models):

    def model(self):
        archive = self.CharField(name='archive')
        draw_date = self.CharField(name='draw_date')
        number_circulations = self.CharField(name='number_circulations')
        content_circulations = self.CharField(name='content_circulations', unique=True)

        return Migration(RapidoModel.__name__, archive, draw_date, number_circulations, content_circulations).makemigration(connectDB=db_connect)

RapidoModel().model()   # Создание базы данных