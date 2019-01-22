import sys
from myblt import init_db, init_engine, new_user, app

if __name__ == "__main__":
    app.config.from_pyfile('config/default_config.py')

    if len(sys.argv) == 2:
        conf = sys.argv[1]
        print('Loading additional config %s...', conf)
        app.config.from_pyfile('config/' + conf + '_config.py')

    init_engine(app.config['DATABASE_URI'])
    init_db()

    # Insert admin user with default credentials
    new_user('admin', 'admin', True)