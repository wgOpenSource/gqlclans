#!/usr/bin/env python
"""
Generate settings_local
"""
import argparse
import os
import sys
from functools import partial


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE_NAME = os.path.join(BASE_DIR, 'settings_local.py')


parser = argparse.ArgumentParser()
parser.add_argument('wgapi_application_id', type=str,
                    help='Application ID (https://developers.wargaming.net/applications/ )')
parser.add_argument('-s', '--silent', action='store_true',
                    help='Silently exit if settings_local exists')
parser.add_argument('-o', '--output', type=str,
                    help='Output file',
                    default=OUTPUT_FILE_NAME)
parser.add_argument('-f', '--force', action='store_true',
                    help='Rewrite exist settings')


def main():
    args = parser.parse_args()
    error = partial(exit_and_print_error, args.silent)
    if not args.force and os.path.isfile(args.output):
        error(f'{args.output} already exists. Use --force to override this file')
    config = generate_settings_file(args)
    with open(args.output, 'w') as output_file:
        output_file.write(config)


def exit_and_print_error(silent, error_text):
    if silent:
        exit(0)
    else:
        print(error_text, file=sys.stderr)


def generate_settings_file(args):
    template = """import os


WGAPI_APPLICATION_ID = %(application_id)s
"""
    return template % {
        'application_id': format_arg(args.wgapi_application_id)
    }


def format_arg(value):
    if value.startswith('os.environ.get'):
        return value
    else:
        return '\'%s\'' % value


if __name__ == '__main__':
    main()
