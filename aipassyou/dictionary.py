import sys 
import re
import unicodedata
from itertools import permutations

#SPECIAL_CHARS = [ '!', '@', '#', '$', '%', '&', '.', ',', '_' ]   
SPECIAL_CHARS = [ '!', '@', '$', '%', '.' ]
#SEPARATOR_CHARS = ["", "_", "%", "4", "-", "&", ".", ","]
SEPARATOR_CHARS = ["", "_", "%"]
#VOW_NUM_CHARS = { 'a': '4', 'e': '3', 'i': '1', 'o': '0' }
VOW_NUM_CHARS = { 'a': '@', 'e': '3', 'i': '1', 'o': '0' }
#PERMUTATIONS = [1, 2]
PERMUTATIONS = [1]
        
class Generator:

    def __init__(self, data: dict, output: str = None):
        self.keywords = []
        self.passwords = []
        self.parse_json(data)
        self.out = sys.stdout if output == None else open(output, "w", encoding="utf-8")
    
    def parse_json(self, json: dict):
        for k, v in json.items():
            if isinstance(v, dict): self.parse_json(v)
            elif isinstance(v, list): 
                if k == 'passwords': self.passwords = list(set(self.passwords + v)) 
                if k == 'name' and " " in v: self.keywords = list(set(self.keywords + v.split(' '))) 
                else: self.keywords = list(set(self.keywords + v)) 
            else: pass

    def normalize(self, string: str) -> str:
        normalized = unicodedata.normalize('NFD', string)
        return normalized.encode('ascii', 'ignore').decode('utf8').casefold()

    def extract_numbers(self, data: str) -> list:
        return re.findall(r'\d+', data)

    def add_numbers(self, data: str, nfrom: int, nto: int, zfill: bool = True):
        nlen = len(str(nto-1))
        for i in range(nfrom, nto):
            n = str(i)
            if zfill: n = n.zfill(nlen)
            self.out.write(data + n + "\n")
            self.add_special_characters(data + n)
    
    def add_special_characters(self, data: str):
        for i in SPECIAL_CHARS: self.out.write(data + i + "\n")

    def add_serial_numbers(self, data: str, nchars: int = 10):
        for i in range(1, nchars):
            data += str(i)
            self.out.write(data + "\n")
            self.add_special_characters(data)
            # leet(key)
    
    def camelcase(self, data: str) -> str:
        return ' '.join(t.title() for t in data.split(' '))

    def vowel_to_number(self, data: str) -> str:
        return ''.join(VOW_NUM_CHARS.get(c, c) for c in data)

    def generate(self):
        numbers = []
        keywords = []

        for key in self.keywords:
            key = self.normalize(key)
            
            numbers = list(set(numbers + self.extract_numbers(key)))
            if key.isnumeric(): continue

            if " " in key:
                for i in SEPARATOR_CHARS:
                    ns_lower = key.replace(" ", i)
                    #ns_upper = ns_lower.upper()
                    ns_camel = self.camelcase(key).replace(" ", i)
                    
                    ns_vn_l = self.vowel_to_number(ns_lower)
                    #ns_vn_u = self.vowel_to_number(ns_upper)
                    ns_vn_c = self.vowel_to_number(ns_camel)
                    #keywords += [ns_lower, ns_upper, ns_camel, ns_vn_l, ns_vn_u, ns_vn_c]
                    keywords += [ns_lower, ns_camel, ns_vn_l, ns_vn_c]

            else:
                ns_camel = key.title()
                #ns_upper = key.upper()

                ns_vn_l = self.vowel_to_number(key)
                #ns_vn_u = self.vowel_to_number(ns_upper)
                ns_vn_c = self.vowel_to_number(ns_camel)
                #keywords += [key, ns_upper, ns_camel, ns_vn_l, ns_vn_u, ns_vn_c]
                keywords += [key, ns_camel, ns_vn_l, ns_vn_c]
        
        for i in PERMUTATIONS:
            for perm in permutations(keywords, i):
                term = "".join(perm)
                self.out.write(term + "\n")
                self.add_special_characters(term)
                self.add_serial_numbers(term)
                self.add_numbers(term, 0, 10)
                self.add_numbers(term, 0, 100, True)
                # Number at the  begining?
                # self.add_numbers(term, 0, 1000, True) # 000-999
                # self.add_numbers(term, 0, 3113, True)
                self.add_numbers(term, 1950, 2030, True)
                for n in numbers: 
                    self.out.write(term + n + "\n")
                    self.add_special_characters(term + n)
