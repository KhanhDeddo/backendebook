import mysql.connector
import os
from dotenv import load_dotenv

# Nạp các biến môi trường từ .env
load_dotenv()

def execute_sql_file(database, file_path):
    """
    Thực thi một tệp SQL trên cơ sở dữ liệu MySQL.
    """
    try:
        # Kết nối đến cơ sở dữ liệu MySQL sử dụng các biến môi trường
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),  # Địa chỉ của MySQL
            user=os.getenv("DB_USER"),  # Tên người dùng
            password=os.getenv("DB_PASSWORD"),  # Mật khẩu
            database=database,  # Tên cơ sở dữ liệu
        )
        cursor = conn.cursor()

        # Đọc tệp SQL
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        # Tạm thời vô hiệu hóa kiểm tra khóa ngoại
        cursor.execute('SET foreign_key_checks = 0;')

        # Thực thi các câu lệnh SQL
        for result in cursor.execute(sql_script, multi=True):
            pass  # Nếu có lỗi, sẽ bị báo tại đây

        # Kích hoạt lại kiểm tra khóa ngoại
        cursor.execute('SET foreign_key_checks = 1;')

        conn.commit()
        print(f"Successfully executed {file_path}")

    except Exception as e:
        print(f"Error executing {file_path}: {e}")

    finally:
        if conn:
            cursor.close()
            conn.close()

def init_db():
    """
    Hàm khởi tạo cơ sở dữ liệu và chạy các tệp SQL từ thư mục migrations.
    """
    database = "buexakx7blzh8zlp6rcd"  # Tên cơ sở dữ liệu MySQL

    # Kiểm tra xem cơ sở dữ liệu có tồn tại không (bạn có thể kiểm tra nếu cần)
    print(f"Tạo mới cơ sở dữ liệu {database}...")

    # Thực thi file schema.sql (tạo bảng)
    execute_sql_file(database, "migrations/schema.sql")

    # Thực thi file seed.sql (nếu có dữ liệu mẫu)
    if os.path.exists("migrations/seed.sql"):
        execute_sql_file(database, "migrations/seed.sql")

    print(f"Khởi tạo cơ sở dữ liệu {database} hoàn tất.")

if __name__ == "__main__":
    init_db()
