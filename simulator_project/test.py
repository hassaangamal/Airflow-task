from django.conf import settings

def get_sqlalchemy_conn_sqlite():
    db_settings = settings.DATABASES['default']
    if db_settings['ENGINE'] != 'django.db.backends.sqlite3':
        raise ValueError("The database engine is not SQLite.")

    # SQLite uses the file path as the connection string
    return f"sqlite:///{db_settings['NAME']}"
print(get_sqlalchemy_conn_sqlite())  