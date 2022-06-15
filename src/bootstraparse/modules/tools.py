"""
List of tools for testing
=========================

Usage:
 - from bootstraparse.modules.tools import __GLk, __GL, find_*_in_file
 - __GLk(n) # Returns a file link n traceback objects back
 - __GL() # Returns a line number at current position
 -  find_*_in_file(file)  # Try to find (class, function or variable) in file and return its line number
"""

import inspect
import os
import re


###############################################################################
# Dictionary checks
########################################

def dict_check(dic, *args):
    """
    Helper function to test existence of a list of succesive keys within a nested dictionary.
    :param dic: The dictionary of dictionaries to check
    :param args: Any number of keys to check the dictionaries for
    :type dic: dict | config.ConfigLoader
    :type args: str
    :return: A table of Booleans for every key checked.
    """
    output = [False for _ in args]
    for i in range(len(args)):
        if args[i] in dic:
            output[i] = True
            dic = dic[args[i]]
        else:
            break
    return output


def str_dict_check(dic, *args):
    """
    Helper function to test existence within a dictionary and return a string of the values of the keys checked
    and wether they exist.
    'arg[0]' : True or False
    :param dic: The nested dictionary to check
    :param args: Any number of keys to check successively
    :type dic: dict
    :type args: str
    :return: A string of the values of the keys checked and wether they exist.
    :rtype: str
    """
    out = dict_check(dic, *args)
    return "\n".join([f"{args[i]}: {out[i]}" for i in range(len(out))])


###############################################################################
# Paths
########################################
def __base():
    """
    Return the path of the main module (relative to the tests)
    :return: Path of the main module
    :rtype: str
    """
    return "."


def __module_path(module_name):
    """
    Return the path of the module module_name
    :param module_name: Name of the module
    :type module_name: str
    :return: Path of the module
    :rtype: str
    """
    return os.path.normpath(os.path.join(os.path.dirname(__file__), __base(), module_name))


###############################################################################
# Frame inspection
########################################
# Cursed frame inspection
def __prev_stack(nb=0):  # pragma: no cover (Cursed frame inspection)
    """
    Return the nth previous stack
    :return: Previous stack
    :rtype: inspect.Traceback
    """
    for frame in inspect.stack()[1 + nb:]:
        return frame
    return inspect.getframeinfo(inspect.currentframe().f_back)


def __GL():  # pragma: no cover (Cursed frame inspection)
    return __prev_stack().lineno


def __GFu():  # pragma: no cover (Cursed frame inspection)
    return __prev_stack().function


def __GFi():  # pragma: no cover (Cursed frame inspection)
    return __prev_stack().filename


def __GLk(n=2):  # pragma: no cover (Cursed frame inspection)
    return f' File "{__prev_stack(n).filename}", line {max(__prev_stack(n).lineno, 1)}'.replace("\\", "/")


###############################################################################
# Code inspection
########################################
def find_string_in_file(file_path, list_regex_to_find):  # pragma: no cover (Cursed code inspection)
    """
    Find the string in the file stream
    :param file_path: Path of the file
    :type file_path: str
    :param list_regex_to_find: List of string to find
    :type list_regex_to_find: list
    :return: Dict of string found and line number
    :rtype: dict
    """
    dict_string_found = {}
    list_regex_to_find_left = [string for string in list_regex_to_find]
    with open(file_path, "r") as file:
        for line_number, line in enumerate(file):
            for string_number, regex_to_find in enumerate(list_regex_to_find_left):
                match = regex_to_find.search(line)
                if match:
                    dict_string_found[match.group(1)] = line_number + 1
                    list_regex_to_find_left.pop(string_number)
                    break
            if not list_regex_to_find_left:
                break
    if list_regex_to_find_left:
        print("String not found: " + str(list_regex_to_find_left))
    return dict_string_found


def find_functions_in_file(file_path, list_function_name):  # pragma: no cover (Cursed code inspection)
    """
    Find the function in the file stream
    :param file_path: Path of the file
    :type file_path: str
    :param list_function_name: List of function name to find
    :type list_function_name: iterable
    :return: Dict of function found and line number
    :rtype: dict
    """
    return find_string_in_file(file_path, [re.compile(f"$def ({function_name})") for function_name in list_function_name])  # noqa


def find_classes_in_file(file_path, list_class_name):  # pragma: no cover (Cursed code inspection)
    """
    Find the class in the file stream
    :param file_path: Path of the file
    :type file_path: str
    :param list_class_name: List of class name to find
    :type list_class_name: iterable
    :return: Dict of class found and line number
    :rtype: dict
    """
    return find_string_in_file(file_path, [re.compile(f"^class ({class_name})") for class_name in list_class_name])


def find_variables_in_file(file_path, list_variable_name):  # pragma: no cover (Cursed code inspection)
    """
    Find the variable in the file stream
    :param file_path: Path of the file
    :type file_path: str
    :param list_variable_name: List of variable name to find
    :type list_variable_name: iterable
    :return: Dict of variable found and line number
    :rtype: dict
    """
    return find_string_in_file(file_path, [re.compile(f"^({variable_name}) ?=") for variable_name in list_variable_name])


if __name__ == "__main__":  # pragma: no cover
    # print(find_string_in_file(__module_path("syntax.py"), [re.compile(r"^(html_insert) ?=")]))
    pass
