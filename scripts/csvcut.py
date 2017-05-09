from argparse import ArgumentParser

import sys

DESCRIPTION = 'csvpp - prints cvs file in human-readable format'
EXAMPLES = 'example: cat file.txt | csvpp -f | less -SR'


def get_index(list, column):
    if column == '':
        return len(list)
    try:
        return int(column) - 1
    except ValueError:
        return list.index(column)


def parse_range(list, columns):
    f = set()
    for column in columns.split(','):
        column = column.split('-')
        f.update(range(get_index(list, column[0]), get_index(list, column[-1]) + 1))
    return f

def main():
    # args = parse_args()
    # input_stream = open(args.file, 'r') if args.file else sys.stdin
    # output_stream = open(args.output_file, 'r') if args.output_file else sys.stdout

    all_fields = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

    print(parse_range(all_fields, '1-3,6, '.strip(", ")))


def parse_args():
    parser = ArgumentParser(description=DESCRIPTION, epilog=EXAMPLES)
    parser.add_argument('-s', '--separator', type=str, help='Separator to be used', default=',')
    parser.add_argument('-o', '--output_file', type=str, help='Output file. stdout is used by default')
    parser.add_argument('-f', '--fields', help="Specify list of fields (comma separated) to cut. Field names or field numbers can be used. Dash can be used to specify fields ranges. Range 'F1-F2' stands for all fields between F1 and F2. Range '-F2' stands for all fields up to F2. Range 'F1-' stands for all fields from F1 til the end.")
    parser.add_argument('-c', '--complement', type=int, help='Instead of leaving only specified columns, leave all except specified.', action="store_false")
    parser.add_argument('-u', '--unique', type=int, help='Remove duplicates from list of FIELDS', action="store_false")
    parser.add_argument('file', nargs='?', help='File to read input from. stdin is used by default')

    args = parser.parse_args()

    return args

main()