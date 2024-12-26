from app import create_app
from waitress import serve
from flask_cors import CORS
app = create_app()
CORS(app)
if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)  # Sử dụng Waitress để phục vụ ứng dụng
