
from app import create_app
from app.data import db

app = create_app()
app.app_context().push()
db.create_all()

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)