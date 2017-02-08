
JMockit Test Coverage Generator
==============================

This script takes in the name of a java class from the command line and generates
a JMockit test class. Generates testing of standard getter and setter methods using JMockit and hamcrest. If targeting a directory structure with a "main" directory, will create the test class in the appropriate "test" directory. Otherwise the test class will be created in the directory from which the script is run. 

Assumes correct coding conventions, IE private class variables and public
getters and setters named appropriately. For example a private int number would
have public getter and setter getNumber() and setNumber(int newNumber).

Only tested on *nix systems, because why are you writing code in Windows?

### To execute use:

    python testcreator.py [name of Java class]
