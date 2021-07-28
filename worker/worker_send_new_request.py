import pika
import json
import os
import django
from django.core.mail import send_mail

os.chdir(os.getcwd()+"/../")

from project.settings import EMAIL_HOST_USER

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")


django.setup()


def send_new_request(ch, method, properties, body):
    '''

    '''
    body = json.loads(body)
    subject = "Новый отклик на ваш сервис"
    time = body.get('data_time')
    message = "Добрый день \r\n "\
              +"Недавно "+str(time.get('day')) + " в "+str(time.get('time')) \
              +".\r\n " +"Пользователь "+body.get('name') +" оставил отклик на вашу услугу " +body.get('services')+" компании "+body.get('company') +".\r\n " \
              +"Его номер "+body.get('phone_number')+", коментарий "+body.get('comment')+"\r\n " \
              +"C уважением сервис застрахуй братуху"
    send_mail(subject, 
            message, EMAIL_HOST_USER, [body.get('email')], fail_silently = False)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("Сообщение отправлено")


connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ["RabbitMQ_HOST"], '5672'))
channel = connection.channel()
channel.queue_declare(queue='send_new_request')

channel.basic_consume(queue='send_new_request',
                      auto_ack=False,
                      on_message_callback=send_new_request)

print ( '[*] Ожидание сообщений.' )
channel.start_consuming ()


#send_confirmation_queue
def send_confirmation(ch, method, properties, body):
    a = 1
    print("I am here")