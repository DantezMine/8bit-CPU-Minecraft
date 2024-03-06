#source: https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Token:
    def __init__(self, _str):
        self.str = _str
        self.type = self.DetermineType()
        return
    
    def DetermineType(self):
        if self.str.isalpha():
            instrSet = {"LDA","STR","MOV","ADD","SUB","INC","DEC","AND","ORA","NOT","BSL","BSR","JMP","JIN","JIZ"}
            if self.str in instrSet:
                return "INSTRUCTION"
            else:
                return "LABEL"
        elif self.str.isalnum():
            if self.str[1] == 'd':
                return "IMMEDIATE"
            elif self.str[1] == 'r':
                return "REGISTER"
            else:
                print("Error: Expected type character of either 'r' or 'd'")
                return


#Seperates each token by whitespace into a list, one list per line
def Tokenizer():
    counter = 0
    instrLine = 0
    for line in programASM:
        counter += 1
        instrLine += 1
        instructions.append(list())
        tokStr = ""
        for i in range(len(line)):
            if line[i].isspace():
                if len(tokStr) > 0:
                    instructions[len(instructions)-1].append(Token(tokStr))
                    tokStr = ""
                continue
            elif line[i] == ":":
                if tokStr in labels:
                    print(f"{bcolors.FAIL}Error: Error tokenizing line %d at index %d. Label %s already exists{bcolors.ENDC}" %(counter, i, tokStr))
                    return -1
                labels[tokStr] = instrLine-1
                break
            elif line[i].isalnum():
                tokStr += line[i]
                continue
            elif line[i] == "#":
                break
            else:
                print(f"{bcolors.FAIL}Error: Error tokenizing line %d at index %d{bcolors.ENDC}" %(counter,i))
                return -1
        if len(instructions[len(instructions)-1]) == 0:
            instructions.pop(len(instructions)-1)
            instrLine -= 1
        
    print("Tokenized correctly")
    return
          
  
def Parser():
    def IsEven(num):
        return num % 2 == 0

    for i in range(len(instructions)):
        instr = instructions[i]
        INSTR, R, A, B = "----", "----", "----", "----"
        ADDR = f'{2*i:08b}'[0:4] + " " + f'{2*i:08b}'[4:8] + " " + f'{2*i+1:08b}'[0:4] + " " + f'{2*i+1:08b}'[4:8]
        
        #Instr | Result | A | B
        def ALUFunc(R, A, B):
            if instr[1].type != "REGISTER" or instr[2].type != "REGISTER" or instr[3].type != "REGISTER":
                print(f"{bcolors.FAIL}Error: On line %d, expected Register, Register, Register{bcolors.ENDC}" %(i+1))
                return
            valueA = int(instr[2].str[2:])
            valueB = int(instr[3].str[2:])
            if not IsEven(valueA):
                print(f"{bcolors.FAIL}Error: On line %d, first source register must be even{bcolors.ENDC}" %(i+1))
            if IsEven(valueB):
                print(f"{bcolors.FAIL}Error: On line %d, second source register must be odd{bcolors.ENDC}" %(i+1))
            R = f'{int(instr[1].str[2:]):08b}'[4:8]
            A = f'{valueA:08b}'[4:8]
            B = f'{valueB:08b}'[4:8]
            return (R, A, B)
        
        #Instr | Result | A or B
        def ALUAltFunc(R, A, B):
            if instr[1].type != "REGISTER" or instr[2].type != "REGISTER":
                print(f"{bcolors.FAIL}Error: On line %d, expected Register, Register{bcolors.ENDC}" %(i+1))
                return
            value = int(instr[2].str[2:])
            R = f'{int(instr[1].str[2:]):08b}'[4:8]
            A = f'{value:08b}'[4:8] if IsEven(value) else '0000'
            B = f'{value:08b}'[4:8] if not IsEven(value) else '0000'
            return (R, A, B)
        
        #Instr | A or B
        def JMPFunc(R, A, B):
            if instr[1].type != "REGISTER":
                print(f"{bcolors.FAIL}Error: On line %d, expected Register{bcolors.ENDC}" %(i+1))
                return
            value = int(instr[1].str[2:])
            R = '0000'
            A = f'{value:08b}'[4:8] if IsEven(value) else '0000'
            B = f'{value:08b}'[4:8] if not IsEven(value) else '0000'
            return (R, A, B)

        #Instr | Result | Immediate or Label
        def LDAFunc(R, A, B):
            if instr[1].type != "REGISTER":
                print(f"{bcolors.FAIL}Error: On line %d, expected Register{bcolors.ENDC}" %(i+1))
            R = f'{int(instr[1].str[2:]):08b}'[4:8]
            A,B = '',''
            if instr[2].type == "IMMEDIATE":
                A = f'{int(instr[2].str[2:]):08b}'[4:8]
                B = f'{int(instr[2].str[2:]):08b}'[0:4]
            elif instr[2].type == "LABEL":
                if instr[2].str not in labels:
                    print(f"{bcolors.FAIL}Error: On line %s, label %d doesn't exist{bcolors.ENDC}" %(instr[2].str,i+1))
                    return(R,A,B)
                A = f'{labels[instr[2].str]*2:08b}'[4:8]
                B = f'{labels[instr[2].str]*2:08b}'[0:4]
            return (R, A, B)
        
        #Instr | Result as source | Immediate as address
        def STRFunc(R, A, B):
            if instr[1].type != "IMMEDIATE" or instr[2].type != "REGISTER":
                print(f"{bcolors.FAIL}Error: On line %d, expected Immediate, Register{bcolors.ENDC}" %(i+1))
            R = f'{int(instr[2].str[2:]):08b}'[4:8]
            A = f'{int(instr[1].str[2:]):08b}'[4:8]
            B = f'{int(instr[1].str[2:]):08b}'[0:4]
            return (R, A, B)
        
        instrMap = {"LDA":'0001',"STR":'0010',"MOV":'0011',"ADD":'0100',"SUB":'0101',"INC":'0110',"DEC":'0111',"AND":'1000',"ORA":'1001',"NOT":'1010',"BSL":'1011',"BSR":'1100',"JMP":'1101',"JIN":'1110',"JIZ":'1111'}
        funcMap = {"LDA":LDAFunc,"STR":STRFunc,"MOV":ALUAltFunc,"ADD":ALUFunc,"SUB":ALUFunc,"INC":ALUAltFunc,"DEC":ALUAltFunc,"AND":ALUFunc,"ORA":ALUFunc,"NOT":ALUAltFunc,"BSL":ALUAltFunc,"BSR":ALUAltFunc,"JMP":JMPFunc,"JIN":JMPFunc,"JIZ":JMPFunc}
            
        if instr[0].type != "INSTRUCTION":
            print(f"{bcolors.FAIL}Error: On line %d, expected instruction{bcolors.ENDC}" %(i+1))
            return -1

        if instr[0].str in instrMap:
            INSTR = instrMap[instr[0].str]
            R, A, B = funcMap[instr[0].str](R,A,B)
            if R is None or A is None or B is None:
                return -1

        programBIN.write("%s %s %s %s %s\n" %(ADDR,A,INSTR,B,R))
    
    print("Parsed correctly")
    return 0

#fileName = 'LogisticMap'
fileName = input("Name of file (without suffix): ")

programASM = open("Programs\\" + fileName + ".txt", "r")
programBIN = open("Programs\\" + fileName + ".bin", "w")

instructions = list()
labels = {}

if Tokenizer() == -1:
    print("Tokenizer failed")
else:
    if Parser() == -1:
        print("Parser failed")

programASM.close()
programBIN.close()