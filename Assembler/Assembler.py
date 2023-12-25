class Token:
    def __init__(self, _str):
        self.str = _str
        self.type = self.DetermineType()
        return
    
    def DetermineType(self):
        if self.str.isalpha():
            return "INSTRUCTION"
        elif self.str.isalnum():
            if self.str[1] == 'd':
                return "IMMEDIATE"
            elif self.str[1] == 'r':
                return "REGISTER"
            else:
                return "Expected type character of either 'r' or 'd'"

def Tokenizer():
    counter = 0
    for line in programASM:
        counter += 1
        instructions.append(list())
        tokStr = ""
        for i in range(len(line)):
            if line[i].isspace():
                if len(tokStr) > 0:
                    instructions[len(instructions)-1].append(Token(tokStr))
                    tokStr = ""
                continue
            elif line[i].isalnum():
                tokStr += line[i]
                continue
            elif line[i] == "#":
                break
            else:
                return "Error tokenizing line %d at index %d" %(counter,i)
        if len(instructions[len(instructions)-1]) == 0:
            instructions.pop(len(instructions)-1)
            
def Parser():

    ALUMap = {"ADD":'0100',"SUB":'0101',"AND":'1000',"ORA":'1001'}
    ALUMapAlt = {"MOV":'0011',"INC":'0110',"DEC":'0111',"NOT":'1010',"BSL":'1011',"BSR":'1100'}
    JMPMap = {"JMP":'1101',"JIN":'1110',"JIZ":'1111'}

    def IsEven(num):
        return num % 2 == 0

    for i in range(len(instructions)):
        instr = instructions[i]
        INSTR, R, A, B = "----", "----", "----", "----"
        ADDR = f'{2*i:08b}'[0:4] + " " + f'{2*i:08b}'[4:8] + " " + f'{2*i+1:08b}'[0:4] + " " + f'{2*i+1:08b}'[4:8]
        
        def ALUFunc(R, A, B):
            if instr[1].type != "REGISTER" or instr[2].type != "REGISTER" or instr[3].type != "REGISTER":
                return "Expected Register, Register, Register line %d" %(i)
            return (f'{int(instr[1].str[2:]):08b}'[4:8],
            f'{int(instr[2].str[2:]):08b}'[4:8] if IsEven(int(instr[2].str[2:])) else '0000',
            f'{int(instr[3].str[2:]):08b}'[4:8] if not IsEven(int(instr[3].str[2:])) else '0000')
        
        def ALUFuncAlt(R, A, B):
            if instr[1].type != "REGISTER" or instr[2].type != "REGISTER":
                return "Expected Register, Register, Register line %d" %(i)
            return (f'{int(instr[1].str[2:]):08b}'[4:8],
            f'{int(instr[2].str[2:]):08b}'[4:8] if IsEven(int(instr[2].str[2:])) else '0000',
            f'{int(instr[2].str[2:]):08b}'[4:8] if not IsEven(int(instr[2].str[2:])) else '0000')
        
        def JMPFunc(R, A, B):
            if instr[1].type != "REGISTER":
                return "Expected Register, line %d" %(i)
            return ('0000',
            f'{int(instr[1].str[2:]):08b}'[4:8] if IsEven(int(instr[1].str[2:])) else '0000',
            f'{int(instr[1].str[2:]):08b}'[4:8] if not IsEven(int(instr[1].str[2:])) else '0000')
    
        if instr[0].type != "INSTRUCTION":
            return "Error parsing line %d" %(i)
        
        elif instr[0].str == "LDA":
            if instr[1].type != "REGISTER" or instr[2].type != "IMMEDIATE":
                return "Expected Register, Immediate line %d" %(i)
            INSTR = '0001'
            R = f'{int(instr[1].str[2:]):08b}'[4:8]
            A = f'{int(instr[2].str[2:]):08b}'[4:8]
            B = f'{int(instr[2].str[2:]):08b}'[0:4]
        
        elif instr[0].str == "STR":
            if instr[1].type != "IMMEDIATE" or instr[2].type != "REGISTER":
                return "Expected Immediate, Register line %d" %(i)
            INSTR = '0010'
            R = f'{int(instr[2].str[2:]):08b}'[4:8]
            A = f'{int(instr[1].str[2:]):08b}'[4:8]
            B = f'{int(instr[1].str[2:]):08b}'[0:4]

        elif instr[0].str in ALUMap:
            INSTR = ALUMap[instr[0].str]
            R, A, B = ALUFunc(R, A, B)

        elif instr[0].str in ALUMapAlt:
            INSTR = ALUMapAlt[instr[0].str]
            R, A, B = ALUFuncAlt(R, A, B)
        
        elif instr[0].str in JMPMap:
            INSTR = JMPMap[instr[0].str]
            R, A, B = JMPFunc(R, A, B)

        programBIN.write("%s %s %s %s %s\n" %(ADDR,A,INSTR,B,R))

fileName = 'LogisticMap'

programASM = open("Programs\\" + fileName + ".txt", "r")
programBIN = open("Programs\\" + fileName + ".bin", "w")

instructions = list()

Tokenizer()
Parser()

programASM.close()
programBIN.close()