from argparse import ArgumentParser
from csvcommon import parse_range

import sys

DESCRIPTION = 'csvpp - prints cvs file in human-readable format'
EXAMPLES = 'example: cat file.txt | csvpp -f | less -SR'


def print_row(row, columns, separator, output_stream):
    """
    Prints a row
    
    :param row: row represented as a list of columns
    :param columns: a list of index columns
    :param separator: a string separator for line
    :param output_stream: a stream to print the row
    """
    output = [row[i] for i in columns]
    output_stream.write(separator.join(output) + "\n")


def main():
    args = parse_args()
    input_stream = open(args.file, 'r') if args.file else sys.stdin
    output_stream = open(args.output_file, 'r') if args.output_file else sys.stdout

    columns = input_stream.readline().strip().split(args.separator)

    cutted = parse_range(columns, args.fields)
    if args.unique:
        cutted = list(set(cutted))
    if args.complement:
        cutted = [x for x in range(len(columns)) if x not in cutted]

    print_row(columns, cutted, args.separator, output_stream)
    for row in input_stream:
        print_row(row.strip().split(args.separator), cutted, args.separator, output_stream)

    if input_stream != sys.stdin:
        input_stream.close()
    if output_stream != sys.stdout:
        output_stream.close()


def parse_args():
    parser = ArgumentParser(description=DESCRIPTION, epilog=EXAMPLES)
    parser.add_argument('-s', '--separator', type=str, help='Separator to be used', default=',')
    parser.add_argument('-o', '--output_file', type=str, help='Output file. stdout is used by default')
    parser.add_argument('-f', '--fields',  type=str, help="Specify list of fields (comma separated) to cut. Field names or field numbers can be used. Dash can be used to specify fields ranges. Range 'F1-F2' stands for all fields between F1 and F2. Range '-F2' stands for all fields up to F2. Range 'F1-' stands for all fields from F1 til the end.", default='1-')
    parser.add_argument('-c', '--complement', help='Instead of leaving only specified columns, leave all except specified.', action="store_true")
    parser.add_argument('-u', '--unique', help='Remove duplicates from list of FIELDS', action="store_false")
    parser.add_argument('file', nargs='?', help='File to read input from. stdin is used by default')

    args = parser.parse_args()

    return args

main()