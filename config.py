import os

APP_ENV=os.environ.get('APP_ENV', 'development')
SQLALCHEMY_DATABASE_URI=os.environ.get('DB_DATABASE_URI')
DEBUG=os.environ.get('APP_DEBUG', False)
SECRET_KEY=os.environ.get('SECRET_KEY')
CACHE_TYPE=os.environ.get('CACHE_TYPE', 'simple')
CACHE_REDIS_URL=os.environ.get('CACHE_REDIS_URL')