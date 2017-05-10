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
    parser.add_argument('-k', '--keys', type=str,
                        help="Comma-separated list of columns to be used as reduce keys. "
                             "Column names or column numbers can be used here",
                        default='1-')
    parser.add_argument('-i', '--integration_step',
                        help='Divide each aggregation group into smaller groups each containing INTEGRATION_STEP rows.')
    parser.add_argument('-a', '--agregators', help="Comma-separated list of value-aggregators. "
                                                   "Each aggregator might be one of the following: "
                                                   "first, last, sum, mean, min, max, std (standard deviation), count. "
                                                   "Each aggragator (except count) is a function expecting "
                                                   "2 arguments: column name or number and the resulting field name. "
                                                   "The resulting field name has a default value of "
                                                   "$AGGREGATOR_NAME_$FIRST_ARGUMENT' (e.g. for sum('a') it will have a "
                                                   "default value of sum_a). Please see the examples for more details.")
    parser.add_argument('--no-sort', help='If provided, the input will not be sorted prior to reduce operation. '
                                          'Be careful, that might lead to an incorrect reduce result. '
                                          'If your input is already sorted by the KEYS, this option will '
                                          'significantly speed up the reduce.',
                        action="store_false")
    parser.add_argument('file', nargs='?', help='File to read input from. stdin is used by default')

    args = parser.parse_args()

    return args


main()