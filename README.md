"# XMLCodeFormatter"
<br>
<br>
<br>
Final version
<br>
Run FormatCode.py with 2 parameters, input directory and output, example:
<br>
python3 FormatCode.py /home/alex/IdeaProjects/testXML/test.xml /home/alex/IdeaProjects/testXML
<br>
Program will create 2 files in output directory "outputErrors.html" for basic formatting and "formatted'filename'.xml"
<br>
<br>
outputErrors.html will contain a list of errors

<br>
Run the ReadFile.py with 3 parameters: input directory, output, -c:
<br>
Go to the params.txt, change your parameters there
<br>
indent is a number, it must be >= 0
<br>
continuation indent is a number, it must be >= 0
<br>
blank lines is a number, it must be >= 0
<br>
space around =" can be "-t" True or "-f" False
<br>
space in empty tag cab be "-t" or "-f"
<br> 
indent in empty line can be "-t" or "-f"
<br>
space after tag can be "-t" or "-f"
<br>
keep white spaces can be "-t" or "-f"
<br>
wrap text can be "-t" or "-f"
<br>
keep line breaks in text can be "-t" or "-f"
<br>
Program will create 2 files in output directory "Errors.html" and "formatted'filename'.xml"
<br>
<br>
example:
python3 FormatCode.py /home/alex/IdeaProjects/testXML/test.xml /home/alex/IdeaProjects/testXML -o

