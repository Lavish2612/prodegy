import tkinter as tk
from tkinter import filedialog, messagebox as mbox
from PIL import ImageTk, Image
import cv2
import numpy as np

class ImageEncryptorDecryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x700")
        self.root.title("Image Encryption Decryption")
        
        self.panelA = None
        self.panelB = None
        self.image_encrypted = None
        self.key = None
        self.filename = None
        self.eimg = None

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Image Encryption\nDecryption", font=("Arial", 40), fg="magenta").place(x=350, y=10)
        tk.Label(self.root, text="Original\nImage", font=("Arial", 40), fg="magenta").place(x=100, y=270)
        tk.Label(self.root, text="Encrypted\nDecrypted\nImage", font=("Arial", 40), fg="magenta").place(x=700, y=230)

        tk.Button(self.root, text="Choose", command=self.open_img, font=("Arial", 20), bg="orange", fg="blue", borderwidth=3, relief="raised").place(x=30, y=20)
        tk.Button(self.root, text="Save", command=self.save_img, font=("Arial", 20), bg="orange", fg="blue", borderwidth=3, relief="raised").place(x=170, y=20)
        tk.Button(self.root, text="Encrypt", command=self.encrypt_image, font=("Arial", 20), bg="light green", fg="blue", borderwidth=3, relief="raised").place(x=150, y=620)
        tk.Button(self.root, text="Decrypt", command=self.decrypt_image, font=("Arial", 20), bg="orange", fg="blue", borderwidth=3, relief="raised").place(x=450, y=620)
        tk.Button(self.root, text="Reset", command=self.reset_image, font=("Arial", 20), bg="yellow", fg="blue", borderwidth=3, relief="raised").place(x=800, y=620)
        tk.Button(self.root, text="Download Encrypted", command=self.download_encrypted, font=("Arial", 15), bg="light blue", fg="blue", borderwidth=3, relief="raised").place(x=30, y=670)
        tk.Button(self.root, text="Download Decrypted", command=self.download_decrypted, font=("Arial", 15), bg="light blue", fg="blue", borderwidth=3, relief="raised").place(x=220, y=670)
        tk.Button(self.root, text="EXIT", command=self.exit_win, font=("Arial", 20), bg="red", fg="blue", borderwidth=3, relief="raised").place(x=880, y=20)

        self.root.protocol("WM_DELETE_WINDOW", self.exit_win)

    def open_img(self):
        path = filedialog.askopenfilename(title='Open Image', filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if path:
            img = Image.open(path)
            img_tk = ImageTk.PhotoImage(img)

            if self.panelA is None or self.panelB is None:
                self.panelA = tk.Label(self.root, image=img_tk)
                self.panelA.image = img_tk
                self.panelA.pack(side="left", padx=10, pady=10)
                self.panelB = tk.Label(self.root, image=img_tk)
                self.panelB.image = img_tk
                self.panelB.pack(side="right", padx=10, pady=10)
            else:
                self.panelA.configure(image=img_tk)
                self.panelB.configure(image=img_tk)
                self.panelA.image = img_tk
                self.panelB.image = img_tk

            self.filename = path
            self.eimg = img

    def encrypt_image(self):
        if self.filename:
            image_input = cv2.imread(self.filename, 0)
            if image_input is not None:
                (x1, y) = image_input.shape
                image_input = image_input.astype(float) / 255.0
                mu, sigma = 0, 0.1
                self.key = np.random.normal(mu, sigma, (x1, y)) + np.finfo(float).eps
                self.image_encrypted = image_input / self.key
                cv2.imwrite('image_encrypted.jpg', self.image_encrypted * 255)
                imge = Image.open('image_encrypted.jpg')
                imge = ImageTk.PhotoImage(imge)
                self.panelB.configure(image=imge)
                self.panelB.image = imge
                mbox.showinfo("Encrypt Status", "Image Encrypted successfully.")
            else:
                mbox.showwarning("Warning", "Failed to read image.")
        else:
            mbox.showwarning("Warning", "No image selected.")

    def decrypt_image(self):
        if self.image_encrypted is not None and self.key is not None:
            image_output = self.image_encrypted * self.key
            image_output *= 255.0
            cv2.imwrite('image_output.jpg', image_output)
            imgd = Image.open('image_output.jpg')
            imgd = ImageTk.PhotoImage(imgd)
            self.panelB.configure(image=imgd)
            self.panelB.image = imgd
            mbox.showinfo("Decrypt Status", "Image decrypted successfully.")
        else:
            mbox.showwarning("Warning", "Image not encrypted yet.")

    def reset_image(self):
        if self.filename:
            img = Image.open(self.filename)
            img_tk = ImageTk.PhotoImage(img)
            self.panelB.configure(image=img_tk)
            self.panelB.image = img_tk
            mbox.showinfo("Success", "Image reset to original format!")
        else:
            mbox.showwarning("Warning", "No image selected.")

    def save_img(self):
        if self.eimg:
            path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
            if path:
                self.eimg.save(path)
                mbox.showinfo("Success", "Image Saved Successfully!")
        else:
            mbox.showwarning("Warning", "No image to save.")

    def download_encrypted(self):
        if self.image_encrypted is not None:
            path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
            if path:
                cv
