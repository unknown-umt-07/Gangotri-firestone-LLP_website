import sys
import os
import json

# Ensure project root is on sys.path when running from scripts/
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database import Database

if __name__ == '__main__':
    db = Database()
    products = db.get_products()
    print(json.dumps({"count": len(products), "sample": products[:5]}, indent=2, default=str))
