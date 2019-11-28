import re
from sys import argv
from Errors import find_errors
tokens = []
new_tokens = []
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
in_tag = ''
doctype = ''
xml_tag_old = ''
xmo_tag_new = ''


directory_path = ''
path_to_res = ''
indent = ''
blank_lines = ''
space_around = ''
space_in_empty_tag = ''


def read_from_file(file_name):
    global input_file
    global doctype
    global blank_lines
    input_file = open(file_name).read()
    if blank_lines == '':
        blank_lines = 2
    input_file = re.sub(r'[\n]' + '[\n]' * blank_lines + '[\n]+', '\n' * (blank_lines + 1), input_file)
    if input_file.count('<!DOCTYPE') != 0:
        left = 1
        right = 0
        index = input_file.find('!DOCTYPE')
        while left != right:
            doctype += input_file[index]
            index += 1
            if input_file[index] == '<':
                left += 1
            elif input_file[index] == '>':
                right += 1
        input_file = input_file.replace(doctype, '```')


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
            text_between_brackets = text_between_brackets
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

    if is_doctype and text_in_brackets.count('<') != text_in_brackets.count('>'):
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

            text_in_brackets = text_in_brackets.replace('\n', '\n' + '\t' * (nesting_level + 2))
            if text_in_brackets != "":
                if text_in_brackets == '```':
                    tokens.append({"doctype": '<' + doctype + '>'})
                else:
                    tokens.append({"in_brackets": text_in_brackets})
            tokens.append({"greater": ">"})
            text_in_brackets = ""
    elif number_of_brackets == 1:
        in_brackets(">")


def new_line():
    if number_of_single_brackets == 0 and number_of_double_brackets == 0:
        tokens.append({"NL": "\n"})
    elif number_of_brackets == 1:
        in_brackets("\n")


def in_brackets(input):
    global text_in_brackets
    global number_of_single_brackets
    global number_of_double_brackets
    global text_between_brackets
    global is_doctype
    if input == '<' and is_doctype:
        text_in_brackets += '<'
        return
    elif input == '>' and is_doctype:
        text_in_brackets += '>'
        return

    else:
        text_in_brackets += input

    global is_comment
    global number_of_brackets
    global nesting_level

    if text_in_brackets.startswith('!') and not is_comment:
        del tokens[-1]
        number_of_brackets -= 1
        text_in_brackets = '<' + text_in_brackets
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
    if text_in_brackets.startswith('<!DOCTYPE') and is_comment:
        is_doctype = True
        # text_between_brackets = text_in_brackets
        # text_in_brackets = ''
        is_comment = False
        tokens.append({"less": "<"})
        number_of_brackets += 1
        text_in_brackets = text_in_brackets[4:]

    if text_in_brackets.endswith('-->'):
        tokens.append({"comment": text_in_brackets})
        text_in_brackets = ""
        is_comment = False


def between_brackets(input):
    global text_between_brackets
    text_between_brackets += input


def create_new_tokens():
    string_tag = ''
    for i in tokens:
        for key, value in i.items():
            if key == 'less':
                string_tag += value
            elif key == 'greater':
                string_tag += value
                if string_tag.startswith('<?'):
                    new_tokens.append({'question_tag': string_tag})
                elif string_tag != '<>':
                    new_tokens.append({'tag': string_tag})
                string_tag = ''
            elif key == 'in_brackets':
                value = re.sub(r'[ ][ ]+', ' ', value)
                value = re.sub(r'[ ]+=[ ]+"', '="', value)
                if space_around == '-t':
                    value = value.replace('="', ' = "')
                while value.startswith(' '):
                    value = value[1:]
                while value.endswith(' '):
                    value = value[:-1]
                if value.endswith('/'):
                    while value[:-1].endswith(' '):
                        value = value [:-2] + '/'
                if value.startswith('/'):
                    while value[1:].startswith(' '):
                        value = '/' + value[2:]
                string_tag += value
            elif key == 'between_brackets':
                value = re.sub(r'[ ][ ]+', ' ', value)
                while value.startswith(' '):
                    value = value[1:]
                while value.endswith(' '):
                    value = value[:-1]
                new_tokens.append({'between_tag': value})
            elif key == 'comment':
                new_tokens.append({'comment': value})
            elif key == 'doctype':
                new_tokens.append({'doctype': '<' + doctype + '>'})


def find_open_tag(value):
    s = ''
    for i in value:
        if i == ' ' or i == '>':
            break
        s += i
    return s


def find_close_tag(value):
    return value[0] + value[2:-1]


def find_some_tag(value):
    s = value[0]
    for i in range(2, len(value)):
        if i == ' ' or i == '>':
            break
        s += value[i]
    return s

