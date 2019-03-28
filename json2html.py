import json
import sys
import os
import html
import re


class ParsedTag:
    def __init__(self, extended_tag):
        a = re.split(r'(\.|#)', extended_tag, maxsplit=1)
        self.tag = a[0]
        self.classes = []
        self.ids = []
        other = a[1] + a[2] if len(a) == 3 else ''
        for mo in re.finditer(r'(\.|#)[^.#]+', other):
            tmp = mo.group()
            if tmp.startswith('.'):
                self.classes.append(tmp[1:])
            else:
                self.ids.append(tmp[1:])

    def open(self):
        output = f'<{self.tag}'
        if self.classes:
            output += ' class="{}"'.format(' '.join(self.classes))
        if self.ids:
            output += ' id="{}"'.format(' '.join(self.ids))
        output += '>'
        return output

    def close(self):
        return f'</{self.tag}>'


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
            escaped_html = html.escape(element)
            converted_output += f'<li>{escaped_html}</li>'
    converted_output += '</ul>'
    return converted_output


def convert_dict(child):
    output = ''
    for tag, content in child.items():
        parsed_tag = ParsedTag(tag)
        if isinstance(content, list):
            output += parsed_tag.open() + convert_list(content) + parsed_tag.close()
        elif isinstance(content, dict):
            output += parsed_tag.open() + convert_dict(content) + parsed_tag.close()
        else:
            escaped_html = html.escape(content)
            output += parsed_tag.open() + escaped_html + parsed_tag.close()
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
