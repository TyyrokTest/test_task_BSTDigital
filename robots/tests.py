from django.test import TestCase, Client
from robots.models import Robot
import json

class SimpleTest(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_without_data_in_request(self):
        response = self.client.post('/robots/add/', data={})
        
        self.assertEqual(response.status_code, 400)
    
    def test_with__empty_json_in_request(self):
        response = self.client.post('/robots/add/', content_type="application/json", data={})
        
        self.assertEqual(response.status_code, 200)
    
    def test_with_incorrect_json_data(self):
        data = "fd"
        response = self.client.post('/robots/add/', content_type="application/json", data=data)
        
        self.assertEqual(response.status_code, 400)
        
    def test_with_incorrect_json_data_2(self):
        data = { "model" : "R5"}
        response = self.client.post('/robots/add/', content_type="application/json", data=data)
        
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(json.loads(response.content)['failure']), 0)
    
    def test_with_correct_json_data(self):
        data = {
            "model": "R1",
            "version": "D1",
            "created": "2022-12-31 23:59:59"
        }
        response = self.client.post('/robots/add/', content_type="application/json", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)['success']), 1)
        self.assertEqual(len(json.loads(response.content)['failure']), 0)
        
    def test_with_correct_multiple_json_data(self):
        data = [
            {
                "model": "R5",
                "version": "D2",
                "created": "2022-12-31 23:59:59"
            },
            {
                "model": "13",
                "version": "XT",
                "created": "2023-01-01 00:00:00"
            },
        ]
        
        response = self.client.post('/robots/add/', content_type="application/json", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)['success']), 2)
        self.assertEqual(len(json.loads(response.content)['failure']), 0)
        
    def test_with_correct_multiple_json_data_with_incorrect_one(self):
        data = [
            {
                "model": "R5",
                "version": "D1",
                "created": "2022-12-31 23:59:59"
            },
            {
                "model": "13",
                "version": "XSs",
                "created": "2023-01-01 00:00:00"
            },
        ]
        
        response = self.client.post('/robots/add/', content_type="application/json", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)['success']), 1)
        self.assertEqual(len(json.loads(response.content)['failure']), 1)

class Task2Test(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test1_check_report_view_page(self):
        response = self.client.get('/robots/report/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="redirecting-link"')
    
    def test2_check_report_download_view_page_with_empy_db(self):
        response = self.client.get('/robots/report/download/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No data for report')
        
class Task2TestWithFixtures(TestCase):
    fixtures = ['robots.json']
    def setUp(self):
        self.client = Client()
    
    def test3_check_report_create_view_page(self):
        response = self.client.get('/robots/report/download/')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(
            response.get('Content-Disposition'),
            'attachment; filename="week_report.xlsx"'
        )