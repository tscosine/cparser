import re
class ast_node:
	type = ''
	value = ''
	subnode = []
	def __init__(self,type,value):
		self.value=value
		self.type=type
		self.subnode = []

	def add_subnode(self,linkname,subnode):
		self.subnode.append([linkname,subnode])

	def nprint(self,level=0):
		print '|-'*level+self.type+' '+self.value
		for s in self.subnode:
			print '|-'*level+s[0]
			s[1].nprint(level+1)

def get_expression_tree(expression):
	print expression
	#The num of expression is base on priority of the opt
	exp1  = re.compile('[\d+]|\.|->|\w+\+\+|\w+--')
	exp2  = re.compile('\+\+|--|\*|&|!|~|sizeof')
	exp3_1= re.compile('(.+)/([^=]{1}.*)')
	exp3_2= re.compile('(.+)\*([^=]{1}.*)')
	exp3_3= re.compile('(.+)%([^=]{1}.*)')
	exp4_1= re.compile('(.*[^+]{1})\+([^=+]{1}.*)')
	exp4_2=	re.compile('(.*[^-]{1})-([^=-]{1}.*)')
	exp5_1= re.compile('(.+)<<([^=]{1}.*)')
	exp5_2= re.compile('([^=]{1}.*)>>(.+)')
	exp6_1= re.compile('(.+)>=(.+)')
	exp6_2= re.compile('([^<]+)<=(.+)')
	exp6_3= re.compile('([^>]+)>([^>]+)')
	exp6_4= re.compile('([^<]+)<([^<]+)')
	exp7_1= re.compile('(.+)==(.+)')
	exp7_2= re.compile('(.+)!=(.+)')
	exp8  = re.compile('([^&]+)&([^&]+)')
	exp9  = re.compile('(.+)\^(.+)')
	exp10 = re.compile('([^\|]+)\|([^\|]+)')
	exp11 = re.compile('(.+)&&(.+)')
	exp12 = re.compile('(.+)\|\|(.+)')
	exp13 = re.compile('(.+)\?(.+):(.+)')

	exp14_1=re.compile('(.+)/=(.+)')
	exp14_2=re.compile('(.+)\*=(.+)')
	exp14_3=re.compile('(.+)%=(.+)')
	exp14_4=re.compile('(.+)\+=(.+)')
	exp14_5=re.compile('(.+)-=(.+)')
	exp14_6=re.compile('(.+)<<=(.+)')
	exp14_7=re.compile('(.+)>>=(.+)')
	exp14_8=re.compile('(.+)&=(.+)')
	exp14_9=re.compile('(.+)\^=(.+)')
	exp14_10=re.compile('(.+)\|=(.+)')
	exp14_11=re.compile('(.*[^<>=]{1})=([^<>=]{1}.*)')

	if re.search(exp13,expression):
		rematch = re.search(exp13,expression)
		node = ast_node('conditional_opt',rematch.group())
		node.add_subnode('conditon',get_expression_tree(rematch.group(1)))
		node.add_subnode('op1',get_expression_tree(rematch.group(2)))
		node.add_subnode('op2',get_expression_tree(rematch.group(3)))
		return node

	elif re.search(exp14_1,expression):
		rematch = re.search(exp14_1,expression)
		node = ast_node('assign',rematch.group())
		node.add_subnode('left',get_expression_tree(rematch.group(1)))
		node.add_subnode('right',get_expression_tree(rematch.group(2)))
		return node
	elif re.search(exp14_2,expression):
		rematch = re.search(exp14_2,expression)
		node = ast_node('assign',rematch.group())
		node.add_subnode('left',get_expression_tree(rematch.group(1)))
		node.add_subnode('right',get_expression_tree(rematch.group(2)))
		return node
	elif re.search(exp14_3,expression):
		rematch = re.search(exp14_3,expression)
		node = ast_node('assign',rematch.group())
		node.add_subnode('left',get_expression_tree(rematch.group(1)))
		node.add_subnode('right',get_expression_tree(rematch.group(2)))
		return node
	elif re.search(exp14_4,expression):
		rematch = re.search(exp14_4,expression)
		node = ast_node('assign',rematch.group())
		node.add_subnode('left',get_expression_tree(rematch.group(1)))
		node.add_subnode('right',get_expression_tree(rematch.group(2)))
		return node
	elif re.search(exp14_5,expression):
		rematch = re.search(exp14_5,expression)
		node = ast_node('assign',rematch.group())
		node.add_subnode('left',get_expression_tree(rematch.group(1)))
		node.add_subnode('right',get_expression_tree(rematch.group(2)))
		return node
	elif re.search(exp14_6,expression):
		rematch = re.search(exp14_6,expression)
		node = ast_node('assign',rematch.group())
		node.add_subnode('left',get_expression_tree(rematch.group(1)))
		node.add_subnode('right',get_expression_tree(rematch.group(2)))
		return node
	elif re.search(exp14_7,expression):
		rematch = re.search(exp14_7,expression)
		node = ast_node('assign',rematch.group())
		node.add_subnode('left',get_expression_tree(rematch.group(1)))
		node.add_subnode('right',get_expression_tree(rematch.group(2)))
		return node
	elif re.search(exp14_8,expression):
		rematch = re.search(exp14_8,expression)
		node = ast_node('assign',rematch.group())
		node.add_subnode('left',get_expression_tree(rematch.group(1)))
		node.add_subnode('right',get_expression_tree(rematch.group(2)))
		return node
	elif re.search(exp14_9,expression):
		rematch = re.search(exp14_9,expression)
		node = ast_node('assign',rematch.group())
		node.add_subnode('left',get_expression_tree(rematch.group(1)))
		node.add_subnode('right',get_expression_tree(rematch.group(2)))
		return node
	elif re.search(exp14_10,expression):
		rematch = re.search(exp14_10,expression)
		node = ast_node('assign',rematch.group())
		node.add_subnode('left',get_expression_tree(rematch.group(1)))
		node.add_subnode('right',get_expression_tree(rematch.group(2)))
		return node
	elif re.search(exp14_11,expression):
		rematch = re.search(exp14_11,expression)
		node = ast_node('assign',rematch.group())
		node.add_subnode('left',get_expression_tree(rematch.group(1)))
		node.add_subnode('right',get_expression_tree(rematch.group(2)))
		return node

	elif re.search(exp12,expression):
		rematch = re.search(exp12,expression)
		node = ast_node('OR',rematch.group())
		node.add_subnode('exp1',get_expression_tree(rematch.group(1)))
		node.add_subnode('exp2',get_expression_tree(rematch.group(2)))
		return node

	elif re.search(exp11,expression):
		rematch = re.search(exp11, expression)
		node = ast_node('AND', rematch.group())
		node.add_subnode('exp1', get_expression_tree(rematch.group(1)))
		node.add_subnode('exp2', get_expression_tree(rematch.group(2)))
		return node

	elif re.search(exp10,expression):
		rematch = re.search(exp10, expression)
		node = ast_node('OR_bit', rematch.group())
		node.add_subnode('exp1', get_expression_tree(rematch.group(1)))
		node.add_subnode('exp2', get_expression_tree(rematch.group(2)))
		return node

	elif re.search(exp9,expression):
		rematch = re.search(exp9,expression)
		node = ast_node('XOR',rematch.group())
		node.add_subnode('exp1',get_expression_tree(rematch.group(1)))
		node.add_subnode('exp2',get_expression_tree(rematch.group(2)))
		return node

	elif re.search(exp8,expression):
		rematch = re.search(exp8,expression)
		node = ast_node('AND_bit',rematch.group())
		node.add_subnode('exp1',get_expression_tree(rematch.group(1)))
		node.add_subnode('exp2',get_expression_tree(rematch.group(2)))
		return node

	elif re.search(exp7_1,expression):
		rematch = re.search(exp7_1,expression)
		node = ast_node('equal',rematch.group())
		node.add_subnode('exp1',get_expression_tree(rematch.group(1)))
		node.add_subnode('exp2',get_expression_tree(rematch.group(2)))
		return node
	elif re.search(exp7_2,expression):
		rematch = re.search(exp7_2,expression)
		node = ast_node('not equal',rematch.group())
		node.add_subnode('exp1',get_expression_tree(rematch.group(1)))
		node.add_subnode('exp2',get_expression_tree(rematch.group(2)))
		return node

	elif re.search(exp6_1,expression):
		rematch = re.search(exp6_1,expression)
		node = ast_node('compare',rematch.group())
		node.add_subnode('exp1',get_expression_tree(rematch.group(1)))
		node.add_subnode('exp2',get_expression_tree(rematch.group(2)))
		return node
	elif re.search(exp6_2,expression):
		rematch = re.search(exp6_2,expression)
		node = ast_node('compare',rematch.group())
		node.add_subnode('exp1',get_expression_tree(rematch.group(1)))
		node.add_subnode('exp2',get_expression_tree(rematch.group(2)))
		return node
	elif re.search(exp6_3,expression):
		rematch = re.search(exp6_2,expression)
		node = ast_node('compare',rematch.group())
		node.add_subnode('exp1',get_expression_tree(rematch.group(1)))
		node.add_subnode('exp2',get_expression_tree(rematch.group(2)))
		return node
	elif re.search(exp6_4,expression):
		rematch = re.search(exp6_2,expression)
		node = ast_node('compare',rematch.group())
		node.add_subnode('exp1',get_expression_tree(rematch.group(1)))
		node.add_subnode('exp2',get_expression_tree(rematch.group(2)))
		return node

	elif re.search(exp5_1,expression):
		rematch = re.search(exp5_1,expression)
		node = ast_node('shift',rematch.group())
		node.add_subnode('exp1',get_expression_tree(rematch.group(1)))
		node.add_subnode('exp2',get_expression_tree(rematch.group(2)))
		return node
	elif re.search(exp5_2,expression):
		rematch = re.search(exp5_2,expression)
		node = ast_node('shift',rematch.group())
		node.add_subnode('exp1',get_expression_tree(rematch.group(1)))
		node.add_subnode('exp2',get_expression_tree(rematch.group(2)))
		return node

	elif re.search(exp4_1,expression):
		rematch = re.search(exp4_1,expression)
		node = ast_node('add',rematch.group())
		node.add_subnode('exp1',get_expression_tree(rematch.group(1)))
		node.add_subnode('exp2',get_expression_tree(rematch.group(2)))
		return node
	elif re.search(exp4_2,expression):
		rematch = re.search(exp4_2,expression)
		node = ast_node('reduce',rematch.group())
		node.add_subnode('exp1',get_expression_tree(rematch.group(1)))
		node.add_subnode('exp2',get_expression_tree(rematch.group(2)))
		return node

	elif re.search(exp3_1,expression):
		rematch = re.search(exp3_1,expression)
		node = ast_node('except',rematch.group())
		node.add_subnode('exp1',get_expression_tree(rematch.group(1)))
		node.add_subnode('exp2',get_expression_tree(rematch.group(2)))
		return node
	elif re.search(exp3_2,expression):
		rematch = re.search(exp3_2,expression)
		node = ast_node('ride',rematch.group())
		node.add_subnode('exp1',get_expression_tree(rematch.group(1)))
		node.add_subnode('exp2',get_expression_tree(rematch.group(2)))
		return node
	elif re.search(exp3_3,expression):
		rematch = re.search(exp3_3,expression)
		node = ast_node('remainder',rematch.group())
		node.add_subnode('exp1',get_expression_tree(rematch.group(1)))
		node.add_subnode('exp2',get_expression_tree(rematch.group(2)))
		return node
	else:
		if re.match('\d+',expression):
			return ast_node('constant',expression)
		else:
			return ast_node('variable',expression)

def get_token(funcbody):
	tokenlist = []
	token = ''
	end_token = ['{','}','(',')',';','']
	status = 0
	for i in range(len(funcbody)):
		if status == 0:
			if funcbody[i] in end_token:
				tokenlist.append(token)
				tokenlist.append(funcbody[i])
				token = ''
				i += 1
			elif re.match('\s',funcbody[i]):
				tokenlist.append(token)
				token = ''
				i += 1
			elif funcbody[i] == '\"':
				tokenlist.append(token)
				status = 1
				token = '\"'
				i += 1
			else:
				token += funcbody[i]
				i += 1	
		
		elif status == 1:
			if funcbody[i] == '\"':
				status = 0
				token += funcbody[i]
				tokenlist.append(token)
				token = ''
				i += 1
			else:
				token += funcbody[i]					

	return tokenlist
if __name__ == '__main__': 
	demo = 'a%=1'
	root = get_expression_tree(demo)
	root.nprint()