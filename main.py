# -*- coding: UTF-8 -*-

import re
import sys
# import cppcheckdata
bracket_count 	= 0
bracket_dict  	= {}
type_trans_count= 0
type_trans_dict = {}
string_count    = 0
string_dict     = {}
CTYPE_LIST = ['short','int','long','float','double','char','void']
class cType:
	isArray  = False
	isStruct = False
	isUnion  = False
	isEnum   = False
	def __init__(self):
		pass

class variable:
	pass

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

	def has_node(self,linkname):
		for s in self.subnode:
			if s[0] == linkname:
				return True
		return False

	def nprint(self,level=0):
		print('|-'*level+self.type+' '+self.value)
		for s in self.subnode:
			print('|-'*level+''+s[0])
			s[1].nprint(level+1)

def get_expression_tree(expression):
	global  bracket_count
	global  bracket_dict
	global  type_trans_count
	global  type_trans_dict
	global  string_dict
	global  string_count
	global  CTYPE_LIST

	expression = expression.strip()#去除空格

	#The num of expression is base on priority of the opt
	exp1_1= re.compile('([^\[]+)\[(.+)\]([^\]]*)')	#[],数组下标
	exp1_2= re.compile('([^\(]*)\((.*)\)([^\)]*)')	#(),括号
	exp1_3= re.compile('(\w+)\.(\w+)')				#.成员选择(对象)
	exp1_4= re.compile('(\w+)->(\w+)')				#->,成员选择(指针)
	exp1_5= re.compile('(.+)\+\+(\W|$)')			#++,后置自增
	exp1_6= re.compile('(.+)--(\W|$)')				#--,后置自减

	exp2_1= re.compile('(\W|^)-([^-=]{1}.*)')		#-,单目运算取负
	exp2_2= re.compile('!([^=]{1}.*)')				#!,逻辑非
	exp2_3= re.compile('~(.+)')						#~,按位取反
	# exp2_4= re.compile('sizeof\((.+)\)')			#sizeof()
	exp2_5= re.compile('([^&]|^)&([^=]{1}.*)')		#&,取地址
	exp2_6= re.compile('(\W|^)--(.+)')				#--,前置自减
	exp2_7= re.compile('(\W|^)\+\+(.+)')			#++,前置自增
	exp2_8= re.compile('(\W|^)\((\w+)\)(.+)')		#强制类型转换

	exp3_1= re.compile('(.+)/([^=]{1}.*)')			#/
	exp3_2= re.compile('(.+)\*([^=]{1}.*)')			#*
	exp3_3= re.compile('(.+)%([^=]{1}.*)')			#%
	exp4_1= re.compile('(.*[^+]{1})\+([^=+]{1}.*)')	#+
	exp4_2=	re.compile('(.*[^-]{1})-([^=\->]{1}.*)')#-
	exp5_1= re.compile('(.+)<<([^=]{1}.*)')			#<<,移位
	exp5_2= re.compile('([^=]{1}.*)>>(.+)')			#>>,移位
	exp6_1= re.compile('(.+)>=(.+)')				#>=,大于等于
	exp6_2= re.compile('([^<]+)<=(.+)')				#<=,小于等于
	exp6_3= re.compile('([^>-]+)>([^>]+)')			#>,大于
	exp6_4= re.compile('([^<]+)<([^<]+)')			#<,小于
	exp7_1= re.compile('(.+)==(.+)')				#==,逻辑等于
	exp7_2= re.compile('(.+)!=(.+)')				#!=,逻辑不等
	exp8  = re.compile('([^&]+)&([^&]+)')			#&,按位与
	exp9  = re.compile('(.+)\^(.+)')				#^,按位异或
	exp10 = re.compile('([^\|]+)\|([^\|]+)')		#|,按位或
	exp11 = re.compile('(.+)&&(.+)')				#&&,逻辑与
	exp12 = re.compile('(.+)\|\|(.+)')				#||,逻辑或
	exp13 = re.compile('(.+)\?(.+):(.+)')			#?:,条件运算符

	exp14_1=re.compile('(.+)/=(.+)')				#/=
	exp14_2=re.compile('(.+)\*=(.+)')				#*=
	exp14_3=re.compile('(.+)%=(.+)')				#%=
	exp14_4=re.compile('(.*[^\+]{1})\+=(.+)')	    #+=
	exp14_5=re.compile('(.*[^-]{1})-=(.+)')			#-=
	exp14_6=re.compile('(.+)<<=(.+)')				#<<=
	exp14_7=re.compile('(.+)>>=(.+)')				#>>=
	exp14_8=re.compile('(.+)&=(.+)')				#&=
	exp14_9=re.compile('(.+)\^=(.+)')				#^=
	exp14_10=re.compile('(.+)\|=(.+)')				#|=
	exp14_11=re.compile('(.*[^<>=]{1})=([^<>=]{1}.*)')#=


	#字符串常量替换
	changed = True
	while changed:
		changed = False
		for i in range(len(expression)):
			s = ''
			if expression[i] == '\"':
				start = i
				i+=1
				while expression[i] != '\"':
					s += expression[i]
					i += 1
				end = i+1
				placeholder = '_string_const_replace_' + str(string_count)
				string_count += 1
				string_dict[placeholder] = ast_node('string',s)
				expression = expression[:start]+placeholder+expression[end:]
				changed = True
				break
			elif expression[i] == '\'':
				start = i
				i+=1
				while expression[i] != '\'':
					s += expression[i]
					i += 1
				end = i+1
				placeholder = '_string_const_replace_' + str(string_count)
				string_count += 1
				string_dict[placeholder] = ast_node('string',s)
				expression = expression[:start]+placeholder+expression[end:]
				changed = True
				break

	#括号,强制类型转换替换
	bracket_list = []
	changed = True
	while changed:
		changed = False
		for i in range(expression.__len__()):
			if expression[i] == '(':
				bracket_list.append((i,'('))
			if expression[i] == ')':
				if bracket_list.__len__()>0:
					start = bracket_list.pop()
					if start[1] == ')':
						#语法出错处理
						print('syntax error')
					else:
						changed = True
						if expression[start[0]+1:i] in CTYPE_LIST:
							#强制类型转换
							placeholder = '_type_trans_replace_' + str(type_trans_count)
							type_trans_count += 1
							type_trans_dict[placeholder] = ast_node('trans_type',expression[start[0]+1:i])
							expression  = expression[:start[0]]+placeholder+expression[i+1:]
						else:
							#普通括号
							placeholder = '_bracket_replace_' + str(bracket_count)
							bracket_count += 1
							bracket_dict[placeholder] = get_expression_tree(expression[start[0]+1:i])
							expression  = expression[:start[0]]+placeholder+expression[i+1:]
						break
				else:
					# 语法出错处理
					print('syntax error')

	if re.match('return (.*)',expression):
		node = ast_node('return','')
		exp_node = get_expression_tree(re.sub('return ','',expression))
		node.add_subnode('exp',exp_node)
		return node
	#变量定义识别
	if re.match('(\w+\s)*\w+\s.+',expression):
		node = ast_node('variable define','')
		explist = expression.split(' ')
		while len(explist)>0:
			exp = explist.pop()
			if exp == 'struct':
				node.add_subnode('para',ast_node('isStruct','true'))
			elif exp == 'enum':
				node.add_subnode('para',ast_node('isEnum','true'))
			elif exp == 'union':
				node.add_subnode('para',ast_node('isUnion','true'))
			elif exp == 'unsigned':
				node.add_subnode('para',ast_node('isUnsigned','true'))
			elif exp == 'static':
				node.add_subnode('para',ast_node('isStatic','true'))
			elif exp == 'const':
				node.add_subnode('para',ast_node('isConst','true'))
			elif exp == 'Entern':
				node.add_subnode('para',ast_node('isEntern','true'))
			elif exp == 'register':
				node.add_subnode('para',ast_node('isRegister','true'))
			elif node.has_node('variablename'):
				node.add_subnode('typename',get_expression_tree(expression.split(' ')[-2]))
			else:
				if re.search('(\w+)\[(\d+)\]',exp):
					rematch = re.search('(\w+)\[(\d+)\]',exp)
					node.add_subnode('para',ast_node('isArray','true'))
					node.add_subnode('para',ast_node('ArraySize',str(rematch.group(2))))
					node.add_subnode('variablename',ast_node('variablename',rematch.group(1)))
				else:
					node.add_subnode('variablename',get_expression_tree(exp))


		return node

	# ,并列表达式
	if re.search(',', expression):
		node = ast_node('parallel', '')
		count = 0
		for exp in expression.split(','):
			count += 1
			node.add_subnode('exp' + str(count), get_expression_tree(exp))
		return node

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
		rematch = re.search(exp6_3,expression)
		node = ast_node('compare',rematch.group())
		node.add_subnode('exp1',get_expression_tree(rematch.group(1)))
		node.add_subnode('exp2',get_expression_tree(rematch.group(2)))
		return node
	elif re.search(exp6_4,expression):
		rematch = re.search(exp6_4,expression)
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



	elif re.search(exp2_1,expression):
		rematch = re.search(exp2_1,expression)
		node = ast_node('negative',rematch.group())
		node.add_subnode('exp',get_expression_tree(rematch.group(2)))
		return node
	elif re.search(exp2_2,expression):
		rematch = re.search(exp2_2,expression)
		node = ast_node('NOT',rematch.group())
		node.add_subnode('exp',get_expression_tree(rematch.group(1)))
		return node
	elif re.search(exp2_3,expression):
		rematch = re.search(exp2_3,expression)
		node = ast_node('~',rematch.group())
		node.add_subnode('exp',get_expression_tree(rematch.group(1)))
		return node
	elif re.search(exp2_5,expression):
		rematch = re.search(exp2_5,expression)
		node = ast_node('address of',rematch.group())
		node.add_subnode('exp',get_expression_tree(rematch.group(2)))
		return node
	elif re.search(exp2_6,expression):
		rematch = re.search(exp2_6,expression)
		node = ast_node('--',rematch.group())
		node.add_subnode('exp',get_expression_tree(rematch.group(1)))
		return node
	elif re.search(exp2_7,expression):
		rematch = re.search(exp2_7,expression)
		node = ast_node('++',rematch.group())
		node.add_subnode('exp',get_expression_tree(rematch.group(1)))
		return node
	elif re.search(exp2_8,expression):
		rematch = re.search(exp2_8,expression)
		node = ast_node('typetrans',rematch.group())
		node.add_subnode('type',get_expression_tree(rematch.group(2)))
		node.add_subnode('exp',get_expression_tree(rematch.group(3)))
		return node

	elif re.search(exp1_1,expression):
		rematch = re.search(exp1_1, expression)
		node = ast_node('get_element', rematch.group())
		node.add_subnode('arr', get_expression_tree(rematch.group(1)))
		node.add_subnode('index', get_expression_tree(rematch.group(2)))
		return node
	elif re.search(exp1_3,expression):
		rematch = re.search(exp1_3, expression)
		node = ast_node('choice_member(object)', rematch.group())
		node.add_subnode('object', get_expression_tree(rematch.group(1)))
		node.add_subnode('member', get_expression_tree(rematch.group(2)))
		return node
	elif re.search(exp1_4,expression):
		rematch = re.search(exp1_4, expression)
		node = ast_node('choice_member(pointer)', rematch.group())
		node.add_subnode('pointer', get_expression_tree(rematch.group(1)))
		node.add_subnode('member', get_expression_tree(rematch.group(2)))
		return node
	elif re.search(exp1_5,expression):
		rematch = re.search(exp1_5, expression)
		node = ast_node('ascend', rematch.group())
		node.add_subnode('exp', get_expression_tree(rematch.group(1)))
		return node
	elif re.search(exp1_6,expression):
		rematch = re.search(exp1_6, expression)
		node = ast_node('descend', rematch.group())
		node.add_subnode('exp', get_expression_tree(rematch.group(1)))
		return node

	#sizeof()
	elif re.match('sizeof(_bracket_replace_\d+)', expression):
		bracket_name = re.match('sizeof(_bracket_replace_\d+)', expression).group(1)
		if bracket_dict.__contains__(bracket_name):
			node = ast_node('sizeof','')
			node.add_subnode('exp',bracket_dict[bracket_name])
			return node
		else:
			return ast_node('variable', expression)

	#funciton call
	elif re.match('(\w+)(_bracket_replace_\d+)',expression):
		rematch = re.match('(\w+)(_bracket_replace_\d+)',expression)
		bracket_name = rematch.group(2)
		if bracket_dict.__contains__(bracket_name):
			node = ast_node('function_call','')
			node.add_subnode('function',get_expression_tree(rematch.group(1)))
			if bracket_dict[bracket_name] != None:
				node.add_subnode('parameters',bracket_dict[bracket_name])
			return node
		else:
			return ast_node('variable', expression)

	#普通括号
	elif re.match('_bracket_replace_\d+',expression):
		if bracket_dict.__contains__(expression):
			return bracket_dict[expression]
		else:
			return ast_node('variable', expression)

	elif re.match('_string_const_replace_\d+',expression):
		if string_dict.__contains__(expression):
			return string_dict[expression]
		else:
			return ast_node('variable',expression)
	#强制类型转换
	elif re.match('(_type_trans_replace_\d+)(.*)',expression):
		rematch = re.match('(_type_trans_replace_\d+)(.*)',expression)
		if type_trans_dict.__contains__(rematch.group(1)):
			node = type_trans_dict[rematch.group(1)]
			node.add_subnode('exp',get_expression_tree(rematch.group(2)))
			return node
		else:
			return ast_node('variable', expression)
	elif re.match('break',expression):
		return ast_node('break','')
	elif re.match('continue',expression):
		return ast_node('continue','')
	#常量
	elif re.match('\d+', expression):
		return ast_node('constant', expression)
	elif expression.__len__() <= 0:
		return None
	else:
		return ast_node('variable',expression)


