# from flask_cors import CORS
# from app import create_app
# import os
# app = create_app()
# CORS(app)  # Cho phép tất cả các nguồn truy cập API

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
import os
from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# Kết nối đến cơ sở dữ liệu MySQL
def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    return connection

@app.route('/')
def index():
    # Truy vấn cơ sở dữ liệu
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Users')  # Thay 'your_table' bằng tên bảng của bạn
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Trả về dữ liệu dưới dạng JSON
    return jsonify(rows)

if __name__ == "__main__":
    app.run(debug=True)
