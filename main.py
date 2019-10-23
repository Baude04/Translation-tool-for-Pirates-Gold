import os
from googletrans import Translator
from classes import *

def main():
    print("Welcome to this beautiful programm which will help you to translate this great game.\nIf you want to stop the translation, input stop\nDon't forget that rom size is limited, make short sentences.")

    translator = Translator()
    
    file_path = input("Enter the path of your rom:\n")
    if file_path == "d": file_path = "../Pirates! Gold (USAtoFR).md"
    
    file = open(file_path, 'rb')
    file = bytearray(file.read())   #bytes
    pointers = Pointers(file, 129817, 129924)
    position = 0x3eec1              #the start position
    a = True
    try:
        while a:
            sentence = Sentence(file, position)
            print("\nOriginal sentence: \n", sentence)
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
            file_name = input("Choose the name of your new translation:\n")
            new_file = open(file_name+".md", "wb")
            new_file.write(file)
            print("Your work has been saved, see you.")
        else:
            print("Strange choice, see you, strange person.")
        os.system("pause")

if __name__ == "__main__":
    main()
