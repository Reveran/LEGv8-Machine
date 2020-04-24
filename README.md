# LEGv8-Machine
 ARM (LEGv8) to Machine binary Translator

## Advice!
 This is **NOT** a compiler, it just generates a simple translation of characters

### Notes

* The labels MUST be separated from the instructions by tabulations "\t" (as many as you like/need)
* Las partes de cada instrucción (OpCode, Rd, Rn, etc.); deben estar separadas por solo 1 espacio espacio

### Status
* Translate type (R, I, D, B, CB) instructions
* Calculates the address offsets of CB and B instructions
* Uses the *Two's Complement* for negative address offsets

### Still Unimplemented
* Some Uncomon Instructions
* Pseudo-Instructions
* IW/IM Instructions
* Commentss


|Labels     |Instructions     |
|:----------|:----------------|
|			|ADDI X14 XZR #0  |
|while0		|SUB X9 X19 X20   |
|			|CBZ X9 endwhile0 |
|			|ADDI X19 X19 #1  |
|			|B while0         |
|endwhile0	|ADD X0 X19 XZR   |