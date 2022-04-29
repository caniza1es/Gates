import ctypes

def val(id):
	return ctypes.cast(id,ctypes.py_object).value

def toForm(A,txt):
	if txt[0] == '-':
		if txt[1] not in A.outputs.keys():
			A.inputs[txt[1]] = I(0)
			alpha = A.inputs[txt[1]]
		else:
			alpha = A.outputs[txt[1]]
		return NOT(alpha)
	elif txt[1] not in ['&','+','-']:
		if txt[0] not in A.outputs.keys():
			A.inputs[txt[0]] = I(0)
			return O(A.inputs[txt[0]])
	elif txt[1] == '&':
		if txt[0] not in A.outputs.keys():
			A.inputs[txt[0]] = I(0)
			alpha = A.inputs[txt[0]]
		else:
			alpha = A.outputs[txt[0]]
		if txt[2] not in A.outputs.keys():
			A.inputs[txt[2]] = I(0)
			beta = A.inputs[txt[2]]
		else:
			beta = A.outputs[txt[2]]
		return AND(alpha,beta)
	elif txt[1] == '+':
		if txt[0] not in A.outputs.keys():
			A.inputs[txt[0]] = I(0)
			alpha = A.inputs[txt[0]]
		else:
			alpha = A.outputs[txt[0]]
		if txt[2] not in A.outputs.keys():
			A.inputs[txt[2]] = I(0)
			beta = A.inputs[txt[2]]
		else:
			beta = A.outputs[txt[2]]
		return OR(alpha,beta)

class CIRCUIT:
	def __init__(self,definition):
		self.text = definition
		self.inputs = {}
		self.outputs = {}
		self.define()
	def define(self):
		forms = self.text.split(',')
		for sub in forms:
			sf = sub.split('=')[0]
			self.outputs[sub[-1]] = toForm(self,sf)
	def display(self):
		print("INPUTS")
		for key in self.inputs:
			print(key,':',bool(self.inputs[key]))
		print("OUTPUTS")
		for key in self.outputs:
			print(key,':',bool(self.outputs[key]))
	def C(self,key):
		self.inputs[key].C()


class I:
	def __init__(self,val):
		self.val = bool(val)
	def __bool__(self):
		return self.val
	def C(self):
		self.val = not self.val

class O:
	def __init__(self,val):
		self.a = id(val)
	def __bool__(self):
		return bool(val(self.a))

class AND:
	def __init__(self,l,r):
		self.p = id(l)
		self.q = id(r)
	def __bool__(self):
		return bool(val(self.p)) & bool(val(self.q))

class OR:
	def __init__(self,l,r):
		self.p = id(l)
		self.q = id(r)
	def __bool__(self):
		return bool(val(self.p)) | bool(val(self.q))

class XOR:
	def __init__(self,l,r):
		self.p = id(l)
		self.q = id(r)
	def __bool__(self):
		return bool(val(self.p)) ^ bool(val(self.q))

class NOT:
	def __init__(self,val):
		self.a = id(val)
	def __bool__(self):
		return not bool(val(self.a))

NAND = CIRCUIT("P&Q=Z,-Z=U")
NAND.display()
NAND.C('P')
NAND.C('Q')
NAND.display()
