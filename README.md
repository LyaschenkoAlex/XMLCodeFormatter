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
Run the ReadFile.py with 6 parameters, input directory, output, indent, blank lines, space around =" and space in empty tag:
<br>
indent is a number, it must be >= 0
<br>
blank lines is a number, it must be >= 0
<br>
space around =" can be "-t" True or "-f" False
<br>
space in empty tag cab be "-t" or "-f"
<br> 
Program will create 2 files in output directory "Errors.html" and "formatted'filename'.xml"
<br>
<br>
example:
python3 FormatCode.py /home/alex/IdeaProjects/testXML/test.xml /home/alex/IdeaProjects/testXML 10 1 -t -t

