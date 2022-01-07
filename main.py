import pandas as pd
import random
from tkinter import *
import gtts
import playsound
import os

from pandas.errors import EmptyDataError

BACKGROUND_COLOR = "#B1DDC6"

known = []


# Flashcard_config
def new_flashcard():
    global timer
    """randomly pick a word from French words or stilltolearn.csv  (if the file exists)"""

    def flip_card():
        """Flips the card"""
        canvas.itemconfig(picked_word, text=flash_card["English"], fill="White")
        canvas.itemconfig(language_text, text=inv_flash_card[flash_card["English"]], fill="White")
        canvas.itemconfig(card_image, image=card_image_back)

    def save():
        """Save the words that are not known to the file"""
        known.append(flash_card)
        stilltolearn = [word for word in file if word not in known]
        # print(f"still to learn words {stilltolearn}")
        # print(f"known words {known}")
        df = pd.DataFrame.from_dict(stilltolearn)
        pd.DataFrame.to_csv(df, "stilltolearn.csv", index=False)
        print("saved")
        new_flashcard()

    def timer_cancel():
        window.after_cancel(timer)

    def playword():
        playsound.playsound("file.mp3", True)

    try:
        file = pd.read_csv("stilltolearn.csv").to_dict(orient="records")
    except FileNotFoundError:
        file = pd.read_csv("data/french_words.csv").to_dict(orient="records")
    except EmptyDataError:
        canvas.itemconfig(picked_word, text="So you have learned all of the words", fill="black",
                          font=("arial", 30, "bold"))
        canvas.itemconfig(language_text, text="Empty 'stilltolearn.csv' file", fill="black",font=("arial", 40, "bold") )


    timer_cancel()
    os.remove("file.mp3")
    flash_card = random.choice(file)
    inv_flash_card = {value: key for key, value in flash_card.items()}
    canvas.itemconfig(card_image, image=card_image_front)
    canvas.itemconfig(picked_word, text=flash_card["French"], fill="black")
    canvas.itemconfig(language_text, text=inv_flash_card[flash_card["French"]], fill="black")
    Button_right.config(command=save)
    Button_play.config(command=playword)
    play_word = gtts.gTTS(flash_card["French"], lang='fr')
    play_word.save("file.mp3")
    # playsound.playsound("file.mp3", True)

    timer = window.after(3000, flip_card)



#                                                       UI setup

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

card_image_back = PhotoImage(file="images/card_back.png")
card_image_front = PhotoImage(file="images/card_front.png")
button_right_image = PhotoImage(file="images/right.png")
button_wrong_image = PhotoImage(file="images/wrong.png")
speaker_icon = PhotoImage(file="images/Speaker.png")
icon = PhotoImage(file="images/icon.PNG")
window.iconphoto(False, icon)
canvas = Canvas(width=800, height=526, highlightbackground=BACKGROUND_COLOR, bg=BACKGROUND_COLOR)
card_image = canvas.create_image(400, 263, image=card_image_front)
canvas.grid(column=0, row=0, columnspan=3)

language_text = canvas.create_text(400, 150, text="Welcome to", font=("arial", 40, "italic"))
picked_word = canvas.create_text(400, 263, text="Flashy Application", font=("arial", 60, "bold"))

Button_right = Button(bg=BACKGROUND_COLOR, highlightcolor=BACKGROUND_COLOR, image=button_right_image,
                      command=new_flashcard, relief="flat")
Button_right.grid(column=2, row=2)

Button_wrong = Button(bg=BACKGROUND_COLOR, highlightcolor=BACKGROUND_COLOR, image=button_wrong_image,
                      command=new_flashcard, relief="flat")
Button_wrong.grid(column=0, row=2)

Button_play = Button(bg=BACKGROUND_COLOR, highlightcolor=BACKGROUND_COLOR, image=speaker_icon,fg=BACKGROUND_COLOR,
                     relief="flat")
Button_play.grid(column=1, row=2)

timer = window.after(3000, lambda: None)

window.mainloop()
