# PBPU2
A 4-Bit Fantasy CPU with basic I/O.
 
 ### Registers
| Letter | Name            | Size  |
|:------:|:--------------- |:-----:|
|   A    | **A**ccumulator | 4-Bit |
|   B    | **B**-Register  | 4-Bit |

A and B can be used together for Input/Output

### Flags
| Letter | Name  |
|:------:|:----- |
|   C    | Carry | 
|   Z    | Zero  |
 
### Instructions
| Num | Mnemonic   | Description                                                               | Size |
|:---:|:---------- |:------------------------------------------------------------------------- |:----:|
|  0  | NOP        | No Operation                                                              |  1   |
|  1  | LDAN num   | Load Number into A                                                        |  2   |
|  2  | LDAM (mem) | Load Contents of Memory into A                                            |  4   |
|  3  | STA (mem)  | Load Contents of A into Memory                                            |  4   |
|  4  | SWAP       | Swap the Contents of A and B                                              |  1   |
|  5  | SHFT       | Shift A Left, Shifts Leftmost Bit into Carry                              |  1   |
|  6  | ADD        | Add A with B, load result into A, Carry exists                            |  1   |
|  7  | SUB        | Subtract B from A, Result in A, Borrow doesn't exist                      |  1   |
|  8  | AND        | AND A with B, Result in A                                                 |  1   |
|  9  | OR         | OR A with B, Result in A                                                  |  1   |
|  A  | XOR        | XOR A with B, Result in A                                                 |  1   |
|  B  | IN         | Wait for Input until Interrupt, load IO-Bus into AB (Can be used as HALT) |  1   |
|  C  | OUT        | Output AB onto IO-Bus until Acknowledged                                  |  1   |
|  D  | JP  mem    | Unconditional Jump                                                        |  4   |
|  E  | JPC mem    | Conditional Jump, if Carry = 1, jump                                      |  4   |
|  F  | JPZ mem    | Conditional Jump, if Zero = 1, jump                                       |  4   |

### Memory
2^(3x4), aka 2^12
4096x4 Address Space
