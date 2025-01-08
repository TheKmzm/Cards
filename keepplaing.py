import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import *
from gtts import gTTS
import random
import pyjokes
import rotatescreen
import time
import os
import sys
import csv
import openai
from playsound import playsound


# Globální proměnné
rotation_angle = 0
original_rotation_angle = 0
buttons_color = "#80e6cc"
original_bg_color = "#99ffcc"
fullscreen = False
original_font = None

smile_button_visible = False
smile_button = None
running_easteregg1 = False
active_ui_mode = True  # True for tkinter UI, False for CMD
cmd_output = None

CARD_FILE = "cards.csv"

def load_cards():
    global cards_properties, deck
    if not os.path.exists(CARD_FILE):
        # Pokud soubor neexistuje, vytvoří výchozí data
        default_cards = [
            {"name": "1", "copies": 4, "property": "Startovací karta"},
            {"name": "2", "copies": 4, "property": "Dva body"},
            {"name": "3", "copies": 4, "property": "Tři body"},
            {"name": "4", "copies": 4, "property": "Čtyři body"},
            {"name": "5", "copies": 4, "property": "Pět bodů"},
            {"name": "6", "copies": 4, "property": "Šest bodů"},
            {"name": "7", "copies": 4, "property": "Sedm bodů"},
            {"name": "8", "copies": 4, "property": "Osm bodů"},
            {"name": "9", "copies": 4, "property": "Devět bodů"},
            {"name": "10", "copies": 4, "property": "Deset bodů"},
            {"name": "J", "copies": 4, "property": "Jack - speciální karta"},
            {"name": "Q", "copies": 4, "property": "Queen - speciální karta"},
            {"name": "K", "copies": 4, "property": "King - speciální karta"},
            {"name": "A", "copies": 4, "property": "Ace - otoč obrazovku"},
        ]
        with open(CARD_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "copies", "property"])
            writer.writeheader()
            writer.writerows(default_cards)

    cards_properties = {}
    deck = []
    with open(CARD_FILE, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            copies = int(row["copies"])
            property = row["property"]
            cards_properties[name] = property
            deck.extend([name] * copies)

def save_card(name, copies, property):
    with open(CARD_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "copies", "property"])
        writer.writerow({"name": name, "copies": copies, "property": property})

def easteregg_colors():
    global running_easteregg1,original_bg_color
    while running_easteregg1:
        random_color = "#" + "".join(random.choices("0123456789ABCDEF", k=6))
        if active_ui_mode:
            root.configure(bg=random_color)
            root.update()
        time.sleep(0.1)  # Zpoždění pro efekt
    if active_ui_mode:
        root.configure(bg=original_bg_color)

def say_joke():
    joke = pyjokes.get_joke(language="en", category="all")
    output(joke,1)

def rotate_screen():
    global rotation_angle
    screen = rotatescreen.get_primary_display()
    rotation_angle = (rotation_angle + 90) % 360
    screen.rotate_to(rotation_angle)

def reset_to_normal():
    global rotation_angle, original_rotation_angle, original_bg_color, original_font, running_easteregg1
    # Reset rotace obrazovky
    screen = rotatescreen.get_primary_display()
    screen.rotate_to(original_rotation_angle)
    rotation_angle = original_rotation_angle
    # Reset barvy pozadí
    if active_ui_mode:
        root.configure(bg=original_bg_color)
        # Reset fontu
        for widget in root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(font=original_font)
    running_easteregg1 = False

def counter(start, stop = 0,step = -1):
    for i in range(start,stop,step):
        show_timed_message(str(i),'warning',1000)

def roll_card():
    global running_easteregg1
    if not deck:
        output("Žádné další karty!")
        return
    card = random.choice(deck)
    if remove_cards.get() if active_ui_mode else True:
        deck.remove(card)
    description = f"Card: {card} - {cards_properties[card]}"
    if active_ui_mode:
        card_label.config(text=description)
    else:
        output(description)

    if card == "A":
        rotate_screen()
    if card in ["5"]:
        counter(int(card))
    if running_easteregg1 and cards_properties.get(card, "") != "jeb_":
        running_easteregg1 = False
    elif cards_properties.get(card, "").startswith("jeb_"):
        running_easteregg1 = True
        easteregg_colors()

