"# XMLCodeFormatter"
<br>
<br>
Paste your .xml code into the "resources/input.xml" file
<br>
<br>
Run the ReadFile.py without parameters
<br>
Program will create 2 files "resources/outputErrors.html" and "resources/outputFormattedCode.xml"
<br>
<br>
outputErrors.html will contain a list of errors for standard formatting
<br>
outputFormattedCode.xml will contain basic formatted .xml code
<br>
<br>
Run the ReadFile.py with parameters
<br>
Program will create 2 files "resources/outputErrors.html", "resources/outputFormattedCode.xml"
<br>
outputFormattedCode.xml will contain formatted .xml code with own parameters
<br>
<br>
example:
ReadFile.py 6 5 True True True
<br>
first parameter - indent, must be > 1
<br>
second parameter - keep blank lines, must be > 1
<br>
third parameter - space around =", must be "True" or "False"
<br>
forth parameter - space in empty tag, must be "True" or "False"
