import json
from scanner import get_token
from anytree import Node, RenderTree


# Ayla Salehi 99105572
# Bahar Dibaei Nia 99105442

def type_token(output): #convert token to terminals
    s0 = ''
    type_ = ''
    if output[1] != 'comment' and output[1] != 'error':
        s0 = '(' + output[1] + ', ' + output[0] + ')'
        if output[1] in ['ID', 'NUM']:
            type_ = output[1]
        else:
            type_ = output[0]

    return s0, type_


def new_token():  #while token is not comment or error get new token
    global line, idx_0, str_in
    out1 = get_token(str_in, idx_0, line)
    idx_0 = out1[-1]
    line = out1[-2]
    out1 = type_token(out1)
    while out1[0] == '' and out1[1] == '':
        out1 = get_token(str_in, idx_0, line)
        idx_0 = out1[-1]
        line = out1[-2]
        out1 = type_token(out1)
    return out1[0], out1[1]


f = open('table.json')

# returns JSON object as
# a dictionary
data = json.load(f)
f.close()

f = open("input.txt", "r")
str_in = f.read()
# str_in = 'int global1;'

parse_table = data['parse_table']
grammars = data['grammar']
follows = data['follow']
firsts = data['first']
terminals = data['terminals']
non_terminals = data['non_terminals']
stack = ['0']
parents = []
idx_0 = 0
line = 1
out = new_token()
s0, s1 = out[0], out[1]
file_parse_tree = open('parse_tree.txt', "w", encoding='utf-8')
file_syntax_error = open('syntax_errors.txt', 'w')
errors = []


def panic_mode(): #error handling
    flag = 0
    split_reg = ', '
    global line, s0, s1, stack, parse_table, idx_0, errors, out, parents, non_terminals
    errors.append(f'#{line} : syntax error , illegal {s0.split(split_reg)[1][:-1]}')
    out = new_token()
    s0, s1 = out[0], out[1]
    while True:
        r = stack[-1]
        keys = parse_table[r].keys()
        for idx in range(len(list(keys))):  # find goto state
            if parse_table[r][list(keys)[idx]].startswith('goto'):
                flag = 1
                break

            if idx == len(list(keys)) - 1:
                stack.pop()
                stack.pop()
                discarded = parents.pop().name
                errors.append(f'syntax error , discarded {discarded} from stack')
        if flag == 1:
            break

    follow_nt = check_follow(stack[-1])
    while follow_nt == '':
        if s1 == '$':
            errors.append(f'#{line} : syntax error , Unexpected EOF')
            return False
        errors.append(
            f'#{line} : syntax error , discarded {s0.split(split_reg)[1][:-1]} from input')
        out = new_token()
        s0, s1 = out[0], out[1]
        follow_nt = check_follow(stack[-1])
    # STEP 3: stack the new non-terminal
    errors.append(f'#{line} : syntax error , missing {follow_nt}')
    next_state = parse_table[stack[-1]][follow_nt].split('_')[1]
    stack.append(follow_nt)
    stack.append(next_state)
    parents.append(Node(follow_nt))
    return True


def check_follow(state): #check if token is in follow one of gotos
    global parse_table, non_terminals, s0, s1, follows
    for key in sorted(parse_table[state].keys()):
        if key in non_terminals and s1 in follows[key]:
            return key
    return ''


while True:
    flag=0
    s0, s1 = out[0], out[1]
    # line = int(out[-2])
    # idx_0 = out[-1]

    while s1 not in parse_table[stack[-1]].keys():
        p = panic_mode()
        if not p:
            parents = []
            flag=1
            break
    if flag==1:
        break

    #check actions
    print(errors)
    action = parse_table[stack[-1]][s1]
    if action == 'accept': #if accept
        break
    action = action.split('_')

    if action[0] == 'shift':
        stack.append(s1)
        if s1 != '$':
            parents.append(Node(s0))
        else:
            parents.append(Node('$', parents[-1]))
        stack.append(action[1])
        out = new_token()
        s0, s1 = out[0], out[1]
        # idx_0, line = out[-1], int(out[-2])
    elif action[0] == 'reduce':
        gr = grammars[action[1]]
        gr = gr[0], gr[2:]
        n = len(gr[1])
        children = []

        if gr[1][0] != 'epsilon':
            for j in range(len(gr[1])):
                stack.pop()
                stack.pop()
                children.append(parents.pop())
        else:
            children.append(Node('epsilon'))

        stack.append(gr[0])
        x = Node(gr[0], children=children[::-1])
        parents.append(x)

        goto = (parse_table[stack[-2]][stack[-1]]).split('_')[1]
        stack.append(goto)
lines = []
if len(parents) > 0:
    for pre, fill, node in RenderTree(parents[-2]):
        lines.append(f'{pre}{node.name}')
file_parse_tree.write('\n'.join(lines))
if len(errors) > 0:
    file_syntax_error.write('\n'.join(errors))
else:
    file_syntax_error.write('There is no syntax error.')

# error
