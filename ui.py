import tkinter as tk
from tkinter import ttk, Label
from constants import LOCALISATION_LIST
from image_operations import update_image, add_block, export_to_pdf


def create_ui(root, state):
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    state["patient_info"] = {}

    state["patient_info"]["name_entry"] = create_entry(frame, "Ф.И.О.:", 1, update_image, state)
    state["patient_info"]["dob_entry"] = create_entry(frame, "Дата рождения:", 2, update_image, state)
    state["patient_info"]["history_entry"] = create_entry(frame, "Номер истории болезни:", 3, update_image, state)

    add_block_label = ttk.Label(frame, text="Локализация:")
    add_block_label.grid(row=4, column=0, padx=5, pady=5)
    state["block_combobox"] = ttk.Combobox(frame, values=LOCALISATION_LIST)
    state["block_combobox"].grid(row=4, column=1, padx=5, pady=5)
    add_block_button = ttk.Button(frame, text="Добавить", command=lambda: add_block(state))
    add_block_button.grid(row=4, column=2, padx=5, pady=5)

    create_blocks_container(frame, state)

    export_button = ttk.Button(frame, text="Экспорт в PDF", command=lambda: export_to_pdf(state))
    export_button.grid(row=6, column=0, columnspan=3, pady=10)

    state["image_label"] = Label(root)
    state["image_label"].grid(row=0, column=1, padx=10, pady=10)
    update_image(state)


def create_entry(frame, label_text, row, update_func, state):
    label = ttk.Label(frame, text=label_text)
    label.grid(row=row, column=0, padx=5, pady=5)
    entry = ttk.Entry(frame)
    entry.grid(row=row, column=1, padx=5, pady=5)
    entry.bind("<KeyRelease>", lambda event: update_func(state))
    return entry


def create_blocks_container(frame, state):
    state["blocks_canvas"] = tk.Canvas(frame)
    state["blocks_canvas"].grid(row=5, column=0, columnspan=3, pady=10, sticky="nsew")

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=state["blocks_canvas"].yview)
    scrollbar.grid(row=5, column=3, sticky="ns")
    state["blocks_canvas"].configure(yscrollcommand=scrollbar.set)

    state["blocks_frame"] = ttk.Frame(state["blocks_canvas"])
    state["blocks_canvas"].create_window((0, 0), window=state["blocks_frame"], anchor="nw")

    state["blocks_frame"].bind("<Configure>", lambda e: state["blocks_canvas"].configure(
        scrollregion=state["blocks_canvas"].bbox("all")
    ))
