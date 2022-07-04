'''Assignment 1 CSC153 Assemblers, Interpreters, and Compilers'''
'''CANONIGO, MERSAN JR. S. BSCS-4 2018-5830'''


class parser:
    def __init__(self):
        self.grammar_for_number = {
            '<number>': [['<integer>'], ['<float>']],
            '<integer>': [['<unsigned integer>'], ['<signed integer>']],
            '<float>': [['<unsigned integer>', '<point>', '<unsigned integer>']],
            '<sign>': [['-'], ['+']],
            '<signed integer>': [['<sign>', '<unsigned integer>'], ['<sign>', '<unsigned integer>']],
            '<unsigned integer>': [['<non-zero digit>'], ['<non-zero digit>', '<unsigned integer>']],
            '<digits>': [['<non-zero dight>'], ['<digits>']],
            '<digit>': [['<zero>'], ['<non-zero digit>']],
            '<non-zero digit>': [['1'], ['2'], ['3'], ['4'], ['5'], ['6'], ['7'], ['8'], ['9']],
            '<zero>': [['0']],
            '<point>': [['.']]

        }
        self.grammar_for_identifer = {
            '<identifier>': [['<letter>'], ['<variable>','<character>']],
            '<character>' : [['<letter>'],['<digit>'],['<under-score>']],
            '<letter>': [['a'],['b'],['c'],['d'],['e'],['f'],['g'],['h'],['i'],['j'],['k'],['l'],['m'],['n'],['o'],['q'],['r'],['s'],['t'],['u'],['v'],['w'],['x'],['y'],['z']],
            '<digit>': [['0'],['1'], ['2'], ['3'], ['4'], ['5'], ['6'], ['7'], ['8'], ['9']],
            '<under-score>' : [['_']]
        }
            
    def parser_type_picker(self,parser_type,input_str):
        if parser_type == NUM:
            return self.parseNum(input_str)
        elif parser_type == IDENT:
            return self.parseIdent(input_str)


    
    def parseNum(self,input_str):
        #this is the non-terminal symbols
        non_terminals_symbols = list(self.grammar_for_number.keys())
        #valid_char or subset of terminal symbols
        
        #Here will check if the input_str length is not equal to 0, no leading zero, and last input_str is not a sign else return error
        if len(input_str) == 0:
            return 'empty string is not a valid number'
        elif input_str[0] == '0':
            return f'{input_str} is not a valid number'
        elif input_str[-1] == "-" or input_str[-1] == "+":
            return f'{input_str} is not a valid number'

        #if the function doesn't return until this point it means that implies input_str is a valid string
        #now to determine if the string belongs to the self.grammar_for_number defined above I will use my modified version of Cocke–Younger–Kasami algorithm for parsing
        
        input_str_to_list = []
        for input in input_str:
            input_str_to_list.append(input)
        n = len(input_str_to_list)

        #Initialize the table
        table = [[set([]) for j in range(n)] for i in range(n)]

        for s in range(0, n):
            for left_hand_side, rule in self.grammar_for_number.items():
                for right_hand_side in rule:
                    if len(right_hand_side) == 1 and right_hand_side[0] == input_str_to_list[s]:
                        table[s][s].add(left_hand_side)

        for l in range(1,n):
            for i in range(0,n-l+1):
                j = i+l-1
                for k in range(n-1,j-1):
                    for left_hand_side, rule in self.grammar_for_number.items():
                        for right_hand_side in rule:
                            if right_hand_side[0] in table[i][k] and right_hand_side[1] in table[k+1][j]:
                                table[i][j].add(left_hand_side)
        
                                
        #determine if string belongs to the self.grammar_for_number
        result = True
        idx = 0
        point = 0
        for r in range(0,len(table)):
            try:
                if list(table[r][idx])[0] in non_terminals_symbols:
                    if list(table[r][idx])[0] == '<point>':
                        point+=1
                        if point==2:
                            result = False
                            break
                        elif list(table[r+1][idx+1])[0] == "<sign>" and list(table[r-1][idx-1])[0] == "<sign>":
                            result = False
                            break
                        else:
                            idx += 1
                    else:
                        idx += 1
                else:
                    result = False
                    break
            except Exception as e:
                result = False
                break
            
        if result == True:
            return f'{input_str} is a valid number'
        else:
            return f'{input_str} is not a valid number'

    def parseIdent(self, input_str):
        reserve_words = ['False', 'await', 'else', 'import', 'pass', 'None', 'break', 'except', 'in', 'raise', 'True', 'class', 'finally', 'is', 'return', 'and', 'continue',
                        'for', 'lambda', 'try', 'as', 'def', 'from', 'nonlocal', 'while', 'assert', 'del', 'global', 'not', 'with', 'async', 'elif', 'if', 'or', 'yield']
        #this is the non-terminal symbols
        non_terminals_symbols = list(self.grammar_for_identifer.keys())
        #valid_char or subset of terminal symbols

        #Here will check if the input_str length is not equal to 0, no leading zero, and last input_str is not a sign else return error
        if len(input_str) == 0:
            return 'empty string is not a valid identifer'
        elif input_str[0] == '0':
            return f'{input_str} is not a valid identifer'
        elif input_str in reserve_words:
            return f'{input_str} is not a valid identifer'


        #if the function doesn't return until this point it means that implies input_str is a valid string
        #now to determine if the string belongs to the self.grammar_for_number defined above I will use my modified version of Cocke–Younger–Kasami algorithm for parsing

        input_str_to_list = []
        for input in input_str:
            input_str_to_list.append(input)
        n = len(input_str_to_list)

        #Initialize the table
        table = [[set([]) for j in range(n)] for i in range(n)]

        for s in range(0, n):
            for left_hand_side, rule in self.grammar_for_identifer.items():
                for right_hand_side in rule:
                    if len(right_hand_side) == 1 and right_hand_side[0] == input_str_to_list[s]:
                        table[s][s].add(left_hand_side)

        for l in range(1, n):
            for i in range(0, n-l+1):
                j = i+l-1
                for k in range(n-1, j-1):
                    for left_hand_side, rule in self.grammar_for_identifer.items():
                        for right_hand_side in rule:
                            if right_hand_side[0] in table[i][k] and right_hand_side[1] in table[k+1][j]:
                                table[i][j].add(left_hand_side)

        #determine if string belongs to the self.grammar_for_identifier
        result = True
        idx = 0
        point = 0
        for r in range(0, len(table)):
            try:
                if idx == 0 and list(table[r][idx])[0] == '<digit>':
                    result = False
                    break
                elif list(table[r][idx])[0] in non_terminals_symbols:
                    idx += 1
                else:
                    result = False
                    break
                    
            except Exception as e:
                result = False
                break
                
            

        if result == True:
            return f'{input_str} is a valid identifier'
        else:
            return f'{input_str} is not a valid identifier'
        
                                

Parser = parser()
NUM = lambda input_str: Parser.parseNum(input_str)
IDENT = lambda input_str: Parser.parseIdent(input_str)

print(Parser.parser_type_picker(NUM,'12'))
print(Parser.parser_type_picker(NUM, '23x'))
print(Parser.parser_type_picker(IDENT, 'x'))
print(Parser.parser_type_picker(IDENT, 'sum1'))
print(Parser.parser_type_picker(IDENT, '23x'))



