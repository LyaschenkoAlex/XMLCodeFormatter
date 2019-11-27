# переход на новую строку > 3 done
import re

# wrong blank lines
ans = []


def find_new_lines(directory_path):
    f = open(directory_path, 'r')
    text = f.read()
    wrong_blank_lines = re.findall(r'[\n][\n][\n][\n]+', text)
    for_wrong = text
    for i in range(len(wrong_blank_lines) - 1, -1, -1):
        index = for_wrong.rfind(wrong_blank_lines[i])
        for_wrong = for_wrong[:index]
        line = for_wrong.count('\n')
        ans.append({'dark': 'line ' + str(line + 2) + ' -&gt; ' + "too much new lines"})


def find_wrong_tab(directory_path):
    f = open(directory_path, 'r')
    text = f.read()
    nesting_level = 0
    arr = text.split('\n')

    for i in range(0, len(arr)):
        a = False
        p = 0
        c = False
        arr_right = re.findall('[^>]>', arr[i])
        arr_left = re.findall('<[^>]', arr[i])
        for j in arr_left:
            if j[1] == '/':
                p -= 1
            elif j[1].isalpha():
                p += 1
                c = True
        if p > 0:
            a = True
        if not a:
            nesting_level += p
        if (len(arr[i]) - len(arr[i].lstrip()) != nesting_level * 4 and len(arr[i]) - len(arr[i].lstrip()) != (
                nesting_level + 1) * 4) and len(arr[i].lstrip()) != 0:
            ans.append({'warning': 'line ' + str(i + 1) + ' -&gt; ' + "wrong tab"})
            # print(len(arr[i]), len(arr[i].lstrip()), nesting_level * 4)
        if a:
            nesting_level += p
        for j in arr_right:
            if j[0] == '/':
                nesting_level -= 1


def find_tag_on_new_line(directory_path):
    f = open(directory_path, 'r')
    text = f.read()
    arr = text.split('\n')
    for line in range(0, len(arr)):
        arr_new = re.findall(r'<[^<]+', arr[line])
        for i in range(0, len(arr_new) - 1):
            last = arr_new[len(arr_new) - 1]
            if last.endswith('>') and not last.startswith('</'):
                ans.append({'primary': 'line ' + str(line + 1) + ' -&gt; ' + "tag must be on the next line"})
                break
            if arr_new[i].endswith('>'):
                first = arr_new[i][1:].split(' ')[0]
                if first.endswith('>'):
                    first = first[:-1]
                second = arr_new[i][2:-1]
                if first != second:
                    ans.append({'primary': 'line ' + str(line + 1) + ' -&gt; ' + "tag must be on the next line"})


def find_errors(directory_path, path_to_res):
    find_new_lines(directory_path)
    find_wrong_tab(directory_path)
    find_tag_on_new_line(directory_path)
    f = open(path_to_res + '/Errors.html', "w")
    f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Bootstrap Example</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
</head>
<body>''')
    f.write('<ul class="list-group">')
    for i in ans:
        for key, value in i.items():
            if key == 'warning':
                f.write('<li class="list-group-item list-group-item-warning">')
                f.write(value)
                f.write('</li>')
            elif key == 'primary':
                f.write('<li class="list-group-item list-group-item-primary">')
                f.write(value)
                f.write('</li>')
            elif key == 'dark':
                f.write('<li class="list-group-item list-group-item-dark">')
                f.write(value)
                f.write('</li>')
    f.write('</ul>')
    f.write('</body>')


