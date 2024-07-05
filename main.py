# main.py

import tkinter as tk
from image_editor import ImageEditorApp

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
