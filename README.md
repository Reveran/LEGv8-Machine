# LEGv8-Machine
 ARM (LEGv8) to Machine binary Translator

## Advice!
 This is **NOT** a compiler, it just generates a simple translation of characters

### Notes

* The Library [*Bitarray*](https://pypi.org/project/bitarray/) is needed, Run: ```pip install bitarray```
* The labels *MUST* be separated from the instructions by tabulations "\t" (as many as you like / need)
* The Instruction parts *MUST* Be separated by *ONE* space " "

    |Labels     |Instructions     |
    |:----------|:----------------|
    |load0		|ADDI X14 XZR #0  |

### Status
* Translate type (R, I, D, B, CB) instructions
* Calculates the address offsets of CB and B instructions
* Uses the *Two's Complement* for negative address offsets

### Still Unimplemented
* Some Uncommon Instructions
* Pseudo-Instructions
* IW/IM Instructions
* Commentss
