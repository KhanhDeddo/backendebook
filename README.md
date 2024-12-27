<!-- 
python -m venv venv
source venv/Scripts/activate
pip install flask requests
pip install flask_sqlalchemy
pip install flask-cors
pip install Flask-Mail
pip install pymysql
pip install python-dotenv
pip install mysql-connector-python


pip freeze > requirements.txt
cd .. tro ra thu muc cha


/project_name
│
├── /app                     # Thư mục chính chứa mã nguồn ứng dụng
│   ├── __init__.py          # Tập tin khởi tạo ứng dụng Flask
│   ├── routes.py            # Tập tin định nghĩa các API endpoint
│   ├── models.py            # Định nghĩa các model (ORM hoặc thủ công)
│   ├── db_init.py           # Tập tin khởi tạo cơ sở dữ liệu SQLite
│   └── utils.py             # Các hàm tiện ích dùng chung
│
├── /migrations              # Thư mục chứa các tệp SQL (tạo bảng, thêm dữ liệu)
│   ├── schema.sql           # Câu lệnh SQL để tạo bảng (dùng để khởi tạo DB)
│   └── seed.sql             # Dữ liệu mẫu ban đầu (tùy chọn)
│
├── run.py                   # Điểm khởi chạy ứng dụng Flask
├── requirements.txt         # Danh sách các thư viện Python cần thiết
├── .gitignore               # Tệp để bỏ qua các file/folder không cần thiết trong Git
└── README.md                # Hướng dẫn sử dụng dự án

-->