from Parser import *
from Code import *
from SymbolTable import *

class Assembler:
	def __init__(self, filename):
		i = filename.find('.')

		if i != -1:
			self.filename = filename[:i]
		else:
			self.filename = filename

		self.p = Parser(filename)
		self.buff = []
		self.ops = []
		self.table = SymbolTable()

	def assemble(self):
		self.__firstpass()
		self.p.reset()
		self.__secondpass()

	def __firstpass(self):
		addrcnt = 0

		while self.p.hasMoreCmds():
			if self.p.cmdType() == self.p.L_CMD:
				label = self.p.sym()
				if self.table.contains(label) == False:
					self.table.addEntry(label, addrcnt)
			else:
				addrcnt += 1

			self.p.advance()

	def __secondpass(self):
		varcnt = 0x10

		while self.p.hasMoreCmds():
			raw = ""
			if self.p.cmdType() == self.p.A_CMD:
				self.ops.append(self.p.getCurrent())
				label = self.p.sym()
				raw += "0"
				val = 0

				if label.isdigit() == False:
					if self.table.contains(label) == False:
						self.table.addEntry(label, varcnt)
						varcnt += 1 
					val = self.table.getAddress(label)
				else:
					val = int(label)

				s = bin(val)[2:]
				raw += -len(s) % 15 * '0' + s
				self.buff.append(raw)

			elif self.p.cmdType() == self.p.C_CMD:
				self.ops.append(self.p.getCurrent())
				raw = "111" + Code.comp(self.p.comp()) + Code.dest(self.p.dest()) + Code.jump(self.p.jump())
				self.buff.append(raw)

			self.p.advance()

	def output(self):
		i = 0
		print "Raw Machine Code..."
		for inst in self.buff:
			print  '%0*X:'%(4, i), inst, '|', self.ops[i]
			i += 1

	def writetofile(self):
		f = open(str(self.filename + ".hack"), 'w')
		for item in self.buff:
			f.write("%s\n"%item)
