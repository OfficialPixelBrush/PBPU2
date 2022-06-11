; "Hello, world!" Program
:hello
STR Hello
; Cool shiz
:mem
LDAM hello
SWAP
:memX
LDAM hello+1
OUT
; Load Pointer Address into A
LDAN 0x1 ; Load 1 into B
SWAP
LDAM mem+3 ; Load Location of Pointer into A
ADD 	  ; Increment A by 1
STA mem+3
LDAM memX+3 ; Load Location of Pointer 2 into A
ADD 	  ; Increment A by 1
STA memX+3
JP mem