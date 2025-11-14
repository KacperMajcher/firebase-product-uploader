# Python Firebase Seeder (Uploader)

A flexible Python script to batch-upload product data (from a JSON file) and corresponding images to Cloud Firestore and Firebase Storage.

This project is separated into user-editable files and the core script logic:

* **`config.py`**: **This is the main file you edit.** It contains all your project settings, paths, and data mapping logic.
* **`products.json`**: An example data file. You can edit this or point `config.py` to a different JSON file.
* **`uploader.py`**: The core script engine. **You don't need to edit this file.**
* **`key.json`**: (You must add this) Your private Firebase Admin SDK key.

---

## Requirements

* Python 3.x
* A Google Firebase project
* **Cloud Firestore** and **Firebase Storage** services enabled (requires "Blaze" plan, but the free tier is generous).

---

## 1. Installation

1.  **Clone the repository:**
    ```bash
    git clone [YOUR_REPO_URL]
    cd [YOUR_REPO_NAME]
    ```

2.  **Install the required library:**
    ```bash
    pip install firebase-admin
    ```

3.  **Get Your Service Account Key:**
    1.  Go to your [Firebase Console](https://console.firebase.google.com/) -> Project Settings -> Service Accounts.
    2.  Click **"Generate new private key"**.
    3.  A `.json` file will be downloaded.
    4.  Rename this file to match the `SERVICE_ACCOUNT_KEY` setting in `config.py` (default is **`key.json`**) and place it in the same folder as this script.

    ⚠️ **CRITICAL: This key file is a secret.** The `.gitignore` file is set up to ignore `key.json`, but never share this file publicly.

---

## 2. Configuration

**Open `config.py` and edit the variables:**

* **`SERVICE_ACCOUNT_KEY`**: Path to your downloaded service account key (e.g., `'key.json'`).
* **`BUCKET_NAME`**: Your Firebase Storage bucket URL (e.g., `'my-project.appspot.com'`).
* **`LOCAL_IMAGES_PATH`**: The absolute path to the folder on your computer containing the images.
* **`PRODUCTS_JSON_PATH`**: The name (or path) of the JSON file containing your data (e.g., `'products.json'`).
* **`STORAGE_FOLDER`**: The folder name inside Firebase Storage where images will be uploaded (e.g., `'products'`).
* **`COLLECTION_NAMES`**: A dictionary mapping the `type` field from your JSON to your Firestore collection names (e.g., `{ 'coffee': 'coffees', 'pastry': 'pastries' }`).
* **`map_product_to_firestore` function**: This is the most powerful part. You can completely change the logic here to define *how* the data from your JSON should be structured (i.e., your "data tree") when it's saved to Firestore.

---

## 3. Data File

Open **`products.json`** (or your custom JSON file) and add your data.

* It must be a valid JSON list `[ ... ]`.
* Each object in the list must have an **`"id"`** key.
* The `"id"` must match the name of the image file (e.g., `"id": "Cappuccino"` requires a `Cappuccino.png` file in your `LOCAL_IMAGES_PATH`).

---

## 4. Usage

Once `config.py` is set up and your `products.json` is ready:

1.  Open your terminal in the script's folder.
2.  Run the uploader:

    ```bash
    python uploader.py
    ```

The script will handle the rest and show the progress in the terminal.# Python Firebase Seeder (Uploader)

A flexible Python script to batch-upload product data (from a JSON file) and corresponding images to Cloud Firestore and Firebase Storage.

This project is separated into user-editable files and the core script logic:

* **`config.py`**: **This is the main file you edit.** It contains all your project settings, paths, and data mapping logic.
* **`products.json`**: An example data file. You can edit this or point `config.py` to a different JSON file.
* **`uploader.py`**: The core script engine. **You don't need to edit this file.**
* **`key.json`**: (You must add this) Your private Firebase Admin SDK key.

---

## Requirements

* Python 3.x
* A Google Firebase project
* **Cloud Firestore** and **Firebase Storage** services enabled (requires "Blaze" plan, but the free tier is generous).

---

## 1. Installation

1.  **Clone the repository:**
    ```bash
    git clone [YOUR_REPO_URL]
    cd [YOUR_REPO_NAME]
    ```

2.  **Install the required library:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Get Your Service Account Key:**
    1.  Go to your [Firebase Console](https://console.firebase.google.com/) -> Project Settings -> Service Accounts.
    2.  Click **"Generate new private key"**.
    3.  A `.json` file will be downloaded.
    4.  Rename this file to match the `SERVICE_ACCOUNT_KEY` setting in `config.py` (default is **`key.json`**) and place it in the same folder as this script.

    ⚠️ **CRITICAL: This key file is a secret.** The `.gitignore` file is set up to ignore `key.json`, but never share this file publicly.

---

## 2. Configuration

**Open `config.py` and edit the variables:**

* **`SERVICE_ACCOUNT_KEY`**: Path to your downloaded service account key (e.g., `'key.json'`).
* **`BUCKET_NAME`**: Your Firebase Storage bucket URL (e.g., `'my-project.appspot.com'`).
* **`LOCAL_IMAGES_PATH`**: The absolute path to the folder on your computer containing the images.
* **`PRODUCTS_JSON_PATH`**: The name (or path) of the JSON file containing your data (e.g., `'products.json'`).
* **`STORAGE_FOLDER`**: The folder name inside Firebase Storage where images will be uploaded (e.g., `'products'`).
* **`COLLECTION_NAMES`**: A dictionary mapping the `type` field from your JSON to your Firestore collection names (e.g., `{ 'coffee': 'coffees', 'pastry': 'pastries' }`).
* **`map_product_to_firestore` function**: This is the most powerful part. You can completely change the logic here to define *how* the data from your JSON should be structured (i.e., your "data tree") when it's saved to Firestore.

---

## 3. Data File

Open **`products.json`** (or your custom JSON file) and add your data.

* It must be a valid JSON list `[ ... ]`.
* Each object in the list must have an **`"id"`** key.
* The `"id"` must match the name of the image file (e.g., `"id": "Cappuccino"` requires a `Cappuccino.png` file in your `LOCAL_IMAGES_PATH`).

---

## 4. Usage

Once `config.py` is set up and your `products.json` is ready:

1.  Open your terminal in the script's folder.
2.  Run the uploader:

    ```bash
    python uploader.py
    ```

The script will handle the rest and show the progress in the terminal.
