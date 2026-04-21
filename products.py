CATEGORIES = [
    {"id": "chicken", "name": "Chicken", "image": "cat-chicken.jpg"},
    {"id": "mutton", "name": "Mutton", "image": "cat-mutton.jpg"},
    {"id": "seafood", "name": "Seafood", "image": "cat-seafood.jpg"},
    {"id": "eggs", "name": "Eggs", "image": "cat-eggs.jpg"},
    {"id": "marinades", "name": "Marinades", "image": "cat-marinades.jpg"},
    {"id": "readyeat", "name": "Ready to Cook", "image": "cat-readyeat.jpg"},
]

PRODUCTS = [
    {"id": "chicken-curry-cut", "name": "Chicken Curry Cut", "category": "chicken",
     "price": 269, "mrp": 320, "weight": "500 g · 12 pcs", "rating": 4.7, "reviews": 1284,
     "image": "cat-chicken.jpg", "featured": True,
     "description": "Tender, antibiotic-free chicken cut into curry-ready pieces. Cleaned, washed and vacuum-packed within 90 minutes of cutting."},
    {"id": "chicken-boneless", "name": "Chicken Breast Boneless", "category": "chicken",
     "price": 289, "mrp": 340, "weight": "500 g", "rating": 4.8, "reviews": 942,
     "image": "cat-chicken.jpg", "featured": True,
     "description": "Lean, skinless chicken breast — perfect for grills, salads and high-protein meals."},
    {"id": "chicken-drumsticks", "name": "Chicken Drumsticks", "category": "chicken",
     "price": 249, "mrp": 299, "weight": "500 g · 4 pcs", "rating": 4.6, "reviews": 612,
     "image": "cat-chicken.jpg",
     "description": "Juicy drumsticks with skin on — ideal for roasts and tandoori."},
    {"id": "mutton-curry-cut", "name": "Mutton Curry Cut", "category": "mutton",
     "price": 749, "mrp": 850, "weight": "500 g · 12 pcs", "rating": 4.8, "reviews": 738,
     "image": "cat-mutton.jpg", "featured": True,
     "description": "Premium goat meat from young animals, hand-cut for the perfect curry."},
    {"id": "mutton-keema", "name": "Mutton Keema", "category": "mutton",
     "price": 699, "mrp": 799, "weight": "500 g", "rating": 4.7, "reviews": 421,
     "image": "cat-mutton.jpg",
     "description": "Freshly minced mutton — soft, lean and ready for kebabs or biryani."},
    {"id": "prawns-medium", "name": "Prawns Medium Cleaned", "category": "seafood",
     "price": 449, "mrp": 520, "weight": "250 g", "rating": 4.6, "reviews": 389,
     "image": "cat-seafood.jpg", "featured": True,
     "description": "Deveined and cleaned prawns sourced from coastal farms."},
    {"id": "rohu-fish", "name": "Rohu Fish Curry Cut", "category": "seafood",
     "price": 299, "mrp": 360, "weight": "500 g", "rating": 4.5, "reviews": 256,
     "image": "cat-seafood.jpg",
     "description": "Fresh-water rohu, cleaned and cut into curry pieces."},
    {"id": "country-eggs", "name": "Country Eggs (Pack of 6)", "category": "eggs",
     "price": 99, "mrp": 120, "weight": "6 eggs", "rating": 4.7, "reviews": 1820,
     "image": "cat-eggs.jpg",
     "description": "Free-range country eggs with a deep orange yolk and richer flavour."},
    {"id": "white-eggs", "name": "Farm White Eggs (Pack of 10)", "category": "eggs",
     "price": 89, "mrp": 110, "weight": "10 eggs", "rating": 4.6, "reviews": 2130,
     "image": "cat-eggs.jpg", "featured": True,
     "description": "Farm-fresh white eggs, antibiotic residue-free."},
    {"id": "tandoori-marinade", "name": "Chicken Tandoori Marinade", "category": "marinades",
     "price": 329, "mrp": 379, "weight": "450 g", "rating": 4.8, "reviews": 512,
     "image": "cat-marinades.jpg", "featured": True,
     "description": "Hung-curd & spice marinated chicken — straight to your tandoor or oven."},
    {"id": "ready-kebabs", "name": "Chicken Seekh Kebabs", "category": "readyeat",
     "price": 279, "mrp": 320, "weight": "8 pcs", "rating": 4.7, "reviews": 642,
     "image": "cat-readyeat.jpg",
     "description": "Restaurant-style seekh kebabs — pan fry in 6 minutes."},
    {"id": "ready-nuggets", "name": "Crispy Chicken Nuggets", "category": "readyeat",
     "price": 219, "mrp": 260, "weight": "400 g", "rating": 4.6, "reviews": 980,
     "image": "cat-readyeat.jpg",
     "description": "Crunchy on the outside, juicy inside — kid-favourite."},
]


def get_product(pid):
    return next((p for p in PRODUCTS if p["id"] == pid), None)


def related_products(pid, limit=4):
    p = get_product(pid)
    if not p:
        return []
    return [x for x in PRODUCTS if x["category"] == p["category"] and x["id"] != pid][:limit]
