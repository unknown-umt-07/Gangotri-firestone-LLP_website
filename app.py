import os
import tempfile
import uuid
# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_socketio import SocketIO
from database import Database

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "gangotri_firestone_secret_key_129847192")

# Admin password (default: admin123)
ADMIN_PASSCODE = os.environ.get("ADMIN_PASSCODE", "admin123")

# Initialize database
db = Database()

# Initialize Socket.IO for realtime updates
socketio = SocketIO(app, cors_allowed_origins="*")

# Helper to check if admin is logged in
def is_admin_logged_in():
    return session.get("admin_authenticated") == True

# Desired liquid product order for the public catalog
LIQUID_PRODUCT_ORDER = [
    "HEXA SNF 200",
    "HEXAPLAST 550",
    "HEXAPLAST 750",
    "HEXAPLAST 900",
    "HC SBR NPU",
    "HC MIX LW+",
    "HC CURING COMPOUND"
]


def sort_products(products):
    order_map = {name: index for index, name in enumerate(LIQUID_PRODUCT_ORDER)}

    def key(product):
        category = product.get("category", "")
        name = product.get("name", "")
        if category == "Liquid Base":
            return (0, order_map.get(name, len(LIQUID_PRODUCT_ORDER)), name)
        if category == "Powder Base":
            return (1, name)
        return (2, name)

    return sorted(products, key=key)


# Ensure uploads folder exists and use a writable temp location in hosted environments.
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")
if not UPLOAD_FOLDER:
    if os.environ.get("RENDER"):
        UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), "gangotri_firestone", "uploads")
    else:
        UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- VIEWS ---

@app.route('/')
def index():
    # Home page highlights
    products = sort_products(db.get_products())
    return render_template('index.html', products=products)

@app.route('/products')
def products_page():
    products = sort_products(db.get_products())
    return render_template('products.html', products=products)

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/contact')
def contact_page():
    products = sort_products(db.get_products())
    return render_template('contact.html', products=products)

@app.route('/product/<product_id>')
def product_detail(product_id):
    # Fetch specific product details
    product = db.get_product(product_id)
    if not product:
        return render_template('404.html'), 404
    return render_template('product.html', product=product)

@app.route('/admin')
def admin():
    if not is_admin_logged_in():
        return render_template('admin.html', authenticated=False)
    
    # Render dashboard if authenticated
    inquiries = db.get_inquiries()
    products = db.get_products()
    return render_template('admin.html', authenticated=True, inquiries=inquiries, products=products)

@app.route('/admin/login', methods=['POST'])
def admin_login():
    passcode = request.form.get("passcode", "")
    if passcode == ADMIN_PASSCODE:
        session["admin_authenticated"] = True
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Invalid passcode"}), 401

@app.route('/admin/logout')
def admin_logout():
    session.pop("admin_authenticated", None)
    return redirect(url_for('index'))


# --- API ENDPOINTS ---

@app.route('/api/inquiry', methods=['POST'])
def submit_inquiry():
    try:
        data = request.json or request.form
        
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        phone = data.get("phone", "").strip()
        company = data.get("company", "").strip()
        message = data.get("message", "").strip()
        selected_products = data.get("products", []) # list of product IDs
        
        if not name or not phone or not message:
            return jsonify({"success": False, "error": "Name, Phone, and Message are required fields."}), 400
            
        inquiry_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "company": company,
            "message": message,
            "products": selected_products
        }
        
        success = db.add_inquiry(inquiry_data)
        if success:
            return jsonify({"success": True, "message": "Inquiry submitted successfully."})
        return jsonify({"success": False, "error": "Failed to save inquiry."}), 500
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/inquiry/<inquiry_id>', methods=['DELETE'])
def delete_inquiry(inquiry_id):
    if not is_admin_logged_in():
        return jsonify({"success": False, "error": "Unauthorized"}), 403
        
    try:
        success = db.delete_inquiry(inquiry_id)
        if success:
            return jsonify({"success": True})
        return jsonify({"success": False, "error": "Inquiry not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        products = db.get_products()
        return jsonify({"success": True, "products": products})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/products', methods=['POST'])
def save_product():
    if not is_admin_logged_in():
        return jsonify({"success": False, "error": "Unauthorized"}), 403
        
    try:
        # Check if form data or JSON
        if request.form:
            product_id = request.form.get("id", "").strip()
            if not product_id:
                # Generate from name
                name = request.form.get("name", "")
                product_id = name.lower().replace(" ", "-").replace("/", "-")
                
            # Handle image file upload
            image_url = request.form.get("image_url", "")
            image_file = request.files.get("image_file")
            if image_file and image_file.filename != '':
                filename = f"{uuid.uuid4().hex}_{image_file.filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(file_path)
                image_url = f"/static/uploads/{filename}"
                
            # Construct product dict
            product_data = {
                "name": request.form.get("name", "").strip(),
                "code": request.form.get("code", "").strip(),
                "category": request.form.get("category", "Liquid Base").strip(),
                "tagline": request.form.get("tagline", "").strip(),
                "description": request.form.get("description", "").strip(),
                "dosage": request.form.get("dosage", "").strip(),
                "compliance": request.form.get("compliance", "").strip(),
                "packaging": request.form.get("packaging", "").strip(),
                "image": image_url
            }
            
            # Read lists (splits by newlines or commas)
            benefits_raw = request.form.get("key_benefits", "")
            product_data["key_benefits"] = [b.strip() for b in benefits_raw.split("\n") if b.strip()]
            
            guide_raw = request.form.get("application_guide", "")
            product_data["application_guide"] = [g.strip() for g in guide_raw.split("\n") if g.strip()]
            
            # Read specs (expected format key:value per line)
            specs_raw = request.form.get("technical_features", "")
            specs = {}
            for line in specs_raw.split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    specs[k.strip()] = v.strip()
            product_data["technical_features"] = specs
            
        else:
            data = request.json
            product_id = data.get("id")
            product_data = data
            
        if not product_id or not product_data.get("name"):
            return jsonify({"success": False, "error": "Product ID and Name are required"}), 400
            
        success = db.add_product(product_id, product_data)
        if success:
            # Notify connected clients that products changed
            try:
                socketio.emit('products_updated', {"action": "save", "product_id": product_id}, broadcast=True)
            except Exception:
                pass
            return jsonify({"success": True, "product_id": product_id})
        return jsonify({"success": False, "error": "Failed to save product"}), 500
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    if not is_admin_logged_in():
        return jsonify({"success": False, "error": "Unauthorized"}), 403
        
    try:
        success = db.delete_product(product_id)
        if success:
            # Notify connected clients that a product was deleted
            try:
                socketio.emit('products_updated', {"action": "delete", "product_id": product_id}, broadcast=True)
            except Exception:
                pass
            return jsonify({"success": True})
        return jsonify({"success": False, "error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # Start web server with Socket.IO support (uses eventlet if installed)
    socketio.run(app, debug=False, host='0.0.0.0', port=5000)
