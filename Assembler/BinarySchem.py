import mcschematic #python 3.9.7 64-bit interpreter necessary, I don't understand why
schem = mcschematic.MCSchematic()

discs = ("minecraft:stick","minecraft:music_disc_13","minecraft:music_disc_cat","minecraft:music_disc_blocks","minecraft:music_disc_chirp","minecraft:music_disc_far","minecraft:music_disc_mall","minecraft:music_disc_mellohi","minecraft:music_disc_stal","minecraft:music_disc_strad","minecraft:music_disc_ward","minecraft:music_disc_11","minecraft:music_disc_wait","minecraft:music_disc_pigstep","minecraft:music_disc_otherside","minecraft:music_disc_5")

class Token:
    def __init__(self,strVal):
        self.disc = discs[int(strVal,2)]
        
def Tokenize():
    instr = list()
    for line in programBINList:
        tokens = list()
        for i in range(8):
            tokens.append(Token(line[i*4:(i*4)+3]))
        instr.append(tokens)
    return instr
        
def FillShulkerBoxes(offset):
    shulkerAmnt = 1 + (len(instr)//13)
    shulkers = list()
    for i in range(shulkerAmnt):
        items = ''
        for k in range(13): #13 pairs fit into a shulker box, one pair per instruction
            if i*13+k >= len(instr):
                break
            items += "{Slot:%db,Count:1b,id:'%s'},"%(k*2  ,instr[i*13+k][offset  ].disc)
            items += "{Slot:%db,Count:1b,id:'%s'},"%(k*2+1,instr[i*13+k][offset+2].disc)
        items = 'Items:[%s],id:"minecraft:shulker_box"'%items[:-1] #remove last comma and add formatting
        shulkers.append(items)
    return shulkers

def FillChest(offset):
    shulkers = FillShulkerBoxes(offset)
    items = ''
    for i in range(len(shulkers)):
        items += '{Slot:%db,Count:1b,id:"minecraft:shulker_box",tag:{BlockEntityTag:{%s}}},'%(i,shulkers[i])
    return items[:-1]

#fileName = "LogisticMap"
fileName = input("Name of file (without suffix): ")

programBINList = list()
for line in open("Programs/%s"%fileName + ".bin", "r"):
    programBINList.append(line.replace(" ",""))

instr = Tokenize()


#0001 0010 0001 0011 1010 0001 0001 0010 = @18 LDA 0r2 0d26
#
#   0001         0010        0001         0011        1010    0001      0001     0010
#addr1-high   addr1-low   addr2-high   addr2-low   imm-low   instr   imm-high   result
schem.setBlock((0, 0,0), "minecraft:chest{Items:[%s]}"%FillChest(1)) #segment 1 and 3 each line
schem.setBlock((0, 9,0), "minecraft:chest{Items:[%s]}"%FillChest(0)) #segment 0 and 2 each line
schem.setBlock((0,18,0), "minecraft:chest{Items:[%s]}"%FillChest(5)) #segment 5 and 7 each line
schem.setBlock((0,27,0), "minecraft:chest{Items:[%s]}"%FillChest(4)) #segment 4 and 6 each line

schem.save( "myschems", "Binary%s" % fileName, mcschematic.Version.JE_1_19_2)