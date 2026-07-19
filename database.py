import os
import json
import tempfile
import threading
from datetime import datetime, timezone

# Thread safety lock for local JSON operations
_db_lock = threading.Lock()

class Database:
    def __init__(self, credentials_path="firebase_credentials.json", local_db_path="local_db.json"):
        # Resolve paths relative to database.py directory if they are relative
        base_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isabs(credentials_path):
            credentials_path = os.path.join(base_dir, credentials_path)

        local_db_override = os.environ.get("LOCAL_DB_PATH")
        if local_db_override:
            local_db_path = local_db_override
        elif os.environ.get("RENDER"):
            local_db_path = os.path.join(tempfile.gettempdir(), "gangotri_firestone", "local_db.json")
        elif not os.path.isabs(local_db_path):
            local_db_path = os.path.join(base_dir, local_db_path)

        self.credentials_path = credentials_path
        self.local_db_path = local_db_path
        self.use_firebase = False
        self.db = None
        self.firebase_app = None
        self.init_db()

    def _get_default_products(self):
        return [
            {
                "id": "hexa-snf-200",
                "name": "HEXA SNF 200",
                "code": "SNF 200",
                "category": "Liquid Base",
                "tagline": "Superplasticizer Admixture (SNF Based)",
                "description": "A Sulpho-naphthalene-formaldehyde based superplasticizer designed to provide high-range water reduction, improve workability, and accelerate early strength development. It reduces concrete permeability and shrinkage, making it safe for reinforced and prestressed concrete.",
                "key_benefits": [
                    "High-range water reduction with improved workability",
                    "Increases early and ultimate compressive strength",
                    "Reduces permeability, shrinkage & creep",
                    "Improves cohesion, pumpability & finishing",
                    "Enables earlier de-moulding in precast concrete",
                    "Chloride-free - safe for RCC & prestressed concrete",
                    "Cost-effective solution for high-performance concrete"
                ],
                "technical_features": {
                    "Type": "SNF-based Superplasticizer",
                    "Base": "Sulphonated Naphthalene Formaldehyde",
                    "Function": "Water-reducing & workability-enhancing admixture",
                    "Nature": "Chloride-free, non-corrosive",
                    "Compatibility": "Suitable with fly ash, slag & pozzolanic materials"
                },
                "application_guide": [
                    "Ready-mix & site-mixed concrete",
                    "Precast concrete elements",
                    "High early strength concrete",
                    "Paver blocks & concrete products",
                    "Reinforced & prestressed concrete"
                ],
                "dosage": "Optimized based on mix design & site trials. Over-dosage may cause segregation or delay in setting time.",
                "compliance": "IS 9103:1999, ASTM C494",
                "packaging": "230 kg, 250 kg"
            },
            {
                "id": "hexaplast-550",
                "name": "HEXAPLAST 550",
                "code": "HEXAPLAST 550",
                "category": "Liquid Base",
                "tagline": "PCE/LPC Based Superplasticizer Admixture",
                "description": "Polycarboxylate Ether (PCE) based superplasticizer that offers exceptional water reduction combined with high-performance workability retention. It allows for high early and ultimate compressive strength, which facilitates faster de-moulding in precast applications.",
                "key_benefits": [
                    "High-range water reduction with improved workability",
                    "High early and ultimate strength development",
                    "Increases early and ultimate compressive strength",
                    "Reduces permeability, shrinkage & creep",
                    "Improves cohesion, pumpability & finishing",
                    "Chloride-free - safe for RCC & prestressed concrete",
                    "Cost-effective solution for high-performance concrete"
                ],
                "technical_features": {
                    "Type": "LPC/PCE-based Superplasticizer",
                    "Base": "Polycarboxylate Ether",
                    "Function": "High-range water reducer & strength enhancer",
                    "Nature": "Chloride-free, non-corrosive",
                    "Compatibility": "Suitable with slag & pozzolanic materials"
                },
                "application_guide": [
                    "Ready-mix & site-mixed concrete",
                    "Precast concrete elements",
                    "High early strength concrete",
                    "Paver blocks & concrete products",
                    "Reinforced & prestressed concrete"
                ],
                "dosage": "Optimized based on mix design & site trials. Over-dosage may cause segregation or delay in setting time.",
                "compliance": "IS 9103:1999, ASTM C494",
                "packaging": "230 kg, 250 kg"
            },
            {
                "id": "hexaplast-750",
                "name": "HEXAPLAST 750",
                "code": "HEXAPLAST 750",
                "category": "Liquid Base",
                "tagline": "PCE/MPC Based Superplasticizer Admixture",
                "description": "A high-performance Polycarboxylate Ether based superplasticizer designed for concrete. It optimizes workability retention and enhances concrete pumpability and cohesion without causing segregation.",
                "key_benefits": [
                    "High-range water reduction with excellent workability retention",
                    "High early and ultimate strength development",
                    "Enables faster de-molding in precast concrete",
                    "Reduces permeability, shrinkage & creep",
                    "Improves cohesion, pumpability & finishing",
                    "Chloride-free - safe for RCC & prestressed concrete",
                    "Cost-effective solution for high-performance concrete"
                ],
                "technical_features": {
                    "Type": "PCE/MPC-based Superplasticizer",
                    "Base": "Polycarboxylate Ether",
                    "Function": "High-range water reducer & strength enhancer",
                    "Nature": "Chloride-free, non-corrosive",
                    "Compatibility": "Suitable with slag & pozzolanic materials"
                },
                "application_guide": [
                    "Ready-mix & site-mixed concrete",
                    "Precast concrete elements",
                    "High early strength concrete",
                    "Paver blocks & concrete products",
                    "Reinforced & prestressed concrete"
                ],
                "dosage": "Optimized based on mix design & site trials. Over-dosage may cause segregation or delay in setting time.",
                "compliance": "IS 9103:1999, ASTM C494",
                "packaging": "230 kg, 250 kg"
            },
            {
                "id": "hexaplast-900",
                "name": "HEXAPLAST 900",
                "code": "HEXAPLAST 900",
                "category": "Liquid Base",
                "tagline": "High-Performance PCE Based Superplasticizer",
                "description": "An premium Polycarboxylate Ether based superplasticizer with high solid content (34-38%). Specially formulated for self-compacting concrete, high-grade structures (M50 and above), and long flow requirements in fast-track projects.",
                "key_benefits": [
                    "Extremely high water reduction for ultra-dense concrete",
                    "Excellent ability for pumped & self-compacting concrete",
                    "High early and ultimate strength development",
                    "Produces very low-permeability, highly durable concrete",
                    "Enables faster stripping in precast & fast-track projects",
                    "Chloride-free safe for RCC & prestressed concrete",
                    "Suitable for high-grade & special concrete applications"
                ],
                "technical_features": {
                    "Type": "High-performance PCE based superplasticizer",
                    "Function": "High-range water reducer & strength enhancer",
                    "Nature": "Chloride-free, non-corrosive",
                    "Appearance": "Light brown / light red liquid",
                    "Solid Content": "34-38%"
                },
                "application_guide": [
                    "Ready-mix & pumped concrete",
                    "Precast concrete elements",
                    "Fast-track construction",
                    "Self-compacting concrete (SCC)",
                    "High-grade concrete (M50 & above)",
                    "Concrete requiring long flow & high performance"
                ],
                "dosage": "0.3% - 1.4% by weight of cement. Optimized through trial mixes.",
                "compliance": "ASTM C494 (Type A & F)",
                "packaging": "230 kg, 250 kg"
            },
            {
                "id": "hc-sbr-npu",
                "name": "HC SBR NPU",
                "code": "HC SBR NPU",
                "category": "Liquid Base",
                "tagline": "Latex Based Bonding Agent, Waterproofing & Repairs",
                "description": "A high-quality, modified Styrene-Butadiene Rubber (SBR) latex polymer designed as an integral bonding agent, waterproofing additive, and repair polymer. It enhances the mechanical properties of concrete and mortar mixes.",
                "key_benefits": [
                    "Excellent bonding between old & new concrete and plaster",
                    "Improves tensile, flexural & impact strength of mortars",
                    "Enhances waterproofing performance in wet areas",
                    "Increases durability and abrasion resistance",
                    "Reduces shrinkage cracks in repair mortars",
                    "Improves adhesion, cohesion & workability",
                    "Suitable for repairs, waterproofing & bonding applications"
                ],
                "technical_features": {
                    "Type": "Liquid Waterproofing Admixture",
                    "Appearance": "Dark brown liquid",
                    "Standard Compliance": "IS 2645:2003",
                    "Chloride Content": "As per IS 2645 (RCC-safe)",
                    "Compatibility": "OPC, PPC, PSC (Not suitable for High Alumina Cement)",
                    "Function": "Water-reducing & waterproofing admixture"
                },
                "application_guide": [
                    "Bond coat for plaster to plaster & concrete to concrete",
                    "Polymer Modified mortars for RCC repairs",
                    "Waterproofing of toilets, bathrooms, terraces & balconies",
                    "Crack repair and patch repair works",
                    "Rebar protection coating",
                    "Tile, stone & cladding fixing"
                ],
                "dosage": "Used as a slurry bond coat or in polymer modified repair mortars.",
                "compliance": "IS 2645:2003",
                "packaging": "50 kgs"
            },
            {
                "id": "hc-mix-lw",
                "name": "HC MIX LW+",
                "code": "HC MIX LW+",
                "category": "Liquid Base",
                "tagline": "Integral Waterproofing Compound",
                "description": "A liquid integral waterproofing admixture formulated for concrete, mortar, and plaster. It reduces the porosity and micro-cracking of cement mixtures, preventing water ingress while lowering water demand by up to 15%.",
                "key_benefits": [
                    "Integral waterproofing throughout the concrete matrix",
                    "Reduces porosity, honeycombing, micro-cracks & maintains or improves compressive strength",
                    "Enhances durability & weather resistance",
                    "Improves workability, cohesion & pumpability",
                    "Reduces water demand (up to 15%)",
                    "Economical - saves cement, time & labour",
                    "No adverse effect on setting time (when used correctly)"
                ],
                "technical_features": {
                    "Type": "Modified Latex",
                    "Appearance": "Free-flowing white liquid",
                    "Solid Content": "42-44%",
                    "pH Value": "7 - 9",
                    "Function": "Bonding agent, waterproofing additive & repair polymer"
                },
                "application_guide": [
                    "Measure required quantity of HC MIX LW+",
                    "Mix into second bucket of water",
                    "Add solution to concrete/mortar/plaster",
                    "Mix thoroughly and adjust water for workability"
                ],
                "dosage": "100-250g per 50kg cement bag (0.2%-0.5% by weight of cement)",
                "compliance": "IS 2645:2003",
                "packaging": "50 kg"
            },
            {
                "id": "hc-curing-compound",
                "name": "HC CURING COMPOUND",
                "code": "HC CURING COMPOUND",
                "category": "Liquid Base",
                "tagline": "White Pigmented Water Based Curing Compound",
                "description": "A white-pigmented curing compound that forms a temporary moisture-retaining protective film on freshly placed concrete. Its white pigmentation reflects solar radiation, preventing rapid moisture loss in hot climates.",
                "key_benefits": [
                    "Improves water retention in freshly placed concrete",
                    "High reflectance reduces rapid moisture loss in hot climates",
                    "Ensures uniform curing for better strength development",
                    "Reduces plastic shrinkage & thermal cracks",
                    "Easy to apply by spray, brush or roller",
                    "Improves ultimate strength of concrete"
                ],
                "technical_features": {
                    "Type": "Water-based white pigmented curing compound",
                    "Appearance": "White emulsion",
                    "Reflection Index": "60-65% of MgO",
                    "Chloride Content": "Nil",
                    "Density": "1.10 ± 0.02"
                },
                "application_guide": [
                    "Pavement & road concrete",
                    "Canal lining & water retaining structures",
                    "Precast concrete elements",
                    "Structural concrete & slabs",
                    "Concrete exposed to hot & tropical conditions",
                    "Apply on green concrete after evaporation of surface water",
                    "Forms thin protective film that decays with time"
                ],
                "dosage": "Apply on green concrete as soon as surface water has evaporated.",
                "compliance": "ASTM C 309 - Type 2, Non-toxic, non-flammable & non-hazardous",
                "packaging": "50 kg"
            },
            {
                "id": "hexa-block-joining-mortar",
                "name": "HEXA BLOCK JOINING MORTAR",
                "code": "BJM 100",
                "category": "Powder Base",
                "tagline": "High-Strength Thin-Bed Jointing Mortar",
                "description": "A high-performance cementitious mortar developed for layout of AAC blocks, fly ash bricks, and concrete blocks. It requires only water addition and offers superior bond strength with minimal joint thickness.",
                "key_benefits": [
                    "High bonding strength prevents water penetration and cracks",
                    "Thin joints (2-3 mm) reduce material consumption and heat bridging",
                    "Ready to use - only add water on site",
                    "Self-curing formulation saves water and labor",
                    "High tensile split strength ensures structural stability"
                ],
                "technical_features": {
                    "Type": "Cement-based Drymix Mortar",
                    "Appearance": "Grey granular powder",
                    "Water Demand": "25% - 30% by weight",
                    "Pot Life": "Approx. 2 hours at 30°C",
                    "Tensile Split Strength": "Excellent (> 0.4 N/mm² at 28 days)"
                },
                "application_guide": [
                    "Clean the block surface from dust and loose particles",
                    "Add 25-30% water to the powder and mix thoroughly for 5-10 minutes",
                    "Apply mortar using a notched trowel to maintain 2-3mm thickness",
                    "Place the block and tap gently for alignment"
                ],
                "dosage": "Used as a thin-bed mortar for block joining.",
                "compliance": "ANSI A118.15, ASTM C1660",
                "packaging": "40 kg bags"
            },
            {
                "id": "hexa-tile-adhesive",
                "name": "HEXA TILE ADHESIVE",
                "code": "GTA 100",
                "category": "Powder Base",
                "tagline": "Polymer-Modified Cementitious Tile Adhesive",
                "description": "A polymer-modified, high-performance cement-based adhesive designed for the installation of ceramic, vitrified tiles, and stones on walls and floors. Suitable for interior and exterior applications.",
                "key_benefits": [
                    "Excellent grab and non-slip properties prevent slippage",
                    "Zero shrinkage cracks ensure durable fixing",
                    "Extended open time allows for easy adjustments",
                    "Highly resistant to water and weathering",
                    "Suitable for large format tiles and heavy stones"
                ],
                "technical_features": {
                    "Type": "Polymer-Modified Adhesive",
                    "Appearance": "Grey or white powder",
                    "Pot Life": "3 hours",
                    "Open Time": "20 - 25 minutes",
                    "Adhesive Strength": "High (> 1.0 N/mm² at 28 days)"
                },
                "application_guide": [
                    "Ensure target substrate is structurally sound, clean and dry",
                    "Mix powder with 20-24% water to form a smooth paste",
                    "Spread paste on the substrate using a notched trowel",
                    "Press tiles firmly into the adhesive and adjust alignment"
                ],
                "dosage": "Approx. 3-4 kg/m² at 3mm bed thickness.",
                "compliance": "IS 15477:2019 Type 1",
                "packaging": "20 kg, 40 kg bags"
            },
            {
                "id": "hexa-ready-plaster",
                "name": "HEXA READY PLASTER",
                "code": "RMP 300",
                "category": "Powder Base",
                "tagline": "Polymer-Modified Ready Mix Plaster",
                "description": "A pre-mixed cementitious plaster containing high-grade graded sand and performance-enhancing polymers. Formulated to replace traditional site-mixed sand-cement plaster, ensuring consistent quality and a smooth finish.",
                "key_benefits": [
                    "Consistent high quality and strength",
                    "Significantly reduces rebound loss during application",
                    "Formulated to minimize shrinkage and drying cracks",
                    "Excellent water resistance and workability",
                    "Allows painting directly after initial curing"
                ],
                "technical_features": {
                    "Type": "Pre-mixed Cement Plaster",
                    "Appearance": "Grey sand-cement powder",
                    "Thickness": "8 mm - 15 mm",
                    "Water Demand": "18% - 22% by weight",
                    "Compressive Strength": "> 8 N/mm² at 28 days"
                },
                "application_guide": [
                    "Pre-wet the brick or concrete block wall surface before plastering",
                    "Mix ready mix plaster with 18-22% water using a mechanical stirrer",
                    "Apply to wall surface using traditional troweling techniques",
                    "Level with straight edge and finish with rubber float for smoothness"
                ],
                "dosage": "Approx. 1.5 - 1.6 kg/m²/mm of thickness.",
                "compliance": "IS 1542:1992",
                "packaging": "40 kg bags"
            }
        ]

    def _seed_default_products(self):
        data = self._read_local_db()
        if data.get("products"):
            return True

        data["products"] = {}
        for product in self._get_default_products():
            product_id = product.get("id") or product["name"].lower().replace(" ", "-")
            data["products"][product_id] = product
        return self._write_local_db(data)

    def _load_firebase_credentials(self):
        """Return Firebase credentials from env var or a local file path if available."""
        credentials_json = os.environ.get("FIREBASE_CREDENTIALS_JSON", "").strip()
        if credentials_json:
            try:
                return json.loads(credentials_json)
            except Exception as e:
                print(f"Database: Invalid FIREBASE_CREDENTIALS_JSON. Error: {e}")

        if os.path.exists(self.credentials_path):
            return self.credentials_path

        return None

    def init_db(self):
        # Check if Firebase is explicitly disabled via environment variable
        use_firebase_env = os.environ.get("USE_FIREBASE", "true").lower()
        if use_firebase_env == "false":
            print("Database: Firebase explicitly disabled via USE_FIREBASE. Using local JSON storage.")
            self.use_firebase = False
            self._ensure_local_db()
            return

        firebase_credentials = self._load_firebase_credentials()
        if firebase_credentials is not None:
            try:
                # pyrefly: ignore [missing-import]
                import firebase_admin
                # pyrefly: ignore [missing-import]
                from firebase_admin import credentials, firestore
                
                # Check if firebase is already initialized to avoid duplicate app errors
                if not firebase_admin._apps:
                    cred = credentials.Certificate(firebase_credentials)
                    self.firebase_app = firebase_admin.initialize_app(cred)
                self.db = firestore.client()
                
                # Run a fast test query to verify API is active and enabled
                print("Database: Testing Firebase Firestore connection...")
                self.db.collection("products").limit(1).get()
                
                self.use_firebase = True
                print("Database: Successfully connected to Firebase Firestore.")
                return
            except Exception as e:
                print(f"Database: Failed to connect to Firebase Firestore. Error: {e}. Falling back to local storage.")
        else:
            print("Database: Firebase credentials not found. Using local JSON storage.")
        
        self.use_firebase = False
        self._ensure_local_db()

    def _ensure_local_db(self):
        """Ensures that local_db.json exists and is formatted correctly."""
        with _db_lock:
            parent_dir = os.path.dirname(self.local_db_path)
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)

            if not os.path.exists(self.local_db_path):
                default_data = {
                    "products": {},
                    "inquiries": []
                }
                with open(self.local_db_path, "w", encoding="utf-8") as f:
                    json.dump(default_data, f, indent=4)

            data = self._read_local_db()
            if not data.get("products"):
                self._seed_default_products()

    def _read_local_db(self):
        """Helper to read local database file."""
        self._ensure_local_db()
        with _db_lock:
            try:
                with open(self.local_db_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error reading local db: {e}")
                return {"products": {}, "inquiries": []}

    def _write_local_db(self, data):
        """Helper to write to local database file."""
        with _db_lock:
            try:
                with open(self.local_db_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)
                return True
            except Exception as e:
                print(f"Error writing local db: {e}")
                return False

    # --- PRODUCTS METHODS ---

    def get_products(self):
        """Returns all products in database as a list of dicts."""
        if self.use_firebase:
            try:
                docs = self.db.collection("products").stream()
                products = []
                for doc in docs:
                    prod = doc.to_dict()
                    prod["id"] = doc.id
                    products.append(prod)
                return products
            except Exception as e:
                print(f"Firebase error in get_products: {e}. Falling back to local.")
                
        # Fallback to local
        data = self._read_local_db()
        products = []
        for pid, pdata in data.get("products", {}).items():
            item = pdata.copy()
            item["id"] = pid
            products.append(item)
        return products

    def get_product(self, product_id):
        """Gets a single product by ID."""
        if self.use_firebase:
            try:
                doc_ref = self.db.collection("products").document(product_id)
                doc = doc_ref.get()
                if doc.exists:
                    pdata = doc.to_dict()
                    pdata["id"] = doc.id
                    return pdata
                return None
            except Exception as e:
                print(f"Firebase error in get_product: {e}. Falling back to local.")

        # Fallback to local
        data = self._read_local_db()
        pdata = data.get("products", {}).get(product_id)
        if pdata:
            item = pdata.copy()
            item["id"] = product_id
            return item
        return None

    def add_product(self, product_id, product_data):
        """Adds or overwrites a product."""
        # Ensure timestamp is included
        if "updated_at" not in product_data:
            product_data["updated_at"] = datetime.now(timezone.utc).isoformat()
            
        if self.use_firebase:
            try:
                self.db.collection("products").document(product_id).set(product_data)
                return True
            except Exception as e:
                print(f"Firebase error in add_product: {e}. Falling back to local.")

        # Fallback to local
        data = self._read_local_db()
        if "products" not in data:
            data["products"] = {}
        data["products"][product_id] = product_data
        return self._write_local_db(data)

    def delete_product(self, product_id):
        """Deletes a product by ID."""
        if self.use_firebase:
            try:
                self.db.collection("products").document(product_id).delete()
                return True
            except Exception as e:
                print(f"Firebase error in delete_product: {e}. Falling back to local.")

        # Fallback to local
        data = self._read_local_db()
        if product_id in data.get("products", {}):
            del data["products"][product_id]
            return self._write_local_db(data)
        return False

    # --- INQUIRIES METHODS ---

    def add_inquiry(self, inquiry_data):
        """Submits a customer inquiry."""
        inquiry_data["created_at"] = datetime.now(timezone.utc).isoformat()
        
        if self.use_firebase:
            try:
                self.db.collection("inquiries").add(inquiry_data)
                return True
            except Exception as e:
                print(f"Firebase error in add_inquiry: {e}. Falling back to local.")

        # Fallback to local
        data = self._read_local_db()
        if "inquiries" not in data:
            data["inquiries"] = []
        data["inquiries"].append(inquiry_data)
        return self._write_local_db(data)

    def delete_inquiry(self, inquiry_id):
        """Deletes an inquiry by ID (document ID in Firestore, or created_at in local DB)."""
        if self.use_firebase:
            try:
                self.db.collection("inquiries").document(inquiry_id).delete()
                return True
            except Exception as e:
                print(f"Firebase error in delete_inquiry: {e}. Falling back to local.")

        # Fallback to local
        data = self._read_local_db()
        inquiries = data.get("inquiries", [])
        
        # Filter out the matching inquiry
        initial_count = len(inquiries)
        filtered_inquiries = [
            inq for inq in inquiries 
            if inq.get("id") != inquiry_id and inq.get("created_at") != inquiry_id
        ]
        
        if len(filtered_inquiries) < initial_count:
            data["inquiries"] = filtered_inquiries
            return self._write_local_db(data)
        return False

    def get_inquiries(self):
        """Returns all inquiries, ordered by newest first."""
        if self.use_firebase:
            try:
                docs = self.db.collection("inquiries").order_by("created_at", direction="DESCENDING").stream()
                inquiries = []
                for doc in docs:
                    inq = doc.to_dict()
                    inq["id"] = doc.id
                    inquiries.append(inq)
                return inquiries
            except Exception as e:
                print(f"Firebase error in get_inquiries: {e}. Falling back to local.")

        # Fallback to local
        data = self._read_local_db()
        inquiries = data.get("inquiries", [])
        # Sort local inquiries by created_at descending
        try:
            inquiries = sorted(inquiries, key=lambda x: x.get("created_at", ""), reverse=True)
        except Exception:
            pass
        return inquiries
