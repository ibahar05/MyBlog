from celery import shared_task
from time import sleep
import requests

@shared_task
def sendEmail():
    sleep(3)
    print("done sending email")