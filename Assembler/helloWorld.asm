; "Hello, world!" Program
STR Hello
; Cool shiz
LDAM 0x0
SWAP
LDAM 0x1
OUT
; Load Pointer Address into A
LDAN 0x1 ; Load 1 into B
SWAP
LDAM 0x13 ; Load Location of Pointer into A
ADD 	  ; Increment A by 1
STA 0x13
LDAM 0x18 ; Load Location of Pointer 2 into A
ADD 	  ; Increment A by 1
STA 0x18
JP 0x10