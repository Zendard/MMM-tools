import sys


def table_to_lists(table):
    lists = []
    rows = get_row_headers(table)
    columns = get_column_headers(table)

    for row in rows:
        row_list = []
        for column in columns:
            if (row, column) in table:
                row_list.append(table[(row, column)])
            else:
                row_list.append(0)

        lists.append(row_list)
    return lists


def get_column_headers(table):
    headers = set()
    for pos in table.keys():
        headers.add(pos[1])
    return sorted(list(headers))


def get_row_headers(table):
    headers = set()
    for pos in table.keys():
        headers.add(pos[0])
    return sorted(list(headers))


def print_table(table):
    lists = table_to_lists(table)
    column_headers = get_column_headers(table)
    row_headers = get_row_headers(table)

    print("%11s|" % "", end="")
    for header in column_headers:
        print("%10d" % int(header), end=" |")
    print()

    for row in range(len(lists)):
        print("%10d" % int(row_headers[row]), end=" | ")
        row_list = lists[row]
        for i in range(len(column_headers)):
            if i < len(row_list):
                print(("%9.7f" % row_list[i]).replace(".", ","), end=" | ")
            else:
                print(("%9.7f" % 0).replace(".", ","), end=" | ")
        print("")


def normalize_table(table):
    row_sums = sum_rows(table)
    normalized_table = {}
    for pos in table:
        value = table[pos]
        normalized_table[pos] = value/row_sums[pos[0]]
    return normalized_table


def sum_rows(table):
    row_sums = {}
    for pos in table:
        value = table[pos]
        if pos[0] not in row_sums:
            row_sums[pos[0]] = value
        else:
            row_sums[pos[0]] += value
    return row_sums


def sum_columns(table):
    column_sums = {}
    for pos in table:
        value = table[pos]
        if pos[1] not in column_sums:
            column_sums[pos[1]] = value
        else:
            column_sums[pos[1]] += value
    return column_sums


def packet_amount_switch(lines):
    switches = {}
    for i in range(0, len(lines)-1):
        packet_amount_0 = parse_line(lines[i])[0]
        packet_amount_1 = parse_line(lines[i+1])[0]

        if (packet_amount_0, packet_amount_1) not in switches:
            switches[(packet_amount_0, packet_amount_1)] = 1
        else:
            switches[(packet_amount_0, packet_amount_1)] += 1
    return switches


def packet_length_switch(lines):
    switches = {}
    for i in range(0, len(lines)-1):
        parsed_0 = parse_line(lines[i])[1]
        parsed_1 = parse_line(lines[i+1])[1]
        packet_length_0 = parsed_0[0] if len(parsed_0) > 0 else 0
        packet_length_1 = parsed_1[0] if len(parsed_1) > 0 else 0

        if (packet_length_0, packet_length_1) not in switches:
            switches[(packet_length_0, packet_length_1)] = 1
        else:
            switches[(packet_length_0, packet_length_1)] += 1
    return switches


def parse_line(line):
    value_list = line.split()
    packet_amount = int(value_list[1])
    packet_lengths = value_list[2:]
    for i in range(len(packet_lengths)):
        packet_lengths[i] = int(packet_lengths[i])
    return (packet_amount, packet_lengths)


def specific_packet_amount_switch(lines, n):
    switch_from_n = 0
    switch_to_n = 0
    n_to_n = 0
    else_to_else = 0

    for i in range(len(lines)-1):
        packet_amount_0 = parse_line(lines[i])[0]
        packet_amount_1 = parse_line(lines[i+1])[0]

        if packet_amount_0 == n and packet_amount_1 != n:
            switch_from_n += 1
        elif packet_amount_0 != n and packet_amount_1 == n:
            switch_to_n += 1
        elif packet_amount_0 == n and packet_amount_1 == n:
            n_to_n += 1
        elif packet_amount_0 != n and packet_amount_1 != n:
            else_to_else += 1
        else:
            print("Something went wrong...")

    return (switch_from_n, switch_to_n, n_to_n, else_to_else)


def specific_packet_length_switch(lines, n):
    switch_from_n = 0
    switch_to_n = 0
    n_to_n = 0
    for i in range(len(lines)-1):
        parsed_0 = parse_line(lines[i])[1]
        parsed_1 = parse_line(lines[i+1])[1]
        packet_length_0 = parsed_0[0] if len(parsed_0) > 0 else 0
        packet_length_1 = parsed_1[0] if len(parsed_1) > 0 else 0

        if packet_length_0 == n and packet_length_1 != n:
            switch_from_n += 1
        elif packet_length_0 != n and packet_length_1 == n:
            switch_to_n += 1
        elif packet_length_0 == n and packet_length_1 == n:
            n_to_n += 1

    return (switch_from_n, switch_to_n, n_to_n)


def normalize_tuple(old_tuple):
    total = 0

    for value in old_tuple:
        total += value

    new_list = []
    for i in range(len(old_tuple)):
        new_list.append(old_tuple[i] / total)
    print(new_list[0]+new_list[1])
    return tuple(new_list)


def print_specific(switches, specific_target):
    print(("From %d to %d:                           %f" %
          (specific_target, specific_target, switches[2]))
          .replace(".", ","))

    print(("From %d to something else:              %f" %
          (specific_target, switches[0]))
          .replace(".", ","))

    print(("From something else to %d:              %f" %
           (specific_target, switches[1]))
          .replace(".", ","))

    print(("From something else to something else: %f" %
           (switches[3]))
          .replace(".", ","))

    switches_dict = {
        (0, 0): switches[0],
        (0, 1): switches[1],
        (1, 0): switches[2],
        (1, 1): switches[3]}
    print_table(switches_dict)


def main(args):
    print("Markov matrix:")
    lines = open(args[1], "r").readlines()

    if "--length" in args:
        switches = packet_length_switch(lines)
    else:
        switches = packet_amount_switch(lines)

    if "-n" not in args:
        switches = normalize_table(switches)

    print_table(switches)
    print()

    if "--specific" in args:
        specific_args_index = args.index("--specific") + 1
        specific_target = int(args[specific_args_index])

        if "--length" in args:
            switches = specific_packet_length_switch(lines, specific_target)
        else:
            switches = specific_packet_amount_switch(lines, specific_target)

        normalized_0 = normalize_tuple((switches[2], switches[0]))
        normalized_1 = normalize_tuple((switches[1], switches[3]))
        print_specific(normalized_0+normalized_1, specific_target)


if __name__ == "__main__":
    args = sys.argv
    main(args)
