from com.unicyb.formatter.Errors import find_errors
from com.unicyb.formatter.OwnFormatCode import start_own_format

from sys import argv
path_to_file = ''
path_to_output = ''

def read_argv():
    global path_to_file
    global path_to_output
    try:
        script, path_to_file, path_to_output, first, second, third, forth, fifth = argv
        print("indent: ", int(first))
        print("keep blank lines: ", int(second))
        print('spaces around "=" attribute: ', third)
        print("space after tag name: ", forth)
        print("space in empty tag: ", fifth)
        if int(first) > 1 and int(second) > 1 and (third == 'True' or third == 'False') and (
                forth == 'True' or forth == 'False') and (fifth == 'True' or fifth == 'False'):
            start_own_format(first, second, third, forth, fifth, path_to_file, path_to_output)
        else:
            print('\n\nERROR\nindent > 1\nkeep blank lines > 1\nspaces around "True" or "False"\nspace after "True" or "False"\nspace in "True" or "False"')
            raise Exception
    except:
        script, path_to_file, path_to_output = argv
        start_own_format('4', '2', "False", "False", "False", path_to_file, path_to_output)
        print('Exception, arguments not valid, only basic formatting')



def status():
    print('program worked correctly')


if __name__ == '__main__':
    read_argv()
    find_errors(path_to_file, path_to_output)
