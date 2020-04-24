# LEGv8-Machine
 ARM (LEGv8) to Machine binary Translator

## Advice!
 This is **NOT** a compiler, it just generates a simple translation of characters

### Notes

* The labels MUST be separated from the instructions by tabulations "\t" (as many as you like/need)
* Las partes de cada instrucción (OpCode, Rd, Rn, etc.); deben estar separadas por solo 1 espacio espacio

### Status
* Translate tipe (R, I, D, B, CB) instructions
* Calculates the address offsets of CB and B instructions
* Uses the *Two's Complement* for negative address offsets

### Still Unimplemented
* Some Uncomon Instructions
* Pseudo-Instructions
* IW/IM Instructions
* Commentss
