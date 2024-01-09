import mcschematic #python 3.9.7 64-bit interpreter necessary, I don't understand why
schem = mcschematic.MCSchematic()

title = "LogisticMap"
prgm = open("Programs/%s"%title + ".bin", "r")
discs = ("minecraft:stick","minecraft:music_disc_13","minecraft:music_disc_cat","minecraft:music_disc_blocks","minecraft:music_disc_chirp","minecraft:music_disc_far","minecraft:music_disc_mall","minecraft:music_disc_mellohi","minecraft:music_disc_stal","minecraft:music_disc_strad","minecraft:music_disc_ward","minecraft:music_disc_11","minecraft:music_disc_wait","minecraft:music_disc_pigstep","minecraft:music_disc_otherside","minecraft:music_disc_5")

#file opens are weird, easy fix
prgmList = list()
for line in prgm:
    prgmList.append(line.replace(" ",""))

#i don't know how to do this properly, since cast to int didn't worok
def parseBin(str):
    if str == '0':
        return 0
    return 1

#takes 4bit string and returns its decimal value
def FourBitBinToDec(num):
    return parseBin(num[0])*8 + parseBin(num[1])*4 + parseBin(num[2])*2 + parseBin(num[3])*1

#takes in line string and returns
def LineToDiscs(line,slotStart, offset):
    items = ""
    val = FourBitBinToDec(line[4*offset:4*offset+4])
    items += "{Slot:%db,Count:1b,id:'%s'},"%(slotStart,discs[val])
    val = FourBitBinToDec(line[4*offset+8:4*offset+12])
    items += "{Slot:%db,Count:1b,id:'%s'},"%(slotStart+1,discs[val])
    return items

#fills shulker boxes up to slot 24 (divisible by 2, fits 12 lines)
def FillShulkerBoxes(offset):
    shulkers = list()
    for i in range(1+(len(prgmList)*2)//24):
        items = 'Items:['
        for k in range(12):
            if i*12+k >= len(prgmList):
                break
            items += LineToDiscs(prgmList[i*12+k],k*2,offset)
        items = items[:-1]
        items += '],id:"minecraft:shulker_box"'
        shulkers.append(items)
    return shulkers

#self explanatory
def FillChest(offset):
    shulkers = FillShulkerBoxes(offset)
    items = ''
    for i in range(len(shulkers)):
        items += '{Slot:%db,Count:1b,id:"minecraft:shulker_box",tag:{BlockEntityTag:{%s}}},'%(i,shulkers[i])
    items = items[:-1]
    return items

schem.setBlock((0, 0,0), "minecraft:chest{Items:[%s]}"%FillChest(1))
schem.setBlock((0, 9,0), "minecraft:chest{Items:[%s]}"%FillChest(0))
schem.setBlock((0,18,0), "minecraft:chest{Items:[%s]}"%FillChest(5))
schem.setBlock((0,27,0), "minecraft:chest{Items:[%s]}"%FillChest(4))

schem.save( "myschems", "Binary%s" % title, mcschematic.Version.JE_1_19_2)