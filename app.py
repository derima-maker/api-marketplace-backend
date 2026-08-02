import os
import sys
import jwt
import bcrypt
import datetime
import secrets
import string
from functools import wraps
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import json

print("=" * 50)
print("🚀 Starting API Marketplace Backend...")
print("=" * 50)

try:
    load_dotenv()
    print("✅ .env loaded")
except Exception as e:
    print(f"❌ .env load error: {e}")

app = Flask(__name__)
CORS(app)

# ─── CONFIG ──────────────────────────────────────────────
DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')
COMMISSION_PERCENT = float(os.getenv('COMMISSION_PERCENT', 10))

print(f"🔧 DATABASE_URL: {DATABASE_URL[:30]}..." if DATABASE_URL else "❌ DATABASE_URL NOT SET!")
print(f"🔧 SECRET_KEY: {'✅ SET' if SECRET_KEY else '❌ NOT SET!'}")
print(f"🔧 COMMISSION_PERCENT: {COMMISSION_PERCENT}")

if not DATABASE_URL:
    print("❌ ERROR: DATABASE_URL environment variable is missing!")
    print("💡 Please add it in Render Environment Variables")
    sys.exit(1)

if not SECRET_KEY:
    print("❌ ERROR: SECRET_KEY environment variable is missing!")
    print("💡 Please add it in Render Environment Variables")
    sys.exit(1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY
app.config['COMMISSION_PERCENT'] = COMMISSION_PERCENT

try:
    db = SQLAlchemy(app)
    print("✅ SQLAlchemy initialized")
except Exception as e:
    print(f"❌ SQLAlchemy error: {e}")
    sys.exit(1)

# ─── HELPERS ──────────────────────────────────────────────
def generate_user_api_key():
    return 'api_' + ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))

def generate_plan_expiry(plan_type, duration):
    if plan_type == 'lifetime':
        return None
    delta_map = {
        'day': datetime.timedelta(days=duration),
        'week': datetime.timedelta(weeks=duration),
        'month': datetime.timedelta(days=duration * 30),
        'year': datetime.timedelta(days=duration * 365)
    }
    delta = delta_map.get(plan_type)
    return datetime.datetime.utcnow() + delta if delta else None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token missing'}), 401
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# ─── MODELS ────────────────────────────────────────────────
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='consumer')
    api_key = db.Column(db.String(100), unique=True, nullable=False, default=generate_user_api_key)
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    earnings = db.Column(db.Float, default=0.0)

    def to_dict(self, show_api_key=False):
        data = {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'role': self.role,
            'verified': self.verified,
            'created_at': self.created_at.isoformat(),
            'earnings': self.earnings
        }
        if show_api_key:
            data['apiKey'] = self.api_key
        return data

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    icon = db.Column(db.String(50), default='fa-cloud-sun')
    color = db.Column(db.String(20), default='#4285f4')
    price_display = db.Column(db.String(50), default='Free')
    pricing_tiers = db.Column(db.Text, default='[{"name":"Free","price":0,"planType":"lifetime","duration":0}]')
    plan_type = db.Column(db.String(20), default='lifetime')
    plan_duration = db.Column(db.Integer, default=0)
    endpoint_url = db.Column(db.String(255), nullable=True)
    documentation_url = db.Column(db.String(255), nullable=True)
    avg_rating = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    creator = db.relationship('User', backref='products')

    def to_dict(self):
        return {
            'id': self.id,
            'creatorId': self.creator_id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'icon': self.icon,
            'color': self.color,
            'priceDisplay': self.price_display,
            'pricingTiers': json.loads(self.pricing_tiers) if self.pricing_tiers else [],
            'planType': self.plan_type,
            'planDuration': self.plan_duration,
            'endpointUrl': self.endpoint_url,
            'documentationUrl': self.documentation_url,
            'avgRating': self.avg_rating,
            'createdAt': self.created_at.isoformat()
        }

