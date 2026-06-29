import os
import sys
import tempfile
import unittest

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import Database


class CatalogTests(unittest.TestCase):
    def test_default_catalog_contains_complete_product_range(self):
        db = Database()
        products = db.get_products()
        names = {product.get("name", "").upper() for product in products}

        required_products = {
            "HEXA SNF 200",
            "HEXAPLAST 550",
            "HEXAPLAST 750",
            "HEXAPLAST 900",
            "HC SBR NPU",
            "HC MIX LW+",
            "HC CURING COMPOUND",
            "HEXA BLOCK JOINING MORTAR",
            "HEXA TILE ADHESIVE",
            "HEXA READY PLASTER",
        }

        missing = sorted(required_products - names)
        self.assertFalse(missing, f"Missing product catalog items: {missing}")

    def test_local_fallback_seeds_complete_catalog_when_storage_is_empty(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            local_db_path = os.path.join(temp_dir, "local_db.json")
            os.environ["USE_FIREBASE"] = "false"
            try:
                db = Database(local_db_path=local_db_path, credentials_path=os.path.join(temp_dir, "firebase_credentials.json"))
                products = db.get_products()
            finally:
                os.environ.pop("USE_FIREBASE", None)

            names = {product.get("name", "").upper() for product in products}
            self.assertIn("HEXA SNF 200", names)
            self.assertIn("HEXA BLOCK JOINING MORTAR", names)
            self.assertEqual(len(products), 10)


if __name__ == "__main__":
    unittest.main()
