#include <stdio.h>

// Flag to check if Program has ended
unsigned char running = 1;

// A and B Register, 0bAAAABBBB
unsigned char regs = 0;
// Temporary Regs Register
unsigned char tempRegs = 0;
// Flags, 0bxxxxxxCZ
unsigned char flags = 0;

// Currently executing Instruction
unsigned char instruction = 0;
// Remaining Clockcycles for the current instruction
unsigned char instRemaining = 0;
// Clockcycles each Instruction takes
unsigned char instCycles[16] = {1,2,4,4,1,1,1,1,1,1,1,1,1,4,4,4};

// Program Counter
unsigned int pc = 0;
// Memory, 2^12 Nibbles
unsigned char mem[4096];
// Pointer for Memory Addressing
unsigned int point = 0;

// Checks if Accumulator is 0, if it is, Zero Flag goes high
int updateZeroFlag() {
	if (regs >> 4 == 0) {
		flags = flags | 0b00000001;
	} else {
		flags = flags & 0b00000010;
	}
	return 0;
}

int main(int argc, char *argv[]) {
	// Load ROM
	FILE *romFile = fopen(argv[argc-1], "rb"); // read only 
 
	// test for files not existing. 
	if (romFile == NULL) 
	{   
		printf("Error! Could not open file\n"); 
		return 1; 
	}  else {
		int i;
		for (i = 0; i < 4096; i++) {
			mem[i] = fgetc(romFile);	
		}
		fclose(romFile);
	}
	
	// Actual Program Loop
	while (running) {
		// Loop Memory
		if (pc >= 4096) {
			pc -= 4096;
		}
		// *** Start of Clockcycle ***
		if (instRemaining>0) { // Check if Instruction has finished
			// If not, resume loading data, dependant on the instruction
			switch(instruction) {
				case 0: // NOP | No Operation
					break;
				case 1: // LDA n | Load Number into A
					regs = regs & 0b00001111;
					regs = regs | (mem[pc]<<4);
					break;
				case 2: // LDA (m) | Load Contents of Memory into A
					switch (instRemaining) {
						case 3:
							point = 0; // Reset point, just in case
							point = point | mem[pc]<<8;
							break;
						case 2:
							point = point | mem[pc]<<4;
							break;
						case 1:
							point = point | mem[pc];
							regs = regs & 0b00001111;
							regs = regs | (mem[point]<<4);
							break;
					}
					break;
				case 3: // STA (m) | Load Contents of A into Memory
					switch (instRemaining) {
						case 3:
							point = 0; // Reset point, just in case
							point = point | mem[pc]<<8;
							break;
						case 2:
							point = point | mem[pc]<<4;
							break;
						case 1:
							point = point | mem[pc];
							mem[point] = regs>>4;
							break;
					}
					break;
				case 4: // SWAP | Swap the Contents of A and B
					tempRegs = regs; 
					regs = tempRegs << 4;
					regs = regs | tempRegs >> 4;
					break;
				case 5: // SHFT | Shift A Left, Shifts Leftmost Bit into Carry
					flags = flags & 0b00000001; // Clear Carry Flag
					if (regs >> 7 == 1) {
						flags = flags | 0b00000010; // Set Carry Flag if leftmost bit of A is 1
					}
					tempRegs = regs & 0b11110000; // Remove B to avoid errors
					tempRegs = regs << 1; // Perform Shift
					regs = regs & 0b00001111; // Remove A from Regs
					regs = regs | tempRegs; // Recombine Regs
					break;					
				case 6: // ADD | Add A with B, load result into A
					tempRegs = regs & 0b00001111; // Put contents of B into tempRegs
					regs = regs & 0b11110000;     // 
					regs = regs >> 4;             // Put contents of A into regs
					regs = regs + tempRegs;  	  // A + B
					// Set Carry 
					flags = flags & 0b00000001; // Clear Carry Flag
					if (regs >> 4 == 1) {
						flags = flags | 0b00000010; // Set Carry Flag if leftmost bit of A is 1
					}
					// Reassemble the Register
					regs = regs << 4; 			  // Put back in A Register
					regs = regs | tempRegs;		// Re-add B
					break;
				case 7: // SUB | Subtract B from A, Result in A <- Probably Broken
					tempRegs = regs & 0b00001111; // Put contents of B into tempRegs
					regs = regs & 0b11110000;     // 
					regs = regs >> 4;             // Put contents of A into regs
					regs = regs - tempRegs;  	  // A - B
					// Reassemble the Register
					regs = regs << 4; 			  // Put back in A Register
					regs = regs | tempRegs;		// Re-add B
					break;
				case 8: // AND | AND A with B, Result in A
					tempRegs = regs & 0b00001111; // Put contents of B into tempRegs
					regs = regs & 0b11110000;     // 
					regs = regs >> 4;             // Put contents of A into regs
					regs = regs & tempRegs;  	  // A & B
					// Reassemble the Register
					regs = regs << 4; 			  // Put back in A Register
					regs = regs | tempRegs;		// Re-add B
					break;
				case 9: // OR | OR A with B, Result in A
					tempRegs = regs & 0b00001111; // Put contents of B into tempRegs
					regs = regs & 0b11110000;     // 
					regs = regs >> 4;             // Put contents of A into regs
					regs = regs | tempRegs;  	  // A & B
					// Reassemble the Register
					regs = regs << 4; 			  // Put back in A Register
					regs = regs | tempRegs;		// Re-add B
					break;
				case 10: // XOR | XOR A with B, Result in A
					tempRegs = regs & 0b00001111; // Put contents of B into tempRegs
					regs = regs & 0b11110000;     // 
					regs = regs >> 4;             // Put contents of A into regs
					regs = regs ^ tempRegs;  	  // A & B
					// Reassemble the Register
					regs = regs << 4; 			  // Put back in A Register
					regs = regs | tempRegs;		// Re-add B
					break;
				case 11: // IN | Wait for Input until Interrupt, load IO-Bus into AB
					regs = getchar();
					break;
				case 12: // OUT | Output AB onto IO-Bus until Acknowledged
					printf("%c",regs);
					break;
				case 13: // JP m | Unconditional Jump
					switch (instRemaining) {
						case 3:
							point = 0; // Reset point, just in case
							point = point | mem[pc]<<8;
							break;
						case 2:
							point = point | mem[pc]<<4;
							break;
						case 1:
							point = point | mem[pc];
							pc = point-1;
							break;
					}
					break;
				case 14: // JPC m | Conditional Jump, if Carry = 1, jump  
					switch (instRemaining) {
						case 3:
							point = 0; // Reset point, just in case
							point = point | mem[pc]<<8;
							break;
						case 2:
							point = point | mem[pc]<<4;
							break;
						case 1:
							point = point | mem[pc];
							if (flags >> 1 == 1) { 
								pc = point-1;
							}
							break;
					}
					break;
				case 15: // JPZ m | Conditional Jump, if Zero = 1, jump  
					switch (instRemaining) {
						case 3:
							point = 0; // Reset point, just in case
							point = point | mem[pc]<<8;
							break;
						case 2:
							point = point | mem[pc]<<4;
							break;
						case 1:
							point = point | mem[pc];
							if (flags & 1 == 1) { 
								pc = point-1;
							}
							break;
					}
					break;
			}
			instRemaining = instRemaining - 1;
			pc = pc + 1;
		} else { // If it has, load/execute new Instruction
			//printf("A:%X B:%X | PC: %X\n", regs>>4, regs & 0b00001111, pc);
			instruction = mem[pc];
			switch (instruction) {
				case 0: // NOP | No Operation
					instRemaining = instCycles[0];
					break;
				case 1: // LDA n | Load Number into A
					instRemaining = instCycles[1];
					break;
				case 2: // LDA (m) | Load Contents of Memory into A
					instRemaining = instCycles[2];
					break;
				case 3: // STA (m) | Load Contents of A into Memory
					instRemaining = instCycles[3];
					break;
				case 4: // SWAP | Swap the Contents of A and B
					instRemaining = instCycles[4];
					break;
				case 5: // SHFT | Shift A Left, Shifts Leftmost Bit into Carry
					instRemaining = instCycles[5];
					break;
				case 6: // ADD | Add A with B, load result into A
					instRemaining = instCycles[6];
					break;
				case 7: // SUB | Subtract B from A, Result in A
					instRemaining = instCycles[7];
					break;
				case 8: // AND | AND A with B, Result in A
					instRemaining = instCycles[8];
					break;
				case 9: // OR | OR A with B, Result in A
					instRemaining = instCycles[9];
					break;
				case 10: // XOR | XOR A with B, Result in A
					instRemaining = instCycles[10];
					break;
				case 11: // IN | Wait for Input until Interrupt, load IO-Bus into AB
					instRemaining = instCycles[11];
					break;
				case 12: // OUT | Output AB onto IO-Bus until Acknowledged
					instRemaining = instCycles[12];
					break;
				case 13: // JP m | Unconditional Jump
					instRemaining = instCycles[13];
					break;
				case 14: // JPC m | Conditional Jump, if Carry = 1, jump  
					instRemaining = instCycles[14];
					break;
				case 15: // JPZ m | Conditional Jump, if Zero = 1, jump       
					instRemaining = instCycles[15];
					break;
				case 16: 
					running = 0;
					break;
			}
		}
		
		// *** End of Clockcycle ***
		updateZeroFlag();
	}
	return 0;
}