from app import db

class User(db.Model):
    __tablename__ = 'Users'  # Đảm bảo bảng có tên đúng trong DB
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(100), nullable=False, unique=True)
    user_phone = db.Column(db.String(20), nullable=False, unique=True)
    user_password = db.Column(db.String(100), nullable=False)
    user_date_of_birth = db.Column(db.String(20), nullable=False)
    user_gender = db.Column(db.String(10), nullable=False)
    user_address = db.Column(db.String(100), nullable=False)
    user_is_admin = db.Column(db.Boolean, nullable=False)
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_email": self.user_email,
            "user_phone": self.user_phone,
            "user_password": self.user_password, 
            "user_date_of_birth": self.user_date_of_birth,
            "user_gender": self.user_gender,
            "user_address": self.user_address,
            "user_is_admin": self.user_is_admin
        }

class Book(db.Model):
    __tablename__ = 'Books'  # Đảm bảo bảng có tên đúng trong DB
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    status_book = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255))  # URL của ảnh sách (nếu có)
    publication_date = db.Column(db.Date)  # Xóa dấu phẩy
    category = db.Column(db.String(100), nullable=False)  # Xóa dấu phẩy
    level_class = db.Column(db.Integer, nullable=False)  # Xóa dấu phẩy
    level_school = db.Column(db.String(50), nullable=False)  # Xóa dấu phẩy
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    publisher = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime, 
        default=db.func.current_timestamp(), 
        onupdate=db.func.current_timestamp()
    )
    
    def to_dict(self):
        return {
            "id": self.book_id,
            "title": self.title,
            "status_book":self.status_book,
            "author": self.author,
            "description": self.description,
            "price": (self.price), 
            "image_url": self.image_url,
            "publication_date": self.publication_date,
            "category": self.category,
            "level_class": self.level_class,
            "level_school": self.level_school,
            "stock_quantity": self.stock_quantity,
            "publisher": self.publisher,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class Order(db.Model):
    __tablename__ = 'Orders'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)  # Đảm bảo tên bảng là 'Users'
    order_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String(100), nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    recipient_name = db.Column(db.Text, nullable=False)
    recipient_phone = db.Column(db.Text, nullable=False)
    recipient_email = db.Column(db.Text, nullable=False)
    shipping_address = db.Column(db.String(255), nullable=False)
    payment_method = db.Column(db.String(100), nullable=False)
    payment_status = db.Column(db.String(100), nullable=False)
    shipping_date = db.Column(db.Date)
    delivery_date = db.Column(db.Date)
    user = db.relationship('User', backref=db.backref('orders', lazy=True))  # Mối quan hệ giữa User và Orders
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    def to_dict(self):
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "order_date": self.order_date,
            "status": self.status,
            "total_price": (self.total_price),
            "recipient_name": self.recipient_name,
            "recipient_phone": self.recipient_phone,
            "recipient_email": self.recipient_email,
            "shipping_address": self.shipping_address,
            "payment_method": self.payment_method,
            "payment_status": self.payment_status,
            "shipping_date": self.shipping_date,
            "delivery_date": self.delivery_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class OrderItem(db.Model):
    __tablename__ = 'Order_Items'

    order_id = db.Column(db.Integer, db.ForeignKey('Orders.order_id'), primary_key=True)  # Khóa ngoại đến Orders
    book_id = db.Column(db.Integer, db.ForeignKey('Books.book_id'), primary_key=True)    # Khóa ngoại đến Books
    quantity = db.Column(db.Integer, nullable=False)
    price_per_item = db.Column(db.Numeric(10, 2), nullable=True)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)

    # Mối quan hệ với bảng Order và Book
    order = db.relationship('Order', backref=db.backref('order_items', lazy=True))
    book = db.relationship('Book', backref=db.backref('order_items', lazy=True))

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "book_id": self.book_id,
            "quantity": self.quantity,
            "price_per_item": (self.price_per_item),
            "total_price": (self.total_price)
        }

class Cart(db.Model):
    __tablename__ = 'Carts'

    cart_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Khóa chính tự động tăng
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False,unique=True)  # Khóa ngoại liên kết với Users
    quantity = db.Column(db.Integer, nullable=False, default=1)  # Số lượng sách trong giỏ
    total_amount = db.Column(db.Float, nullable=False, default=0)
    def to_dict(self):
        return {
            "cart_id": self.cart_id,
            "user_id": self.user_id,
            "quantity": self.quantity,
            "total_amount": self.total_amount
        }
class CartItem(db.Model):
    __tablename__ = 'Cart_Items'

    cart_id = db.Column(db.Integer, db.ForeignKey('Carts.cart_id'), primary_key=True)  # Khóa chính
    book_id = db.Column(db.Integer, db.ForeignKey('Books.book_id'), primary_key=True)  # Khóa chính
    quantity = db.Column(db.Integer, nullable=False, default=1)  # Số lượng sách trong giỏ
    price_at_purchase = db.Column(db.Integer, nullable=False)
    added_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # Thời gian thêm vào giỏ

    # Mối quan hệ với bảng Cart và Book
    cart = db.relationship('Cart', backref=db.backref('cart_items', lazy=True))
    book = db.relationship('Book', backref=db.backref('cart_items', lazy=True))

    def to_dict(self):
        return {
            "cart_id": self.cart_id,
            "book_id": self.book_id,
            "quantity": self.quantity,
            "price_at_purchase":(self.price_at_purchase),
            "added_at": self.added_at
        }


