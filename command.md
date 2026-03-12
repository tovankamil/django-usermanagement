### setup django
jalankan perintah ini di commmand prompt

python -m venv venv
source venv/Scripts/activate
pip install --upgrade pip
pip install django
pip install djangorestframework
pip install psycopg2-binary
pip install python-dotenv
pip install redis
pip install django-redis
pip install PyJWT
pip install drf-spectacular
pip freeze > requirements.txt
django-admin startproject config .
pip install django-environ
pip install coverage

mkdir apps
mkdir apps/users
mkdir apps/users/migrations

mkdir -p apps/users/{domain,application,infrastructure,interfaces,migrations} && touch apps/__init__.py apps/users/__init__.py apps/users/{domain,application,infrastructure,interfaces,migrations}/__init__.py apps/users/domain/{entities,repositories}.py apps/users/application/{services,dto}.py apps/users/infrastructure/{models,repositories,cache}.py apps/users/interfaces/{serializers,views,urls}.py apps/users/{migrations/.gitkeep,apps.py}

coverage run manage.py test
coverage report
