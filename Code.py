class Code:
	@staticmethod
	def dest(mnem):
		if mnem == None:
			return "000"
			
		s = ""

		if 'A' in mnem:
			s += '1'
		else:
			s += '0'

		if 'D' in mnem:
			s += '1'
		else:
			s += '0'

		if 'M' in mnem:
			s += '1'
		else:
			s += '0'

		return s

	@staticmethod
	def comp(mnem):
		if ('A' in mnem) and ('M' in mnem):
			raise CodeError("Cannot have both A and M in a computation.")

		s = ""

		if 'A' in mnem:
			s += "0"
			mnem = mnem.replace('A', 'X')
		elif 'M' in mnem:
			s += "1"
			mnem = mnem.replace('M', 'X')
		else:
			s += "0"
		
		if "0" == mnem:
			s += "101010"
		elif "1" == mnem:
			s += "111111"
		elif "-1" == mnem:
			s += "111010"
		elif "D" == mnem:
			s += "001100"
		elif "X" == mnem:
			s += "110000"
		elif "!D" == mnem:
			s += "001101"
		elif "!X" == mnem:
			s += "110001"
		elif "-D" == mnem:
			s += "001111"
		elif "-X" == mnem:
			s += "110011"
		elif "D+1" == mnem:
			s += "011111"
		elif "X+1" == mnem:
			s += "110111"
		elif "D-1" == mnem:
			s += "001110"
		elif "X-1" == mnem:
			s += "110010"
		elif "D+X" == mnem:
			s += "000010"
		elif "D-X" == mnem:
			s += "010011"
		elif "X-D" == mnem:
			s += "000111"
		elif "D&X" == mnem:
			s += "000000"
		elif "D|X" == mnem:
			s += "010101"
		else:
			raise CodeError("Invalid computation code.")

		return s


	@staticmethod
	def jump(mnem):
		if mnem == None:
			return "000"
		elif "JGT" == mnem:
			return "001"
		elif "JEQ" == mnem:
			return "010"
		elif "JGE" == mnem:
			return "011"
		elif "JLT" == mnem:
			return "100"
		elif "JNE" == mnem:
			return "101"
		elif "JLE" == mnem:
			return "110"
		elif "JMP" == mnem:
			return "111"
		else:
			raise CodeError("Invalid jump code.")

class CodeError(Exception):
	def __init__(self, sstr):
		self.val = sstr

	def __str__(self):
		print ':', self.val
		