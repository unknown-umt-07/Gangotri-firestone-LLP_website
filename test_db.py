import sys
import os

# Ensure the script directory is in the Python search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import Database

def test_database():
    print("Testing Database wrapper...")
    db = Database()
    
    # 1. Check products count, seed if empty
    products = db.get_products()
    if len(products) == 0:
        print("Database is empty. Seeding products automatically...")
        import seed_products
        seed_products.seed()
        products = db.get_products()
        
    print(f"Total products fetched: {len(products)}")
    assert len(products) > 0, "Products list should not be empty!"
    
    # 2. Test fetching single product
    test_id = products[0]["id"]
    product = db.get_product(test_id)
    print(f"Fetched product '{test_id}': {product is not None}")
    assert product is not None, "Failed to fetch single product!"
    assert product["name"] == products[0]["name"], "Product names do not match!"
    
    # 3. Test submitting inquiry
    test_inquiry = {
        "name": "Test Builder",
        "email": "test@builder.com",
        "phone": "+91 99999 88888",
        "company": "Builders Association",
        "message": "Interested in bulk pricing for HEXA SNF 200.",
        "products": ["HEXA SNF 200"]
    }
    
    print("Submitting mock inquiry...")
    success = db.add_inquiry(test_inquiry)
    print(f"Inquiry submission: {success}")
    assert success, "Failed to submit inquiry!"
    
    # 4. Verify inquiry list contains the mock submission
    inquiries = db.get_inquiries()
    print(f"Total inquiries in DB: {len(inquiries)}")
    assert len(inquiries) > 0, "Inquiries should have at least 1 entry!"
    
    newest_inq = inquiries[0]
    print(f"Newest inquiry name: '{newest_inq['name']}'")
    assert newest_inq["name"] == "Test Builder", "Inquiry name mismatch!"
    
    print("All database tests passed successfully!")

if __name__ == "__main__":
    test_database()
