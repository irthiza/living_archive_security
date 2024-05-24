1. Create a virtual Environment

python -m venv env

2. Activate it

source env/bin/activate for Mac

.\env\Scripts\activate.bat for windows

3. Install all the required libraries

pip install -r requirements.txt

4. Update the database

python manage.py migrate 

5. Create a superuser

python manage.py createsuperuser

6. Run the server

python manage.py runserver

http://127.0.0.1:8005/admin #for admin access