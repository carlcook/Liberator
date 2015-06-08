import sys
import fileinput
import re

externals = set()

def getExternalName(line):
	name = line[line.rfind('x_'):]
	name = name[:name.find(")")]
	index = name.find('"')
	if index > 0: name = name[:index]
	index = name.find("'")
	if index > 0: name = name[:index]
	return name

def checkLine(line):
	global externals
	if line.upper().startswith("USE_EXTERNAL") and line.find('\\libs') == -1:
		external = getExternalName(line)
		if external in externals:
			index = line.find(external)
			modifiedLine = line[:index] + external + '\\libs' + line[index + len(external):]
			return modifiedLine
		return line
	else:
		return line

# read list of externals
with open('externals') as f:
	externals = set(f.read().splitlines())

# edit toplevel makefile and add libs where appropriate
# note that stdout is redirected here
for i, line in enumerate(fileinput.input('CMakeFile.txt', inplace=1)):
	sys.stdout.write(checkLine(line))

# TODO walk sub directories and do the same
