# -*- coding: UTF-8 -*-

import re
import sys
# import cppcheckdata
bracket_count 	= 0
bracket_dict  	= {}
type_trans_count= 0
type_trans_dict = {}
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

	def nprint(self,level=0):
		print '|-'*level+self.type+' '+self.value
		for s in self.subnode:
			print '|-'*level+s[0]
			s[1].nprint(level+1)


def get_expression_tree(expression):
	global  bracket_count
	global  bracket_dict
	global  type_trans_count
	global  type_trans_dict
	global  CTYPE_LIST
	# print expression
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
	exp14_4=re.compile('(.+)\+=(.+)')				#+=
	exp14_5=re.compile('(.+)-=(.+)')				#-=
	exp14_6=re.compile('(.+)<<=(.+)')				#<<=
	exp14_7=re.compile('(.+)>>=(.+)')				#>>=
	exp14_8=re.compile('(.+)&=(.+)')				#&=
	exp14_9=re.compile('(.+)\^=(.+)')				#^=
	exp14_10=re.compile('(.+)\|=(.+)')				#|=
	exp14_11=re.compile('(.*[^<>=]{1})=([^<>=]{1}.*)')#=


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
				else:
					# 语法出错处理
					print 'syntax error'
				if start[1] == ')':
					#语法出错处理
					print 'syntax error'
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

	elif re.match('sizeof(_bracket_replace_\d+)', expression):
		bracket_name = re.match('sizeof(_bracket_replace_\d+)', expression).group(1)
		if bracket_dict.has_key(bracket_name):
			node = ast_node('sizeof','')
			node.add_subnode('exp',bracket_dict[bracket_name])
			return node
		else:
			return ast_node('variable', expression)

	elif re.match('_bracket_replace_\d+',expression):
		if bracket_dict.has_key(expression):
			return bracket_dict[expression]
		else:
			return ast_node('variable', expression)

	elif re.match('(_type_trans_replace_\d+)(.*)',expression):
		rematch = re.match('(_type_trans_replace_\d+)(.*)',expression)
		if type_trans_dict.has_key(rematch.group(1)):
			node = type_trans_dict[rematch.group(1)]
			node.add_subnode('exp',get_expression_tree(rematch.group(2)))
			return node
		else:
			return ast_node('variable', expression)

	elif re.match('\d+', expression):
		return ast_node('constant', expression)

	else:
		return ast_node('variable',expression)

def get_token(funcbody):
	tokenlist = []
	token = ''
	end_token = ['{','}','(',')',';']
	status = 0
	for i in range(len(funcbody)):
		if status == 0:
			if funcbody[i] in end_token:
				if not re.match('\s',token):
					print 'get a token:'+token
					tokenlist.append(token)

				print 'get a end_token:'+funcbody[i]
				tokenlist.append(funcbody[i])
				token = ''
				i += 1
			elif re.match('\s',funcbody[i]):
				if not re.match('\s',token):
					print 'get a token:'+token
					tokenlist.append(token)
					token = ''
				i += 1
			elif funcbody[i] == '\"':
				if not re.match('\s',token):
					print 'get a token:'+token
					tokenlist.append(token)

				print 'turn tp status 1'
				status = 1
				token = '\"'
				i += 1
			else:
				print 'read:'+funcbody[i]
				token += funcbody[i]
				i += 1	
		
		elif status == 1:
			#读字符串
			if funcbody[i] == '\"':
				print 'get token:'+token
				print 'turn to status 0'
				status = 0
				token += funcbody[i]
				tokenlist.append(token)
				token = ''
				i += 1
			else:
				print 'read str'
				token += funcbody[i]					
		elif status == 2:
			#读字符串
			pass
		elif status == 3:
			#读注释
			pass
	return tokenlist
if __name__ == '__main__':
	demo = sys.argv[1]
	# demo = '(int)(a+b)+sizeof(c)'
	# demo = 'a->b'
	root = get_expression_tree(demo)
	root.nprint()