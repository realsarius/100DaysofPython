import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageDraw, ImageFont

def apply_watermark():
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[
            ("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
            ("All files", "*.*")
        ]
    )
    if not file_path:
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
        title="Save watermarked image as"
    )
    if not save_path:
        return
    
    watermark_text = simpledialog.askstring("Watermark", "Enter watermark text:")
    if not watermark_text:
        return

    try:
        image = Image.open(file_path)
        draw = ImageDraw.Draw(image)
        width, height = image.size

        font_size = min(width, height) // 10
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()
            font_size = 20 

        text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = width - text_width - 10
        text_y = height - text_height - 10

        draw.text((text_x, text_y), watermark_text, font=font, fill=(255, 255, 255, 128))

        image.save(save_path)
        messagebox.showinfo("Success", "Watermarked image saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

root = tk.Tk()
root.title("Image Watermarker")

button = tk.Button(root, text="Apply Watermark", command=apply_watermark)
button.pack(pady=20)

root.mainloop()
