import cloudinary
from cloudinary import CloudinaryImage, uploader, api
import json
from dotenv import load_dotenv
import os
from flask import Flask, request, render_template, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

# Ładowanie zmiennych środowiskowych z pliku .env
load_dotenv()

# Konfiguracja połączenia z Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Inicjalizacja Firebase
cred = credentials.Certificate('programowanie-defensywne-firebase-adminsdk-z3qgq-3dbdbc517c.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        try:
            # Przesyłanie obrazu na Cloudinary
            upload_result = uploader.upload(file)
            public_id = upload_result['public_id']
            image_url = upload_result['url']

            # Zapisanie URL do Firestore
            doc_ref = db.collection('images').document(public_id)
            doc_ref.set({
                'image_url': image_url,
                'tags': []
            })

            return jsonify(status='success', image_url=image_url, public_id=public_id)
        except Exception as e:
            print(f"Error uploading image: {e}")
            return jsonify(status='error', message=str(e))
    else:
        return jsonify(status='error', message='No file uploaded')

@app.route('/tag', methods=['POST'])
def tag():
    data = request.json
    tag = data['tag']
    x = data['x']
    y = data['y']
    width = data['width']
    height = data['height']
    public_id = data['public_id']
    
    try:
        # Dodawanie tagu do obrazu w Cloudinary
        response = api.update(public_id, tags=tag)
        
        # Dodawanie tagu do Firestore
        doc_ref = db.collection('images').document(public_id)
        doc = doc_ref.get()

        if doc.exists:
            # Jeśli dokument już istnieje, aktualizuj go
            doc_ref.update({
                'tags': firestore.ArrayUnion([{
                    'tag': tag,
                    'x': x,
                    'y': y,
                    'width': width,
                    'height': height
                }])
            })
        else:
            # Jeśli dokument nie istnieje, utwórz go
            doc_ref.set({
                'image_url': CloudinaryImage(public_id).build_url(),
                'tags': [{
                    'tag': tag,
                    'x': x,
                    'y': y,
                    'width': width,
                    'height': height
                }]
            })

        print(f"Tag {tag} został dodany do obrazu.")
        return jsonify(status='success', tags=response.get('tags', []))
    except Exception as e:
        print(f"Error: {e}")
        return jsonify(status='error', message=str(e))

if __name__ == "__main__":
    app.run(debug=True)