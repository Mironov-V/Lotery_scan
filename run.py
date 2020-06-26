from settings import BASE_SETTINGS
from main import Main


''' Для того что бы можно было масштабировать приложение
    без урона базовой функциональности, все плагины должны
    подключаться в файле "run" '''

if __name__ == "__main__":
    try:
        print('<!Bot-Success>')
        app = Main(token=BASE_SETTINGS['access_token'])
        app.app()
    except:
        print('<!Bot-ErrorConnectServer>')
