import cloudinary
from cloudinary import CloudinaryImage, uploader, api
import json
from dotenv import load_dotenv
import os
from tkinter import Tk, Button, filedialog

# Ładowanie zmiennych środowiskowych z pliku .envdsad
load_dotenv()

# Konfiguracja połączenia z Cloudinary
cloudinary.config( 
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"), 
    api_key = os.getenv("CLOUDINARY_API_KEY"), 
    api_secret = os.getenv("CLOUDINARY_API_SECRET") 
)

# Funkcja do przesyłania obrazu
def upload_image_from_disk(image_path):
    try:
        # Przesyłanie obrazu na Cloudinary z dysku
        response = uploader.upload(image_path, unique_filename=False, overwrite=True)

        # Pobieranie adresu URL przesłanego obrazu
        src_url = CloudinaryImage(response['public_id']).build_url()

        # Wyświetlanie adresu URL w konsoli
        print("****2. Przesyłanie obrazu****\nAdres URL obrazu: ", src_url, "\n")
    
    except Exception as e:
        print("Wystąpił błąd podczas przesyłania obrazu:", e)

# Funkcja do pobierania informacji o zasobie
def get_asset_info():
    try:
        # Pobieranie informacji o obrazie z Cloudinary
        image_info = api.resource("quickstart_butterfly")
        
        # Wyświetlanie informacji o obrazie w konsoli
        print("****3. Pobieranie informacji o obrazie****\nInformacje o przesłanym obrazie:\n", 
              json.dumps(image_info, indent=2), "\n")

        # Aktualizacja tagów na podstawie szerokości obrazu
        width = image_info["width"]
        tags = "large" if width > 900 else "medium" if width > 500 else "small"
        update_resp = api.update("quickstart_butterfly", tags=tags)

        # Wyświetlanie nowych tagów w konsoli
        print("Nowe tagi: ", update_resp["tags"], "\n")
    
    except Exception as e:
        print("Wystąpił błąd podczas pobierania informacji o obrazie:", e)

# Funkcja do transformowania obrazu
def create_transformation():
    try:
        # Tworzenie przekształconego adresu URL obrazu
        transformed_url = CloudinaryImage("quickstart_butterfly").build_url(width=100, height=150, crop="fill")

        # Wyświetlanie przekształconego adresu URL w konsoli
        print("****4. Transformacja obrazu****\nPrzekształcony adres URL obrazu: ", transformed_url, "\n")

        # Możesz również użyć poniższego kodu, aby wygenerować pełny element obrazu HTML:
        # imageTag = cloudinary.CloudinaryImage("quickstart_butterfly").image(radius="max", effect="sepia")
        # print("****4. Transformacja obrazu****\nTag obrazu HTML: ", imageTag, "\n")
    
    except Exception as e:
        print("Wystąpił błąd podczas transformacji obrazu:", e)

# Funkcja do interakcji z użytkownikiem
def user_interface():
    def choose_file():
        # Funkcja wywoływana po naciśnięciu przycisku "Wybierz plik"
        file_path = filedialog.askopenfilename(title="Wybierz obraz", initialdir="/", filetypes=[("Image files", "*.jpg *.png")])
        if file_path:
            # Jeśli użytkownik wybrał plik, przesyłaj obraz na Cloudinary
            upload_image_from_disk(file_path)
            get_asset_info()
            create_transformation()

    root = Tk()
    root.title("Wybierz zdjęcie")

    button = Button(root, text="Wybierz plik", command=choose_file)
    button.pack(padx=20, pady=20)

    root.mainloop()

# Główna funkcja programu
def main():
    user_interface()

if __name__ == "__main__":
    main()
