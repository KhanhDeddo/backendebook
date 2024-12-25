from flask_cors import CORS
from app import create_app
import os
app = create_app()
CORS(app)  # Cho phép tất cả các nguồn truy cập API

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
