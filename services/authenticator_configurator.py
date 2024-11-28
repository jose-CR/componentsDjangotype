import os
import ast
from django.core.management.base import BaseCommand
from django.core.management import call_command

class DjangoProjectManager(BaseCommand):
    def __init__(self, app_name, project_name):
        self.app_name = app_name
        self.project_name = project_name

    def create_app(self):
        """
        Crea una aplicación de Django con el nombre especificado si no existe.
        """
        app_name = self.app_name
        if not os.path.exists(app_name):
            print(f"Creando la aplicación '{app_name}'...")
            call_command('startapp', app_name)
            if os.path.exists(app_name):
                print(f"La aplicación '{app_name}' fue creada exitosamente.")
            else:
                print(f"Error: No se pudo crear la aplicación '{app_name}'.")
        else:
            print(f"La aplicación '{app_name}' ya existe.")
    
    def installed_app(self):
        """
        Agrega la aplicación al archivo settings.py en la lista INSTALLED_APPS
        si no está ya presente. Asegura que se mantenga el formato adecuado.
        """
        settings_path = os.path.join(self.project_name, 'settings.py')

        # Leer el archivo settings.py
        with open(settings_path, 'r') as file:
            settings_content = file.read()

        # Comprobar si la aplicación ya está en INSTALLED_APPS
        if f"'{self.app_name}'" not in settings_content:
            # Buscar la línea donde está la lista INSTALLED_APPS
            installed_apps_start = settings_content.find("INSTALLED_APPS = [")
            installed_apps_end = settings_content.find("]", installed_apps_start) + 1

            # Extraer la lista INSTALLED_APPS
            installed_apps_content = settings_content[installed_apps_start:installed_apps_end]

            # Comprobar si la aplicación no está ya en INSTALLED_APPS
            if f"'{self.app_name}'" not in installed_apps_content:
                # Insertar la aplicación dentro de la lista
                new_installed_apps = installed_apps_content[:-1] + f"\n'{self.app_name}',\n]"

                # Reemplazar el bloque INSTALLED_APPS con la nueva lista
                new_settings_content = settings_content[:installed_apps_start] + new_installed_apps + settings_content[installed_apps_end:]

                # Escribir los cambios de vuelta en settings.py
                with open(settings_path, 'w') as file:
                    file.write(new_settings_content)

                print(f"'{self.app_name}' fue agregado a INSTALLED_APPS.")
            else:
                print(f"'{self.app_name}' ya está en INSTALLED_APPS.")
        else:
            print(f"'{self.app_name}' ya está en INSTALLED_APPS.")
        
    def create_urls(self):
            """
            Crea el archivo 'urls.py' si no existe, y si existe, agrega nuevas rutas
            sin sobrescribir el contenido existente.
            """
            urls_path = os.path.join(self.app_name, 'urls.py')
            
            if not os.path.exists(urls_path):
                # Si el archivo no existe, lo creamos con un contenido básico
                self.stdout.write(f"Creando el archivo '{urls_path}'...")
                with open(urls_path, 'w') as f:
                    f.write("""from django.contrib import admin
from django.urls import path, include\n\n

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(Home.urls)),
    # Añade tus rutas aquí
]\n""")
            else:
                # Si el archivo ya existe, lo leemos y agregamos nuevas rutas
                self.stdout.write(f"El archivo '{urls_path}' ya existe. Agregando nuevas rutas...")
                
                with open(urls_path, 'r') as f:
                    urls_content = f.read()

                # Verificar si ya existe una lista 'urlpatterns'
                if 'urlpatterns = [' in urls_content:
                    # Verificar si 'path' ya está en la lista
                    if 'path' not in urls_content:
                        urls_content = urls_content.replace(
                            "urlpatterns = [",
                            "urlpatterns = [\n    path('admin/', admin.site.urls),"
                        )
                    # Verificar si 'include' ya está presente en urlpatterns
                    if 'include' not in urls_content:
                        urls_content = urls_content.replace(
                            "]\n", 
                            "    path('', include('home.urls')),\n    # Otras rutas aquí\n]"
                        )
                    else:
                        # Si ya contiene 'include', solo agregamos una nueva ruta
                        urls_content = urls_content.replace(
                            "]\n", 
                            "    path('', include('home.urls')),\n    # Otras rutas aquí\n]"
                        )
                    
                    # Escribir el contenido actualizado en el archivo
                    with open(urls_path, 'w') as f:
                        f.write(urls_content)
                    self.stdout.write(f"Nuevas rutas fueron agregadas a '{urls_path}'.")
                else:
                    self.stdout.write(f"No se encontró la lista 'urlpatterns' en '{urls_path}'.")

    def creation_auth(self):
        services_dir = os.path.join(self.app_name, 'services')
        authentication_dir = os.path.join(services_dir, 'authentication')
        os.makedirs(authentication_dir, exist_ok=True)

        authentication_path = os.path.join(authentication_dir, 'auth.py')

        if not os.path.exists(authentication_path):
            self.stdout.write(f"Creando el archivo '{authentication_path}'...")

            auth_path = os.path.join(self.app_name, 'services', 'authentication', 'auth.py')

            # Leer el código del archivo de origen
            with open(auth_path, 'r') as file:
                auth_code = file.read()

            # Escribir el código en el archivo de destino
            with open(authentication_path, 'w') as file:
                file.write(auth_code)

            self.stdout.write(f"El archivo '{authentication_path}' fue creado y el código fue escrito.")
        else:
            self.stdout.write(f"El archivo '{authentication_path}' ya existe.")



























