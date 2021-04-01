# HTMLTestRunner

HTMLTestRunner for python unit test

A TestRunner for use with the Python unit testing framework. It generates a HTML report to show the result at a glance.
The simplest way to use this is to invoke its main method. E.g. import unittest from HTMLTestRunner.runner import
HTMLTestRunner ... define your tests ... For more customization options, instantiates a HTMLTestRunner object.
HTMLTestRunner is a counterpart to unittest's TextTestRunner. E.g.

# Creating suite

my_test_suite = unittest.TestSuite()

# output to a file

runner = HTMLTestRunner(
title='My unit test', open_in_browser=True
)

# run the test

runner.run(my_test_suite)