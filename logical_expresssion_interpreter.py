from lark import Lark, Transformer, v_args

'''CANONIGO, MERSAN JR. S. 2018-2830'''
'''I have added assignment expression sir'''
lexp_grammar = """
    ?start: lexp
        | NAME ":=" lexp        -> assign_var 
    ?lexp: lexp "|" conj        -> logical_or 
        | conj

    ?conj: conj "&" lval        -> logical_and
        | lval

    ?lval: val
        | "!" lval              -> logical_not

    ?val: "T"                   -> true
    | "F"                       -> false
    | NAME                      -> var
    | "(" lexp ")"      

    %import common.CNAME        -> NAME
    %import common.WS_INLINE
    %ignore WS_INLINE
    """ 

@v_args(inline=True)
class logicalExpression(Transformer):
    def __init__(self):
        self.vars = {}
        
    def assign_var(self, name, value):
        self.vars[name] = value
        return value

    def var(self, name):
        try:
            return self.vars[name]
        except KeyError:
            return "Variable not found: {}".format(name)
        
    def logical_or(self, lexp, conj):
        return eval(str(lexp)) or eval(str(conj))
    
    def logical_and(self, conj, lval):
        return eval(str(conj)) and eval(str(lval))
    
    def logical_not(self,lval):
        return not(eval(str(lval)))
    
    def true(self):
        return True
    
    def false(self):
        return False 
    

lexp_parser = Lark(lexp_grammar, parser='lalr',transformer=logicalExpression())
lexp = lexp_parser.parse


def main():
    while True:
        try:
            input_string = input('eval> ')
            if input_string == "exit":
                quit()
            else:
                print(lexp(input_string))
        except:
            print("INVALID INPUT STRING")
        

if __name__ == '__main__':
    main()
