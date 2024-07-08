from celery import shared_task
import time

@shared_task
def add_numbers(x, y):
    time.sleep(5)
    return x + y

@shared_task
def multiply_numbers(x, y):
    time.sleep(10)
    return x * y