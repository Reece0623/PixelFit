import tkinter as tk
from tkinter import filedialog, Scrollbar, Canvas, Frame
from PIL import Image, ImageTk
import os

TARGET_WIDTH = 960
TARGET_HEIGHT = 540

images = []
image_filenames = []


def resize_and_pad_image(img):
    original_width, original_height = img.size

    if original_width / TARGET_WIDTH > original_height / TARGET_HEIGHT:
        new_width = TARGET_WIDTH
        new_height = int((TARGET_WIDTH / original_width) * original_height)
    else:
        new_height = TARGET_HEIGHT
        new_width = int((TARGET_HEIGHT / original_height) * original_width)

    img = img.resize((new_width, new_height), Image.LANCZOS)
    new_img = Image.new("RGB", (TARGET_WIDTH, TARGET_HEIGHT), (255, 255, 255))

    x_offset = (TARGET_WIDTH - new_width) // 2
    y_offset = (TARGET_HEIGHT - new_height) // 2
    new_img.paste(img, (x_offset, y_offset))

    return new_img


def upload_images():
    global images, image_filenames
    file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])

    if not file_paths:
        return

    for path in file_paths:
        img = resize_and_pad_image(Image.open(path))
        images.append(img)
        image_filenames.append(os.path.splitext(os.path.basename(path))[0])

    display_images()


def display_images():
    for widget in image_frame.winfo_children():
        widget.destroy()

    for i, img in enumerate(images):
        display_processed = ImageTk.PhotoImage(img.resize((300, 200), Image.LANCZOS))
        frame = tk.Frame(image_frame, bg="white")
        frame.pack(side=tk.LEFT, padx=5, pady=5)

        label = tk.Label(frame, image=display_processed)
        label.image = display_processed
        label.pack()

        remove_btn = tk.Button(frame, text="Remove", command=lambda index=i: remove_image(index))
        remove_btn.pack()

    image_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


def remove_image(index):
    del images[index]
    del image_filenames[index]
    display_images()


def clear_all_images():
    global images, image_filenames
    images.clear()
    image_filenames.clear()
    display_images()


def save_images():
    if images:
        folder_path = filedialog.askdirectory()
        if folder_path:
            for i, processed_img in enumerate(images):
                save_path = os.path.join(folder_path, f"{image_filenames[i]}_resized.jpg")
                processed_img.save(save_path)
            status_label.config(text="Images saved successfully!", fg="green")
    else:
        status_label.config(text="No images to save!", fg="red")


root = tk.Tk()
root.title("Image Resizer")
root.geometry("1000x600")
root.configure(bg="white")

upload_btn = tk.Button(root, text="Upload Images", command=upload_images, font=("Arial", 12))
upload_btn.pack(pady=10)

clear_btn = tk.Button(root, text="Clear All Images", command=clear_all_images, font=("Arial", 12))
clear_btn.pack(pady=5)

canvas_frame = tk.Frame(root)
canvas_frame.pack(fill=tk.X, expand=True, padx=10)

canvas = Canvas(canvas_frame, bg="white", height=250)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_x = Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
canvas.configure(xscrollcommand=scrollbar_x.set)

image_frame = Frame(canvas, bg="white")
canvas.create_window((0, 0), window=image_frame, anchor="nw")

save_btn = tk.Button(root, text="Save All Processed Images", command=save_images, font=("Arial", 12))
save_btn.pack(pady=5)

status_label = tk.Label(root, text="", font=("Arial", 10), bg="white")
status_label.pack()

root.mainloop()
