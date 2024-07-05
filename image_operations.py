import tkinter as tk
from tkinter import ttk  # Добавляем импорт ttk
from PIL import ImageDraw, ImageFont, ImageTk
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
import tempfile
import os

from constants import (
    LOCALISATION_LIST,
    FORMATION_LIST,
    LOCALISATION_COORDINATES,
    TEXT_BLOCK_COORDINATES
)


def update_image(state):
    apply_changes(state)
    tk_image = ImageTk.PhotoImage(state["image"])
    state["image_label"].config(image=tk_image)
    state["image_label"].image = tk_image


def apply_changes(state):
    state["image"] = state["original_image"].copy()
    state["draw"] = ImageDraw.Draw(state["image"])

    for block in state["blocks"]:
        block_name = block['name']
        formations = []
        for j, var in enumerate(block['text_vars']):
            if var.get():
                text = f"{FORMATION_LIST[j]}"
                comment = block['comment_entries'][j].get().strip()
                if comment:
                    text += f": {comment}"
                formations.append(text)
        state["localisation_with_info"][block_name]['formations'] = formations

    state["text_block_positions"] = TEXT_BLOCK_COORDINATES.copy()

    for localisation, info in state["localisation_with_info"].items():
        if info['formations']:
            draw_arrow(state, localisation)
            draw_text(state, localisation)
            for formation in info['formations']:
                draw_text(state, formation)

    patient_info_text = (
        f"ФИО: {state['patient_info']['name_entry'].get()}\n"
        f"Дата рождения: {state['patient_info']['dob_entry'].get()}\n"
        f"Номер истории болезни: {state['patient_info']['history_entry'].get()}"
    )
    font = ImageFont.truetype("arial.ttf", 15)
    state["draw"].text((10, 10), patient_info_text, font=font, fill="black")


def draw_arrow(state, localisation):
    start_point = LOCALISATION_COORDINATES[localisation]
    if state["text_block_positions"]:
        relative_position = state["text_block_positions"].pop(0)
        image_width, image_height = state["image"].size
        destination = (int(image_width * relative_position[0]),
                       int(image_height * relative_position[1]))
    else:
        destination = start_point

    state["draw"].line([start_point, destination], fill="black", width=1)
    state["current_text_position"] = destination


def draw_text(state, text):
    font_size = 12
    padding = 5

    script_dir = os.path.dirname(__file__)  # Получаем путь к текущему скрипту
    bold_font_path = os.path.join(script_dir, "resources/Arial-Bold.ttf")  # Полный путь к файлу шрифта

    if text in LOCALISATION_LIST:
        font_path = bold_font_path
        draw_frame = True  # Рисуем рамку для названия локализации
    else:
        font_path = "resources/Arial.ttf"
        draw_frame = False  # Не рисуем рамку для названия образований

    try:
        font = ImageFont.truetype(font_path, font_size)
    except OSError as e:
        print(f"Error opening font file: {e}")
        return

    text_bbox = state["draw"].textbbox((0, 0), text, font=font)
    text_size = (text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1])

    if draw_frame:
        box_coords = [
            (state["current_text_position"][0] - text_size[0] // 2 - padding,
             state["current_text_position"][1] - padding),
            (state["current_text_position"][0] + text_size[0] // 2 + padding,
             state["current_text_position"][1] + text_size[1] + padding)
        ]
        state["draw"].rectangle(box_coords, fill="white", outline="black")

    text_position = (state["current_text_position"][0] - text_size[0] // 2,
                     state["current_text_position"][1])
    state["draw"].text(text_position, text, font=font, fill="black")

    state["current_text_position"] = (state["current_text_position"][0],
                                      state["current_text_position"][1] +
                                      text_size[1] + padding * 2)


def add_block(state):
    block_name = state["block_combobox"].get()
    if block_name and (
        len(state["blocks"]) < 7
         ) and (
        block_name not in [block['name'] for block in state["blocks"]]
    ):
        create_block(state, block_name)


