from argparse import ArgumentParser

import sys

DESCRIPTION = 'csvpp - prints cvs file in human-readable format'
EXAMPLES = 'example: cat file.txt | csvpp -f | less -SR'


def print_row(row, column_widths, output_stream, cutted_columns):
    """
    Prints a row in human-readable format taking column widths into account

    :param row: row represented as a list of columns
    :param column_widths: a list of column list widths to be used for pretty printing
    :param output_stream: a stream to pretty print the row
    """
    output_line = '|'
    for j in cutted_columns:
        output_line += ' ' + row[j] + ' ' * (column_widths[j] - len(row[j]) + 1) + '|'
    # for i, column in enumerate(row):
        # if i in cutted_columns:
        #     output_line += ' ' + column + ' ' * (column_widths[i] - len(column) + 1) + '|'
    output_line += '\n'
    output_stream.write(output_line)


def column_index(columns, column):
    if column == '':
        return len(columns)
    try:
        return int(column) - 1
    except ValueError:
        return columns.index(column)


def parse_range(columns, fields):
    f = []
    for field in fields.split(','):
        field = field.split('-')
        if field[0] == "":
            continue
        for i in range(column_index(columns, field[0]), column_index(columns, field[-1]) + 1):
            f.append(i)
    return f


def main():
    args = parse_args()
    input_stream = open(args.file, 'r') if args.file else sys.stdin
    output_stream = open(args.output_file, 'r') if args.output_file else sys.stdout

    columns = input_stream.readline().rstrip().split(args.separator)

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
