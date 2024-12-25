-- DROP các bảng nếu đã tồn tại
DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,       -- Mã người dùng (khóa chính, tự động tăng)
    user_name VARCHAR(255) NOT NULL,               -- Tên người dùng (không được để trống)
    user_email VARCHAR(255) NOT NULL UNIQUE,       -- Email người dùng (phải là duy nhất)
    user_phone VARCHAR(255) NOT NULL UNIQUE,       -- Số điện thoại
    user_password VARCHAR(255) NOT NULL,           -- Mật khẩu
    user_date_of_birth DATE NOT NULL,              -- Ngày sinh
    user_gender VARCHAR(10) NOT NULL,              -- Giới tính
    user_address TEXT NOT NULL,                    -- Địa chỉ
    user_is_admin TINYINT(1) NOT NULL DEFAULT 0    -- Quyền admin, mặc định là không phải admin
);

DROP TABLE IF EXISTS Books;
CREATE TABLE Books (
    book_id INT PRIMARY KEY AUTO_INCREMENT,        -- Mã sách (khóa chính, tự động tăng)
    title VARCHAR(255) NOT NULL,                    -- Tiêu đề sách
    status_book VARCHAR(50) NOT NULL,               -- Trang thái
    author VARCHAR(255) NOT NULL,                   -- Tác giả
    description TEXT,                               -- Mô tả sách
    price INT NOT NULL,                             -- Giá sách
    image_url TEXT,                                 -- URL (hình ảnh hoặc sách điện tử)
    publication_date DATE,                          -- Ngày xuất bản
    category VARCHAR(100) NOT NULL,                 -- Thể loại sách
    level_class INT NOT NULL,                       -- Lớp
    level_school VARCHAR(50) NOT NULL,              -- Cấp trường (Tiểu học, Trung học cs, Trung học pt)
    stock_quantity INT NOT NULL DEFAULT 0,          -- Số lượng tồn kho
    publisher VARCHAR(255) NOT NULL,                -- Nhà xuất bản
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Ngày tạo bản ghi
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Ngày cập nhật bản ghi
);

DROP TABLE IF EXISTS Orders;
CREATE TABLE Orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,        -- Mã đơn hàng (khóa chính, tự động tăng)
    user_id INT NOT NULL,                           -- Mã người dùng (khóa ngoại)
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Ngày đặt hàng
    status VARCHAR(50) NOT NULL DEFAULT 'Chờ xác nhận', -- Trạng thái đơn hàng
    total_price INT NOT NULL,                       -- Tổng giá trị đơn hàng
    recipient_name VARCHAR(255) NOT NULL,           -- Tên người nhận
    recipient_phone VARCHAR(255) NOT NULL,          -- Số điện thoại người nhận 
    recipient_email VARCHAR(255) NOT NULL,          -- Email người nhận
    shipping_address TEXT NOT NULL,                 -- Địa chỉ giao hàng
    payment_method VARCHAR(100) NOT NULL,           -- Phương thức thanh toán
    payment_status VARCHAR(50) NOT NULL DEFAULT 'Chưa thanh toán', -- Trạng thái thanh toán
    shipping_date DATE,                             -- Ngày vận chuyển
    delivery_date DATE,                             -- Ngày giao hàng thành công
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Ngày tạo bản ghi
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Ngày cập nhật bản ghi
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE -- Ràng buộc khóa ngoại
);

DROP TABLE IF EXISTS Order_Items;
CREATE TABLE Order_Items (
    order_id INT NOT NULL,                          -- Mã đơn hàng (khóa phụ)
    book_id INT NOT NULL,                           -- Mã sản phẩm (khóa phụ)
    quantity INT NOT NULL,                          -- Số lượng sản phẩm
    price_per_item INT,                             -- Giá mỗi sản phẩm
    total_price INT NOT NULL,                       -- Tổng giá trị của mục này (quantity * price_per_item)
    PRIMARY KEY (order_id, book_id),                -- Đặt order_id và book_id làm khóa chính
    FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES Books(book_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS Carts;
CREATE TABLE Carts (
    cart_id INT PRIMARY KEY AUTO_INCREMENT,         -- Mã giỏ hàng
    user_id INT NOT NULL UNIQUE,                     -- Mã người dùng (khóa ngoại, đảm bảo mỗi user chỉ có một giỏ hàng)
    quantity INT NOT NULL DEFAULT 0,                 -- Số lượng sách trong giỏ
    total_amount INT NOT NULL DEFAULT 0,             -- Tổng tiền trong giỏ
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS Cart_Items;
CREATE TABLE Cart_Items (
    cart_id INT NOT NULL,                            -- Mã giỏ hàng (khóa ngoại)
    book_id INT NOT NULL,                            -- Mã sách (khóa ngoại)
    quantity INT NOT NULL DEFAULT 1,                 -- Số lượng sách trong giỏ
    price_at_purchase INT NOT NULL,                  -- Giá tại thời điểm thêm
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,    -- Ngày giờ thêm sách vào giỏ
    PRIMARY KEY (cart_id, book_id),                  -- Khóa chính
    FOREIGN KEY (cart_id) REFERENCES Carts(cart_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES Books(book_id) ON DELETE CASCADE
);