class Purchase(db.Model):
    __tablename__ = 'purchases'
    id = db.Column(db.Integer, primary_key=True)
    consumer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    key = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='active')
    purchased_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    tier_name = db.Column(db.String(50), nullable=True)
    amount_paid = db.Column(db.Float, default=0.0)
    requests_count = db.Column(db.Integer, default=0)
    last_used = db.Column(db.DateTime, nullable=True)

    consumer = db.relationship('User', backref='purchases')
    product = db.relationship('Product', backref='purchases')

    def is_active(self):
        if self.status != 'active':
            return False
        if self.expires_at and datetime.datetime.utcnow() > self.expires_at:
            return False
        return True

    def to_dict(self):
        return {
            'id': self.id,
            'consumerId': self.consumer_id,
            'productId': self.product_id,
            'key': self.key,
            'status': self.status,
            'purchasedAt': self.purchased_at.isoformat(),
            'expiresAt': self.expires_at.isoformat() if self.expires_at else None,
            'tierName': self.tier_name,
            'amountPaid': self.amount_paid,
            'requestsCount': self.requests_count,
            'lastUsed': self.last_used.isoformat() if self.last_used else None,
            'isActive': self.is_active(),
            'product': self.product.to_dict() if self.product else None
        }

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    user = db.relationship('User')
    product = db.relationship('Product', backref='reviews')

    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'userName': self.user.name if self.user else None,
            'productId': self.product_id,
            'rating': self.rating,
            'comment': self.comment,
            'createdAt': self.created_at.isoformat()
        }

class ForumTopic(db.Model):
    __tablename__ = 'forum_topics'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    pinned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    user = db.relationship('User')
    product = db.relationship('Product', backref='topics')
    posts = db.relationship('ForumPost', backref='topic', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'productId': self.product_id,
            'userId': self.user_id,
            'userName': self.user.name if self.user else None,
            'title': self.title,
            'pinned': self.pinned,
            'createdAt': self.created_at.isoformat(),
            'postsCount': len(self.posts)
        }

class ForumPost(db.Model):
    __tablename__ = 'forum_posts'
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('forum_topics.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    user = db.relationship('User')

    def to_dict(self):
        return {
            'id': self.id,
            'topicId': self.topic_id,
            'userId': self.user_id,
            'userName': self.user.name if self.user else None,
            'content': self.content,
            'createdAt': self.created_at.isoformat()
        }

print("✅ Models defined")

# ─── ROUTES ──────────────────────────────────────────────
@app.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    if not email or not password or not name:
        return jsonify({'error': 'Missing fields'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    user = User(email=email, password_hash=hashed.decode('utf-8'), name=name, verified=False)
    db.session.add(user)
    db.session.commit()
    return jsonify({'success': True, 'user': user.to_dict(show_api_key=True)}), 201

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'error': 'Missing credentials'}), 400
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        return jsonify({'error': 'Invalid credentials'}), 401
    if not user.verified:
        return jsonify({'error': 'Please verify your email first.'}), 403
    token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)},
                       app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'success': True, 'token': token, 'user': user.to_dict(show_api_key=True)}), 200

@app.route('/auth/me', methods=['GET'])
@token_required
def get_me(current_user):
    return jsonify({'user': current_user.to_dict(show_api_key=True)}), 200

@app.route('/auth/resend-verification', methods=['POST'])
def resend_verification():
    data = request.json
    email = data.get('email')
    user = User.query.filter_by(email=email).first()
    if not user or user.verified:
        return jsonify({'error': 'User not found or already verified'}), 400
    return jsonify({'success': True, 'message': 'Verification email sent.'}), 200

@app.route('/api/products', methods=['GET'])
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category')
    min_rating = request.args.get('min_rating', type=float)
    search = request.args.get('search', '').strip()
    query = Product.query
    if category:
        query = query.filter_by(category=category)
    if min_rating:
        query = query.filter(Product.avg_rating >= min_rating)
    if search:
        query = query.filter(
            db.or_(
                Product.name.ilike(f'%{search}%'),
                Product.description.ilike(f'%{search}%')
            )
        )
    paginated = query.order_by(Product.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'products': [p.to_dict() for p in paginated.items],
        'total': paginated.total,
        'page': page,
        'per_page': per_page,
        'pages': paginated.pages
    }), 200

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product.to_dict()), 200

