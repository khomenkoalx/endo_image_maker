import tkinter as tk
from PIL import Image, ImageDraw

from constants import TEXT_BLOCK_COORDINATES
from ui import create_ui


def main():
    root = tk.Tk()
    root.title("Image Editor")

    state = {
        "image_path": "resources/digest.png",
        "original_image": None,
        "image": None,
        "draw": None,
        "blocks": [],
        "text_block_positions": TEXT_BLOCK_COORDINATES.copy(),
        "localisation_with_info": {}
    }

    state["original_image"] = Image.open(state["image_path"])
    state["image"] = state["original_image"].copy()
    state["draw"] = ImageDraw.Draw(state["image"])

    create_ui(root, state)

    root.mainloop()


if __name__ == "__main__":
    main()
