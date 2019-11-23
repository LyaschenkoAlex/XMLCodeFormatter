import re
from com.unicyb.formatter.FormatCode import read_from_file

input_file = ""


# переход на новую строку > 3 done
# неправильные пробелы внутри тега  done
#  = "fwef" inside tag done
# ajojirjf<fjoiwej> done
# неправильная табуляция
# <><><> done

def check_new_lines(path_to_output):
    tmp_input_file = input_file
    arr_new_line = re.findall(r"[\n][\n][\n][\n]+", tmp_input_file)
    ans_arr = []
    for i in range(len(arr_new_line) - 1, -1, -1):
        ans_arr.append('<span class="check_NL"><span class="line">line - ' + str(
            tmp_input_file[:tmp_input_file.rfind(arr_new_line[i])].count('\n') + 2) +
                       '</span> -> too many NL in a row, max - 3</span>')
        tmp_input_file = tmp_input_file[:tmp_input_file.rfind(arr_new_line[i])]
    read_to_file('<!DOCTYPE html><html><head><link rel="stylesheet" href="styles.css"></head><body><p>' + "<br>".join(
        ans_arr[::-1]), "w", path_to_output)


def wrong_spaces_inside_tag(path_to_output):
    tmp_input_file = input_file
    arr_inside_tags = re.findall(r"<[^<]+>", tmp_input_file)
    ans_arr = []
    for i in range(len(arr_inside_tags) - 1, -1, -1):

        str_tag = arr_inside_tags[i]
        if str_tag != str_tag.strip() or str_tag != str_tag.replace("  ", " "):
            str_replaced = str_tag.replace("<", "&lt;")
            str_replaced = str_replaced.replace(">", "&gt;")
            str_replaced = str_replaced.replace(" ", "&nbsp;")
            str_ans = '<span class="inside_tag"><span class="line">line - ' + str(
                tmp_input_file[:tmp_input_file.rfind(arr_inside_tags[i])].count('\n') + 1) + \
                      ' -> </span> inside tag &lt;...&gt; wrong whitespaces (' + str_replaced + ')</span>'
            ans_arr.append(str_ans)
            tmp_input_file = tmp_input_file[:tmp_input_file.rfind(arr_inside_tags[i])]
    read_to_file("<br>" + "<br>".join(ans_arr[::-1]), "a+", path_to_output)


def equal_sign(path_to_output):
    tmp_input_file = input_file
    arr_inside_tags = re.findall(r"<[^<]+>", tmp_input_file)
    ans_arr = []

    for i in range(len(arr_inside_tags) - 1, -1, -1):
        arr_inside_tags_whitespace_after = re.findall(r"=[ ]+", arr_inside_tags[i])
        arr_inside_tags_whitespace_before = re.findall(r"[ ]+=", arr_inside_tags[i])
        if len(arr_inside_tags_whitespace_before) or len(arr_inside_tags_whitespace_after):
            str_tag = arr_inside_tags[i]
            index = tmp_input_file.rfind(str_tag)
            tmp_input_file = tmp_input_file[:index]
            num_line = tmp_input_file[:index].count('\n')
            str_tag = str_tag.replace('<', '&lt;')
            str_tag = str_tag.replace('>', '&gt;')
            str_tag = str_tag.replace(' ', '&nbsp;')
            str_ans = '<span class="equal"> <span class="line">line - ' + str(
                num_line + 1) + '</span> -> after and before equal sign should not be whitespace (' + str_tag + ')</span>'
            ans_arr.append(str_ans)
    read_to_file("<br>" + "<br>".join(ans_arr[::-1]), "a+",path_to_output)


