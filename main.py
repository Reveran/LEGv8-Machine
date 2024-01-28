from bitarray import bitarray
from bitarray.util import int2ba
from re import sub

typeR = {"ADD", "SUB", "AND", "ORR", "EOR"}
typeR2 = {"LSL", "LSR"}
typeI = {"ADDI", "SUBI", "ANDI", "ORRI", "EORI"}
typeD = {"LDUR", "STUR"}
typeB = {"B", "BL"}
typeCB = {"CBZ", "CBNZ", "B.EQ", "B.NE", "B.LT", "B.LE", "B.GT", "B.GE"}
typeIM = {"MOVZ", "MOVK"}

inst = {
	"ADD" : "10001011000",
	"SUB" : "11001011000",
	"AND" : "10001010000", 
	"ORR" : "10101010000", 
	"EOR" : "11001010000",

	"ADDI" : "1001000100",
	"SUBI" : "1101000100",
	"ANDI" : "1001001000",
	"ORRI" : "1011001000",
	"EORI" : "1101001000",

	"LDUR" : "11111000010",
	"STUR" : "11111000000",

	"B" : "000101",
	"BL" : "100101",

	"CBZ" : "10110100",
	"CBNZ" : "10110101",
	"B." : "01010100",

	"MOVZ" : "110100101",
	"MOVK" : "111100101"
}

reg = {
	"X0" : "00000",	"X1" : "00001",	"X2" : "00010",	"X3" : "00011",	"X4" : "00100",
	"X5" : "00101",	"X6" : "00110",	"X7" : "00111",	"X8" : "01000",	"X9" : "01001",
	"X10" : "01010", "X11" : "01011", "X12" : "01100", "X13" : "01101",	"X14" : "01110",
	"X15" : "01111", "X16" : "10000", "X17" : "10001", "X18" : "10010",	"X19" : "10011",
	"X20" : "10100", "X21" : "10101", "X22" : "10110", "X23" : "10111",	"X24" : "11000",
	"X25" : "11001", "X26" : "11010", "X27" : "11011", "X28" : "11100",	"X29" : "11101",
	"X30" : "11110", "X31" : "11111",
	"XZR" : "11111", "SP" : "11100", "FP" : "11101", "LR" : "11110", "IP0" : "10000", "IP1" : "10001",
}

cond = 	{
	"EQ" : "00000",
	"NE" : "00001",
	"LT" : "00011",
	"LE" : "01101",
	"GT" : "01100",
	"GE" : "01010"
}

entrada = open("input.txt", "r")
tags = {}
for x,line in enumerate(entrada):
	if line.split("	")[0] != "":
		tags[line.split("	")[0]] = x

entrada.seek(0)

def clean(line):
	
	# Remove "//" and all text after it
    line = sub(r'\s*//.*', '', line)

    # Remove "[" and "]"
    line = sub(r'[\[\]]', '', line)
    
    # Remove semicolons
    line = line.replace(':', '	')

	# Remove commas
    line = line.replace(',', '')

    return line
	
class Instruccion():
	def __init__(self, line, pos):
		self.tag = line.split("	")[0]
		self.s = line.split("	")[-1].split(" ")
		self.pos = pos
		self.normalize()
		self.type = self.setType()
		self.opcode = self.setOPcode()
		self.LSL = self.setLSL()
		self.Rd = self.setRd()
		self.Rn = self.setRn()
		self.Rm = self.setRm()
		self.ShIn = self.setShIn()
		self.machine = self.build()

	def normalize(self):
		tmp = self.s[-1]
		if tmp[-1:] == "\n":
			self.s[-1] = tmp[:-1]

	def setType(self):
		tmp = self.s[0]
		if tmp in typeR:
			return("R")
		elif tmp in typeR2:
			return("R2")
		elif tmp in typeI:
			return("I")
		elif tmp in typeD:
			return("D")
		elif tmp in typeB:
			return("B")
		elif tmp in typeCB:
			return("CB")
		elif tmp in typeIM:
			return("IM")
	def setOPcode(self):
		if self.type == "CB" and self.s[0][:2] == "B.":
			return inst.get(self.s[0][:2]) 
		return inst.get(self.s[0])
	def setLSL(self):
		if self.type == "IM":
			return format(int(self.s[3][1:]), '02b')
		return ""
	def setRd(self):
		if self.type == "CB" and self.s[0][2:] in cond:
			return cond.get(self.s[0][2:])
		if self.type != "B":
			return reg.get(self.s[1])
	def setRn(self):
		if self.type != "B" and self.type != "CB":
			return reg.get(self.s[2])
		return ""
	def setRm(self):
		if self.type == "R":
			return reg.get(self.s[3])
	def setShIn(self):
		tmp = "000000"
		if self.type == "R2" or self.type == "I":
			tmp = bin(int(self.s[3][1:]))[2:]
			if self.type == "R2":
				while len(tmp) < 6:
					tmp = "0" + tmp
			elif self.type == "I":	
				while len(tmp) < 12:
					tmp = "0" + tmp
		
		elif self.type == "D":
			add = int(self.s[-1][1:])
			if add < 0:
				tmp = int((~ int2ba(-add, 9)).to01(), 2)
				tmp = tmp + 1
				tmp = int2ba(tmp, 9)
			else:
				tmp = int2ba(add, 9)
			tmp = str(tmp)[10:-2]

		elif self.type == "B" or self.type == "CB":
			jmp = 0
			tmp = bitarray()
			size = 19
			if self.type == "B":
				size = 26		
			jmp = tags[self.s[-1]] - self.pos
			if jmp < 0:
				tmp = int((~ int2ba(-jmp, size)).to01(), 2)
				tmp = tmp + 1
				tmp = int2ba(tmp, size)
			else:
				tmp = int2ba(jmp, size)
			tmp = str(tmp)[10:-2]

		elif self.type == "IM":
			size = 16
			tpm = bitarray()
			tmp = int2ba(int(self.s[2][1:]), size)
			tmp = str(tmp)[10:-2]
		return tmp
	
	def build(self):
		a = ""
		if self.type == "R" or self.type == "R2":
			a = self.opcode + self.Rm + self.ShIn + self.Rn + self.Rd
		elif self.type == "I":
			a = self.opcode + self.ShIn + self.Rn + self.Rd
		elif self.type == "D":
			a = self.opcode + self.ShIn + "00" + self.Rn + self.Rd
		elif self.type == "B":
			a = self.opcode + self.ShIn
		elif self.type == "CB":
			a = self.opcode + self.ShIn + self.Rd
		elif self.type == "IM":
			a= self.opcode + self.LSL + self.ShIn + self.Rd 
		return(a)

salida = open("output.txt", "w")
for pos,line in enumerate(entrada):
	line = clean(line)
	if(len(line)>3):
		salida.write("32'b" + Instruccion(line, pos).machine + ","+ "\n")
salida.close()
entrada.close()