def add_card():
    if active_ui_mode:
        card_name = simpledialog.askstring("Přidat kartu", "Zadejte název karty:")
    else:
        card_name = input("Zadejte název karty: ")
    if not card_name:
        return
    try:
        if active_ui_mode:
            copies = int(simpledialog.askstring("Počet kopií", "Zadejte počet kopií (celé číslo):"))
        else:
            copies = int(input("Zadejte počet kopií (celé číslo): "))
        if copies <= 0:
            raise ValueError("Počet kopií musí být kladné číslo.")
    except (ValueError, TypeError):
        output("Neplatný počet kopií.")
        return

    if active_ui_mode:
        card_property = simpledialog.askstring("Vlastnost karty", "Zadejte vlastnost karty:")
    else:
        card_property = input("Zadejte vlastnost karty: ")
    if not card_property:
        return

    cards_properties[card_name] = card_property
    deck.extend([card_name] * copies)
    save_card(card_name, copies, card_property)
    output(f"Karta '{card_name}' byla přidána s {copies} kopií.")

def toggle_ui_mode():
    global active_ui_mode, root
    active_ui_mode = not active_ui_mode
    if active_ui_mode:
        os.execl(sys.executable, sys.executable, *sys.argv)  # Restart with tkinter
    else:
        if root:
            root.destroy()
        output("Přepnuto do CMD režimu. Použij příkazy:")
        output(" - 'roll': Vytáhne kartu.")
        output(" - 'add': Přidá kartu.")
        output(" - 'exit': Ukončí program.")
        cmd_loop()

def cmd_loop():
    global original_rotation_angle
    while True:
        cmd = input("Zadejte příkaz: ").strip().lower()
        if cmd == "roll":
            roll_card()
        elif cmd == "add":
            add_card()
        elif cmd == "pyjoke":
            say_joke()
        elif cmd == "exit":
            print("Ukončuji...")
            screen = rotatescreen.get_primary_display()
            screen.rotate_to(original_rotation_angle)
            sys.exit()
        else:
            print("Neplatný příkaz. Použijte 'roll', 'add' nebo 'exit'.")

def output(message, voice = 0):
    if active_ui_mode:
        if voice:
            myobj = gTTS(text=message, lang="en", slow=False)
            myobj.save("helpfile.mp3")
            playsound('./helpfile.mp3')
            messagebox.showinfo('Here it is',message)
            os.remove("helpfile.mp3") 
        else:
            messagebox.showinfo("Info", message)
    else:
        print(message)

def txt_2_mp3(message):
    myobj = gTTS(text=message, lang="en", slow=False)
    myobj.save("helpfile.mp3")
    playsound("helpfile.mp3")
    os.remove("helpfile.mp3") 

def show_timed_message(message, type='info', timeout=1000):
    root = tk.Tk()
    root.withdraw()
    try:
        root.after(timeout, root.destroy)
        if type == 'info':
            messagebox.showinfo('Info', message, master=root)
        elif type == 'warning':
            messagebox.showwarning('Warning', message, master=root)
        elif type == 'error':
            messagebox.showerror('Error', message, master=root)
    except:
        pass

# Načtení karet ze souboru
load_cards()

if active_ui_mode:
    # Vytvoření hlavního okna
    root = tk.Tk()
    w = Label(root,bg=buttons_color, text='Jen tahej nahodne karty.')
    w.pack()
    root.title("Card Game UI")
    root.attributes('-fullscreen',fullscreen)
    root.configure(bg=original_bg_color)
    # Globální proměnná pro odstranění karet
    remove_cards = tk.BooleanVar(value=True)

    # Zobrazení aktuální karty
    card_label = tk.Label(root,bg=buttons_color, text="Card: None", font=("Helvetica", 16))
    card_label.pack(pady=20)

    # Tlačítka pro akce
    roll_button = tk.Button(root,bg=buttons_color, text="Roll Card", command=roll_card)
    roll_button.pack(pady=5)

    add_button = tk.Button(root,bg=buttons_color, text="Add Card", command=add_card)
    add_button.pack(pady=5)

    toggle_button = tk.Button(root,bg=buttons_color, text="Toggle UI Mode", command=toggle_ui_mode)
    toggle_button.pack(pady=5)

    toggle_button = tk.Button(root,bg=buttons_color, text="Say pyjoke", command=say_joke)
    toggle_button.pack(pady=5)

    # Přepínač pro odstranění karet
    remove_checkbox = tk.Checkbutton(root,bg=buttons_color, text="Odstraňovat karty", variable=remove_cards)
    remove_checkbox.pack(pady=5)

    # Tlačítko pro ukončení
    exit_button = tk.Button(root, text="Exit",bg=buttons_color, command=lambda: [reset_to_normal(), root.quit()])
    exit_button.pack(pady=20)

    # Spuštění hlavní smyčky aplikace
    root.mainloop()
else:
    cmd_loop()
