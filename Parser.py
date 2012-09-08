
class Parser:
	A_CMD = 0
	C_CMD = 1
	L_CMD = 2

	ALPHABET = ['D', 'M', 'A', '0', '1', '!', '+', '-', '|', '&', '=', ';',
				'J', 'E', 'M', 'Q', 'N', 'G', 'L', 'T', 'P']
	JUMPABET = ["JEQ", "JMP", "JNE", "JLT", "JGT", "JGE", "JLE"]

	def __init__(self, infile):
		self.cmds = []
		self.index = 0

		for line in (open(infile, 'r')):
			i = line.find("//")
			newstr = ""

			if i != -1:
				newstr += line[:i]
			else:
				newstr += line

			nowhite = "".join(newstr.split())

			if len(nowhite) > 0:
				self.cmds.append(nowhite)

	def hasMoreCmds(self):
		return self.index < len(self.cmds)

	def advance(self):
		self.index += 1

	def reset(self):
		self.index = 0

	def getCurrent(self):
		if not self.hasMoreCmds(): 
			return None
		return self.cmds[self.index]

	def cmdType(self):
		curr = self.getCurrent()

		if curr[0] == '@':
			return self.A_CMD
		elif set([i in self.ALPHABET for i in curr]) == set([True]):
			return self.C_CMD
		elif (curr[0] == '(') and (curr.find(')') != -1):
			return self.L_CMD
		else:
			raise ParseError("Invalid command type.")

	def sym(self):
		if self.cmdType() == self.C_CMD:
			return None

		curr = self.getCurrent()
		symbol = ""
		if self.cmdType() == self.L_CMD:
			symbol += curr[1:curr.find(')')]
		else:
			symbol += curr[1:]

		digits = [chr(i+0x30) for i in range(10)]
		lowers = [chr(i+0x61) for i in range(26)]
		uppers = [chr(i+0x41) for i in range(26)]
		specials = ['.', '$', ':', '_']

		if (symbol[0] in digits) and (self.cmdType() == self.L_CMD):
			raise ParseError("A label cannot be a number.")

		for n in symbol:
			if n not in digits\
			and n not in lowers\
			and n not in uppers\
			and n not in specials:
				raise ParseError(str("Symbol cannot contain the following character: " + n))

		return symbol

	def dest(self):
		c = self.getCurrent()
		if '=' not in c:
			return None

		s = ""
		i = 0

		while c[i] != '=':
			if c[i] not in self.ALPHABET[:3]:
				raise ParseError("Destination field can only consist of D, M, and A.")
			if i > 3:
				raise ParseError("Destination field can be no more than 3 characters.")

			s += c[i]
			i += 1

		return s

	def comp(self):
		if self.cmdType() != self.C_CMD:
			return None
			
		c = self.getCurrent()
		i = c.find('=')
		j = c.find(';')
		s = ""

		if i == -1 and j == -1:
			s = c
			return s
		elif i == -1:
			s += "".join([c[n] for n in range(j)])
			return s
		elif j == -1:
			s += c[i+1:]
			return s
		else:
			s = c[i:j]
			return s

	def jump(self):
		c = self.getCurrent()
		i = c.find(';')
		if i == -1:
			return None

		s = c[i+1:]
		if s not in self.JUMPABET:
			print s
			raise ParseError("Not a valid jump instruction.")

		return s


class ParseError(Exception):
	def __init__(self, sstr):
		self.val = sstr

	def __str__(self):
		print ':', self.val