'''
去掉注释,换行符,制表符,和不必要的空格
'''
def kill_space(block):
	note_index=[]
	#标记注释
	for i in range(len(block)):
		start = 0
		end   = 0
		if re.match('//',block[i:i+2]):
			start = i
			while block[i] != '\n' and i < block.__len__():
				i += 1
			end = i
			note_index.append((start,end))
		elif re.match('/\*',block[i:i+2]):
			start = i
			while not re.match('\*/', block[i:i+2]):
				i += 1
			end = i + 1
			note_index.append((start,end))

	#删除注释
	while note_index.__len__() > 0:
		start,end = note_index.pop()
		block = block[:start]+block[end+1:]

	block = re.sub('\t|\n',' ',block)#换行符和制表符替换为空格

	#清除多余的空格
	finish = False
	while not finish:
		finish = True
		i=0
		while i < block.__len__():
			if block[i] == ' ':
				if re.match('\w|\d|&|\*',block[i-1]) and re.match('[^\w\d&\*]',block[i+1]):
					block = block[:i]+block[i+1:]
					finish = False
				elif re.match('[^\w\d&\*]',block[i-1]) and re.match('\w|\d|&|\*',block[i+1]):
					block = block[:i] + block[i + 1:]
					finish = False
				elif re.match('\'|\"',block[i-1]) or re.match('\"|\'',block[i+1]):
					block = block[:i] + block[i + 1:]
					finish = False
				elif re.match('{|}',block[i+1]) or re.match('{|}',block[i-1]):
					block = block[:i] + block[i + 1:]
					finish = False
				elif re.match('\(',block[i+1]) or re.match('\)',block[i-1]):
					block = block[:i] + block[i + 1:]
					finish = False
				elif re.match('\[',block[i+1]) or re.match('\]',block[i-1]):
					block = block[:i] + block[i + 1:]
					finish = False
			i+=1

	return block