def create_block(state, block_name):
    block_frame = ttk.Frame(state["blocks_frame"], padding="5")
    block_frame.pack(fill='y', pady=5)

    block_label = ttk.Label(block_frame, text=f"{block_name}")
    block_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

    # Определение доступных образований в зависимости от выбранной локализации
    available_formations = []
    if block_name == "Кардиальный отдел желудка" or block_name == "Тело желудка" \
            or block_name == "Антральный отдел желудка" or block_name == "Пилорический отдел желудка":
        available_formations = ["Полип", "Опухоль", "Язва", "Пятно", "Атрофия", "Дивертикул", "Вена", "Стеноз", "Эрозия", "Инородное тело", "Метаплазия"]
    elif block_name == "Нижняя треть пищевода":
        available_formations = ["Полип", "Опухоль", "Язва", "Пятно", "Вена", "Геморроидальный узел", "Стеноз", "Эрозия", "Инородное тело", "Метаплазия"]
    elif block_name == "Прямая кишка":
        available_formations = ["Полип", "Опухоль", "Язва", "Пятно", "Геморроидальный узел", "Стеноз", "Эрозия", "Инородное тело"]
    else:
        available_formations = ["Полип", "Опухоль", "Язва", "Пятно", "Дивертикул", "Вена", "Стеноз", "Эрозия", "Инородное тело"]

    block_text_vars = [tk.BooleanVar() for _ in range(len(FORMATION_LIST))]
    block_checkbuttons = []
    block_comments = []

    for j, formation in enumerate(FORMATION_LIST):
        if formation in available_formations:
            block_checkbutton = ttk.Checkbutton(
                block_frame, text=f"{formation}", variable=block_text_vars[j],
                command=lambda: update_image(state))
            block_checkbutton.grid(row=1 + j, column=0, padx=5, pady=5)
            block_checkbuttons.append(block_checkbutton)

            comment_entry = ttk.Entry(block_frame)
            comment_entry.grid(row=1 + j, column=1, padx=5, pady=5)
            comment_entry.bind("<KeyRelease>", lambda event: update_image(state))
            block_comments.append(comment_entry)

    state["blocks"].append({
        'name': block_name,
        'frame': block_frame,
        'text_vars': block_text_vars,
        'comment_entries': block_comments
    })

    # Инициализация пустого списка для новой локализации
    state["localisation_with_info"][block_name] = {
        'coordinates': LOCALISATION_COORDINATES[block_name],
        'formations': []
    }

    update_image(state)


def get_patient_filename(state):
    full_name = state["patient_info"]["name_entry"].get().strip()
    if not full_name:
        return "output.pdf"

    name_parts = full_name.split()
    last_name = name_parts[0]
    initials = ''.join([part[0].upper() for part in name_parts[1:]])
    filename = f"{last_name}{initials}.pdf"

    return filename


def export_to_pdf(state):
    apply_changes(state)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
        state["image"].save(tmpfile, format="PNG")
        tmpfile_path = tmpfile.name

    image_width, image_height = state["image"].size
    page_width, page_height = landscape(letter)

    aspect_ratio_image = image_width / image_height
    aspect_ratio_page = page_width / page_height

    if aspect_ratio_image > aspect_ratio_page:
        new_width = page_width
        new_height = page_width / aspect_ratio_image
    else:
        new_height = page_height
        new_width = page_height * aspect_ratio_image

    x_offset = (page_width - new_width) / 2
    y_offset = (page_height - new_height) / 2

    c = canvas.Canvas(get_patient_filename(state), pagesize=landscape(letter))

    c.setFont("Helvetica", 8)
    c.drawString(100, 550, f"Name: {state['patient_info']['name_entry'].get()}")
    c.drawString(100, 535, f"Date of Birth: {state['patient_info']['dob_entry'].get()}")
    c.drawString(100, 520, f"History Number: {state['patient_info']['history_entry'].get()}")

    c.drawImage(tmpfile_path, x_offset, y_offset, width=new_width, height=new_height)
    c.showPage()
    c.save()

    os.remove(tmpfile_path)

    print("Экспорт в PDF успешно выполнен.")
