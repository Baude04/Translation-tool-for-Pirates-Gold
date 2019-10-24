import os
from googletrans import Translator
from classes import *
from tkinter.filedialog import (askopenfilename, asksaveasfilename)
from tkinter import Tk

if __name__ == "__main__":
    print("Welcome to this beautiful programm which will help you to translate this great game.\nIf you want to stop the translation, input stop\nDon't forget that rom size is limited, make short sentences.")

    translator = Translator()

    tk = Tk()
    tk.withdraw()#empeche une fenetre inutile d'apparaitre
    file_path = askopenfilename(title="Choose a rom file",filetypes = (("md rom","*.md"),("all files","*.*")))
    
    file = open(file_path, 'rb')
    file = bytearray(file.read())   #bytes
    pointers = Pointers(file, 129817, 129924)
    position = 0x3eec1              #the start position
    a = True
    try:
        while a:
            sentence = Sentence(file, position)
            print("Sentence at offset:", hex(sentence.offset))
            print("Original sentence: \n", sentence)
            print("Cheap translation by google:\n", translator.translate(str(sentence), "fr", "en").text)
            new = input("Enter the new sentence:\n")
            if new == "stop".lower(): raise Exception("You have asked to stop")
            elif new == "": new = sentence.sentence
            sentence.sentence = new
            position = sentence.end_offset + 1

    except Exception as ex:
        print(ex)
        print("Do you want to save changes?(y/n)")
        response = input()
        if response in ["yes","y","ok","if you want","","of course I want","yes, of course","of course","oui","o","ja","j","will you pay me?"]:
            #empeche des fenetres inutiles de s'afficher
            tk.deiconify()
            tk.withdraw()
            
            file_name = asksaveasfilename(title="Save", filetypes = (("md rom file","*.md"),("all files","*.*")) )
            if not file_name.endswith(".md"): file_name += ".md"
            new_file = open(file_name, "wb")
            new_file.write(file)
            print("Your work has been saved, see you.")
        else:
            print("Strange choice, see you, strange person.")
        os.system("pause")
