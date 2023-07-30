from ursina import *
import os

def run_action_file():
    with open('action.py', 'r') as file:
        code_to_execute = file.read()
    exec(code_to_execute, globals())

app = Ursina()

def on_button_click():
    run_action_file()

button = Button(text='Join the game!', on_click=on_button_click)
button.scale *= 1.5
button.y -= 0.2

app.run()
