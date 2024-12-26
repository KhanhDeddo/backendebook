from dotenv import load_dotenv
import os
load_dotenv()  # Tải các giá trị từ file .env vào môi trường

from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# Kết nối đến cơ sở dữ liệu MySQL
def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=int(os.getenv("PORT", 3306))  # Đảm bảo cổng được chuyển thành int
    )
    return connection

@app.route('/')
def index():
    # # Truy vấn cơ sở dữ liệu
    # conn = get_db_connection()
    # cursor = conn.cursor(dictionary=True)
    # cursor.execute('SELECT * FROM Users')  # Thay 'your_table' bằng tên bảng của bạn
    # rows = cursor.fetchall()
    # cursor.close()
    # conn.close()
    
    # # Trả về dữ liệu dưới dạng JSON
    # return jsonify(rows)
    return "haha"

from waitress import serve
if __name__ == "__main__":
    # # app.run(debug=True)
    serve(app, host='0.0.0.0', port=5000)  # Sử dụng Waitress để phục vụ ứng dụng