def create_new_xml():
    global nesting_level
    global result_string
    for i in range(len(new_tokens)):
        for key, value in new_tokens[i].items():
            if key == 'tag':
                if i > 0 and value.startswith('</'):
                    for key_i, value_i in new_tokens[i - 1].items():
                        if key_i == 'tag' and result_string.endswith('\t'):
                            result_string = result_string[:-1]
                if i > 2 and value.startswith('</') and not result_string.endswith('\t') and not result_string.endswith('\n'):
                    for key_i, value_i in new_tokens[i - 1].items():
                        if key_i == 'tag':
                            if not value_i.startswith('</') and not value_i.endswith('/>'):
                                a = find_open_tag(value_i)
                                b = find_close_tag(value)
                                if a != b:
                                    result_string = result_string + '\n' + '\t' * (nesting_level - 1)
                            else:
                                result_string = result_string + '\n' + '\t' * (nesting_level - 1)
                        else:
                            for key_i_i, value_i_i in new_tokens[i - 2].items():
                                if key_i_i == 'tag':
                                    if not value_i_i.startswith('</') and not value_i_i.endswith('/>'):
                                        a = find_open_tag(value_i_i)
                                        b = find_close_tag(value)
                                        if a != b:
                                            result_string = result_string + '\n' + '\t' * (nesting_level - 1)
                                    else:
                                        result_string = result_string + '\n' + '\t' * (nesting_level - 1)

                result_string += value
                if not value.startswith('</') and not value.endswith('/>'):
                    nesting_level += 1
                elif value.startswith('</'):
                    nesting_level -= 1
                if len(new_tokens) > i + 1:
                    if not value.startswith('</') and not value.endswith('/>'):
                        for key_i, value_i in new_tokens[i + 1].items():
                            if key_i == 'tag':
                                if not value_i.startswith('</'):
                                    result_string += '\n' + '\t' * nesting_level
                    else:
                        for key_i, value_i in new_tokens[i + 1].items():
                            if key_i == 'tag':
                                result_string += '\n' + '\t' * nesting_level
                ####################
                aa = re.split(r'\n', result_string)
                for ii in range(len(aa) - 1, -1, -1):
                    if aa[ii].strip() != '':
                        if aa[ii].count('</') == 1 and aa[ii].count('<') == 1:
                            if not aa[ii].startswith('<'):
                                aa[ii] = aa[ii].replace('<', '\n' + '\t' * nesting_level + '<')
                                result_string = '\n'.join(aa)
                        break
                # if result_string.split('\n')[-1].count('</') == 1 and result_string.split('\n')[-1].count('<') == 1:
                #     if not result_string.split('\n')[-1].startswith('<'):
                #         k = result_string.split('\n')[-1]
                #         result_string = result_string[:len(result_string) - len(k)] + result_string.split('\n')[-1].replace('<', '\n' + '\t' * nesting_level + '<')


            if key == 'between_tag':
                value = value.replace('\n', '\n' + '\t' * nesting_level)
                if len(new_tokens) > i + 1:
                    for key_i, value_i in new_tokens[i + 1].items():
                        if key_i == 'tag' and value_i.startswith('</') and value.endswith('\t'):
                            value = value[:-1]
                result_string += value
            if key == 'comment':
                result_string += value
            if key == 'question_tag':
                result_string += value
            if key == 'doctype':
                value = re.sub(r'[ ][ ]+', ' ', value)
                value = value.replace('\n', '\n' + '\t' * (nesting_level + 1))
                result_string += value




def start_format(path_to_file):
    global result_string
    read_from_file(path_to_file)
    get_char_from_file()
    create_new_tokens()
    # print(tokens)
    # print(new_tokens)
    create_new_xml()
    # print(result_string)

if __name__ == '__main__':
    # global directory_path
    # global path_to_res
    # global indent
    # global blank_lines
    # global space_around
    # global space_in_empty_tag
    try:
        program_path, directory_path, path_to_res, indent, blank_lines, space_around, space_in_empty_tag = argv
        print("input path -> " + directory_path)#+
        print("output path -> " + path_to_res)#+
        print("indent -> " + indent)#+
        print("blank lines -> " + blank_lines)#+
        print("space around -> " + space_around)#+
        print("space in empty tag -> " + space_in_empty_tag)#+
        blank_lines = int(blank_lines)
        indent = int(indent)
    except:
        program_path, directory_path, path_to_res = argv
        print('Only basic formatting')
    start_format(directory_path)
    f = open(path_to_res + '/' + "formatted" + directory_path.split('/')[-1], 'w')
    if space_in_empty_tag == '-t':
        result_string = result_string.replace('/>', ' />')
    if indent != '':
        result_string = result_string.replace('\t', ' ' * indent)
    a = result_string.split('\n')
    for i in range(len(a)):
        if a[i].count('</') == 1 and a[i].count('<') == 1:
            if not a[i].strip().startswith('<'):
                a[i]
    f.write(result_string)
    f.close()
    find_errors(directory_path, path_to_res)