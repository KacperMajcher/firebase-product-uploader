import os
import firebase_admin
from firebase_admin import credentials, firestore, storage

# ----------------- CONFIGURATION -----------------

# 1. Path to your Firebase Admin SDK service account key
SERVICE_ACCOUNT_KEY = 'key.json'

# 2. Your Firebase Storage bucket name
# (Find this in your Firebase Console -> Storage. It looks like 'my-project.appspot.com')
BUCKET_NAME = 'x.firebasestorage.app'

# 3. Path to your local images folder
# (Use forward slashes '/' even on Windows)
LOCAL_IMAGES_PATH = 'C:/Users/x/Downloads'

# -------------------------------------------------


# 4. Product data list to upload
products_data = [
  # --- COFFEES ---
  {
    'id': 'Cappuccino', 'type': 'coffee', 'category': 'hot', 'price': 14.00,
    'name_pl': 'Cappuccino', 'name_en': 'Cappuccino',
    'description_pl': 'Klasyczne włoskie cappuccino, którego nazwa nawiązuje do kapturów (cappuccio) mnichów kapucynów. Składa się z idealnej proporcji espresso, gorącego mleka i kremowej pianki. W "Kocim Oczku" dbamy o perfekcyjną teksturę mleka, aby każdy łyk był przyjemnością.',
    'description_en': 'A classic Italian cappuccino, its name referencing the "cappuccio" hoods of Capuchin friars. It consists of a perfect balance of espresso, hot milk, and creamy foam. At "Kocie Oczko", we ensure a perfect milk texture for a delightful sip every time.',
  },
  {
    'id': 'Espresso', 'type': 'coffee', 'category': 'hot', 'price': 10.00,
    'name_pl': 'Espresso', 'name_en': 'Espresso',
    'description_pl': 'Serce każdej kawy, wynalezione w Turynie w 1884 roku. Nasze espresso to intensywny, skoncentrowany napar o bogatym aromacie i trwałej cremie. Używamy starannie wyselekcjonowanych ziaren, aby dostarczyć Ci zastrzyk czystej energii i smaku.',
    'description_en': 'The heart of every coffee, invented in Turin in 1884. Our espresso is an intense, concentrated brew with a rich aroma and lasting crema. We use carefully selected beans to provide you with a shot of pure energy and flavor.',
  },
  {
    'id': 'Latte Macchiato', 'type': 'coffee', 'category': 'hot', 'price': 16.00,
    'name_pl': 'Latte Macchiato', 'name_en': 'Latte Macchiato',
    'description_pl': 'Po włosku "splamione mleko". To efektowna, trójwarstwowa kompozycja gorącego mleka, espresso i mlecznej pianki. W naszej kawiarni serwujemy je w wysokiej szklance, abyś mógł podziwiać perfekcyjne rozdzielenie warstw przed ich wymieszaniem.',
    'description_en': 'Italian for "stained milk." It\'s a stunning three-layered composition of hot milk, espresso, and milk foam. In our café, we serve it in a tall glass so you can admire the perfect separation of layers before stirring.',
  },
  {
    'id': 'Flat White', 'type': 'coffee', 'category': 'hot', 'price': 15.00,
    'name_pl': 'Flat White', 'name_en': 'Flat White',
    'description_pl': 'Pochodzący z Australii lub Nowej Zelandii (spór trwa!), flat white to idealny balans między kawą a mlekiem. Dwie porcje espresso połączone z aksamitnie spienionym mlekiem (microfoam) tworzą intensywny, ale gładki napój. Idealny dla tych, którzy lubią mocniejszy smak kawy w mlecznym wydaniu.',
    'description_en': 'Originating from Australia or New Zealand (the debate continues!), the flat white is the perfect balance between coffee and milk. Two shots of espresso combined with velvety microfoam create an intense yet smooth drink. Ideal for those who love a stronger coffee taste in a milky form.',
  },
  {
    'id': 'Americano', 'type': 'coffee', 'category': 'hot', 'price': 12.00,
    'name_pl': 'Americano', 'name_en': 'Americano',
    'description_pl': 'Legenda głosi, że powstało podczas II wojny światowej, gdy amerykańscy żołnierze we Włoszech rozcieńczali espresso gorącą wodą. Nasze Americano to pełna filiżanka bogatej w smaku kawy, idealna dla tych, którzy wolą łagodniejszą intensywność niż espresso, ale wciąż cenią jego charakter.',
    'description_en': 'Legend says it was created during WWII when American soldiers in Italy diluted espresso with hot water. Our Americano is a full cup of rich-flavored coffee, perfect for those who prefer a milder intensity than espresso but still appreciate its character.',
  },
  {
    'id': 'Iced Coffee', 'type': 'coffee', 'category': 'iced', 'price': 16.00,
    'name_pl': 'Kawa Mrożona', 'name_en': 'Iced Coffee',
    'description_pl': 'Idealne orzeźwienie na ciepłe dni. Przygotowujemy ją na bazie świeżo parzonego espresso, schładzamy i serwujemy z kostkami lodu. Możesz ją personalizować, dodając mleko, syrop smakowy lub bitą śmietanę, tworząc swój ulubiony chłodzący napój.',
    'description_en': 'The perfect refreshment for warm days. We prepare it with freshly brewed espresso, chill it, and serve it over ice. You can customize it by adding milk, flavored syrup, or whipped cream to create your favorite cooling drink.',
  },
  {
    'id': 'Espresso Macchiato', 'type': 'coffee', 'category': 'hot', 'price': 11.00,
    'name_pl': 'Espresso Macchiato', 'name_en': 'Espresso Macchiato',
    'description_pl': 'Kolejny włoski klasyk, którego nazwa oznacza "splamiony" lub "naznaczony". To pojedyncze lub podwójne espresso z niewielką ilością spienionego mleka na wierzchu. Idealne dla tych, którzy szukają intensywności espresso, ale z delikatnym mlecznym złagodzeniem.',
    'description_en': 'Another Italian classic, its name meaning "stained" or "marked." It\'s a single or double shot of espresso with a small dollop of foamed milk on top. Perfect for those seeking the intensity of espresso but with a gentle milky touch.',
  },
  {
    'id': 'EspressoTonic', 'type': 'coffee', 'category': 'special', 'price': 17.00,
    'name_pl': 'Espresso Tonic', 'name_en': 'Espresso Tonic',
    'description_pl': 'Nowoczesny i niezwykle orzeźwiający specjał, który podbił kawiarnie na całym świecie. Połączenie intensywmego espresso z musującym tonikiem i lodem tworzy zaskakujący, cytrusowo-kawowy smak. W "Kocim Oczku" serwujemy go z plasterkiem cytryny lub limonki dla podkreślenia rześkości.',
    'description_en': 'A modern and incredibly refreshing specialty that has taken the coffee world by storm. The combination of intense espresso with sparkling tonic and ice creates a surprising, citrus-coffee flavor. At "Kocie Oczko", we serve it with a slice of lemon or lime to enhance its crispness.',
  },
  {
    'id': 'Cortado', 'type': 'coffee', 'category': 'hot', 'price': 13.00,
    'name_pl': 'Cortado', 'name_en': 'Cortado',
    'description_pl': 'Pochodzący z Hiszpanii napój, którego nazwa "cortar" oznacza "ciąć". Jest to espresso "przecięte" niewielką ilością ciepłego, lekko spienionego mleka, co łagodzi jego kwasowość. Serwowane w małej szklaneczce, idealnie balansuje moc kawy z kremowością mleka.',
    'description_en': 'Originating from Spain, its name "cortar" means "to cut." It\'s an espresso "cut" with a small amount of warm, lightly foamed milk, which mellows its acidity. Served in a small glass, it perfectly balances the power of coffee with the creaminess of milk.',
  },
  {
    'id': 'IrishCoffee', 'type': 'coffee', 'category': 'special', 'price': 20.00,
    'name_pl': 'Kawa po Irlandzku', 'name_en': 'Irish Coffee',
    'description_pl': 'Stworzona w 1943 roku, by rozgrzać pasażerów na lotnisku w Foynes. To rozgrzewający koktajl kawowy łączący gorącą czarną kawę, irlandzką whiskey, brązowy cukier i warstwę lekko ubitej śmietanki. Idealna na chłodne wieczory, serwowana z szacunkiem dla tradycji.',
    'description_en': 'Created in 1943 to warm passengers at Foynes Airport. This warming coffee cocktail combines hot black coffee, Irish whiskey, brown sugar, and a layer of lightly whipped cream. Perfect for chilly evenings, served with respect for tradition.',
  },
  # --- PASTRIES ---
  {
    'id': 'NewYorkCheesecake', 'type': 'pastry', 'category': 'cake', 'price': 18.00,
    'name_pl': 'Sernik Nowojorski', 'name_en': 'New York Cheesecake',
    'description_pl': 'Symbol Nowego Jorku, znany ze swojej gęstej, bogatej i kremowej konsystencji. Wypiekany na spodzie z ciasteczek graham, nasz sernik jest idealnie gładki. Serwujemy go klasycznie lub z musem z owoców leśnych, który doskonale przełamuje jego słodycz.',
    'description_en': 'A symbol of New York, known for its dense, rich, and creamy texture. Baked on a graham cracker crust, our cheesecake is perfectly smooth. We serve it classic style or with a berry coulis that perfectly cuts through its sweetness.',
  },
  {
    'id': 'ChocolateLavaCake', 'type': 'pastry', 'category': 'cake', 'price': 19.00,
    'name_pl': 'Lava Cake', 'name_en': 'Chocolate Lava Cake',
    'description_pl': 'Czekoladowe marzenie, znane również jako "fondant au chocolat". To małe ciastko z chrupiącą skórką i płynnym, gorącym wnętrzem. W "Kocim Oczku" podajemy je na ciepło, często z gałką lodów waniliowych, co tworzy niezapomniany kontrast temperatur.',
    'description_en': 'A chocolate dream, also known as "fondant au chocolat." It\'s a small cake with a crisp crust and a liquid, hot center. At "Kocie Oczko", we serve it warm, often with a scoop of vanilla ice cream, creating an unforgettable temperature contrast.',
  },
  {
    'id': 'RedVelvetCake', 'type': 'pastry', 'category': 'cake', 'price': 17.00,
    'name_pl': 'Ciasto Red Velvet', 'name_en': 'Red Velvet Cake',
    'description_pl': 'Aksamitne ciasto o charakterystycznym, głębokim czerwonym kolorze i delikatnym kakaowym smaku. Jego historia sięga epoki wiktoriańskiej. Przekładane jest puszystym kremem na bazie serka śmietankowego, co tworzy idealnie zbalansowaną, wilgotną i efektowną całość.',
    'description_en': 'A velvety cake with a distinctive deep red color and a mild cocoa flavor. Its history dates back to the Victorian era. It is layered with a fluffy cream cheese frosting, creating a perfectly balanced, moist, and stunning dessert.',
  },
  {
    'id': 'CarrotCake', 'type': 'pastry', 'category': 'cake', 'price': 16.00,
    'name_pl': 'Ciasto Marchewkowe', 'name_en': 'Carrot Cake',
    'description_pl': 'Jeden z ulubieńców naszych gości. Wilgotne, korzenne ciasto z dodatkiem świeżo startej marchewki i orzechów włoskich. Przełożone kremem z serka śmietankowego z nutą cytryny. To ciasto udowadnia, że warzywa w deserach to strzał w dziesiątkę!',
    'description_en': 'A customer favorite. A moist, spiced cake made with freshly grated carrots and walnuts. Layered with a cream cheese frosting with a hint of lemon. This cake proves that vegetables in desserts are a fantastic idea!',
  },
  {
    'id': 'Tiramisu', 'type': 'pastry', 'category': 'cake', 'price': 18.00,
    'name_pl': 'Tiramisu', 'name_en': 'Tiramisu',
    'description_pl': 'Włoski klasyk oznaczający "podnieś mnie". To deser bez pieczenia, złożony z biszkoptów nasączonych mocnym espresso i likierem amaretto. Przekładany jest aksamitnym kremem z serka mascarpone i jajek, a całość posypana jest gorzkim kakao.',
    'description_en': 'An Italian classic meaning "pick me up." It\'s a no-bake dessert made of ladyfingers dipped in strong espresso and amaretto liqueur. Layered with a velvety cream of mascarpone and eggs, and dusted with bitter cocoa powder.',
  },
]


