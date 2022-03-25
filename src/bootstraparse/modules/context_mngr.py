# Interprets where the parser is located and resolves errors
class BaseContainer:
    pass
    # Must define __init__, __str__, __repr__ and a print_all method
    # will contain all sub-tokens and/or sub-containers
    # Defines a method to get all token elements (__iter__) and a method to get a specific element (__getitem__)
    # Defines a method to get the number of elements (__len__)
    # Defines a method to get the name of the container (__name__)
    # Defines a method to the optionals inside the container ( ? .optional())

# Define containers all the Enhanced text elements, divs, headers, list and any element that can be a container


class ContextManager:
    pass
# Defines all methods to manage the context of the parser as a file is being parsed
# Builds all containers as the parser is parsing the file

