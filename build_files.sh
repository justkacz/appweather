pip install -r requirements.txt
python3.9 manage.py collectstatic --no-input
python3.9 manage.py compress --force
python3.9 manage.py makemigrations
python3.9 manage.py migrate
