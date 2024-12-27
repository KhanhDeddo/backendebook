from flask import Blueprint, request, jsonify
from app import db, mail
from flask_mail import Message
from .models import Book, User, Order, Cart,CartItem,OrderItem
api_bp = Blueprint('api', __name__)

def error_response(message, status_code):
    return jsonify({"error": message}), status_code
# ----------------------------------------------------------------------------------
# Route Send Mail
@api_bp.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()
    recipient = data.get('recipient')
    subject = data.get('subject')
    message = data.get('message')

    try:
        msg = Message(subject=subject, recipients=[recipient], body=message)
        mail.send(msg)
        return jsonify({"success": True, "message": "Email sent successfully!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
# ----------------------------------------------------------------------------------
# Route cho trang chủ
@api_bp.route('/', methods=['GET'])
def home():
    return "Welcome to the E-Book API!"
# ----------------------------------------------------------------------------------
#Route để lấy danh sách người dùng
@api_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    if not users:
        return jsonify([]), 200
    return jsonify([user.to_dict() for user in users]), 200
# ----------------------------------------------------------------------------------
# Route tạo người dùng mới
@api_bp.route('/users', methods=['POST'])
def create_user():
    """
    Tạo người dùng mới từ dữ liệu JSON gửi lên.
    """
    data = request.get_json()  # Lấy dữ liệu JSON từ client
    try:
        # Tạo đối tượng User mới
        new_user = User(
            user_name=data['user_name'],
            user_email=data['user_email'],
            user_phone=data['user_phone'],
            user_password=data['user_password'],  # Mã hóa mật khẩu nếu cần
            user_date_of_birth=data['user_date_of_birth'],
            user_gender=data['user_gender'],
            user_address=data['user_address'],
            user_is_admin=data.get('user_is_admin', False)  # Mặc định là người dùng thường
        )
        db.session.add(new_user)  # Thêm vào session
        db.session.commit()  # Lưu vào database
        return jsonify(new_user.to_dict()), 201  # Trả về thông tin người dùng mới
    except Exception as e:
        db.session.rollback()  # Hủy bỏ nếu có lỗi
        return jsonify({"error": f"Failed to create user: {str(e)}"}), 400
# ----------------------------------------------------------------------------------
# Route cập nhật thông tin người dùng theo ID
@api_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Cập nhật thông tin người dùng dựa vào ID.
    """
    data = request.get_json()  # Lấy dữ liệu JSON từ client
    user = User.query.get(user_id)  # Tìm người dùng theo ID
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        # Cập nhật thông tin người dùng
        user.user_name = data.get('user_name', user.user_name)
        user.user_email = data.get('user_email', user.user_email)
        user.user_phone = data.get('user_phone', user.user_phone)
        user.user_password = data.get('user_password', user.user_password)  # Cập nhật mật khẩu nếu cần
        user.user_date_of_birth = data.get('user_date_of_birth', user.user_date_of_birth)
        user.user_gender = data.get('user_gender', user.user_gender)
        user.user_address = data.get('user_address', user.user_address)
        user.user_is_admin = data.get('user_is_admin', user.user_is_admin)

        db.session.commit()  # Lưu thay đổi vào database
        return jsonify(user.to_dict()), 200  # Trả về thông tin người dùng sau khi cập nhật
    except Exception as e:
        db.session.rollback()  # Hủy bỏ nếu có lỗi
        return jsonify({"error": f"Failed to update user: {str(e)}"}), 400
# ----------------------------------------------------------------------------------
# Route xóa người dùng
@api_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Xóa người dùng dựa vào ID.
    """
    user = User.query.get(user_id)  # Tìm người dùng theo ID
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        db.session.delete(user)  # Xóa người dùng
        db.session.commit()  # Lưu thay đổi vào database
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()  # Hủy bỏ nếu có lỗi
        return jsonify({"error": f"Failed to delete user: {str(e)}"}), 400
# ----------------------------------------------------------------------------------
# Route để lấy danh sách sách
@api_bp.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()  # Lấy tất cả sách từ cơ sở dữ liệu
    books_list = [book.to_dict() for book in books]  # Chuyển mỗi book thành dict
    return jsonify(books_list), 200
# ----------------------------------------------------------------------------------
# Route để lấy thông tin sách theo id
@api_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    """
    Lấy thông tin sách dựa vào ID từ cơ sở dữ liệu và trả về dưới dạng JSON.
    """
    book = Book.query.get(book_id)  # Tìm sách theo ID
    if not book:
        return jsonify({"error": "Book not found"}), 404  # Trả về lỗi nếu không tìm thấy sách
    return jsonify(book.to_dict()), 200  # Trả về thông tin sách dưới dạng JSON
# ------------------------------------------------------------------------------------
# Router để Thêm sách mới
@api_bp.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()  # Nhận dữ liệu JSON từ client
    try:
        # Tạo đối tượng sách mới
        new_book = Book(
            title=data['title'],
            status_book = data["status_book"],
            author=data['author'],
            description=data.get('description', ''),
            price=data['price'],
            category=data['category'],
            level_class=data['level_class'],
            level_school=data['level_school'],
            stock_quantity=data.get('stock_quantity', 0),
            publisher=data['publisher']
        )
        db.session.add(new_book)  # Thêm sách mới vào session
        db.session.commit()  # Lưu thay đổi vào database
        return jsonify(new_book.to_dict()), 201  # Trả về thông tin sách vừa thêm
    except Exception as e:
        db.session.rollback()  # Hủy bỏ nếu có lỗi
        return jsonify({"error": f"Failed to create book: {str(e)}"}), 400
# -------------------------------------------------------------------------------------
# Route để cập nhật thông tin sách
@api_bp.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()  # Nhận dữ liệu JSON từ client
    book = Book.query.get(book_id)  # Tìm sách theo ID
    if not book:
        return jsonify({"error": "Book not found"}), 404  # Nếu không tìm thấy sách

    try:
        # Cập nhật thông tin sách
        book.title = data.get('title', book.title)
        book.status_book = data.get('status_book',book.status_book)
        book.author = data.get('author', book.author)
        book.description = data.get('description', book.description)
        book.price = data.get('price', book.price)
        book.category = data.get('category', book.category)
        book.level_class = data.get('level_class', book.level_class)
        book.level_school = data.get('level_school', book.level_school)
        book.stock_quantity = data.get('stock_quantity', book.stock_quantity)
        book.publisher = data.get('publisher', book.publisher)
        db.session.commit()  # Lưu thay đổi vào database
        return jsonify(book.to_dict()), 200  # Trả về thông tin sách vừa cập nhật
    except Exception as e:
        db.session.rollback()  # Hủy bỏ nếu có lỗi
        return jsonify({"error": f"Failed to update book: {str(e)}"}), 400

# -----------------------------------------------------------------------------------
#Route để lấy danh sách giỏ hàng
@api_bp.route('/carts',methods=['GET'])
def get_carts():
    carts= Cart.query.all()
    carts_list = [cart.to_dict() for cart in carts]
    if not carts:
         return jsonify({"error": "Cart not found"}), 404 
    return jsonify(carts_list), 200
# -----------------------------------------------------------------------------------
# Route để Thêm giỏ hàng mới
@api_bp.route('/carts', methods=['POST'])
def create_cart():
    data = request.get_json()
    try:
        new_cart = Cart(
            user_id=data['user_id'],
            quantity=data.get('quantity', 0),
            total_amount=data.get('total_amount', 0.0)
        )
        db.session.add(new_cart)
        db.session.commit()
        return jsonify(new_cart.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create cart: {str(e)}"}), 400
# -----------------------------------------------------------------------------------
# Route để Cập nhật giỏ hàng
@api_bp.route('/carts/<int:cart_id>', methods=['PUT'])
def update_cart(cart_id):
    data = request.get_json()
    cart = Cart.query.get(cart_id)
    if not cart:
        return jsonify({"error": "Cart not found"}), 404

    try:
        cart.quantity = data.get('quantity', cart.quantity)
        cart.total_amount = data.get('total_amount', cart.total_amount)
        db.session.commit()
        return jsonify(cart.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update cart: {str(e)}"}), 400
# -----------------------------------------------------------------------------------
# Route để Xóa giỏ hàng
@api_bp.route('/carts/<int:cart_id>', methods=['DELETE'])
def delete_cart(cart_id):
    cart = Cart.query.get(cart_id)
    if not cart:
        return jsonify({"error": "Cart not found"}), 404

    try:
        db.session.delete(cart)
        db.session.commit()
        return jsonify({"message": "Cart deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete cart: {str(e)}"}), 400
# -----------------------------------------------------------------------------------
#Route để lấy giỏ hàng theo user_id
@api_bp.route('/carts/<int:user_id>', methods=['GET'])
def get_user_cart(user_id):
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return error_response("Cart not found for this user", 404)
    cart_items = CartItem.query.filter_by(cart_id=cart.cart_id).all()
    return jsonify([item.to_dict() for item in cart_items]), 200
# ------------------------------------------------------------------------------------
# Route để lấy tất cả CartItem của giỏ hàng
@api_bp.route('/cartitems', methods=['GET'])
def get_cart_items():
    cart_items = CartItem.query.all()  # Lấy tất cả CartItem
    if not cart_items:
        return jsonify([]), 200  # Trả về danh sách rỗng nếu không có CartItem
    return jsonify([item.to_dict() for item in cart_items]), 200  # Trả về danh sách CartItem
# ------------------------------------------------------------------------------------
# Route để lấy CartItem theo ID
@api_bp.route('/cartitems/<int:cart_id>/<int:book_id>', methods=['GET'])
def get_cart_item(cart_id, book_id):
    cart_item = CartItem.query.get((cart_id, book_id))
    if cart_item is None:
        return jsonify({'message': 'Cart Item not found'}), 404
    return jsonify({
        'cart_id': cart_item.cart_id,
        'book_id': cart_item.book_id,
        'quantity': cart_item.quantity,
        'price_at_purchase': str(cart_item.price_at_purchase),
        'added_at': cart_item.added_at
    })
# ------------------------------------------------------------------------------------
# Route để thêm CartItem mới vào giỏ hàng
@api_bp.route('/cartitems', methods=['POST'])
def create_cart_item():
    data = request.get_json()
    try:
        # Tạo mới CartItem
        new_cart_item = CartItem(
            cart_id=data['cart_id'],  # Giỏ hàng mà CartItem thuộc về
            book_id=data['book_id'],  # Sách trong giỏ hàng
            quantity=data.get('quantity', 1),  # Số lượng sách trong giỏ
            price_at_purchase=data['price_at_purchase']  # Giá mỗi sách
        )
        db.session.add(new_cart_item)  # Thêm CartItem vào session
        db.session.commit()  # Lưu vào database
        return jsonify(new_cart_item.to_dict()), 201  # Trả về thông tin CartItem mới tạo
    except Exception as e:
        db.session.rollback()  # Rollback nếu có lỗi
        return jsonify({"error": f"Failed to create cart item: {str(e)}"}), 400
# ------------------------------------------------------------------------------------
# Route để cập nhật CartItem
@api_bp.route('/cartitems/<int:cart_id>/<int:book_id>', methods=['PUT'])
def update_cart_item(cart_id, book_id):
    data = request.get_json()
    cart_item = CartItem.query.get((cart_id, book_id))
    if cart_item is None:
        return jsonify({'message': 'Cart Item not found'}), 404
    cart_item.quantity = data.get('quantity', cart_item.quantity)
    cart_item.price_at_purchase = data.get('price_at_purchase', cart_item.price_at_purchase)

    db.session.commit()
    return jsonify({'message': 'Cart item updated successfully'})
# ------------------------------------------------------------------------------------
# Route để xóa CartItem
@api_bp.route('/cartitems/<int:cart_id>/<int:book_id>', methods=['DELETE'])
def delete_cart_item(cart_id, book_id):
    cart_item = CartItem.query.get((cart_id, book_id))

    if cart_item is None:
        return jsonify({'message': 'Cart Item not found'}), 404

    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message': 'Cart item deleted successfully'})
# ------------------------------------------------------------------------------------
# Route kiểu tra cartItem có tồn tại hay không
@api_bp.route('/cartitems/check/<int:cart_id>/<int:book_id>', methods=['GET'])
def check_cart_item(cart_id, book_id):
    cart_item = CartItem.query.get((cart_id, book_id))
    if cart_item:
        return jsonify({'exists': True}), 200
    return jsonify({'exists': False}), 404
# ------------------------------------------------------------------------------------
# Route để lấy danh sách đơn hàng
@api_bp.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    orders_list = [order.to_dict() for order in orders]
    return jsonify(orders_list),200
# ------------------------------------------------------------------------------------
# Route để lấy danh sách đơn hàng theo user_id
@api_bp.route('/orders/<int:user_id>', methods=['GET'])
def get_orders_by_user_id(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    if not orders:
        return error_response("No orders found for this user", 404)
    return jsonify([order.to_dict() for order in orders]), 200
# -------------------------------------------------------------------------------------
# Route tạo đơn hàng
@api_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    try:
        new_order = Order(
            user_id=data['user_id'],
            recipient_name=data['recipient_name'],
            recipient_phone=data['recipient_phone'],
            recipient_email=data['recipient_email'],
            shipping_address=data['shipping_address'],
            payment_method=data['payment_method'],
            total_price=data.get('total_price', 0.0),
            status=data.get('status', 'Chờ xác nhận'),
            payment_status=data.get('payment_status', 'Chưa thanh toán')
        )
        db.session.add(new_order)
        db.session.commit()
        return jsonify(new_order.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error creating order: {e}") 
        return jsonify({"error": f"Failed to create cart: {str(e)}"}), 400
# -------------------------------------------------------------------------------------
# Route để Cập nhật đơn hàng
@api_bp.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Cart not found"}), 404

    try:
        order.status = data.get('status', order.status)
        order.payment_status = data.get('payment_status', order.payment_status)
        db.session.commit()
        return jsonify(order.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update cart: {str(e)}"}), 400
# -------------------------------------------------------------------------------------
# Route để lấy danh sách OrderItems
@api_bp.route('/orderitems', methods=['GET'])
def get_order_items():
    orderItems = OrderItem.query.all()
    ordersItems_list = [item.to_dict() for item in orderItems]
    return jsonify(ordersItems_list),200
# ------------------------------------------------------------------------------------
# Route để lấy danh sách orderItems theo order_id
@api_bp.route('/orderitems/<int:order_id>', methods=['GET'])
def get_user_orders(order_id):
    list_orderItems_of_order = Order.query.filter_by(order_id=order_id).first()
    if not list_orderItems_of_order:
        return error_response("Cart not found for this user", 404)
    order_items = OrderItem.query.filter_by(order_id=list_orderItems_of_order.order_id).all()
    return jsonify([item.to_dict() for item in order_items]), 200
# 
# Route để thêm OrderItem mới vào Đơn hàng
@api_bp.route('/orderitems', methods=['POST'])
def create_order_item():
    data = request.get_json()
    try:
        # Tạo mới OrderItem
        new_cart_item = OrderItem(
            order_id=data['order_id'],  # Đơn hàng mà orderItem thuộc vể
            book_id=data['book_id'],  # Sách trong giỏ hàng
            price_per_item=data['price_per_item'],#Giá sách
            quantity=data.get('quantity', 1),  # Số lượng sách
            total_price=data['total_price']  # Tổng tiền
        )
        db.session.add(new_cart_item)  # Thêm OrderItem vào session
        db.session.commit()  # Lưu vào database
        return jsonify(new_cart_item.to_dict()), 201  # Trả về thông tin OrderItem mới tạo
    except Exception as e:
        db.session.rollback()  # Rollback nếu có lỗi
        return jsonify({"error": f"Failed to create cart item: {str(e)}"}), 400
    
# ----------------------------------------------------------------------------------
# Route cho dashboard
@api_bp.route('/dashboard', methods=['GET'])
def dashboard():
    orders = Order.query.count()
    books  =  Book.query.all()
    users = User.query.count()
    item = 0
    for book in books:
        item += book.stock_quantity
    return jsonify(
        {
            "order": orders,
            "book" : len(books),
            "user" : users,
            "item": item
        }
    ), 201
# ----------------------------------------------------------------------------------
LIMIT_RECENT = 5
@api_bp.route('/order-recent', methods=['GET'])
def OrderRecent():
    entities = Order.query.order_by(Order.created_at.desc()).limit(LIMIT_RECENT).all()
    entities_list = [order.to_dict() for order in entities]  # Chuyển mỗi book thành dict
    return jsonify(entities_list), 200

@api_bp.route('/user-recent', methods=['GET'])
def UserRecent():
    entities = User.query.limit(LIMIT_RECENT).all()
    entities_list = [user.to_dict() for user in entities]  # Chuyển mỗi book thành dict
    return jsonify(entities_list), 200