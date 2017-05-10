from argparse import ArgumentParser
from csvcommon import parse_range

import sys

DESCRIPTION = 'csvpp - prints cvs file in human-readable format'
EXAMPLES = 'example: cat file.txt | csvpp -f | less -SR'


def main():
    args = parse_args()
    input_stream = open(args.file, 'r') if args.file else sys.stdin
    output_stream = open(args.output_file, 'r') if args.output_file else sys.stdout

    columns = input_stream.readline().strip().split(args.separator)

<<<<<<< HEAD
    cutted = parse_range(columns, args.fields)
    if args.unique:
        cutted = list(set(cutted))
    if args.complement:
        cutted = [x for x in range(len(columns)) if x not in cutted]

    print_row(columns, cutted, args.separator, output_stream)
    for row in input_stream:
        print_row(row.strip().split(args.separator), cutted, args.separator, output_stream)
=======
    cutted_columns = parse_range(columns, args.fields)
    if args.unique:
        cutted_columns = list(set(cutted_columns))
    if args.complement:
        cutted_columns = [x for x in range(len(columns)) if x not in cutted_columns]

    first_rows = [columns]
    for i in range(100):
        first_rows.append(input_stream.readline().strip().split(args.separator))
    column_widths = [max([len(column) for column in [row[i] for row in first_rows]]) for i in range(len(columns))]

    for row in first_rows:
        print_row(row, column_widths, output_stream, cutted_columns)
    for row in input_stream:
        print_row(row.strip().split(args.separator), column_widths, output_stream, cutted_columns)
>>>>>>> f3f94c0c8ce19a5fe45ce71c2f5f10f36e02bed9

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
    parser.add_argument('-u', '--unique', help='Remove duplicates from list of FIELDS', action="store_true")
    parser.add_argument('file', nargs='?', help='File to read input from. stdin is used by default')

    args = parser.parse_args()

    return args

main()
