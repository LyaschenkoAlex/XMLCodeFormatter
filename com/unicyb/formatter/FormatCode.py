import re

tokens = []
number_of_brackets = 0  # <  >
number_of_single_brackets = 0  # '  '
number_of_double_brackets = 0  # "  "
text_in_brackets = ""
input_file = ""
text_between_brackets = ""
nesting_level = 0
result_string = ""
is_comment = False
keywords_in_brackets = []
is_doctype = False


def read_from_file(file_name):
    global input_file
    input_file = open(file_name).read()
    input_file = re.sub(r'[\n][\n][\n]+', '\n\n\n', input_file)
    return open(file_name).read()


def get_char_from_file():
    global input_file
    for i in input_file:
        parse(i)


def parse(input):
    if is_comment:
        in_brackets(input)
    elif input == "<":
        less(input)
    elif input == ">":
        greater(input)
    elif number_of_brackets == 1:
        in_brackets(input)
    elif number_of_brackets == 0:
        between_brackets(input)


def less(input):
    if is_doctype:
        in_brackets(input)
        return
    global number_of_brackets
    if number_of_brackets == 0 and number_of_single_brackets == 0 and number_of_double_brackets == 0:
        global text_between_brackets
        if text_between_brackets != "":
            text_between_brackets = re.sub(r'[ ]+', ' ', text_between_brackets)
            text_between_brackets = re.sub(r'\n[ ]+', '\n', text_between_brackets)
            text_between_brackets = text_between_brackets.replace('\n', '<br>')
            if text_between_brackets != "":

                tokens.append({"between_brackets": text_between_brackets})
            text_between_brackets = ""
        number_of_brackets += 1
        tokens.append({"less": "<"})
    elif number_of_brackets == 1:
        in_brackets("<")


def greater(input):
    global text_in_brackets
    global number_of_brackets
    global is_doctype

    if is_doctype and text_in_brackets.count('&lt;') != text_in_brackets.count('&gt;'):
        in_brackets(input)
        return
    else:
        is_doctype = False

    if number_of_brackets == 1 and number_of_single_brackets == 0 and number_of_double_brackets == 0:
        number_of_brackets = number_of_brackets - 1
        if text_in_brackets != "":
            text_in_brackets = text_in_brackets.strip()
            text_in_brackets = re.sub(r'[ ]+', ' ', text_in_brackets)
            text_in_brackets = re.sub(r'\n[ ]+', '\n', text_in_brackets)

            text_in_brackets = text_in_brackets.replace('\n', '\n&emsp;' * (nesting_level+2))
            if text_in_brackets != "":
                tokens.append({"in_brackets": text_in_brackets})
            tokens.append({"greater": ">"})
            text_in_brackets = ""
    elif number_of_brackets == 1:
        in_brackets(">")


def new_line():
    if number_of_single_brackets == 0 and number_of_double_brackets == 0:
        tokens.append({"NL": "<br>"})
    elif number_of_brackets == 1:
        in_brackets("<br>")


def in_brackets(input):
    global text_in_brackets
    global number_of_single_brackets
    global number_of_double_brackets
    global text_between_brackets
    global is_doctype
    if input == '<' and is_doctype:
        text_in_brackets += '&lt;'
        return
    elif input == '>' and is_doctype:
        text_in_brackets += '&gt;'
        return

    else:
        text_in_brackets += input

    global is_comment
    global number_of_brackets
    global nesting_level

    if text_in_brackets.startswith('!') and not is_comment:
        del tokens[-1]
        number_of_brackets -= 1
        text_in_brackets = '&lt;' + text_in_brackets
        is_comment = True
    if not is_comment:
        if number_of_double_brackets == 1 and input == '"':
            number_of_double_brackets -= 1
        elif number_of_single_brackets == 0 and input == '"' and number_of_double_brackets == 0:
            number_of_double_brackets += 1
        if number_of_single_brackets == 1 and input == "'":
            number_of_single_brackets -= 1
        elif number_of_single_brackets == 0 and input == "'" and number_of_double_brackets == 0:
            number_of_single_brackets += 1
    if text_in_brackets.startswith('&lt;!DOCTYPE') and is_comment:
        is_doctype = True
        # text_between_brackets = text_in_brackets
        # text_in_brackets = ''
        is_comment = False
        tokens.append({"less": "<"})
        number_of_brackets += 1
        text_in_brackets = text_in_brackets[4:]

    if text_in_brackets.endswith('-->'):
        tokens.append({"comment": text_in_brackets.replace('>', '&gt')})
        text_in_brackets = ""
        is_comment = False


