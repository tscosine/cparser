# cparser

## Introduction
Get AST and the list of functioncall and variable from C code

## AST Node

|编号|节点类型|子节点(链接类型)|子节点(节点类型)|对应c表达式
|---|-----|-----|-----|-----|
|00|cblock| | |c代码块
|01|expression| | |c表达式
|02|if|condition|expression|if-else
| | |ifbody|cblock| |
| | |else*|else| |
|03|else|condition|expression|if-else
| | |elsebody|cblock|
|04|while|condition|expression|while
| | |loop|cblock| |
|06|for|condition_init|expression|for
| | |condition_end|expression| |
| | |condition_iteration|expression| |
| | |loop|cblock| |
|07|switch|condition|expression|switch-case
| | |case|case| |
|08|case|condition*|expression|switch-case
| | | body|cblock|
|09|try|body|cblock|try-catch|
| | |catch|catch| |
|10|catch|exception|expression|try-catch
| | |body|cblock|

## Expression
|编号|表达式|nodetype
|---|---|---|
11|=|assign
12|丨=|assign_or
13|^=|assign_xor
14|&=|assign_and
15|>>=|assign_shift
16|<<=|assign_shift
17|-=|assign_reduce
18|+=|assign_add
19|%=|assign_remain
20|*=|assign_mult
21|/=|assign_except
22|?:|conditional_opt
23|丨丨|or
24|&&|and
25|丨|or_bit
26|^|xor
27|a&b|and_bit
28|!=|equal
29|==|not_equal
30|<|compare
31|\>|compare
32|<=|compare
33|\>=|compare
34|\>\>|shift
35|<<|shift
36|-|reduce
37|+|add
38|*|mult
39|/|except
40|%|remain
41|(int)|typetrans
42|++a|++
43|--a|--
44|&a|address_of
45|sizeof()|sizeof
46|-|negative
47|!|not
48|~|~
49|a--|descend
50|a++|ascend
51|->|choice_member(pointer)
52|.|choice_member(object)
53|[]|get_element
54|return|return
55|goto|goto
56|变量定义|variable_define
| |变量定义参数|isStruct
| |变量定义参数|isEnum
| |变量定义参数|isUnion
| |变量定义参数|isUnsigned
| |变量定义参数|isStatic
| |变量定义参数|isConst
| |变量定义参数|isEntern
| |变量定义参数|isRegister
| |变量定义参数|isArray
| |,|parallel
57|函数调用|function_call
58|变量|variable
59|break|break
60|continue|continue
61|常量|constant
62|字符串|string

## AST function
### astnode.funccall_list()
返回调用函数列表
### astnode.variable_list()
返回变量定义列表
### astnode.feature()
返回特征化序列

## Other function
### cparse.get_func_node(funcbody)
返回AST根节点
