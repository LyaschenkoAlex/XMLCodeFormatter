tokens = []
number_of_brackets = 0  # <  >
number_of_single_brackets = 0  # '  '
number_of_double_brackets = 0  # "  "
text_in_brackets = ""
text_between_brackets = ""
nesting_level = ""


def read_from_file(file_name):
    return open(file_name).read()


def get_char_from_file(input_file):
    for i in input_file:
        parse(i)


def get_element_from_array(array):
    for i in array:
        create_formatted_text(i)


def parse(input):
    if input == "<":
        less()
    elif input == ">":
        greater()
    elif input == "\n" and number_of_brackets == 1:
        new_line()
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


# def create_formatted_text():
#


if __name__ == '__main__':
    get_char_from_file(read_from_file('../resources/input.xml'))
    for i in tokens:
        for key in i:
            print(key, '->', i[key])
