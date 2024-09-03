from django.core.management import call_command
from django.test import TestCase
from django.apps import apps
import os

class CreateComponentTest(TestCase):

    def setUp(self):
        self.app_name = 'mytest'
        self.file_path = 'helloWorld.html'
        self.js_file_path = 'component.js'
        self.css_file_path = 'style.css'
        self.template_dir = os.path.join(apps.get_app_config(self.app_name).path, 'templates')
        self.static_dir = os.path.join(apps.get_app_config(self.app_name).path, 'static')
        
        if os.path.exists(os.path.join(self.template_dir, self.file_path)):
            os.remove(os.path.join(self.template_dir, self.file_path))
        if os.path.exists(os.path.join(self.static_dir, self.js_file_path)):
            os.remove(os.path.join(self.static_dir, self.js_file_path))

    def tearDown(self):
        if os.path.exists(os.path.join(self.template_dir, self.file_path)):
            os.remove(os.path.join(self.template_dir, self.file_path))
        if os.path.exists(os.path.join(self.static_dir, self.js_file_path)):
            os.remove(os.path.join(self.static_dir, self.js_file_path))

    def test_create_template_component(self):
        call_command('createcomponent', self.app_name, self.file_path, '--type', 'template')
        file_full_path = os.path.join(self.template_dir, self.file_path)
        self.assertTrue(os.path.exists(file_full_path))
        with open(file_full_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, '<div>Este es el contenido del componente.</div>')

    def test_create_js_component(self):
        call_command('createcomponent', self.app_name, self.js_file_path, '--type', 'static')
        file_full_path = os.path.join(self.static_dir, self.js_file_path)
        self.assertTrue(os.path.exists(file_full_path))
        with open(file_full_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, 'console.log("Este es el contenido del componente.");')

    def test_create_css_component(self):
        call_command('createcomponent', self.app_name, self.css_file_path, '--type', 'static')
        file_full_path = os.path.join(self.static_dir, self.css_file_path)
        self.assertTrue(os.path.exists(file_full_path))
        with open(file_full_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, '/* Este es el contenido del componente */')