# ----------------- UPLOAD SCRIPT LOGIC (DO NOT CHANGE) -----------------

def upload_files():
    # Initialize Firebase Admin
    try:
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
        firebase_admin.initialize_app(cred, {
            'storageBucket': BUCKET_NAME
        })
        print("✅ Firebase initialized successfully.")
    except Exception as e:
        print(f"❌ ERROR: Failed to initialize Firebase. Check your service key file ('{SERVICE_ACCOUNT_KEY}') and bucket name ('{BUCKET_NAME}').")
        print(f"System error: {e}")
        return

    # Prepare database and storage clients
    db = firestore.client()
    bucket = storage.bucket()

    print("\nStarting product upload...")

    for product in products_data:
        product_id = product['id']
        product_type = product['type']
        file_name = f"{product_id}.png"
        
        # Path to the local file
        local_file_path = os.path.join(LOCAL_IMAGES_PATH, file_name).replace("\\", "/")
        
        # Path in Firebase Storage
        storage_path = f"products/{file_name}"

        print(f"\n--- Processing: {product_id} ---")

        # --- Step 1: Upload image to Storage ---
        try:
            if not os.path.exists(local_file_path):
                print(f"  ❌ FILE ERROR: File not found: {local_file_path}")
                continue # Skip this product

            blob = bucket.blob(storage_path)
            blob.upload_from_filename(local_file_path)

            # Make the file publicly accessible
            blob.make_public()
            image_url = blob.public_url
            print(f"  ✅ Image uploaded: {image_url}")

        except Exception as e:
            print(f"  ❌ STORAGE ERROR: Failed to upload image {file_name}.")
            print(f"     System error: {e}")
            continue # Skip this product

        # --- Step 2: Prepare data for Firestore (with PL/EN map) ---
        firestore_data = {}
        if product_type == 'coffee':
            firestore_data = {
                'id': product_id,
                # NOTE: Save 'name' and 'description' as a map
                'name': {
                    'pl': product['name_pl'],
                    'en': product['name_en'],
                },
                'description': {
                    'pl': product['description_pl'],
                    'en': product['description_en'],
                },
                'price': product['price'],
                'imageUrl': image_url,
                'category': product['category'],
                'rating': 0.0,
                'isAvailable': True,
                'sizes': ['Small', 'Medium', 'Large'],
            }
        elif product_type == 'pastry':
            firestore_data = {
                'id': product_id,
                # NOTE: Save 'name' and 'description' as a map
                'name': {
                    'pl': product['name_pl'],
                    'en': product['name_en'],
                },
                'description': {
                    'pl': product['description_pl'],
                    'en': product['description_en'],
                },
                'price': product['price'],
                'imageUrl': image_url,
                'category': product['category'],
                'allergens': [],
                'isAvailable': True,
                'rating': 0.0,
                'isVegetarian': False,
                'isVegan': False,
            }

        # --- Step 3: Save data to Firestore ---
        try:
            collection_name = 'coffees' if product_type == 'coffee' else 'pastries'
            
            # Use .set() to make the document ID match the product ID
            db.collection(collection_name).document(product_id).set(firestore_data)
            print(f"  ✅ Saved data to Firestore (collection: {collection_name}).")

        except Exception as e:
            print(f"  ❌ FIRESTORE ERROR: Failed to save data for {product_id}.")
            print(f"     System error: {e}")

    print("\n--------------------------------------")
    print("✅ COMPLETE! All products processed.")
    print("--------------------------------------")

# Run the main function
if __name__ == "__main__":
    upload_files()