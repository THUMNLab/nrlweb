uwsgi --socket 127.0.0.1:6666 --protocol=http -w wsgi:app --processes 4 --threads 2 --plugin python
