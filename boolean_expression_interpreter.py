'''CANONIGO, MERSAN JR. S. BSCS 4 2018-5830'''
from lark import Lark, Transformer, v_args
import operator

bexp_grammar = """

   
    ?start: bexp

    ?bexp: bterm
        | bexp "||" bterm                               -> or_

    ?bterm: notfactor
        | bterm "&&" notfactor                         -> and_
        

    ?notfactor: bfactor
        | "!" bfactor                                  -> not_

    ?bfactor: bliteral 
        | bident 
        | rexp

    ?rexp: nexp
        |nexp ">" nexp                                      -> gt
        | nexp "<"  nexp                                   -> lt
        | nexp "==" nexp                                   -> eq
    
    ?nexp: term
        | term "+" term                                 -> add
        | term "-" term                                 -> sub

    ?term: factor
        | factor "*" factor                               -> mul
        | factor "/" factor                               -> div


    ?factor: NUMBER                                     -> number
        | "-" factor                                    -> neg
        | NAME                                          -> ident
        | "(" nexp ")"
    


    ?bliteral: "F"                                      -> false
        | "T"                                           -> true
        | "(" bexp ")"
    
    ?bident: NAME ":=" bexp                             -> assign_var
            
    


%import common.CNAME -> NAME
%import common.NUMBER
%import common.WS_INLINE
%ignore WS_INLINE
"""


@v_args(inline=True)
class Interpreter(Transformer):
    number = int

    def __init__(self):
        self.vars = {}

    def assign_var(self, name, value):
        self.vars[name] = value
        return value

    def ident(self, name):
        try:
            return self.vars[name]
        except KeyError:
            return "Undefined variable: {}".format(name)
        
    def add(self, nexp, term):
        return operator.add(nexp, term)

    def sub(self, nexp, term):
        return operator.sub(nexp,term)

    def mul(self, factor, term):
        return operator.mul(factor, term)

    def div(self, factor, term):
        return operator.truediv(factor, term)

    def neg(self, factor):
        return operator.neg(factor)

    def true(self):
        return True

    def false(self):
        return False

    def or_(self, bexp, bterm):
        return operator.or_(bexp, bterm)

    def and_(self, bterm, notfactor):
        return operator.and_(bterm, notfactor)

    def not_(self, a):
        return not(a)

    def gt(self, nexp1, nexp2):
        return operator.gt(nexp1, nexp2)

    def lt(self, nexp1, nexp2):
        return operator.lt(nexp1, nexp2)

    def eq(self, nexp1, nexp2):
        return operator.eq(nexp1, nexp2)




bexp_parser = Lark(bexp_grammar, parser='lalr', transformer=Interpreter())


def main():
    while True:
        try:
            eval = input('> ')
        except:
            print("INVALID STRING")
            break
        if len(eval) == 0:
            print("Error, empty string.")
        else:
            print(bexp_parser.parse(eval))

if __name__ == '__main__':

    main()
