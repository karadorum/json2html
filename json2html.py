import json
import sys
import os


def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        return json_data


def conv_to_html(json_data):
    for block in json_data:
        for tag, content in block.items():
            if tag == 'title':
                print('<h1>{}</h1>'.format(content))
            elif tag == 'body':
                print('<p1>{}</p1>'.format(content))


if __name__ == "__main__":
    try:
        json_data = load_data(sys.argv[1])
        conv_to_html(json_data)
    except FileNotFoundError:
        print('file not found')
    except json.JSONDecodeError:
        print('file must be json')
