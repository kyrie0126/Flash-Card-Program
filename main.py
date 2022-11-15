import tkinter as tk
import pandas as pd
import random as rd
import json

BACKGROUND_COLOR = "#B1DDC6"
LABEL_FONT = ("arial", 20, "italic")
TERM_FONT = ("arial", 50, "bold")
NUM_FONT = ("arial", 15, "normal")


# ---------------------------------- Data ----------------------------------
data = pd.read_csv("data/spanish_words.csv")
all_terms = data.to_dict(orient="records")
current_card = {}
known_terms = {}
unknown_terms = {}


# ----------------------------- Generate Random Word -----------------------------
def generate():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = rd.choice(all_terms)
    canvas.itemconfig(card_image, image=card_front_img)
    canvas.itemconfig(card_title, text="Spanish")
    canvas.itemconfig(card_term, text=f"{current_card['Spanish']}")
    canvas.itemconfig(card_num, text=f"{len(known_terms)+len(unknown_terms)+1}/100")
    flip_timer = window.after(3000, func=flip)


# ----------------------------- Flip Cards -----------------------------
def flip():
    canvas.itemconfig(card_title, text="English")
    canvas.itemconfig(card_term, text=f"{current_card['English']}")
    canvas.itemconfig(card_image, image=card_back_img)


# ----------------------------- Save Known/Unknown Terms -----------------------------
def is_known():
    global known_terms
    try:
        all_terms.remove(current_card)
        known_terms[current_card["Spanish"]] = current_card["English"]
        with open("correct_terms.json", mode="w") as correct_file:
            json.dump(known_terms, correct_file, indent=4)
        generate()
    except ValueError:
        generate()


def is_unknown():
    global unknown_terms
    try:
        all_terms.remove(current_card)
        unknown_terms[current_card["Spanish"]] = current_card["English"]
        with open("incorrect_terms.json", mode="w") as incorrect_file:
            json.dump(unknown_terms, incorrect_file, indent=4)
        generate()
    except ValueError:
        generate()


# ---------------------------------- GUI ----------------------------------
# window
window = tk.Tk()
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

flip_timer = window.after(3000, func=flip)

# images
card_front_img = tk.PhotoImage(file="images/card_front.png")
card_back_img = tk.PhotoImage(file="images/card_back.png")
right_img = tk.PhotoImage(file="images/right.png")
wrong_img = tk.PhotoImage(file="images/wrong.png")

# canvas - card front/back
canvas = tk.Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_image = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Ready to learn Spanish?", font=LABEL_FONT)
card_term = canvas.create_text(400, 263, text="Let's begin!", font=TERM_FONT)
card_num = canvas.create_text(400, 350, text="", font=NUM_FONT)
canvas.grid(column=0, row=0, columnspan=2)

# buttons - using grid placement
wrong_button = tk.Button(command=is_unknown, image=wrong_img, highlightthickness=0, bg=BACKGROUND_COLOR, borderwidth=0)
wrong_button.grid(column=0, row=1)
right_button = tk.Button(command=is_known, image=right_img, highlightthickness=0, bg=BACKGROUND_COLOR, borderwidth=0)
right_button.grid(column=1, row=1)

window.mainloop()
