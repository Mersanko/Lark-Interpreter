'''CANONIGO, MERSAN JR. S. BSCS 4 2018-5830'''
from lark import Lark, Transformer, v_args


calc_grammar = """
        ?start: exp 
                | NAME ":=" exp             -> assign_var 
        ?exp: term
                | exp "+" term              -> add
                | exp "-" term              -> sub

        ?term: factor
                | factor "*" term           -> mul
                | factor "/" term           -> div

        ?factor: SIGNED_NUMBER              -> number
                | NAME                      -> var1
                | factor "^" factor         -> pow
                | "(" exp ")"
                
                
                
        %import common.CNAME                -> NAME
        %import common.SIGNED_NUMBER 
        %import common.WS_INLINE

        %ignore WS_INLINE                    
    """


@v_args(inline=True)   
class CalculateTree(Transformer):
    from operator import add, sub, mul, truediv as div
    number = float

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
    
    def pow(self,base,exponent):
        return base**exponent
        

calc_parser = Lark(calc_grammar, parser='lalr',transformer=CalculateTree())
calc = calc_parser.parse


def main():
    while True:
        try:
            input_string = input('> ')
            if input_string == "exit":
                quit()
        except EOFError:
            break
        print(calc(input_string))


if __name__ == '__main__':
    main()
