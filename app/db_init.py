from dotenv import load_dotenv
import mysql.connector
import os
load_dotenv()

def execute_sql_file(file_path):
    try:
        # Kết nối đến cơ sở dữ liệu MySQL
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),  
            user=os.getenv("DB_USER"),  
            password=os.getenv("DB_PASSWORD"),  
            database=os.getenv('DB_NAME'),
            port=int(os.getenv("PORT"))
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
    database = os.getenv("DB_NAME") 
    print(f"Tạo mới cơ sở dữ liệu {database}...")
    execute_sql_file("migrations/schema.sql")
    if os.path.exists("migrations/seed.sql"):
        execute_sql_file("migrations/seed.sql")
    print(f"Khởi tạo cơ sở dữ liệu {database} hoàn tất.")

if __name__ == "__main__":
    init_db()
