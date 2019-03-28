import json
import sys
import os


def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        return json_data


def convert_list(input_list):
    converted_output = '<ul>'
    for element in input_list:
        if isinstance(element, dict):
            tmp = convert_dict(element)
            converted_output += f'<li>{tmp}</li>'
        elif isinstance(element, str):
            converted_output += f'<li>{element}</li>'
    converted_output += '</ul>'
    return converted_output


def convert_dict(child):
    output = ''
    for tag, content in child.items():
        if isinstance(content, list):
            output += f'<{tag}>' + convert_list(content) + f'</{tag}>'
        elif isinstance(content, dict):
            output += f'<{tag}>' + convert_dict(content) + f'</{tag}>'
        else:
            output += f'<{tag}>{content}</{tag}>'
    return output


def main_output(json_data):
    result = ''
    if isinstance(json_data, list):
        result += convert_list(json_data)
    elif isinstance(json_data, dict):
        result += convert_dict(json_data)
    return result


def critical_error(message):
    print(message, file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    filename = sys.argv[1]
    try:
        json_data = load_data(filename)
    except FileNotFoundError:
        critical_error('file {} not found'.format(filename))
    except json.JSONDecodeError:
        critical_error('file must be json')
    sys.stdout.write(main_output(json_data))
