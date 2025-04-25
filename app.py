from flask import Flask
from flask import session
from routes.auth import auth_bp
from routes.upload import upload_bp
from routes.dashboard import dashboard_bp
from routes.calculate import calculate_bp

app = Flask(__name__)
app.secret_key = 'rahasia123'  # ganti di deploy

# Blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(calculate_bp)

if __name__ == '__main__':
    app.run(debug=True)
