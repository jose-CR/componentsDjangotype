# componentsDjangoType/management/commands/createcomponentApp.py
import os
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Crea una aplicación llamada Home, estructura de carpetas y configura urls automáticamente en el proyecto especificado'

    def handle(self, *args, **kwargs):
        # Nombre de la aplicación a crear
        app_name = "Home"

        # Paso 1: Solicitar el nombre de la aplicación principal al usuario
        project_name = input(
            "Por favor, ingresa el nombre de la aplicación principal del proyecto: ")

        # Paso 2: Crear la aplicación "Home" si no existe
        if not os.path.exists(app_name):
            self.stdout.write(f"Creando la aplicación '{app_name}'...")
            call_command('startapp', app_name)
        else:
            self.stdout.write(f"La aplicación '{app_name}' ya existe.")

        # Paso 3: Crear el archivo urls.py en la aplicación "Home" si no existe
        urls_path = os.path.join(app_name, 'urls.py')
        if not os.path.exists(urls_path):
            self.stdout.write(f"Creando el archivo '{urls_path}'...")
            with open(urls_path, 'w') as f:
                f.write(
                    "from django.urls import path\n\n"
                    "urlpatterns = [\n"
                    "    # Añade tus rutas aquí\n"
                    "]\n"
                )
        else:
            self.stdout.write(f"El archivo '{urls_path}' ya existe.")

        # Paso 4: Modificar el archivo urls.py principal del proyecto
        project_urls_path = os.path.join(project_name, 'urls.py')
        if os.path.exists(project_urls_path):
            with open(project_urls_path, 'r') as f:
                content = f.read()

            include_statement = "path('', include('Home.urls'))"
            if include_statement not in content:
                self.stdout.write(f"Añadiendo la ruta '{
                                  include_statement}' al archivo urls.py principal...")
                with open(project_urls_path, 'a') as f:
                    f.write(
                        "\nfrom django.urls import include, path\n\n"
                        "urlpatterns += [\n"
                        f"    {include_statement},\n"
                        "]\n"
                    )
            else:
                self.stdout.write(
                    "La ruta ya existe en el archivo urls.py principal.")
        else:
            self.stdout.write(f"No se encontró el archivo principal urls.py en '{
                              project_urls_path}'. Asegúrate de que el nombre del proyecto sea correcto.")

        # Paso 5: Crear la carpeta services y el archivo authentication.py en Home
        services_dir = os.path.join(app_name, 'services')
        # Crea la carpeta si no existe
        os.makedirs(services_dir, exist_ok=True)
        authentication_file_path = os.path.join(
            services_dir, 'authentication.py')

        if not os.path.exists(authentication_file_path):
            self.stdout.write(f"Creando el archivo '{
                              authentication_file_path}'...")
            with open(authentication_file_path, 'w') as f:
                f.write(
                    "from django.shortcuts import render, redirect\n"
                    "from django.contrib.auth.forms import UserCreationForm, AuthenticationForm\n"
                    "from django.contrib.auth.models import User\n"
                    "from django.contrib.auth import login, logout, authenticate\n"
                    "from django.db import IntegrityError\n\n\n"
                    "class Authentication:\n"
                    "    @staticmethod\n"
                    "    def get_signup(request):\n"
                    "        if request.method == 'GET':\n"
                    "            return render(request, 'singup.html', {\n"
                    "                'form': UserCreationForm()\n"
                    "            })\n"
                    "        elif request.method == 'POST':\n"
                    "            if request.POST['password1'] == request.POST['password2']:\n"
                    "                try:\n"
                    "                    # Register user\n"
                    "                    user = User.objects.create_user(\n"
                    "                        username=request.POST['username'], password=request.POST['password2'])\n"
                    "                    user.save()\n"
                    "                    login(request, user)\n"
                    "                    return redirect('logged')\n"
                    "                except IntegrityError:\n"
                    "                    return render(request, 'singup.html', {\n"
                    "                        'form': UserCreationForm(),\n"
                    "                        'error': 'User already exists'\n"
                    "                    })\n"
                    "            return render(request, 'singup.html', {\n"
                    "                'form': UserCreationForm(),\n"
                    "                'error': 'Passwords do not match'\n"
                    "            })\n\n"
                    "    @staticmethod\n"
                    "    def get_signout(request):\n"
                    "        logout(request)\n"
                    "        return redirect('home')\n\n"
                    "    @staticmethod\n"
                    "    def get_signing(request):\n"
                    "        if request.method == 'GET':\n"
                    "            return render(request, 'login.html', {\n"
                    "                'form': AuthenticationForm,\n"
                    "            })\n"
                    "        elif request.method == 'POST':\n"
                    "            try:\n"
                    "                User.objects.get(username=request.POST['username'])\n"
                    "            except User.DoesNotExist:\n"
                    "                return render(request, 'login.html', {\n"
                    "                    'form': AuthenticationForm,\n"
                    "                    'error': 'User does not exist in the database'\n"
                    "                })\n"
                    "            user = authenticate(\n"
                    "                request, username=request.POST['username'], password=request.POST['password'])\n"
                    "            if user is None:\n"
                    "                return render(request, 'login.html', {\n"
                    "                    'form': AuthenticationForm,\n"
                    "                    'error': 'username or password is incorrect'\n"
                    "                })\n"
                    "            else:\n"
                    "                login(request, user)\n"
                    "                return redirect('logged')\n\n"
                    "    @staticmethod\n"
                    "    def get_logged(request):\n"
                    "        return render(request, 'logged.html')\n\n"
                    "    def dispatch(self, request, *args, **kwargs):\n"
                    "        match request.path:\n"
                    "            case \"/signup\":\n"
                    "                return self.get_signup(request)\n"
                    "            case \"/login\":\n"
                    "                return self.get_signing(request)\n"
                    "            case \"/logout\":\n"
                    "                return self.get_signout(request)\n"
                    "            case \"/logged\":\n"
                    "                return self.get_logged(request)\n"
                    "            case \"/\":\n"
                    "                return self.get(request)\n"
                    "            case _:\n"
                    "                return self.get(request)\n"
                )
        else:
            self.stdout.write(
                f"El archivo '{authentication_file_path}' ya existe.")

        # Paso 6: Crear la carpeta templates y los archivos HTML
        templates_dir = os.path.join(project_name, 'templates')
        layouts_dir = os.path.join(templates_dir, 'layouts')
        static_dir = os.path.join(project_name, 'static')
        css_dir = os.path.join(static_dir, 'css')
        js_dir = os.path.join(static_dir, 'js')

        # Crear los directorios necesarios
        os.makedirs(js_dir, exist_ok=True)
        os.makedirs(css_dir, exist_ok=True)
        os.makedirs(layouts_dir, exist_ok=True)
        os.makedirs(templates_dir, exist_ok=True)
        os.makedirs(static_dir, exist_ok=True)

        # Rutas de los archivos fuente y destino
        css_source_path = os.path.join('utils', 'css', 'authentication.css')
        authentication_css = os.path.join(css_dir, 'authentication.css')
        js_source_path = os.path.join('utils', 'js', 'alertErrors.js')
        alertErrors_js = os.path.join(js_dir, 'alertErrors.js')

        # Crear archivos si no existen
        if not os.path.exists(authentication_css):
            try:
                with open(css_source_path, 'r') as source_file:
                    css_content = source_file.read()
                with open(js_source_path, 'r') as source_file:
                    js_content = source_file.read()

                with open(authentication_css, 'w') as f:
                    f.write(css_content)
                with open(alertErrors_js, 'w') as f:
                    f.write(js_content)

                print(f"Archivo CSS creado exitosamente en {
                      authentication_css}")
                print(f"Archivo JS creado exitosamente en {alertErrors_js}")
            except FileNotFoundError as e:
                print(f"Archivo fuente no encontrado: {e}")
            except Exception as e:
                print(f"Error al crear el archivo: {e}")

        # Crear el archivo de layout (index.html) si no existe
        index_page_source = os.path.join('utils', 'layouts', 'index.html')
        layouts_source = os.path.join(layouts_dir, 'index.html')

        if not os.path.exists(layouts_source):
            try:
                with open(index_page_source, 'r') as source_file:
                    index_content = source_file.read()

                with open(layouts_source, 'w') as f:
                    f.write(index_content)

                print("Archivo de layout creado exitosamente")
            except FileNotFoundError as e:
                print(f"Archivo fuente no encontrado: {e}")
            except Exception as e:
                print(f"Error al crear el archivo: {e}")

        # Crear las páginas HTML adicionales (home, signup, login, logged)
        # Rutas de los archivos fuente
        home_page = os.path.join('utils', 'pages', 'home.html')
        signup_page = os.path.join('utils', 'pages', 'signup.html')
        login_page = os.path.join('utils', 'pages', 'login.html')
        logged_page = os.path.join('utils', 'pages', 'logged.html')

        # Rutas de los archivos de destino
        home_dest = os.path.join(templates_dir, 'home.html')
        signup_dest = os.path.join(templates_dir, 'signup.html')
        login_dest = os.path.join(templates_dir, 'login.html')
        logged_dest = os.path.join(templates_dir, 'logged.html')

        # Crear cada archivo HTML si no existe
        for source_path, dest_path, page_name in [
            (home_page, home_dest, 'Home'),
            (signup_page, signup_dest, 'Signup'),
            (login_page, login_dest, 'Login'),
            (logged_page, logged_dest, 'Logged')
        ]:
            if not os.path.exists(dest_path):
                try:
                    with open(source_path, 'r') as source_file:
                        content = source_file.read()
                    with open(dest_path, 'w') as dest_file:
                        dest_file.write(content)
                    print(f"Archivo {page_name} creado exitosamente en {
                          dest_path}")
                except FileNotFoundError as e:
                    print(f"Archivo fuente no encontrado: {source_path}")
                except Exception as e:
                    print(f"Error al crear el archivo {page_name}: {e}")

        self.stdout.write(self.style.SUCCESS(
            "Comando ejecutado exitosamente."))