@app.route('/api/products', methods=['POST'])
@token_required
def create_product(current_user):
    data = request.json
    required = ['name', 'description', 'category']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing fields'}), 400
    product = Product(
        creator_id=current_user.id,
        name=data['name'],
        description=data['description'],
        category=data['category'],
        icon=data.get('icon', 'fa-cloud-sun'),
        color=data.get('color', '#4285f4'),
        price_display=data.get('priceDisplay', 'Free'),
        plan_type=data.get('planType', 'lifetime'),
        plan_duration=data.get('planDuration', 0),
        endpoint_url=data.get('endpointUrl', ''),
        documentation_url=data.get('documentationUrl', ''),
        pricing_tiers=json.dumps(data.get('pricingTiers', []))
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@token_required
def delete_product(current_user, product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    if product.creator_id != current_user.id and current_user.role != 'admin':
        return jsonify({'error': 'Permission denied'}), 403
    db.session.delete(product)
    db.session.commit()
    return jsonify({'success': True}), 200

@app.route('/api/products/my', methods=['GET'])
@token_required
def get_my_products(current_user):
    products = Product.query.filter_by(creator_id=current_user.id).all()
    return jsonify([p.to_dict() for p in products]), 200

@app.route('/api/products/<int:product_id>/purchase', methods=['POST'])
@token_required
def purchase_product(current_user, product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    data = request.json or {}
    tier_name = data.get('tierName')
    tiers = json.loads(product.pricing_tiers) if product.pricing_tiers else []
    selected_tier = None
    if tier_name:
        selected_tier = next((t for t in tiers if t.get('name') == tier_name), None)
    if not selected_tier and tiers:
        selected_tier = tiers[0]
    if not selected_tier:
        selected_tier = {'name': 'Standard', 'price': 0, 'planType': product.plan_type, 'duration': product.plan_duration}
    amount_paid = float(selected_tier.get('price', 0))
    plan_type = selected_tier.get('planType', 'lifetime')
    duration = int(selected_tier.get('duration', 0))
    existing = Purchase.query.filter_by(consumer_id=current_user.id, product_id=product_id).first()
    if existing:
        if existing.is_active():
            return jsonify({'success': True, 'key': existing.key, 'expiresAt': existing.expires_at}), 200
        else:
            existing.expires_at = generate_plan_expiry(plan_type, duration)
            existing.status = 'active'
            existing.tier_name = selected_tier['name']
            existing.amount_paid = amount_paid
            db.session.commit()
            commission = amount_paid * app.config['COMMISSION_PERCENT'] / 100
            creator = User.query.get(product.creator_id)
            if creator:
                creator.earnings += amount_paid - commission
                db.session.commit()
            return jsonify({'success': True, 'key': existing.key, 'expiresAt': existing.expires_at}), 200
    expires_at = generate_plan_expiry(plan_type, duration)
    purchase = Purchase(
        consumer_id=current_user.id,
        product_id=product_id,
        key=current_user.api_key,
        expires_at=expires_at,
        tier_name=selected_tier['name'],
        amount_paid=amount_paid
    )
    db.session.add(purchase)
    commission = amount_paid * app.config['COMMISSION_PERCENT'] / 100
    creator = User.query.get(product.creator_id)
    if creator:
        creator.earnings += amount_paid - commission
    db.session.commit()
    return jsonify({'success': True, 'key': current_user.api_key, 'expiresAt': expires_at.isoformat() if expires_at else None}), 201

@app.route('/api/purchases/my', methods=['GET'])
@token_required
def get_my_purchases(current_user):
    purchases = Purchase.query.filter_by(consumer_id=current_user.id).all()
    return jsonify([p.to_dict() for p in purchases]), 200

@app.route('/test-proxy', methods=['POST'])
@token_required
def test_proxy(current_user):
    data = request.json
    product_id = data.get('productId')
    method = data.get('method', 'GET')
    path = data.get('path', '')
    body = data.get('body', {})
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    if not product.endpoint_url:
        return jsonify({'error': 'No endpoint URL configured'}), 400
    purchase = Purchase.query.filter_by(consumer_id=current_user.id, product_id=product_id).first()
    if not purchase or not purchase.is_active():
        return jsonify({'error': 'No active subscription'}), 403
    target = product.endpoint_url.rstrip('/') + '/' + path.lstrip('/')
    headers = {'X-API-Key': current_user.api_key, 'Content-Type': 'application/json'}
    try:
        if method.upper() == 'GET':
            resp = requests.get(target, headers=headers, timeout=10)
        elif method.upper() == 'POST':
            resp = requests.post(target, json=body, headers=headers, timeout=10)
        else:
            return jsonify({'error': 'Method not supported'}), 400
        purchase.requests_count += 1
        purchase.last_used = datetime.datetime.utcnow()
        db.session.commit()
        try:
            response_data = resp.json()
        except:
            response_data = resp.text
        return jsonify({'status': resp.status_code, 'headers': dict(resp.headers), 'data': response_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products/<int:product_id>/reviews', methods=['GET'])
def get_reviews(product_id):
    reviews = Review.query.filter_by(product_id=product_id).order_by(Review.created_at.desc()).all()
    return jsonify([r.to_dict() for r in reviews]), 200

@app.route('/api/products/<int:product_id>/reviews', methods(['POST'])
@token_required
def create_review(current_user, product_id):
    data = request.json
    rating = data.get('rating')
    comment = data.get('comment')
    if not rating or rating < 1 or rating > 5:
        return jsonify({'error': 'Rating must be 1-5'}), 400
    purchase = Purchase.query.filter_by(consumer_id=current_user.id, product_id=product_id).first()
    if not purchase:
        return jsonify({'error': 'You must have access to review'}), 403
    review = Review(user_id=current_user.id, product_id=product_id, rating=rating, comment=comment)
    db.session.add(review)
    product = Product.query.get(product_id)
    if product:
        all_reviews = Review.query.filter_by(product_id=product_id).all()
        product.avg_rating = sum(r.rating for r in all_reviews) / len(all_reviews) if all_reviews else rating
    db.session.commit()
    return jsonify(review.to_dict()), 201

@app.route('/api/forum/topics', methods=['GET'])
def get_topics():
    product_id = request.args.get('product_id', type=int)
    query = ForumTopic.query
    if product_id:
        query = query.filter_by(product_id=product_id)
    topics = query.order_by(ForumTopic.pinned.desc(), ForumTopic.created_at.desc()).all()
    return jsonify([t.to_dict() for t in topics]), 200

@app.route('/api/forum/topics', methods=['POST'])
@token_required
def create_topic(current_user):
    data = request.json
    product_id = data.get('productId')
    title = data.get('title')
    if not product_id or not title:
        return jsonify({'error': 'Missing fields'}), 400
    topic = ForumTopic(product_id=product_id, user_id=current_user.id, title=title)
    db.session.add(topic)
    db.session.commit()
    return jsonify(topic.to_dict()), 201

@app.route('/api/forum/topics/<int:topic_id>/posts', methods=['GET'])
def get_posts(topic_id):
    posts = ForumPost.query.filter_by(topic_id=topic_id).order_by(ForumPost.created_at.asc()).all()
    return jsonify([p.to_dict() for p in posts]), 200

@app.route('/api/forum/topics/<int:topic_id>/posts', methods=['POST'])
@token_required
def create_post(current_user, topic_id):
    data = request.json
    content = data.get('content')
    if not content:
        return jsonify({'error': 'Content required'}), 400
    post = ForumPost(topic_id=topic_id, user_id=current_user.id, content=content)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201

@app.route('/api/forum/topics/<int:topic_id>/pin', methods=['POST'])
@token_required
def pin_topic(current_user, topic_id):
    topic = ForumTopic.query.get(topic_id)
    if not topic:
        return jsonify({'error': 'Topic not found'}), 404
    data = request.json
    pinned = data.get('pinned', False)
    topic.pinned = pinned
    db.session.commit()
    return jsonify({'success': True, 'pinned': pinned}), 200

@app.route('/api/analytics/me', methods=['GET'])
@token_required
def get_analytics(current_user):
    purchases = Purchase.query.filter_by(consumer_id=current_user.id).all()
    total_requests = sum(p.requests_count for p in purchases)
    active_keys = sum(1 for p in purchases if p.is_active())
    my_products = Product.query.filter_by(creator_id=current_user.id).all()
    product_ids = [p.id for p in my_products]
    product_purchases = Purchase.query.filter(Purchase.product_id.in_(product_ids)).all() if product_ids else []
    total_api_calls = sum(p.requests_count for p in product_purchases)
    total_subscribers = len(product_purchases)
    top_products = []
    if my_products:
        usage = {}
        for p in my_products:
            usage[p.id] = sum(pur.requests_count for pur in product_purchases if pur.product_id == p.id)
        top_products = sorted(usage.items(), key=lambda x: x[1], reverse=True)[:5]
        top_products = [{'product_id': pid, 'calls': count, 'product_name': next((p.name for p in my_products if p.id == pid), 'Unknown')} for pid, count in top_products]
    return jsonify({
        'totalRequests': total_requests,
        'activeKeys': active_keys,
        'totalApiCalls': total_api_calls,
        'totalSubscribers': total_subscribers,
        'myEarnings': current_user.earnings,
        'topProducts': top_products
    }), 200

@app.route('/admin/users', methods=['GET'])
@token_required
def admin_list_users(current_user):
    if current_user.role != 'admin':
        return jsonify({'error': 'Admin only'}), 403
    users = User.query.all()
    return jsonify([u.to_dict() for u in users]), 200

@app.route('/admin/users/<int:user_id>', methods=['PUT'])
@token_required
def admin_update_user(current_user, user_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Admin only'}), 403
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    data = request.json
    if 'role' in data:
        user.role = data['role']
    if 'earnings' in data:
        user.earnings = data['earnings']
    db.session.commit()
    return jsonify({'success': True, 'user': user.to_dict()}), 200

@app.route('/admin/users/<int:user_id>', methods=['DELETE'])
@token_required
def admin_delete_user(current_user, user_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Admin only'}), 403
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'success': True}), 200

@app.route('/admin/products', methods=['GET'])
@token_required
def admin_list_products(current_user):
    if current_user.role != 'admin':
        return jsonify({'error': 'Admin only'}), 403
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products]), 200

print("✅ Routes defined")

# ─── SEED DATABASE ──────────────────────────────────────
with app.app_context():
    try:
        db.create_all()
        print("✅ Database tables created")
    except Exception as e:
        print(f"❌ Database table creation error: {e}")
        sys.exit(1)

    if User.query.count() == 0:
        print("🌱 Seeding database with demo data...")
        try:
            demo_user = User(
                email='demo@example.com',
                password_hash=bcrypt.hashpw('demo123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                name='Demo User',
                verified=True
            )
            admin_user = User(
                email='admin@example.com',
                password_hash=bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                name='Admin',
                role='admin',
                verified=True
            )
            db.session.add_all([demo_user, admin_user])
            db.session.commit()

            products = [
                Product(creator_id=demo_user.id, name='Weather API', description='Real-time weather data.', category='Weather',
                        icon='fa-cloud-sun', color='#4285f4', price_display='$5/month', plan_type='month', plan_duration=1,
                        endpoint_url='https://api.weatherapi.com/v1/current.json'),
                Product(creator_id=demo_user.id, name='Translate Pro', description='AI translation for 100+ languages.', category='Language',
                        icon='fa-language', color='#34a853', price_display='$10/month', plan_type='month', plan_duration=1,
                        endpoint_url='https://api.example.com/translate'),
                Product(creator_id=demo_user.id, name='ImageForge AI', description='Generate images from text.', category='AI',
                        icon='fa-image', color='#fbbc04', price_display='$15/month', plan_type='year', plan_duration=1,
                        endpoint_url='https://api.example.com/image'),
                Product(creator_id=demo_user.id, name='SMS Gateway', description='Send global SMS.', category='Communication',
                        icon='fa-sms', color='#ea4335', price_display='$0.01/message', plan_type='day', plan_duration=30,
                        endpoint_url='https://api.example.com/sms'),
                Product(creator_id=demo_user.id, name='PayFlow API', description='Unified payment integration.', category='Finance',
                        icon='fa-credit-card', color='#ff6d00', price_display='$29/month', plan_type='month', plan_duration=1,
                        endpoint_url='https://api.example.com/pay'),
                Product(creator_id=demo_user.id, name='Analytics Hub', description='Track user behavior.', category='Analytics',
                        icon='fa-chart-pie', color='#7c4dff', price_display='Free', plan_type='lifetime', plan_duration=0,
                        endpoint_url='https://api.example.com/analytics'),
            ]
            for p in products:
                db.session.add(p)
            db.session.commit()
            print("✅ Seeding complete! Login with demo@example.com / demo123 or admin@example.com / admin123")
        except Exception as e:
            print(f"❌ Seeding error: {e}")
            sys.exit(1)

print("=" * 50)
print("✅ App is ready to start! 🚀")
print("=" * 50)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f"🔌 Starting server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)