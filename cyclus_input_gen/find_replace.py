import numpy as np

def replace_file(input_string, replace_start, replace_end,
                 replacement_file, insert=False):
    """ replaces parts of the string with a replacement file"""
    start = input_string.find(replace_start)
    end = input_string.find(replace_end)
    with open(replacement_file) as f:
        replacement_string = f.read()
    if not insert:
        result = input_string.replace(
            input_string[start:end], replacement_string)
    if insert:
        result = input_string[:end] + '\n' + \
            replacement_string + '\n' + input_string[end:]
    return result


def replace_string(input_string, replace_start, replace_end,
                   replacement_string, insert=False):
    """ replaces parts of the string with a string"""
    start = input_string.find(replace_start)
    end = input_string.find(replace_end)
    if not insert:
        result = input_string.replace(
            input_string[start:end], replacement_string)
    if insert:
        result = input_string[:end] + '\n' + \
            replacement_string + '\n' + input_string[end:]
    return result
