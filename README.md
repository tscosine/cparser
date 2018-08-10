# cparser

##Introduction
Get AST and the list of functioncall and variable from C code

##AST Node

|节点类型|子节点(链接类型)|子节点(节点类型)|对应c表达式
|-----|-----|-----|-----|
|cblock| | |c代码块
|expression| | |c表达式
|if|condition|expression|if-else
| |ifbody|cblock| |
| |else*|else| |
|else|condition|expression|if-else
| |elsebody|cblock|
|while|condition|expression|while
| |loop|cblock| |
|for|condition_init|expression|for
| |condition_end|expression| |
| |condition_iteration|expression| |
| |loop|cblock| |
|switch|condition|expression|switch-case
| |case|case| |
|case|condition*|expression|switch-case
| | body|cblock|
|try|body|cblock|try-catch|
| |catch|catch| |
|catch|exception|expression|try-catch
| |body|cblock|

##Expression
...
##AST function
###astnode.funccall_list()
返回调用函数列表
###astnode.variable_list()
返回变量定义列表
###astnode.feature()
返回特征化序列

##Other function
###cparse.get_func_node(funcbody)
返回AST根节点