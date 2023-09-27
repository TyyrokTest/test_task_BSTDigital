from django.test import TestCase, Client
from django.core import mail
from orders.models import Order
from robots.models import Robot
from django.utils import timezone

class Task3Test(TestCase):
    fixtures = ['orders.json', 'customers.json', 'robots.json']
    url = '/orders/add/'
    
    def setUp(self):
        self.client = Client()
        
    def test_1_get_add_order_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
    def test_2_post_add_order_view_without_data(self):
        response = self.client.post(self.url, {'customer':''})
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.context['errors']), 0)
        
    def test_3_post_add_order_view_with_incorrect_email(self):
        response = self.client.post(self.url, {'customer':'example.com', 'robot_serial': 'R2-D2'})    
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a valid email address')
        
    def test_4_post_add_order_view_with_incorrect_serial(self):
        response = self.client.post(self.url, {'customer':'example@d.com', 'robot_serial': 'R2dD2'})  
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 
                            u"Серийный номер должен состоять только из цифр, букв и быть в формате")
        
    def test_5_post_add_order_view_with_correct_data_robot_in_stock(self):
        response = self.client.post(self.url, {'customer':'example@d.com', 'robot_serial': 'R2-D2'})  
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, u"У нас на складе имеется необходимый вам робот,")
        
    def test_6_post_add_order_view_with_correct_data_robot(self):
        response = self.client.post(self.url, {'customer':'example@d.com', 'robot_serial': 'Z2-D2'})  
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, u"Ваш заказ успешно создан!")
        order = Order.objects.filter(robot_serial='Z2-D2')
        self.assertGreater(len(order), 0)
        
class EmailTest(TestCase):
    fixtures = ['orders.json', 'customers.json', 'robots.json']
        
    def setUp(self):
        self.client = Client()
    
    def test_sending_notification_email(self):
        Robot.objects.create(model='R7', version='D7', serial='R7-D7',
                             created=timezone.now())
        self.assertGreater(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Робот R7-D7 теперь в наличии!")
        
    
