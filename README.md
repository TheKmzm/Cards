# 🎴 Card Game Application (Tkinter & CMD Interface)

This is a fun Card Game Application built in Python using Tkinter for the graphical interface and an optional Command-Line Mode. The app allows users to draw cards from a deck, add new cards, tell jokes, rotate the screen, and even play text-to-speech outputs.

The application supports two modes:

    Graphical User Interface (GUI) mode using Tkinter.
    Command-Line (CMD) mode for terminal-based usage.

## 🛠 Features

    🎲 Draw Random Cards: Pull random cards from a customizable deck.
    🃏 Add New Cards: Dynamically add new cards to the deck with custom properties.
    🤡 Tell Jokes: The app can tell a random joke using the PyJokes library.
    🔄 Screen Rotation: Special cards trigger screen rotation using the rotatescreen library.
    🎨 Color Easter Egg: Some cards trigger a color-changing background effect.
    🎙️ Text-to-Speech Output: The app can read messages aloud using gTTS.

## 📥 Installation

    Clone the repository:

git clone https://github.com/yourusername/card-game-app.git
cd card-game-app

Install required libraries:

    pip install -r requirements.txt

Requirements

    Python 3.8+
    Libraries: tkinter, gtts, pyjokes, rotatescreen, playsound

## 🚀 How to Run
GUI Mode (Default)

Run the script directly to launch the graphical interface:

python card_game.py

You will see a window with buttons to:

    Roll Card: Draw a random card from the deck.
    Add Card: Add a new card to the deck with custom properties.
    Say PyJoke: Tell a random joke.
    Toggle UI Mode: Switch to Command-Line Mode.

CMD Mode

To switch to the Command-Line Mode, click the Toggle UI Mode button in the GUI, or launch directly in CMD by running:

python card_game.py

In CMD Mode, use the following commands:

    roll – Draw a random card.
    add – Add a new card to the deck.
    pyjoke – Get a random joke.
    exit – Exit the application.

## 🎴 Card Properties

Cards are managed using a cards.csv file. Each card has:

    Name – The name of the card (e.g., Ace, King, 5).
    Copies – Number of copies in the deck.
    Property – The special effect of the card.

Example cards.csv file:

name,copies,property
1,4,Startovací karta
A,4,Ace - otoč obrazovku
5,4,Pět bodů

Special Cards:
Card	Property
Ace	Rotates the screen
J	Special card effect
Q	Special card effect
K	Special card effect
🧪 Example Usage

GUI Mode:

    Click Roll Card to draw a random card.
    If the card is an Ace, your screen will rotate!
    Click Add Card to add a new custom card to the deck.
    Click Say PyJoke to hear a random joke.

CMD Mode:

Zadejte příkaz: roll
Card: Ace - otoč obrazovku

Zadejte příkaz: add
Zadejte název karty: Joker
Zadejte počet kopií (celé číslo): 2
Zadejte vlastnost karty: Surprise effect

📋 How to Add New Cards

    Click the Add Card button in the GUI.
    Enter the Card Name, Number of Copies, and Property.
    The card will be saved to the deck and the cards.csv file.

## 📄 License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it.
🖼️ Screenshots

Main GUI Window:

(Add a screenshot of the GUI window here.)
## 🤔 Known Issues

    The rotatescreen feature only works on Windows systems.
    The app may crash if gTTS or playsound cannot access the audio device.
