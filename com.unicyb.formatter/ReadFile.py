import re

tokens = []
number_of_brackets = 0  # <  >
number_of_single_brackets = 0  # '  '
number_of_double_brackets = 0  # "  "
text_in_brackets = ""
text_between_brackets = ""
nesting_level = 0
result_string = ""
keywords_in_brackets = []


def read_from_file(file_name):
    return open(file_name).read()


def get_char_from_file(input_file):
    for i in input_file:
        parse(i)


def format_element_from_array(array):
    for i in array:
        create_formatted_text(i)


def parse(input):
    if input == "<":
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
            green_style()
            tokens.append({"in_brackets": text_in_brackets})
            tokens.append({"greater": ">"})
            text_in_brackets = ""
    elif number_of_brackets == 1:
        in_brackets(">")


def green_style():
    global text_in_brackets
    text_in_brackets = re.sub(r'[ ]+=', '=', text_in_brackets)
    text_in_brackets = re.sub(r'=[ ]+', '=', text_in_brackets)
    arr = re.findall(r'[=]["][\w\d\s\-\,.!]+["]', text_in_brackets)
    for i in arr:
        text_in_brackets = text_in_brackets.replace(i, '<span class="green">' + i + '</span>')
    arr = re.findall(r"[=]['][\w\d\s\-\,.!]+[']", text_in_brackets)
    for i in arr:
        text_in_brackets = text_in_brackets.replace(i, '<span class="green">' + i + '</span>')


def new_line():
    if number_of_single_brackets == 0 and number_of_double_brackets == 0:
        tokens.append({"NL": "<br>"})
    elif number_of_brackets == 1:
        in_brackets("<br>")


def in_brackets(input):
    global text_in_brackets
    global number_of_single_brackets
    global number_of_double_brackets
    if number_of_double_brackets == 1 and input == '"':
        number_of_double_brackets -= 1
    elif number_of_single_brackets == 0 and input == '"' and number_of_double_brackets == 0:
        number_of_double_brackets += 1
    if number_of_single_brackets == 1 and input == "'":
        number_of_single_brackets -= 1
    elif number_of_single_brackets == 0 and input == "'" and number_of_double_brackets == 0:
        number_of_single_brackets += 1

    text_in_brackets += input


def between_brackets(input):
    global text_between_brackets
    text_between_brackets += input


def create_formatted_text(dict):
    for token, value in dict.items():
        if token == "less":
            formatted_less()
        elif token == "greater":
            formatted_greater()
        elif token == "between_brackets":
            formatted_between_brackets(value)
        elif token == "in_brackets":
            formatted_in_brackets(value)
        elif token == "NL":
            formatted_new_line()


def formatted_less():
    global result_string
    # if len(result_string) > 6 and result_string[len(result_string) - 6:] == "&emsp;":
    result_string = re.sub(r'<br>(&emsp;)+[ ]*$', '<br>', result_string)
    i = result_string.rfind('<br>')
    b = False
    for j in range(i + 4, len(result_string) - 1):
        if result_string[j].isalnum():
            b = True
            break
    if not b:
        result_string += nesting_level * "&emsp;"
    result_string += '<span class="bracket"><</span>'


def formatted_greater():
    global result_string
    i = result_string.rfind('<br>')
    result_string = re.sub(r'<span class="bracket">></span><span class="bracket"><</span>',
                           '<span class="bracket">></span><br>' + (nesting_level - 1) * '&emsp;'
                           + '<span class="bracket"><</span>', result_string)

    result_string += '<span class="bracket">></span>'


def formatted_between_brackets(string):
    global result_string
    string = string.replace("\n", "<br>" + nesting_level * "&emsp;")
    result_string += string


def formatted_in_brackets(string):
    global result_string
    keyword = string.split(" ")[0]
    global nesting_level
    if not keyword.startswith("/") and not keyword.startswith("?") and not keyword.endswith("/"):
        nesting_level += 1
        keywords_in_brackets.append(keyword)
    elif keyword.startswith("/"):
        try:
            last_index = result_string.rindex("&emsp;")
            print(result_string[last_index:].count("<"))

            if result_string[last_index:].count("<") == 3:
                result_string = result_string[:last_index] + result_string[last_index + 6:]
        except:
            print("exception")
        nesting_level -= 1
        keywords_in_brackets.remove(keyword[1:])
    string = string.replace("\n", "<br>" + nesting_level * "&emsp;")
    result_string += string


def formatted_new_line():
    global result_string
    result_string += "\n" + nesting_level * "&emsp;" + "qqqqqqq"


if __name__ == '__main__':
    get_char_from_file(read_from_file('../resources/input.xml'))
    format_element_from_array(tokens)
    result_string = result_string.replace("\n", "<br>")
    result_string = result_string.replace("\t", "&emsp;")
    result_string = re.sub(r'[ ]+<span class="bracket">', '<span class="bracket">', result_string)
    result_string = re.sub(r'&emsp;[ ]+', '&emsp;', result_string)
    result_string = re.sub(r'&emsp;[ ]+', '&emsp;', result_string)
    result_string = re.sub(r'<br>&emsp;(<br>&emsp;)+', '<br>&emsp;<br>&emsp;', result_string)
    f = open("test.html", "w")
    result_string = '<!DOCTYPE html><html><head><link rel="stylesheet" href="styles.css"></head><body><p>' \
                    + result_string + '</p></body></html>'
    f.write(result_string)
    f.close()
    print(result_string)
