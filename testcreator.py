#!/usr/bin/python

import sys
import re

def create_test(method_name):
	testFile.write("\t@Test\n\tpublic void " + method_name + "Test() {\n" +
		"\t\tnew MockUp<>() {\n\t\t\t@Mock\n\t\t};\n\n" +
		"\t\tnew Expectations() {{\n\n\t\t}};\n\n" +
		"\t\tassertThat(,is());\n\n" +
		"\t\tnew Verifications() {{\n\n\t\t}};\n" +
		"\t}\n\n")

targetName = sys.argv[1]
if re.match("(.+)\.java", targetName):
	targetName = targetName[0:targetName.index(".")]

with open(targetName + ".java", "r") as lines:
	array = list()
	for line in lines:
		array.append(line)

testName = targetName
if re.match("(.+)/(.+)", targetName):
	if re.match("(.+)(\W)(main)(\W)(.+)", targetName):
		testName = targetName.replace("/main/", "/test/")
	targetName = re.match("(.+)/(.+)", targetName).group(2)

testName = testName + "Test"
testFile = open(testName+".java", "w")
className = targetName[0].lower() + targetName[1:]

print(targetName)
for line in array:
	if re.match("package(.+)", line):
		testFile.write(line + "\n")
		testFile.write("import mockit.Mock;\nimport mockit.MockUp;\nimport mockit.Mocked;\nimport mockit.Tested;\nimport mockit.Expectations;\nimport mockit.Deencapsulation;\n" +
			"import mockit.Verifications;\nimport org.junit.Before;\nimport org.junit.Test;\n\nimport java.util.Date;\n" +
			"import java.util.Map;\nimport java.util.HashMap;\nimport java.util.HashSet;\nimport java.util.Set;\n" +
			"import java.util.LinkedList;\nimport java.util.List;\n\nimport static org.hamcrest.MatcherAssert.assertThat;\n"+
			"import static org.hamcrest.core.Is.is;\nimport static org.hamcrest.Matchers.nullValue;\n\n")
		testFile.write("public class " + targetName + "Test { " + '\n\t@Tested\n\tprivate ' + targetName + " "
		        + className + ";\n\n\t@Before\n\tpublic void setup() " 
			+ " {\n\t\t" + className + " = new " + targetName + "();\n\t}\n\n")
	elif re.match("(\s+)?(.+)(public)(\s)(boolean)(\s)(equals)(.+)(\n)?(.+)({)", line):
		testFile.write("\t@Test\n\tpublic void equalsSelf() {\n\t\tassertThat(" + className +
			".equals(" + className + "), is(true));\n\t}\n\n\t@Test\n\tpublic void equalsWrongClass() {" +
			"\n\t\tassertThat(" + className + ".equals(new String()), is(false));\n\t}\n\n\t@Test\n\tpublic void equalsNull() {\n\t\tassertThat(" 
				+ className + ".equals(null), is(false));\n\t}\n\n\t@Test\n\tpublic void equalsOther() {\n\t\t"
			+ targetName + " " + className + "1 = new " + targetName + "();\n\n\t\tassertThat(" + className + ".equals(" + className + "1), is(true));\n\t}\n\n\t")
	elif re.match("(\s+)?(public|protected)(\W)(static)(\W)(\w+)(\W)(\w+)(.+)(\n)?(.+)({)", line, re.MULTILINE):
		methodName = re.match("(\s+)?(public|protected)(\W)(static)(\W)(\w+)(\W)(\w+)(.+)(\n)?(.+)({)", line, re.MULTILINE).group(8)
		print(methodName)
		create_test(methodName)
	elif re.match("(\s+)?(public|protected)(\W)(?!static)(?!enum)(?!class)(\w+)(\W)(\w+)(.+)(\n)?(.+)({)", line, re.MULTILINE):
		methodName = re.match("(\s+)?(public|protected)(\W)(?!static)(?!enum)(?!class)(\w+)(\W)(\w+)(.+)(\n)?(.+)({)", line, re.MULTILINE).group(6)
		print(methodName)
		create_test(methodName)
	elif re.search("(\s+)(if)(.+)(\n)?(.+)({)", line, re.MULTILINE):
		print(methodName + " if branch")
		create_test(methodName + "IfBranch")

testFile.write("}\n")
testFile.close()
