# config.py
# This file contains all user-configurable variables for the uploader script.

# ----------------- 1. FILE & PROJECT SETTINGS -----------------
# Path to your Firebase Admin SDK service account key
# (This file is ignored by .gitignore for security)
SERVICE_ACCOUNT_KEY = 'key.json' 

# Your Firebase Storage bucket name (e.g., 'my-project.appspot.com')
BUCKET_NAME = 'YOUR_BUCKET_NAME.appspot.com'

# Path to your local images folder (use forward slashes '/')
LOCAL_IMAGES_PATH = 'C:/Users/YourUser/Path/To/Images'

# Path to your JSON file containing the product data
PRODUCTS_JSON_PATH = 'products.json'

# ----------------- 2. FIREBASE STRUCTURE SETTINGS -----------------

# Folder name within Firebase Storage to upload images to
STORAGE_FOLDER = 'products'

# A dictionary to map the 'type' from your JSON to the correct Firestore collection name
COLLECTION_NAMES = {
    'coffee': 'coffees',
    'pastry': 'pastries'
    # Add other types here, e.g.: 'drink': 'beverages'
}

# ----------------- 3. DATA MAPPING LOGIC -----------------
# This function defines HOW your data from JSON is structured in Firestore.
# !! CRITICAL: This structure MUST match what your mobile app (Flutter) expects to read. !!

def map_product_to_firestore(product, image_url):
    """
    Maps a single product dictionary from the JSON to the desired
    Firestore document structure.

    Args:
        product (dict): The product data from the JSON file.
        image_url (str): The public URL of the uploaded image.

    Returns:
        dict: The final dictionary to be saved in Firestore.
    """
    
    product_type = product.get('type')
    product_id = product.get('id')

    # --- EXAMPLE 1: 'coffee' type data structure ---
    # This structure matches the 'Kocie Oczko' Flutter models
    if product_type == 'coffee':
        return {
            'id': product_id,
            'name': {
                'pl': product.get('name_pl'),
                'en': product.get('name_en'),
            },
            'description': {
                'pl': product.get('description_pl'),
                'en': product.get('description_en'),
            },
            'price': product.get('price'),
            'imageUrl': image_url,
            'category': product.get('category'),
            'rating': 0.0,
            'isAvailable': True,
            'sizes': ['Small', 'Medium', 'Large'],
        }

    # --- EXAMPLE 2: 'pastry' type data structure ---
    # This structure matches the my Flutter models
    elif product_type == 'pastry':
        return {
            'id': product_id,
            'name': {
                'pl': product.get('name_pl'),
                'en': product.get('name_en'),
            },
            'description': {
                'pl': product.get('description_pl'),
                'en': product.get('description_en'),
            },
            'price': product.get('price'),
            'imageUrl': image_url,
            'category': product.get('category'),
            'allergens': [],
            'isAvailable': True,
            'rating': 0.0,
            'isVegetarian': False,
            'isVegan': False,
        }

    # --- DEFAULT (if type is unknown) ---
    # Fallback structure if the 'type' is not 'coffee' or 'pastry'
    return {
        'id': product_id,
        'name': product.get('name_en'),
        'description': product.get('description_en'),
        'price': product.get('price'),
        'imageUrl': image_url,
    }