from flask import Blueprint, request, jsonify
from .models import Product, ChatLog, User
from . import db

main = Blueprint('main', __name__)

@main.route("/")
def home():

    return " E-commerce Chatbot Backend is Running!"

@main.route("/search")
def search_products():
    query = request.args.get('query')
    results = Product.query.filter(Product.name.ilike(f"%{query}%")).all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'description': p.description,
        'rating': p.rating
    } for p in results])

@main.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 409

    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"})


@main.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return jsonify({"message": "Login successful!"})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@main.route("/admin-products", methods=["GET"])
def admin_products():
    products = Product.query.all()
    return jsonify([{
        "name": p.name,
        "category": p.category,
        "price": p.price,
        "rating": p.rating
    } for p in products])


@main.route('/add-product', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get("name")
    category = data.get("category")
    price = data.get("price")
    rating = data.get("rating")

    if not all([name, category, price, rating]):
        return jsonify({"success": False, "message": "Missing data"}), 400

    new_product = Product(
        name=name,
        category=category,
        price=price,
        rating=rating,
        description="Added by admin",
    )
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"success": True, "message": "Product added successfully"})



@main.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "").lower().strip()
    print(f"User said: {user_msg}")

    reply = ""
    products_cards = []

    if not user_msg:
        reply = "Please type something..."
    elif "hello" in user_msg or "hi" in user_msg:
        reply = "Hey there! 👋 I'm your shopping assistant. Here are some things you can try:"
    elif "help" in user_msg:
        reply = ("Here are some things you can try:\n"
                 "- 'show mobiles'\n"
                 "- 'search books'\n"
                 "- 'under 1000'\n"
                 "- 'show all'\n"
                 "- 'reset'")
    elif "show mobiles" in user_msg:
        products = Product.query.filter(Product.category.ilike("%Mobile%")).limit(3).all()
        if products:
            reply = "Here are some mobiles:"
            products_cards = [{
                "name": p.name,
                "price": p.price,
                "image": "https://via.placeholder.com/100",
                "rating": p.rating
            } for p in products]
        else:
            reply = "No mobiles found!"
    elif "search books" in user_msg:
        products = Product.query.filter(Product.category.ilike("%Book%")).limit(3).all()
        if products:
            reply = "Here are some books:"
            products_cards = [{
                "name": p.name,
                "price": p.price,
                "image": "https://via.placeholder.com/100",
                "rating": p.rating
            } for p in products]
        else:
            reply = "No books found!"
    elif "under 1000" in user_msg:
        products = Product.query.filter(Product.price <= 1000).limit(3).all()
        if products:
            reply = "Here are some budget products:"
            products_cards = [{
                "name": p.name,
                "price": p.price,
                "image": "https://via.placeholder.com/100",
                "rating": p.rating
            } for p in products]
        else:
            reply = "Nothing found under ₹1000."
    elif "show all" in user_msg:
        products = Product.query.limit(5).all()
        reply = "Showing some products:"
        products_cards = [{
            "name": p.name,
            "price": p.price,
            "image": "https://via.placeholder.com/100",
            "rating": p.rating
        } for p in products]
    elif "top rated" in user_msg:
        products = Product.query.filter(Product.rating >= 4.5).limit(3).all()
        if products:
            reply = "Here are top-rated products:"
            products_cards = [{
                "name": p.name,
                "price": p.price,
                "image": "https://via.placeholder.com/100",
                "rating": p.rating
            } for p in products]
        else:
            reply = "No top-rated products found."
    elif "category" in user_msg:
        reply = "Please type a category like 'Mobiles', 'Books', or 'Fashion'"
    else:
        reply = "Sorry, I didn’t understand that. Type 'help' to see what I can do."

    log = ChatLog(user_msg=user_msg, bot_reply=reply)
    db.session.add(log)
    db.session.commit()

    return jsonify({"reply": reply, "products": products_cards})
