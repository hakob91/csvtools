def parse_range(columns, fields):
    def column_index(columns, column):
        if column == '':
            return len(columns)
        try:
            return int(column) - 1
        except ValueError:
            return columns.index(column)

    field_indexes = []
    for field in fields.split(','):
        field = field.split('-')
        field_indexes.extend(list(range(column_index(columns, field[0]), column_index(columns, field[-1]) + 1)))
    return field_indexes