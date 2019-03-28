import json
import sys


def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        return json_data


def conv_to_html(json_data):
    output_string = ''
    for block in json_data:
        for tag, content in block.items():
                output_string += f'<{tag}>{content}</{tag}>'
    return output_string


if __name__ == "__main__":
    try:
        json_data = load_data(sys.argv[1])

    except FileNotFoundError:
        print('file not found')
    except json.JSONDecodeError:
        print('file must be json')
    sys.stdout.write(conv_to_html(json_data))