def between_brackets(input):
    global text_between_brackets
    text_between_brackets += input


def format_element_from_array(array):
    for i in array:
        create_formatted_text(i)


def create_formatted_text(dict):
    for tkn, vl in dict.items():
        if tkn == 'less':
            formatted_less()
        elif tkn == 'in_brackets':
            formatted_in_brackets(vl)
        elif tkn == 'greater':
            formatted_greater()
        elif tkn == 'comment':
            formatted_comment(vl)
        elif tkn == 'between_brackets':
            formatted_between_brackets(vl)


def formatted_less():
    global result_string
    global nesting_level
    index_br = result_string.rfind('<br>')
    index_gt = result_string.rfind('&gt')
    if index_gt < index_br and result_string[index_br:] != '<br>':
        result_string += '```'
        #######################
    if ((index_br == -1 and result_string.count('&lt;') > 0) or result_string[index_br + 3:].count('&lt;') > 0) \
            and (result_string.endswith('&gt') or result_string[index_gt + 3].isspace()):
        result_string += '```'
    result_string += nesting_level * '&emsp;' + '&lt;'
    nesting_level += 1


def formatted_in_brackets(value):
    value = re.sub(r'[ ]*=[ ]*', '=', value)
    global nesting_level
    global result_string
    # print(result_string)
    if result_string.endswith('\n'):
        value = 4 * nesting_level * ' ' + '    ' + value
        print('true')
    if value.startswith('?') or value.startswith('!DOCTYPE'):
        nesting_level -= 1
    if value.startswith('/'):
        if nesting_level != 0:
            index = result_string.rfind('&emsp;')
            index_br = result_string.rfind('<br>')
            if result_string[index_br:].count('&lt;') > 1:
                result_string = result_string[:index - (nesting_level - 2) * 6] + '&lt;'
            else:
                result_string = result_string[:index] + '&lt;'
            nesting_level -= 2
    if value.endswith('/'):
        nesting_level -= 1
    result_string += value


def formatted_between_brackets(value):
    global result_string
    value = value.strip()
    value = re.sub(r'<br><br>(<br>)+', '<br><br><br>', value)
    if value != '<br>':
        value = re.sub(r'<br>', '<br>' + nesting_level * '&emsp;', value)
    while value.endswith('&emsp;'):
        value = value[:len(value) - 6]
    result_string += value


def formatted_greater():
    global result_string
    global nesting_level
    index_of_br = result_string.rfind('<br>')
    count_of_less = result_string[index_of_br:].count('&lt;')
    if count_of_less > 1:
        index_less = result_string.rfind('&lt;')
        index_less_less = result_string[:index_less].rfind('&lt;')
        string_less = result_string[index_less_less + 4: index_less]
        # string_less = string_less.replace('<br>', '')
        string_less = string_less.replace('&emsp;', '')
        string_less = string_less.replace('&gt', '')
        string = result_string[index_less + 4:]
        string = string.replace('<br>', '')
        string = string.replace('&emsp;', '')
        string = string.replace('&gt', '')
        if string.startswith('/'):
            try:
                if string[1:] == string_less.replace('```', '') or (string_less.startswith('!') and
                                                                    string_less.replace('```', '') != string_less):
                    index_greater = result_string[:index_less].rfind('&gt')
                    result_string = result_string[:index_greater] + '&gt' + '&lt;' + string

                else:
                    result_string = result_string.replace('```', '<br>' + (nesting_level) * '&emsp;')
            except:
                print('exception - 201')
        elif string.startswith('!'):
            result_string = result_string.replace('```', '<br>' + (nesting_level) * '&emsp;')
            # print('comment')
        else:
            result_string = result_string.replace('```', '<br>')
            result_string += '&gt'
    else:
        result_string = result_string.replace('```', '<br>')
    result_string += '&gt'


def formatted_comment(value):
    global result_string
    if result_string.endswith('<br>'):
        result_string = result_string + nesting_level * '&emsp;'
    result_string += value


def start_format(path_to_file):
    global result_string
    read_from_file(path_to_file)
    get_char_from_file()
    format_element_from_array(tokens)
    result_string = result_string.replace('&gt&gt', '&gt')
    result_string = result_string.replace('&gt', '<span class="bracket">&gt</span>')
    result_string = result_string.replace('&lt;', '<span class="bracket">&lt;</span>')
    while result_string.startswith('<br>'):
        result_string = result_string[4:]
    result_string = '<!DOCTYPE html><html><head><link rel="stylesheet" href="styles.css"></head><body><p>' \
                    + result_string + '</p></body></html>'
    return result_string