def count_tags_in_line(path_to_output):
    tmp_input_file = input_file
    arr_new_line = input_file.split('\n')
    ans_arr = []
    for i in range(len(arr_new_line) - 1, - 1, - 1):
        tmp_input_file = tmp_input_file[:tmp_input_file.rfind(arr_new_line[i]) + len(arr_new_line[i])]
        arr_tags = re.findall(r"<[^<]+>", arr_new_line[i])
        cnt = 0
        for j in arr_tags:
            if j[1:].startswith('!'):
                cnt += 1
        if len(arr_tags) - cnt > 2:
            arr_new_line[i] = arr_new_line[i].replace('<', '&lt;')
            arr_new_line[i] = arr_new_line[i].replace('>', '&gt;')
            arr_new_line[i] = arr_new_line[i].strip()
            arr_new_line[i] = arr_new_line[i].replace(' ', '&nbsp;')
            str_ans = '<span class="count_tags"> <span class="line">line - ' + str(
                i + 1) + ' -&gt;</span> too much tags in one line, MAX - 2 (' + \
                      arr_new_line[i] + ')</span>'
            ans_arr.append(str_ans)
    read_to_file("<br>" + "<br>".join(ans_arr[::-1]), "a+", path_to_output)


def teg_on_next_line(path_to_output):
    tmp_input_file = input_file
    arr_new_line = input_file.split('\n')
    ans_arr = []
    for i in range(len(arr_new_line) - 1, - 1, - 1):
        tmp_input_file = tmp_input_file[:tmp_input_file.rfind(arr_new_line[i]) + len(arr_new_line[i])]
        arr_tags = re.findall(r"<[^<]+>", arr_new_line[i])
        cnt = 0
        for j in arr_tags:
            if j[1:].startswith('!'):
                cnt += 1
        if len(arr_tags) == 1 and '!' not in arr_tags[0]:
            if arr_new_line[i][:arr_new_line[i].find('<')].replace(' ', '') != '':
                index_NL = tmp_input_file[:tmp_input_file.rfind(arr_new_line[i])].count('\n')
                arr_new_line[i] = arr_new_line[i].replace('>', '&gt;')
                arr_new_line[i] = arr_new_line[i].replace('<', '&lt;')
                arr_new_line[i] = arr_new_line[i].replace(' ', '&nbsp;')
                arr_new_line[i] = arr_new_line[i][arr_new_line[i].find('&lt;'):]
                str_ans = '<span class = "teg_next_line"><span class="line">line - ' + str(
                    index_NL + 1) + ' -&gt; </span>' + arr_new_line[i] + ' - should be on the next line</span>'
                ans_arr.append(str_ans)
    read_to_file("<br>" + "<br>".join(ans_arr[::-1]), "a+", path_to_output)


def wrong_tab(path_to_output):
    tmp_input_file = input_file
    nesting_level = 0
    ans_arr = []
    arr_new_line = input_file.split('\n')
    arr_tags = []
    for i in range(0, len(arr_new_line)):
        nesting_level_upd = nesting_level
        if arr_new_line[i].lstrip()[1:].startswith('/'):
            nesting_level_upd -= 1
        if (nesting_level_upd * 4) * ' ' + arr_new_line[i].lstrip() != arr_new_line[i] and arr_new_line[i] != '':
            str_ans = '<span class="wrong_tab"><span class="line">line - ' + str(i + 1) + ' -&gt; </span> wrong tab!'
            ans_arr.append(str_ans)
        for j in re.findall(r"<[^<!?]+>", arr_new_line[i]):
            tag = j
            tag = tag.replace('<', '')
            tag = tag.replace('>', '')
            if tag.startswith('/'):
                nesting_level -= 1
            elif not tag.endswith('/') and not tag.startswith('!') and not tag.startswith('?'):
                nesting_level += 1

    read_to_file("<br>" + "<br>".join(ans_arr), "a+", path_to_output)


def read_to_file(result_string, state, path_to_output):
    f = open(path_to_output + '/' + "outputErrors.html", state)
    f.write(result_string)
    f.close()


def find_errors(path_to_file, path_to_output):
    global input_file
    input_file = read_from_file(path_to_file)
    check_new_lines(path_to_output)
    wrong_spaces_inside_tag(path_to_output)
    equal_sign(path_to_output)
    count_tags_in_line(path_to_output)
    teg_on_next_line(path_to_output)
    wrong_tab(path_to_output)
    read_to_file('</p></body></html>', "a+", path_to_output)
