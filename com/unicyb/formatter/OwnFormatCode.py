from com.unicyb.formatter.FormatCode import start_format
from com.unicyb.formatter.FormatCode import read_from_file

import re

# indent = 4 - done
# keep blank lines = 2
# space around =" in attribute - done
# space after tag name - done
# space in empty tag - done

input_string = start_format()


def space_after_in_tag_name(space_after, space_in):
    global input_string

    text_in_brackets = re.findall(r'<[^<]+>', input_string)
    for i in text_in_brackets:
        if '!' not in i and '?' not in i:
            if space_after == 'True':
                if i[:-1].endswith('/'):
                    input_string = input_string.replace(i, i[:-2] + ' />')
                else:
                    input_string = input_string.replace(i, i[:-1] + ' >')
            elif space_in == 'True' and space_after == 'False':
                if i[:-1].endswith('/'):
                    input_string = input_string.replace(i, i[:-2] + ' />')


def format_input():
    global input_string
    input_string = input_string.replace('<span class="bracket">', '')
    input_string = input_string.replace('</span>', '')
    input_string = input_string[84:-18]
    input_string = input_string.replace('&lt;', '<')
    input_string = input_string.replace('&gt', '>')
    input_string = input_string.replace('<br>', '\n')


def reformat_input():
    global input_string
    i = 0
    while i <= len(input_string) - 1:
        k = input_string[i]
        if input_string[i] == '<':
            input_string = input_string[:i] + '<span class="bracket">&lt;</span>' + input_string[i + 1:]
            i += len('<span class="bracket">&lt;</span>') - 1
        elif input_string[i] == '>':

            input_string = input_string[:i] + '<span class="bracket">&gt</span>' + input_string[i + 1:]
            i += len('<span class="bracket">&gt</span>') - 1
        i += 1
    input_string = input_string.replace('\n', '<br>')


def indent_in_text(indent):
    global input_string
    input_string = input_string.replace('&emsp;', int(indent) * '&nbsp;')


def space_around_attribute(space_around):
    global input_string
    if space_around == 'True':
        input_string = input_string.replace('="', ' = "')


def keep_blank_lines(read_input, blank_lines):
    global input_string
    arr = re.findall(r'[\n][\n]+', read_input)
    input_string = re.sub('(&emsp;)*[\n]', '\n', input_string)
    arr1 = re.findall(r'[\n]{2,}', input_string)
    index = 0
    for i in arr:
        if len(i) > 2:
            k = len(i)
            index = index + input_string[index:].find('\n\n\n')
            s = min(len(i), int(blank_lines) + 1)
            input_string = input_string[:index] + min(len(i), int(blank_lines) + 1) * '\n' + input_string[index + 3:]
            index += min(len(i), int(blank_lines) + 1)

            ################################


def start_own_format(indent, blank_lines, space_around, space_after, space_in):
    global input_string
    format_input()
    space_after_in_tag_name(space_after, space_in)
    keep_blank_lines(read_from_file('../../../resources/input.xml'), blank_lines)

    indent_in_text(indent)
    space_around_attribute(space_around)
    reformat_input()
    input_string = input_string.replace('<span class="bracket">&gt</span>', '>')
    input_string = input_string.replace('<span class="bracket">&lt;</span>', '<')
    input_string = input_string.replace('&nbsp;', ' ')
    input_string = input_string.replace('<br>', '\n')
    while input_string.startswith('\n'):
        input_string = input_string[1:]
    input_string = input_string.replace('msp;', '')
    input_string = re.sub((int(blank_lines) + 1) * '[\n]' + '[\n]+', (int(blank_lines) + 1) * '\n', input_string)
    if space_in == 'False':
        input_string = re.sub(r'[ ]+[/][>]', '/>', input_string)
    arr = input_string.split('\n')
    left = 0
    right = 0
    l = 0
    r = 0
    for i in range(0, len(arr) - 1):
        if left != right:
            if l == r:
                arr[i] = int(indent) * (left - right) * ' ' + int(indent) * ' ' + arr[i]
            # else:
            #     arr[i] = int(indent) * (left - right) * ' ' + arr[i]
        left += arr[i].count('<')
        right += arr[i].count('>')
        l += arr[i].count('<!--')
        r += arr[i].count('-->')

    input_string = '\n'.join(arr)

    f = open("../../../resources/outputFormattedCode.xml", "w")
    f.write(input_string)
    f.close()
