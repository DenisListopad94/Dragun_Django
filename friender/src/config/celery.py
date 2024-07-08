
import os
from celery import Celery

# Установка переменной окружения, чтобы Celery знал, где найти настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создание экземпляра Celery
app = Celery('booking_service')

# Загрузка настроек из файла настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач в приложениях Django
app.autodiscover_tasks()




app.conf.beat_schedule = {
    # выполняется каждые 3 минуты 40 секунд 
    'add_numbers_every_3m40s': {
        'task': 'booking_service.tasks.add_numbers',
        'schedule': 220,  # 3 минуты 40 секунд в секундах
    },
    # 3 раза с 19 до 21 часов, по разу каждый час
    'multiply_numbers_3_times_between_19_and_21': {
        'task': 'booking_service.tasks.multiply_numbers',
        'schedule': {
            'crontab': '0 19-21 * * *',  # запускать каждый час с 19 до 21 часа
            'options': {
                'expires': 3600 * 2,  # время жизни задачи 2 часа
                'expires_method': 'skip'
            }
        },
    },
}