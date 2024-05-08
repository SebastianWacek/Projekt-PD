import cloudinary
from cloudinary import CloudinaryImage, uploader, api
import json
from dotenv import load_dotenv
import os
from tkinter import Tk, Label, Button, filedialog, Entry, Frame, StringVar, PhotoImage, Canvas
from PIL import Image, ImageTk

# Load environment variables from .env file
load_dotenv()

# Configure connection to Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Upload image function
def upload_image_from_disk(image_path, tags_string):
    tags = [tag.strip() for tag in tags_string.split(',')]  # Split tags by commas and strip whitespace
    try:
        # Upload the image to Cloudinary from disk with tags
        response = uploader.upload(image_path, tags=tags, unique_filename=False, overwrite=True)

        # Retrieve the URL of the uploaded image
        src_url = CloudinaryImage(response['public_id']).build_url()

        # Display the image URL in the console
        print("**** Image Upload ****\nImage URL: ", src_url, "\n")
    except Exception as e:
        print("An error occurred during image upload:", e)

# User interface function
def user_interface():
    def choose_file():
        # Function called after pressing the "Choose File" button
        file_path = filedialog.askopenfilename(title="Select an Image", initialdir="/", filetypes=[("Image files", "*.jpg *.png")])
        if file_path:
            # Load and display the selected image in the canvas
            img = Image.open(file_path)
            img = img.resize((300, 300), Image.Resampling.NEAREST)  # Resize the image to fit the canvas
            photo = ImageTk.PhotoImage(img)
            canvas.image = photo  # Keep a reference so the image is not garbage collected
            canvas.create_image(0, 0, image=photo, anchor="nw")
            upload_button.config(command=lambda: upload_image_from_disk(file_path, tags_entry.get()))  # Set command for upload button

    root = Tk()
    root.title("Image Selector")
    root.geometry("400x500")  # Increase the window size

    frame = Frame(root)
    frame.pack(padx=20, pady=20)

    tags_label = Label(frame, text="Enter Tags (comma-separated):")
    tags_label.pack()

    tags_entry = Entry(frame, width=50)
    tags_entry.pack(padx=10, pady=10)

    choose_button = Button(frame, text="Choose File", command=choose_file)
    choose_button.pack(pady=10)

    upload_button = Button(frame, text="Upload Image")
    upload_button.pack(pady=10)

    canvas = Canvas(root, width=300, height=300)
    canvas.pack(padx=10, pady=10)

    root.mainloop()

# Main function of the program
def main():
    user_interface()

if __name__ == "__main__":
    main()