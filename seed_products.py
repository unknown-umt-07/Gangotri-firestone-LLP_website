import sys
import os

# Ensure the script directory is in the Python search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import Database

def seed():
    print("Seeding database...")
    db = Database()
    
    products = [
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
    
    for product in products:
        pid = product["id"]
        # Save product using database wrapper
        success = db.add_product(pid, product)
        if success:
            print(f"Successfully seeded: {pid}")
        else:
            print(f"Failed to seed: {pid}")
            
    print("Database seeding completed.")

if __name__ == "__main__":
    seed()
