__author__ = 'john'

import types

from pyparsing import *


def evaluate(context, val):
    if isinstance(val, list):
        cmd = evaluate(context, val[0])

        if isinstance(cmd, types.FunctionType):
            return cmd(context, val[1:])
        else:
            return cmd

    if isinstance(val, types.FunctionType):
        return val

    try:
        return int(val)
    except(ValueError, TypeError):
        pass

    if val[0] == "'" and val[len(val) - 1] == "'":
        return val

    # I don't think I need this
    # if isinstance(context[val], types.FunctionType):
    #    return context[val]
    if val in context:
        return context[val]
    return evaluate(context, context[val])


# Flow Operators
def c_if(context, vals):
    x = evaluate(context, vals[0])

    if x:
        return evaluate(context, vals[1])

    if len(vals) == 3:
        return evaluate(context, vals[2])


def c_list(context, vals):
    ret = []
    for c in vals:
        ret.append(evaluate(context, c))
    return ret


def c_car(context, vals):
    tmp = evaluate(context, vals)
    return tmp[0]


def c_cdr(context, vals):
    tmp = evaluate(context, vals)
    return tmp[1:]


# Comparison Operators
def c_eq(context, vals):
    return 1 if evaluate(context, vals[0]) == evaluate(context, vals[1]) else 0


def c_gt(context, vals):
    return 1 if evaluate(context, vals[0]) > evaluate(context, vals[1]) else 0


def c_lt(context, vals):
    return 1 if evaluate(context, vals[0]) < evaluate(context, vals[1]) else 0


def c_ex(context, vals):
    return 1 if len(vals[0]) > 0 else 0


# Math Operators
def c_minus(context, vals):
    tmp = evaluate(context, vals[0])
    for a in vals[1:]:
        tmp -= evaluate(context, a)
    return tmp


def c_add(context, vals):
    tmp = 0
    for a in vals:
        el = evaluate(context, a)
        if isinstance(el, list):
            tmp += c_add(context, el)
        else:
            tmp += el
    return tmp


def c_mult(context, vals):
    tmp = 1
    for a in vals:
        tmp *= evaluate(context, a)
    return tmp


def c_div(context, vals):
    tmp = evaluate(context, vals[0])
    for a in vals[1:]:
        tmp /= evaluate(context, a)


def c_set_var(context, vals):
    var = vals[0]
    if len(vals[1:]) == 1:
        context[var] = evaluate(context, vals[1])
    else:
        context[var] = evaluate(context, vals[1:])


# Other Operators
def c_print(context, vals):
    a = evaluate(context, vals)
    print a


def c_lambda(commands, vals):
    params = vals[0]
    command = vals[1]

    def func(new_com2, vals):
        new_com = new_com2.copy()

        for i, p in enumerate(params):
            new_com[p] = evaluate(new_com2, vals[i])

        return evaluate(new_com, command)

    return func


def c_cat(commands, vals):
    return commands.keys()


def c_nop(commands, vals):
    return evaluate(commands, vals)


GLOB_context = {'+': c_add,
                '-': c_minus,
                '*': c_mult,
                '/': c_div,
                'set': c_set_var,
                'list': c_list,
                'print': c_print,
                'lambda': c_lambda,
                'if': c_if,
                '>': c_gt,
                '<': c_lt,
                '=': c_eq,
                'cdr': c_cdr,
                'car': c_car,
                'notnull': c_eq,
                'cat': c_cat,
                "!": c_nop}

# Returns a complete command array
def parse(phrase):
    if len(phrase) == 0:
        return []

    command = []

    a = phrase.pop()

    while 1:

        if len(a) == 0:
            if len(phrase):
                continue
            else:
                return command

        if a[0] == "(":
            if len(a) >= 1:
                phrase.append(a[1:])

            command.append(parse(phrase))

            if len(phrase):
                a = phrase.pop()
            else:
                a = ""
            continue

        # This doesn't support multiple end brackets
        if a[len(a) - 1] == ")":
            if len(a) > 1:
                command.append(a[:len(a) - 1])
            return command

        command.append(a)

        if len(phrase):
            a = phrase.pop()
        else:
            return command

    return command


def scheme_parse_re(commands):
    exp = Forward()

    number = Word(nums).setResultsName('int', True).setParseAction(lambda s, l, t: int(t[0]))
    lparen = Literal('(').suppress()
    rparen = Literal(')').suppress()
    varname = Word(alphanums).setResultsName('var')
    op = Word(printables).setResultsName('op')  # .setParseAction(lambda s, l, t: op_map[t[0]])
    string = QuotedString("'").setName('str')
    exp << Group(lparen + op('op') + OneOrMore(number('int') ^ exp ^ varname ^ string("string")) + rparen)

    a = exp.parseString(commands)
    return a


def scheme_parse(commands):
    '''Need to work in reverse order'''
    return parse(commands.split(' ')[::-1])


while (1):
    line = raw_input("%s>" % len(GLOB_context))

    if line.find("(") < 0:
        print GLOB_context
        continue
    commands = None
    try:
        commands = scheme_parse_re(line).asList()
    except ParseException, e:
        print "Syntax error at position %d:\n%s" % (e.col, e.line)
        print (" " * (e.col - 1)) + "^"
        print e.msg

    if commands:
        try:
            evaluate(GLOB_context, commands)
        except KeyError:
            print "Undefined variable or function used"