'''
解析switch语句{}中的部分,返回AST节点列表
'''
def get_switch_node(switch_body):
	result = []
	pattern1 = re.compile('case (\d+):(.*?break;)')
	pattern2 = re.compile('default:(.*break;)')

	for m in re.findall(pattern1,switch_body):
		case_node = ast_node('case','')
		case_node.add_subnode('condition_value',ast_node('exp',m[0]))
		case_node.add_subnode('condition_body',get_block_tree(m[1],'codeblock'))
		result.append(case_node)

	for m in re.findall(pattern2,switch_body):
		case_node = ast_node('default', '')
		case_node.add_subnode('body', get_block_tree(m,'codeblock'))
		result.append(case_node)

	return result



'''
get_block_tree()
为代码块生成AST节点
	输入:代码块,代码块名
	输出:AST根节点
'''
def get_block_tree(block,blockname='root'):
	'''
	生成括号对照词典，保存括号配对信息
	'''
	parenthesis_stack = [] #()
	bracket_stack     = [] #[]
	brace_stack       = [] #{}
	bracket_dict      = {} #all of theme
	for i in range(block.__len__()):
		# print(block[i])
		if block[i] == '(':
			parenthesis_stack.append((i,'('))
		elif block[i] == ')':
			if parenthesis_stack.__len__() <= 0 or parenthesis_stack[-1][1] != '(':
				pass
			else:
				match = parenthesis_stack.pop()
				bracket_dict[match[0]] = i
				bracket_dict[i] = match[0]

		if block[i] == '[':
			bracket_stack.append((i,'['))
		elif block[i] == ']':
			if bracket_stack.__len__() <= 0 or bracket_stack[-1][1] != '[':
				pass
			else:
				match = bracket_stack.pop()
				bracket_dict[match[0]] = i
				bracket_dict[i] = match[0]

		if block[i] == '{':
			brace_stack.append((i,'{'))
		elif block[i] == '}':
			if brace_stack.__len__() <= 0 or brace_stack[-1][1] != '{':
				pass
			else:
				match = brace_stack.pop()
				bracket_dict[match[0]] = i
				bracket_dict[i] = match[0]

	'''
	开始分析
	'''
	expression = ''
	expression_count = 0
	root_node = ast_node(blockname,'')
	i = 0
	while i < len(block):
		# print('expression:'+expression)
		# print('block[i]:'+block[i])
		# print('-------------------')

		#if语句
		if block[i] == '(' and expression == 'if':
			#条件语句
			ifnode = ast_node('ifnode','')
			condition_end = bracket_dict[i]
			condition = block[i+1:condition_end]
			condition_node = get_expression_tree(condition)
			ifnode.add_subnode('condition',condition_node)
			i = condition_end + 1

			#if块内语句
			ifblockbody = ''
			#正常if语句,有{}
			if block[i] == '{':
				ifblock_end = bracket_dict[i]
				ifblockbody = block[i+1:ifblock_end]
				i = ifblock_end + 1
			#单行if语句的情况，不检查本身的语法问题
			else:
				while i < len(block):
					ifblockbody += block[i]
					if block[i] == ';':
						break
					i += 1
				i += 1
			ifblock_node = get_block_tree(ifblockbody,'ifbody')
			ifnode.add_subnode('ifbody',ifblock_node)


			#匹配else块
			while i < block.__len__():
				if block[i:i+7] == 'else if':
					i+=7
					assert block[i] == '('
					else_condition=block[i+1:bracket_dict[i]]
					i=bracket_dict[i]+1

				elif block[i:i+4] == 'else':
					else_condition=None
					i+=4
				else:
					i += 1
					continue

				elseblock=''
				if block[i] == '{':
					#有{}
					elsebody_end = bracket_dict[i]
					elseblock = block[i+1:elsebody_end]
					i = elsebody_end + 1
				else:
					while i < len(block):
						elseblock += block[i]
						if block[i] == ';':
							break
						i += 1
				elseblock_node = get_block_tree(elseblock,'elsebody')
				if else_condition != None:
					elseblock_node.add_subnode('condition',get_expression_tree(else_condition))
				ifnode.add_subnode('elsebody',elseblock_node)

			root_node.add_subnode('if', ifnode)
			expression = ''

		#检索匹配while代码块
		elif block[i] == '(' and re.match('\s*while',expression):
			whilenode = ast_node('while','')
			condition_end = bracket_dict[i]
			condition = block[i+1:condition_end]
			i = condition_end + 1
			while_condition_node = get_expression_tree(condition)
			whilenode.add_subnode('condition',while_condition_node)

			circlebody = ''
			if block[i] == '{':
				#有{}
				circle_end = bracket_dict[i]
				circlebody = block[i+1:circle_end]
				i = circle_end + 1
			else:
				while i < len(block):
					i += 1
					if block[i] != ';':
						circlebody += block[i]
					else:
						break
				i += 1
			circle_node = get_block_tree(circlebody,'circlebody')
			whilenode.add_subnode('circle',circle_node)
			root_node.add_subnode('while',whilenode)
			expression = ''

		#检索匹配for代码块
		elif block[i] == '(' and re.match('\s*for',expression):
			fornode = ast_node('for', '')
			for_end = bracket_dict[i]
			condition = block[i+1:for_end]
			i = for_end + 1
			condition = condition.split(';')
			for_condition_node1 = get_expression_tree(condition[0])
			for_condition_node2 = get_expression_tree(condition[1])
			for_condition_node3 = get_expression_tree(condition[2])
			fornode.add_subnode('condition_init', for_condition_node1)
			fornode.add_subnode('condition_end', for_condition_node2)
			fornode.add_subnode('condition_iteration', for_condition_node3)

			#循环体
			circlebody = ''
			if block[i] == '{':
				# 有{}
				circle_end = bracket_dict[i]
				circlebody = block[i+1:circle_end]
				i = circle_end + 1
			else:
				while i < len(block):
					i += 1
					if block[i] != ';':
						circlebody += block[i]
					else:
						break
				i += 1

			circle_node = get_block_tree(circlebody, 'circlebody')
			fornode.add_subnode('circle', circle_node)
			root_node.add_subnode('for', fornode)
			expression = ''

		#switch代码块
		elif block[i] == '(' and expression == 'switch':
			switch_node = ast_node('switch','')
			switch_condition_end = bracket_dict[i]
			switch_condition = block[i+1:switch_condition_end]
			switch_node.add_subnode('condition',get_expression_tree(switch_condition))

			i = switch_condition_end + 1
			switch_body_end = bracket_dict[i]
			switch_body = block[i+1:switch_body_end]
			switch_node_list = get_switch_node(switch_body)
			for node in switch_node_list:
				switch_node.add_subnode('case',node)
			root_node.add_subnode('switch',switch_node)
			expression = ''
			i = switch_body_end+1
		#普通语句
		elif block[i] == ';':
			# print('get expression:'+expression)
			expression_node = get_expression_tree(expression)
			root_node.add_subnode('exp'+str(expression_count),expression_node)
			expression = ''
			expression_count += 1
			i += 1

		#读入字符
		else:
			expression += block[i]
			i += 1
	return root_node

def get_func_node(funcbody):
	print(funcbody)
	for i in range(funcbody.__len__()):
		if funcbody[i] == "{":
			start = i
			break
	for i in range(funcbody.__len__())[::-1]:
		if funcbody[i] == "}":
			end = i
			break
	funcname = funcbody[:start]
	funcbody = funcbody[start+1:end]

	funcbodynode = get_block_tree(funcbody,'')
	return (funcname,funcbodynode)

if __name__ == '__main__':
	# demo = sys.argv[1]
	file=open('function.c')
	funcbody=file.read()
	funcbody = kill_space(funcbody)

	result = get_func_node(funcbody)
	print(result[0])
	result[1].nprint()