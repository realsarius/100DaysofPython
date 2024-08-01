import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def upload_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = Image.open(file_path)
        
        image.thumbnail((root.winfo_screenwidth() - 50, root.winfo_screenheight() - 150))
        photo = ImageTk.PhotoImage(image)
        

        canvas.config(scrollregion=canvas.bbox("all"))
        canvas.config(width=image.width, height=image.height)


        canvas.create_image(0, 0, anchor="nw", image=photo)
        canvas.image = photo 

        messagebox.showinfo("Success", "Image uploaded successfully!")


root = tk.Tk()
root.title("Image Uploader")

root.geometry("800x600")

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

v_scroll = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

h_scroll = tk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

canvas.config(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

upload_button = tk.Button(root, text="Upload Image", command=upload_image)
upload_button.pack(pady=10)

root.mainloop()
