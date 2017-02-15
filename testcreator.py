#!/usr/bin/python

import sys, re

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

testName = testName + "Test";
testFile = open(testName+".java", "w")
className = targetName[0].lower() + targetName[1:]

print(targetName)
for line in array:
	if re.match("package(.+)", line):
		testFile.write(line + "\n")
		testFile.write("import mockit.Mock;\nimport mockit.MockUp;\nimport mockit.Tested;\nimport mockit.Expectations;\nimport mockit.Verifications;\n" +
                        "import org.junit.Before;\nimport org.junit.Test;\n\nimport java.util.Date;\nimport java.util.HashSet;\n" +
                        "import java.util.Set;\nimport java.util.LinkedList;\n\n" +
                         "import static org.hamcrest.MatcherAssert.assertThat;\nimport static org.hamcrest.core.Is.is;\n\n")
		testFile.write("public class " + targetName + "Test { " + '\n\t@Tested\n\tprivate ' + targetName + " "
		        + className + ";\n\n\t@Before\n\tpublic void setup() " 
			+ " {\n\t\t" + className + " = new " + targetName + "();\n\t}\n\n")
	elif re.match("(\s+)(public)(\W)(static)(\W)(\w+)(\W)(\w+)(.+)({)", line):
		methodName = re.match("(\s+)(public)(\W)(static)(\W)(\w+)(\W)(\w+)(.+)({)", line).group(8)
		print(methodName)
		testFile.write("\t@Test\n\tpublic void " + methodName + "Test() {\n\t")
		testFile.write("\tnew Expectations() {{\n\n\t\t}};\n\n")
		testFile.write("\tnew Verifications() {{\n\n\t\t}};\n")
		testFile.write("\t}\n\n")
	elif re.match("(\s+)(public)(\W)(?!static)(\w+)(\W)(\w+)(.+)({)", line):
		methodName = re.match("(\s+)(public)(\W)(\w+)(\W)(\w+)(.+)({)", line).group(6)
		print(methodName)
		testFile.write("\t@Test\n\tpublic void " + methodName + "Test() {\n\t")
		testFile.write("\tnew Expectations() {{\n\n\t\t}};\n\n")
		testFile.write("\tnew Verifications() {{\n\n\t\t}};\n")
		testFile.write("\t}\n\n")

testFile.write("}\n");
testFile.close()