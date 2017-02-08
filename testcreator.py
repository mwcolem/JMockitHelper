#!/usr/bin/python

import sys;
import re;

targetName = sys.argv[1]
if (re.match("(.+)\.java", targetName)):
	targetName = targetName[0:targetName.index(".")]

with open(targetName + ".java", "r") as lines:
	array = list()
	for line in lines:
		array.append(line)

testName = targetName
if (re.match("(.+)/(.+)", targetName)):
	if (re.match("(.+)(\W)(main)(\W)(.+)", targetName)):
		testName = targetName.replace("/main/", "/test/")
	targetName = re.match("(.+)/(.+)", targetName).group(2)

testName = testName + "Test";
testFile = open(testName+".java", "w")
className = targetName[0].lower() + targetName[1:]

print testName
for line in array:
	if (re.match("package(.+)", line)):
		testFile.write(line + "\n")
		testFile.write("import mockit.Mock;\nimport mockit.MockUp;\nimport mockit.Tested;\nimport mockit.Verifications;\n" +
                        "import org.junit.Before;\nimport org.junit.Test;\n\nimport java.util.Date;\nimport java.util.HashSet;\n" +
                        "import java.util.Set;\nimport java.util.LinkedList;\n\n" +
                         "import static org.hamcrest.MatcherAssert.assertThat;\nimport static org.hamcrest.core.Is.is;\n\n")
		testFile.write("public class " + targetName + "Test { " + '\n\t@Tested\n\tprivate ' + targetName + " "
		        + className + ";\n\n\t@Before\n\tpublic void setup() " 
			+ " {\n\t\t" + className + " = new " + targetName + "();\n\t}\n\n")
	elif (re.match("(\s+)private", line)):	
		variableType = re.search('(\s+)?private( static)?( transient)?( final)?(\W)(\S+)(\[\])?(\W\w+\W)?(\W)?(\w+)(\W)?(\s=(.+))?', line).group(6)
		variable = re.search('(\s+)?private( static)?( transient)?( final)?(\W)(\S+)(\[\])?(\W\w+\W)?(\W)?(\w+)(\W)?(\s=(.+))?', line).group(10)
		variable = variable[0].capitalize() + variable[1:]
		print variableType
		print variable
		testFile.write("\t@Test\n\tpublic void test" + variable + "Methods() {\n\t\t")
		if (variableType=="int" or variableType=="Integer"):
			testFile.write(className + ".set" + variable + "(1);\n\t")
		elif (variableType=="double" or variableType=="Double"):
			testFile.write(className + ".set" + variable + "(1.0);\n\t")
		elif (variableType=="String"):
			testFile.write("String testText = \"testText\";\n\t\t")
			testFile.write(className + ".set" + variable + "(testText);\n\t")
		elif (variableType=="long" or variableType=="Long"):
			testFile.write(className + ".set" + variable + "(1l);\n\t")
		elif (variableType=="boolean" or variableType=="Boolean"):
			testFile.write(className + ".set" + variable + "(true);\n\t")
		elif (re.match('List(\W)(\S+)(\W)',variableType)):
			objectListed = re.match('List(\W)(\S+)(\W)',variableType).group(2)
			testFile.write("LinkedList<" + objectListed + "> testList = new LinkedList<>();\n\t\t") 
			testFile.write("testList.add(new " + objectListed + "());\n\t\t")
			testFile.write(className + ".set" + variable + "(testList);\n\t")
		elif (re.match('Set(\W)(\S+)(\W)',variableType)):
			objectListed = re.match('Set(\W)(\S+)(\W)',variableType).group(2)
			testFile.write("Set<" + objectListed + "> testSet = new HashSet<>();\n\t\t") 
			testFile.write("testSet.add(new " + objectListed + "());\n\t\t")
			testFile.write(className + ".set" + variable + "(testSet);\n\t")
		else:
			testVar = "test" + variable[0].capitalize() + variable[1:]
			testFile.write(variableType[0].capitalize() + variableType[1:] + " " + testVar + " = new ")
			testFile.write(variableType[0].capitalize() + variableType[1:] + "();\n\t\t")
			testFile.write(className + ".set" + variable + "(" + testVar + ");\n\t")
		testFile.write("\tassertThat(" +  className + ".get" + variable + "(), is());\n\t")
		testFile.write("}\n\n")

testFile.write("}\n");
testFile.close()
