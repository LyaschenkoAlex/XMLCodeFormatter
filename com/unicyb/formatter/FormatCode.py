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
        less()
    elif input == ">":
        greater()
    elif number_of_brackets == 1:
        in_brackets(input)
    elif number_of_brackets == 0:
        between_brackets(input)


def less():
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


def greater():
    global number_of_brackets
    if number_of_brackets == 1 and number_of_single_brackets == 0 and number_of_double_brackets == 0:
        number_of_brackets = number_of_brackets - 1
        global text_in_brackets
        if text_in_brackets != "":
            text_in_brackets = text_in_brackets.strip()
            text_in_brackets = re.sub(r'[ ]+', ' ', text_in_brackets)
            text_in_brackets = re.sub(r'\n[ ]+', '\n', text_in_brackets)
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
        result_string += '<br>'
    if ((index_br == -1 and result_string.count('&lt;') > 0) or result_string[index_br + 3:].count('&lt;') > 0) \
            and (result_string.endswith('&gt') or result_string[index_gt + 3].isspace()):
        result_string += '<br>'
    result_string += nesting_level * '&emsp;' + '&lt;'
    nesting_level += 1


def formatted_in_brackets(value):
    value = re.sub(r'[ ]*=[ ]*', '=', value)
    global nesting_level
    if value.startswith('?'):
        nesting_level -= 1
    if value.startswith('/'):
        if nesting_level != 0:
            global result_string
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
    index_less = result_string.rfind('&lt;')
    index_less_less = result_string[:index_less].rfind('&lt;')
    string_less = result_string[index_less_less + 4: index_less]
    string_less = string_less.replace('<br>', '')
    string_less = string_less.replace('&emsp;', '')
    string_less = string_less.replace('&gt', '')
    string = result_string[index_less + 4:]
    string = string.replace('<br>', '')
    string = string.replace('&emsp;', '')
    string = string.replace('&gt', '')
    if string.startswith('/'):
        try:
            if string[1:] == string_less:
                index_greater = result_string[:index_less].rfind('&gt')
                result_string = result_string[:index_greater] + '&gt' + '&lt;' + string
        except:
            print('exception - 201')
    result_string += '&gt'


def formatted_comment(value):
    global result_string
    result_string += value


def start_format():
    global result_string
    read_from_file('../../../resources/input.xml')
    get_char_from_file()
    format_element_from_array(tokens)
    result_string = result_string.replace('&gt', '<span class="bracket">&gt</span>')
    result_string = result_string.replace('&lt;', '<span class="bracket">&lt;</span>')
    f = open("../../../resources/test.html", "w")
    result_string = '<!DOCTYPE html><html><head><link rel="stylesheet" href="styles.css"></head><body><p>' \
                    + result_string + '</p></body></html>'
    f.write(result_string)
    f.close()
