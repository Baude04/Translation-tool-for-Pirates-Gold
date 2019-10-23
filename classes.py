class Pointer():
    def __init__(self, file, pointer_offset):
        self.offset = pointer_offset
        self.file = file
    @property
    def value(self):
        return self.file[self.offset:self.offset+4]

    @value.setter
    def value(self, value:int):
        value = value.to_bytes(4, "big")
        actual_offset = self.offset
        for i in value:
            self.file[actual_offset] = i
            actual_offset += 1

class Pointers():
    def __init__(self, file, start:int, end:int):
        self.start = start
        self.end = end
        self.file = file
    def get_pointer(self, pointer_value:int):
        """Return the pointer which point to the value
        """
        pointers_chunk = self.file[self.start : self.end+1]
        pointer_value = pointer_value.to_bytes(4, "big")
        if pointers_chunk.find(pointer_value) == -1:
            raise Exception("there is no pointer which has this value, try to change the start or the end offset of the Pointers object you are using")
        pointer_offset = pointers_chunk.find(pointer_value) + self.start
        return Pointer(self.file, pointer_offset)
    
class Sentence():
    def __init__(self, file, offset):
        self.file = file
        self.offset = offset
        self.end_offset = offset + len(self.sentence)

    def __fill_sentence_with_space(self):
        """Fill the sentence with space, including the end character
        """
        char_offset = self.offset
        a = True
        while a:
            octet = hex(self.file[char_offset])
            if octet == "0x0":
                a = False
            self.file[char_offset] = ord(' ')
            char_offset += 1
    
    @property
    def sentence(self):
        char_offset = self.offset
        a = True
        result = ""
        while a:
            octet = hex(self.file[char_offset])
            if octet == "0x0":
                a = False
            else:
                result += chr(int(octet, 16))
                char_offset += 1
        return result

    @sentence.setter
    def sentence(self, new_sentence):
        char_offset = self.offset
        if len(new_sentence) > len(self.sentence): raise Exception("The new sentence has to be shorter than the original one")#if you really want to make a longer sentence, you can delete this condition, but you will write on the next sentence, and the displaying of the next sentence will be incomplete
        self.__fill_sentence_with_space()
        for i in new_sentence:
            #this condition will never happens except if you have deleted the condition before, so don't delete it
            if hex(self.file[char_offset]) == "0x0":
                raise Exception("Too large sentence")
            
            self.file[char_offset] = ord(i)
            char_offset += 1
        self.file[char_offset] = int.from_bytes(bytes.fromhex("00"), "big")#pose le caractère de fin de la phrase
        
        #change le pointeur
        pointeurs = Pointers(self.file, 129816, 129924)#changez ces valeurs pour traduire une nouvelle partie du texte
        pter = pointeurs.get_pointer(self.end_offset + 1)
        pter.value = char_offset + 1
        
        self.end_offset = char_offset

    def __str__(self):
        return self.sentence




if __name__ == "__main__":
    file = open("../Pirates! Gold (USAtoFR).md", 'rb')
    file = bytearray( file.read())#bytes

    pointeurs = Pointers(file, 129816, 129924)
    pter = pointeurs.get_pointer(0x3eec1)
    if pter.offset != 129816:
        print("error 1")
        
    ph = Sentence(file, 0x3eec1)
    print(ph.sentence)
    ph.sentence = input("nvl phrase")


    ph = Sentence(file, 0x3eec1)
    print("nouvelle_phrase: ", ph)

    ph2 = Sentence(file, ph.end_offset+1)
    print("phrase suivante: ", ph2)

    
