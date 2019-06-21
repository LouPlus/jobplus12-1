from jobplus.app import create_app
from jobplus.config import config

env = 'dev'
conf = config.get(env)

app = create_app(conf)

if __name__ == '__main__':
    app.run()
