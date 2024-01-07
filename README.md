ADDING THE WORLD TO MINECRAFT:
1. Locate your Minecraft directory
    Windows: Search for "%APPDATA%\.minecraft" in the search bar
    macOS: Search for "~/Library/Application Support/minecraft"
    Linux: "~/.minecraft" where "~" refers to the home directory
    More information can be found on the Minecraft Wiki: https://minecraft.wiki/w/.minecraft
2. Locate the "saves" folder
3. Download the world file, ending in ".rar"
4. Extract the folder within into the "saves" folder
5. The world should now appear in your Singleplayer worlds list


USING THE ASSEMBLER:
Note: The current version is not very user-friendly and requires editing the code to change the file name
1. Verify that the assembly code is in the folder called "Programs" in the same directory as the "assembler.py" file
2. Open the "assembler.py" file in any text editor
3. Locate the variable "fileName" and change its value to the name of the target file, without the suffix ".txt"
4. Run the "assembler.py"
5. The binary file should appear in the same "Programs" folder with the ".bin" suffix


LOADING A PROGRAM INTO MEMORY FROM A BINARY FILE:
Note: The current version is not very user-friendly and requires editing the code to change the file name
Note: This program requires the python module "mcschematic" and python version 3.9.7, any other versions may not work
Note: To use the generated schematics, the mod "Litematica" (Video Guide: https://www.youtube.com/watch?v=KFzyNtyN8qI) is required
1. Verify that the binary file is in the folder called "Programs" in the same directory as the "assembler.py" file
2. Open the "BinarySchem.py" file in any text editor
3. Locate the variable "title" and change its value to the name of the target file, without the suffix ".bin"
4. Run the "BinarySchem.py"
5. The schematic file should appear in the "myschems" folder with the ".schem" suffix
6. Locate the Minecraft directory as shown above and open the "schematics" folder 
7. Move/copy the schematic file into the "schematic" folder and any subfolders as desired
8. Locate the disc reader (tall, thin structure next to the control panel, the only structure using pistons, hoppers, droppers and command blocks)
9. Load the schematic file and place the lowest chest on the lowest free hopper in the disc reader
10. Right-click the lever at the bottom of the disc reader exactly once to arm the system
11. Add a power source (typically a redstone block or a lever) behind the comparator on the gray concrete floor
12. If using the "carpet" mod, feel free to set the tick rate to 200 (usually the highest it will actually run at) with "/tick rate 200"
13. Wait for the redstone lamps at the output of the disc reader to stop changing and all be off
14. The byte at location zero, i.e. 0b0 will be overridden to a value of zero and must be manually entered
    The value can be located in the ".bin" file as the third byte (two groups of four) in the first row
15. Run the program from the control panel


USING THE CONTROL PANEL:
Note: Each interface part is given in order from left to right
1. The Output lamps on the left side display the output. When I/O is toggled off, it will show the data of where the program counter is pointing to, else it shows the output at the address of the address byte.
2. The I/O switch controls whether the data and address set on the right panel are fed into RAM.
3. The Reset PC button sets the program counter to zero.
4. The PULSE Updt button writes the data set on the right panel into RAM.
5. The Clock On/Off switch turns the clock on or off, i.e. runs the CPU.
6. The Clock cycle button runs the clock for exactly one cycle.
7. The Address lamps give the address in RAM for both the Input and the Output lamps.
8. The Input lamps set the input at the address pointed to by the Address lamps.


INSTRUCTION SET:
Note: A, B and X are assumed to be registers, while I is an immediate formed by A and B, where B is the higher and A the lower valued half of the byte
Note: The Flags column indicates whether the flags register is updated during the operation.
Note: A must always be an even numbered register, while B must always be odd numbered.

    Instr. Result A   B      Flags  Opcode  Description
    LDA    X      I          no     0001    Loads I into Register X
    STR    X      I          no     0010    Stores Register X into Address I
    MOV    X      A   or B   no     0011    Moves Register A/B into X
    ADD    X      A      B   yes    0100    Adds A and B into X
    SUB    X      A      B   yes    0101    Subtracts B from A into X
    INC    X      A   or B   yes    0110    Increments A/B into X
    DEC    X      A   or B   yes    0111    Decrements A/B into X
    AND    X      A      B   yes    1000    Binary AND A and B into X
    ORA    X      A      B   yes    1001    Binary OR A and B into X
    NOT    X      A          yes    1010    Binary NOT A/B into X
    BSL    X      A   or B   yes    1011    Bit-shift-left A/B into X
    BSR    X      A   or B   yes    1100    Bit-shift-right A/B into X
    JMP           A   or B   no     1101    Jumps to instruction at A or B
    JIN           A   or B   no     1110    Jumps to instruction at A or B if negative flag
    JIZ           A   or B   no     1111    Jumps to instruction at A or B if zero flag


ENCODING AN INSTRUCTION:
Note: Instructions are always built up of two bytes. The first, lower byte includes A and the Opcode in that order, and the second, higher byte includes B and the Result.
Note: When inputting the instruction, the first byte is always in an even numbered address and the second byte right after it.
Note: The registers addresses from 1 to 14.
Some examples:
    ADD 0r2 0r2 0r3 encodes as 0010 0100 for the first byte and 0011 0010 for the second byte
    LDA 0r2 0d154 encodes as 1010 0001 for the first byte and 1001 0010 for the second byte
    JMP 0r5 encodes as 0000 1101 for the first byte and 0101 0000 for the second byte
