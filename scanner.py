symbols = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '/', '=', '<']
whitespace = [' ', '\n', '\r', '\t', '\v', '\f']
keywords = ['if', 'else', 'void', 'int', 'while', 'break', 'switch', 'default', 'case', 'return', 'endif']


def get_token(str_in, idx, line_no=1):
    global symbols
    global whitespace
    global keywords
    output = ''

    while True:

        if idx >= len(str_in):
            return '$', '', '', line_no, idx+1
        s = str_in[idx]
        if s == '\n':
            line_no += 1
        if not (s == '\n' or s == '\f' or s == '\v' or s == '\t' or s == '\r' or ord(s) == 32):
            # ------------------------------------------- number
            if ord(s) in range(48, 58):
                output += s
                idx += 1
                s = str_in[idx]
                while ord(s) in range(48, 58):
                    output += s
                    idx += 1
                    s = str_in[idx]
                if ord(s) in range(65, 91) or ord(s) in range(97, 123) or (
                        not (s in symbols) and not (s in whitespace)):
                    output += s
                    if ord(s) in range(65, 91) or ord(s) in range(97, 123):
                        return output, 'error', 'Invalid number', line_no, idx + 1
                    else:
                        return output, 'error', 'Invalid input', line_no, idx + 1
                else:
                    return output, 'NUM', '', line_no, idx
            # ---------------------------------------------- ID-Keyword

            elif ord(s) in range(65, 91) or ord(s) in range(97, 123):
                output += s
                idx += 1
                s = str_in[idx]
                while ord(s) in range(48, 58) or ord(s) in range(65, 91) or ord(s) in range(97, 123):
                    output += s
                    idx += 1
                    s = str_in[idx]
                if not (s in symbols) and not (s in whitespace):
                    output += s
                    return output, 'error', 'Invalid input', line_no, idx + 1
                else:
                    if output in keywords:

                        return output, 'KEYWORD', '', line_no, idx
                    else:
                        return output, 'ID', '', line_no, idx

            # --------------------------------------------------- comments
            elif s == '=':
                output += s
                if idx + 1 < len(str_in) and str_in[idx + 1] == '=':
                    output += '='
                    idx += 1
                    return output, 'SYMBOL', '', line_no, idx + 1
                else:
                    if idx + 1 >= len(str_in) or (str_in[idx + 1] in whitespace) or (str_in[idx + 1] in symbols) or (
                            ord(str_in[idx + 1]) in range(48, 58)) or ord(s) in range(65, 91) or ord(s) in range(97,
                                                                                                                 123):
                        return output, 'SYMBOL', '', line_no, idx + 1
                    else:
                        return output + str_in[idx + 1], 'error', 'Invalid input', line_no, idx + 2

            elif s == '*' and str_in[idx + 1] == '/':
                return '*/', 'error', 'Unmatched comment', line_no, idx + 2

            elif s == '/' and str_in[idx + 1] == '/':
                idx += 2
                while str_in[idx] != '\n' and idx < len(str_in):
                    idx += 1
                # if str_in[idx] == '\n':
                #    line_no += 1
                return '', 'comment', '', line_no, idx  # +1

            elif s == '/' and str_in[idx + 1] == '*':
                idx += 2
                line_no_temp = line_no
                while idx < len(str_in) - 1 and not (str_in[idx] == '*' and str_in[idx + 1] == '/'):
                    output += str_in[idx]
                    if str_in[idx] == '\n':
                        line_no += 1
                    idx += 1
                if idx >= len(str_in) - 1:
                    return '/*' + output[:5] + '...', 'error', 'Unclosed comment', line_no_temp, idx + 1
                else:
                    return '', 'comment', '', line_no, idx + 2

            # ---------------------------------------------------- symbols

            elif s in symbols:
                output += s
                return output, 'SYMBOL', '', line_no, idx + 1
            else:
                output += s
                return output, 'error', 'Invalid input', line_no, idx + 1
        else:
            idx += 1


def write_error(output, last_line):
    errors = ''
    line_num = output[-2]
    if output is not None and output[1] == 'error':
        if line_num != last_line:
            if last_line != 0:
                errors += '\n' + str(line_num) + '.\t'
            else:
                errors += str(line_num) + '.\t'
            last_line = line_num
        errors += '(' + output[0] + ', ' + output[2] + ') '
    return errors, last_line


def write_symbol_table(output):
    if output is not None and output[1] == 'ID':
        return output[0]


def write_token(output, last_line):
    str_token = ''
    line_num = int(output[-2])
    if output[1] != 'comment' and output[1] != 'error':
        if line_num != last_line:
            if last_line != 0:
                str_token += '\n' + str(line_num) + '.\t'
            else:
                str_token += str(line_num) + '.\t'
            last_line = line_num
        str_token += '(' + output[1] + ', ' + output[0] + ') '
    return str_token, last_line


# f = open("input.txt", "r")
# # f= open('testcases_phase1_v2 (5)\T11\input.txt')
# file_token = open("tokens.txt", "w")
# file_error = open("lexical_errors.txt", "w")
# file_symbol_table = open("symbol_table.txt", "w")
# str_in = f.read()
# idx_0 = 0
# line = 1
# last_update_line = 0
# last_update_line_error = 0
# count_error = 0
# id_list = []
# identifiers = ''
# final_identifiers = []
# sym_no = 11
# while True:
#     out = get_token(str_in, idx_0, line)
#     if not out:
#         break
#     line = int(out[-2])
#     idx_0 = out[-1]
#     write_tokens = write_token(out, last_update_line)
#     last_update_line = write_tokens[1]
#     file_token.write(write_tokens[0])
#
#     write_errors = write_error(out, last_update_line_error)
#     last_update_line_error = write_errors[1]
#     file_error.write(write_errors[0])
#
#     id_list.append(write_symbol_table(out))
#     if (write_errors[0]) != '':
#         count_error += 1
#
# if count_error == 0:
#     file_error.write("There is no lexical error.")
# for i in id_list:
#     if i not in final_identifiers:
#         final_identifiers.append(i)
# identifiers += str(1) + '.\tif\n'
# identifiers += str(2) + '.\telse\n'
# identifiers += str(3) + '.\tvoid\n'
# identifiers += str(4) + '.\tint\n'
# identifiers += str(5) + '.\twhile\n'
# identifiers += str(6) + '.\tbreak\n'
# identifiers += str(7) + '.\tswitch\n'
# identifiers += str(8) + '.\tdefault\n'
# identifiers += str(9) + '.\tcase\n'
# identifiers += str(10) + '.\treturn\n'
# identifiers += str(11) + '.\tendif\n'
# for ele in final_identifiers:
#     if ele is not None:
#         sym_no += 1
#         identifiers += str(sym_no) + '.\t' + ele + '\n'
# file_symbol_table.write(identifiers[:-1])
# file_symbol_table.close()
# file_error.close()
# file_token.close()
