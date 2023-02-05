import re
from enum import Enum
class Category(Enum):
      KEYWORD=0
      PUNC=1
      COMMENT=2
      IDENTIFIER=3
      VALUE=4

class Token:
    def __init__(self,category,value):
        self.category=category
        self.value=value
    def __repr__(self):
        if self.category==Category.KEYWORD:
            return  ('<KEYWORD , "%s" >' % self.value)
        if self.category==Category.PUNC:
            return  ('<PUNC , "%s" >' % self.value)
        if self.category==Category.COMMENT:
            return  ('<COMMENT , "%s" >' % self.value)
        if self.category==Category.IDENTIFIER:
            return  ('<IDENTIFER , "%s" >' % self.value)
        if self.category==Category.VALUE:
            return ('<VALUE , "%s" >' % self.value)
class Tokenizer:
    def __init__(self,filename=""):
        self.filename=filename
        self.line_count=0
        self.keywords={}
        self.punclst=[]
        self.source=[]
        self.token_lst=[]

        self.generate_punc()
        self.get_keywords()
        self.open_file()
        self.get_token()
    def print_token(self):
        for token in self.token_lst:
            print(token)
    def is_ID(self,st):
        try:
            st.index("'")
            return False
        except:
            pass
        
        try:
            st.index('"')
            return False
        except:
            pass
        
        try:
            int(st[0])
            return False
        except:
            pass
        
        find=True
        for s in st:
            if (s.isalpha() or s.isdigit()):
                continue
            else:
                find=False
                break
        if find:
            return find
        return False

    def get_keywords(self):
        filename="keywords.txt"
        txt=open(filename,'r',encoding='utf-8').readlines()
        key_words={}
        for s in txt:
            KEY=s.split(":")[0]
            KEY=KEY.lstrip()
            KEY=KEY.rstrip()
            key_words[KEY]=[]
            VALUE=s.split(":")[1].replace('\n',"").split(",")
            for value in VALUE:
                value=value.lstrip()
                value=value.rstrip()
                key_words[KEY].append(value)
        self.keywords=key_words
    def generate_punc(self):
        self.punclst= [".",";",":","!","?","/","\\",",","@","$","&",")","(","\"","#",
"[", "]", "{", "}", "=", "+=", "-=", "*=", "/=", "//=", "%=", "&=", "|=",
"^=", ">>=", "<<=", "**=", "+", '-', '==']
    
    def is_punc(self,ch):
        if ch in self.punclst:
            return True
        return ch in self.punclst
    
    def open_file(self):
        try:
            fin = open(self.filename, 'r',encoding="utf8")
        except:
            print ("Input file does not exists: %s" % self.filename)
            return False
        lines = fin.readlines()

        # if the file is empty
        if len(lines) <= 0:
            print ("Input file %s is empty" % self.filename)
            return []
        self.source=lines
        return lines
    
    def breakup_line(self,line):
            words=line.split()
            newwords=[]
            for word in words:
                if (word[0]=="'" or word[0] =='"') and (word[-1]=="'" or word[-1] =='"'):
                    newwords.append(word)
                else:
                    t = re.findall(r"[\w]+|[^\s\w]|[-:\w]", word)
                    newwords.extend(t)
            return newwords
    
    def get_string(self,words):
            new_words = []
            adding = False
            tmpstring = ''
            skip = False
            for w in words:

                if ('"' in w or "'" in w) and (w.count('"') < 2 and w.count("'") < 2):
                    adding = not adding
                if not adding:
                    new_words.append(tmpstring+w)
                    tmpstring = ''
                    skip = True
                if adding:
                    tmpstring += w + ' '
                else:
                    if skip:
                        skip = False
                    else:
                        new_words.append(w)
            return new_words
    def is_keyword(self,a):
        for k, v in self.keywords.items():
            if a in v:
                return True
        return False
    def get_token(self):
        skip = False
        print ("<Category , Value>")
        cnt=0
        for line in self.source:
            self.line_count=self.line_count+1
            if '#' in line:
                comment_start=line.index("#")
                line=line[comment_start+1]
                token=Token(Category.COMMENT,line)
                self.token_lst.append(token)
                continue
            tokens = self.breakup_line(line)
            final = self.get_string(tokens)
            for c, item in enumerate(final):
        # print cnt
                cnt=cnt+1
                if not skip:
                    if self.is_punc(item):
                        try:
                            if self.is_punc(item + final[c+1]):
                                token=Token(Category.PUNC,item + final[c+1])
                                self.token_lst.append(token)
                                skip = True
                            else:
                                token=Token(Category.PUNC,item)
                                self.token_lst.append(token)
                        except:
                            token=Token(Category.PUNC,item)
                            self.token_lst.append(token)
                    elif self.is_keyword(item):
                        token=Token(Category.KEYWORD,item)
                        self.token_lst.append(token)
                    elif self.is_ID(item):
                        token=Token(Category.IDENTIFIER,item)
                        self.token_lst.append(token)
                    else:
                        token=Token(Category.VALUE,item)
                        self.token_lst.append(token)
                else:
                    skip = False
                
            

if __name__=="__main__":
    filename="example.py"
    test=Tokenizer(filename)
    test.print_token()



        

        

    
    
    