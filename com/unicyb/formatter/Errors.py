import re
from com.unicyb.formatter.FormatCode import read_from_file

input_file = ""


# переход на новую строку > 3 done
# неправильные пробелы внутри тега  done
#  = "fwef" inside tag
# ajojirjf<fjoiwej>
# <> fwjoe  fweio <>
# неправельная табуляция
# <><>

def check_new_lines():
    tmp_input_file = input_file
    arr_new_line = re.findall(r"[\n][\n][\n][\n]+", tmp_input_file)
    ans_arr = []
    for i in range(len(arr_new_line) - 1, -1, -1):
        ans_arr.append('<span class="check_NL">line - ' + str(
            tmp_input_file[:tmp_input_file.rfind(arr_new_line[i])].count('\n') + 2) +
                       ' -> too many NL in a row, max - 3</span>')
        tmp_input_file = tmp_input_file[:tmp_input_file.rfind(arr_new_line[i])]
    read_to_file('<!DOCTYPE html><html><head><link rel="stylesheet" href="styles.css"></head><body><p>' + "<br>".join(
        ans_arr[::-1]), "w")


def wrong_spaces_inside_tag():
    tmp_input_file = input_file
    arr_inside_tags = re.findall(r"<[^<]+>", tmp_input_file)
    ans_arr = []
    for i in range(len(arr_inside_tags) - 1, -1, -1):

        str_tag = arr_inside_tags[i]
        if str_tag != str_tag.strip() or str_tag != str_tag.replace("  ", " "):
            str_replaced = str_tag.replace("<", "&lt;")
            str_replaced = str_replaced.replace(">", "&gt;")
            str_replaced = str_replaced.replace(" ", "&nbsp;")
            str_ans = '<span class="inside_tag">line - ' + str(
                tmp_input_file[:tmp_input_file.rfind(arr_inside_tags[i])].count('\n') + 1) + \
                      ' -> inside tag &lt;...&gt; wrong whitespaces (' + str_replaced + ')</span>'
            print(tmp_input_file.rfind(arr_inside_tags[i]))
            print(arr_inside_tags[i])
            print(tmp_input_file[:tmp_input_file.rfind(arr_inside_tags[i])].count('\n'))
            ans_arr.append(str_ans)
            tmp_input_file = tmp_input_file[:tmp_input_file.rfind(arr_inside_tags[i])]
    read_to_file("<br>" + "<br>".join(ans_arr[::-1]), "a+")


def read_to_file(result_string, state):
    f = open("../../../resources/errors.html", state)
    f.write(result_string)
    f.close()


def find_errors():
    global input_file
    input_file = read_from_file('../../../resources/input.xml')
    check_new_lines()
    wrong_spaces_inside_tag()
    read_to_file('</p></body></html>', "a+")
