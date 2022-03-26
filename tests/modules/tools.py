import inspect
import os
import re


###############################################################################
# List of tools for testing
###############################################################################
###############################################################################
# Paths
########################################


def __base():
    """
    Return the path of the main module (relative to the tests)
    :return: Path of the main module
    :rtype: str
    """
    return "../../src/bootstraparse/"


def __module_path(module_name):
    """
    Return the path of the module module_name
    :param module_name: Name of the module
    :type module_name: str
    :return: Path of the module
    :rtype: str
    """
    return os.path.normpath(os.path.join(os.path.dirname(__file__), __base(), "modules", module_name))


###############################################################################
# Frame inspection
########################################
# Cursed frame inspection
def __GL():
    return inspect.getframeinfo(inspect.currentframe().f_back).lineno


###############################################################################
# Code inspection
########################################
def find_string_in_file(file_path, list_regex_to_find):
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


def find_functions_in_file(file_path, list_function_name):
    """
    Find the function in the file stream
    :param file_path: Path of the file
    :type file_path: str
    :param list_function_name: List of function name to find
    :type list_function_name: iterable
    :return: Dict of function found and line number
    :rtype: dict
    """
    return find_string_in_file(file_path, [re.compile(f"$def ({function_name})") for function_name in list_function_name])


def find_classes_in_file(file_path, list_class_name):
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


def find_variables_in_file(file_path, list_variable_name):
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


if __name__ == "__main__":
    # print(find_string_in_file(__module_path("syntax.py"), [re.compile(r"^(html_insert) ?=")]))
    pass