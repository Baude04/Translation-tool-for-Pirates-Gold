class Pointer():
    def __init__(self, file, pointer_offset):
        self.offset = pointer_offset

    @property
    def value(self):
        return file[self.offset:self.offset+4]

    @value.setter
    def value(self, value:int):
        value = value.to_bytes(4, "big")
        actual_offset = self.offset
        for i in value:
            file[actual_offset] = i
            actual_offset += 1

class Pointers():
    def __init__(self, file, start, end):
        self.start = start
        self.end = end
        self.file = file
    def get_pointer(self, pointer_value:int):
        """Return the pointer which point to the value
        """
        pointer_value = pointer_value.to_bytes(4, "big")
        pointer_offset = self.file.find(pointer_value)
        return Pointer(file, pointer_offset)
    
class Sentence():
    def __init__(self, file, offset):
        self.file = file
        self.offset = offset
        self.end_offset = offset + len(self.sentence)
        
    @property
    def sentence(self):
        char_offset = self.offset
        a = True
        result = ""
        while a:
            octet = hex(file[char_offset])
            if octet == "0x0":
                a = False
            else:
                result += chr(int(octet, 16))
                char_offset += 1
        return result

    @sentence.setter
    def sentence(self, sentence):
        char_offset = self.offset
        for i in sentence:
            if hex(self.file[char_offset]) == "0x0":
                raise Exception("phrase trop longue")
            self.file[char_offset] = ord(i)
            char_offset += 1
        self.file[char_offset] = int.from_bytes(bytes.fromhex("00"), "big")#pose le caractère de fin de la phrase
        
        #change le pointeur
        pointeurs = Pointers(file, 0, 10000)
        pter = pointeurs.get_pointer(self.end_offset + 1)
        pter.value = char_offset + 1
        
        self.end_offset = char_offset

file = open("Pirates! Gold (USAtoFR).md", 'rb')
file = bytearray( file.read())#bytes
ph = Sentence(file, 0x3eec1)
print(ph.sentence)
ph.sentence = input("nvl phrase")


ph2 = Sentence(file, 0x3eec1)
print("nouvelle_phrase: " + ph2.sentence)

pointeurs = Pointers(file, 0, 10000)
pter = pointeurs.get_pointer(0x3eec1)
if pter.offset != 129816:
    print("error 1")




