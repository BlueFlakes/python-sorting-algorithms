import csv
import os
import time


def file_reader(filename, show_bugs):
    """Read file and filters out bugs, have option to show which rows got errors
    Parameters
    ----------
    filename : string
    show_bugs: bool

    Returns
    -------
    temp_storage : list of int
    """

    temp_storage = []
    invalid_type_data_storage = []
    row_counter = 0

    with open(filename, 'r') as csvfile:
        data_reader = csv.reader(csvfile)

        for row in data_reader:
            row_counter += 1

            try:
                temp_storage.append(int(row[0]))

            except ValueError:
                invalid_type_data_storage.append([row[0], row_counter])

        if invalid_type_data_storage and show_bugs:
            show_broken_rows(invalid_type_data_storage)

    return temp_storage


def read_data(amount_data, show_bugs=False):
    """Read data
    Parameters
    ----------
    amount_data : int
    show_bugs: bool

    Returns
    -------
    data_storage : list of int
    """
    red = "\033[1;31m"
    off = "\033[0;0m"
    filename = amount_data_filename(amount_data)

    try:
        data_storage = file_reader(filename, show_bugs)

    except FileNotFoundError:
        print(red + "File not found or directory does not exist.\n" + off)
        exit()

    return data_storage


def amount_data_filename(amount_data):
    """Convert integer value to right directory of stored data

    Parameters
    ----------
    amount_data: int

    Returns
    -------
    filename: string
    """
    amount_data = str(amount_data)

    file_path = {
        '1000':'data_to_sort/one_thousand.csv',
        '10000':'data_to_sort/ten_thousand.csv',
        '50000':'data_to_sort/fifty_thousand.csv',
        '100000':'data_to_sort/one_hundred_thousand.csv',
        '500000':'data_to_sort/five_hundred_thousand.csv',
        '1000000':'data_to_sort/one_million.csv',
        '3000000':'data_to_sort/three_millions.csv'}

    if amount_data in file_path:
        filename = file_path[amount_data]
    else:
        filename = amount_data

    return filename


def show_broken_rows(broken_data):
    """Printing rows which got inappropriate values
    Parameters
    ----------
    broken_data : list of invalid data types which were found while reading
    data from file.

    Returns
    -------
    None
    """
    for record in broken_data:
        print("Invalid data type in row: {} \n'{}'".format(record[1], record[0]))


def check_for_direction():
    """Look for direction, if couldn't find then make dir.
    """
    if not os.path.exists('sorted_data'):
        os.makedirs('sorted_data')


def save_data(numbers):
    """Saving data to file
    Parameters
    ----------
    numbers : list of int

    Returns
    -------
    None

    """
    # if path doesn't exist then func check_direction() create dir
    check_for_direction()
    filename = 'sorted_data/sorted_' + str(len(numbers)) + ".csv"
    list_of_numbers = numbers

    with open(filename, 'w') as csvfile:
        data_writer = csv.writer(csvfile)

        for number in list_of_numbers:
            data_writer.writerow([number])


def bubble_sort(numbers):
    """Sort values using bubble sort algorithm
    Parameters
    ----------
    numbers : list of int

    Returns
    -------
    numbers : sorted list of int
    """
    sorted_list = False

    while not sorted_list:
        sorted_list = True

        for i in range(len(numbers)-1):
            if numbers[i] > numbers[i+1]:
                temp_value = numbers[i]
                numbers[i] = numbers[i+1]
                numbers[i+1] = temp_value
                sorted_list = False

    return numbers


def selection_sort(numbers):
    """Sort values using selection sort algorithm
    Parameters
    ----------
    numbers : list of int

    Returns
    -------
    numbers : sorted list of int
    """
    for i in range(len(numbers)):
        for j in range(i, len(numbers)):
            if numbers[i] > numbers[j]:
                temp_value = numbers[i]
                numbers[i] = numbers[j]
                numbers[j] = temp_value

    return numbers


def insertion_sort(numbers):
    """Sort values using insertion sort algorithm
    Parameters
    ----------
    numbers : list of int

    Returns
    -------
    numbers : list of int
    """

    for i in range(len(numbers)-1):
        k = 0

        while numbers[i-k] > numbers[i-k+1] and k <= i:
            temp_value = numbers[i-k]
            numbers[i-k] = numbers[i-k+1]
            numbers[i-k+1] = temp_value
            k += 1

    return numbers


def sort_data(amount_data, sort_type='bubble'):
    """
    Parameters
    ----------
    amount_data : int
    sort_type : string, optional

    Returns
    -------
    data : list of int
    """
    data = read_data(amount_data)
    sort_type = sort_type.lower()

    if sort_type == 'bubble':
        data = bubble_sort(data)
    elif sort_type == 'insertion':
        data = insertion_sort(data)
    else:
        raise NameError("'" + sort_type + "'" + " this type of sort does not exist.")

    return data


def get_computing_time(amount_data, computing_type='import data'):
    """
    Parameters
    ----------
    amount_data : int
    computing_type : string, optional

    Returns
    -------
    time_counter : int
    """
    red = "\033[1;31m"
    off = "\033[0;0m"
    computing_type_copy = computing_type
    computing_type = str(computing_type).lower()
    time_counter = 0
    data = read_data(amount_data)
    if computing_type == 'export data':
        data = [str(number) for number in data]

    possible_types = {'export data': [save_data, data],
                 'bubble sort': [bubble_sort, data],
                 'insertion sort': [insertion_sort, data],
                 'selection sort': [selection_sort, data],
                 'import data': [read_data, amount_data]}

    if computing_type in possible_types:
        func, arg = possible_types[computing_type][0], possible_types[computing_type][1]

        start = time.time()
        func(arg)
        time_counter = int((time.time() - start) * 1000)

    else:
        try:
            raise NameError("'" + computing_type_copy + "'" + " this type of sorting does not exist.")

        except TypeError:
            print(red + "Incorrect command type.\n" + off)
            exit()

    return time_counter


def compute_data():
    """Stacks data into readable format for tests :)

    Returns
    -------
    dictionary: dict
    """
    possible_data_amount = [1000]
    computing_types = ['selection sort', 'import data', 'bubble sort', 'insertion sort', 'export data']
    dictionary = {}

    for comp_type in computing_types:
        for amount in possible_data_amount:
            dictionary[(comp_type, amount)] = get_computing_time(amount, comp_type)

    return dictionary


def get_table_sizes(data):
    """Taking longest sizes for board
    Parameters
    ----------
    data : dict : { key : tuple: (string, int), value : int }

    Returns
    -------
    table_sizes: dict
    """
    highest_data_amount = 0
    widest_data_operation = ''
    highest_time_value = 0
    columns_amount = []
    rows_amount = []

    for key, value in data.items():
        data_amount = key[1]
        if data_amount > highest_data_amount:
            highest_data_amount = data_amount

        # widest name of data operation
        data_operation = key[0]
        if len(data_operation) > len(widest_data_operation):
            widest_data_operation = data_operation

        if value > highest_time_value:
            highest_time_value = value

        if key[0] not in rows_amount:
            rows_amount.append(key[0])

        if key[1] not in columns_amount:
            columns_amount.append(key[1])

    table_sizes = {'columns_number': len(columns_amount),
             'rows_number': len(rows_amount),
             'highest_data_amount': str(highest_data_amount),
             'highest_time_value': str(highest_time_value),
             'widest_data_operation': widest_data_operation}

    return table_sizes


def from_sizes_get_table_width(sizes):
    """
    Parameters
    ----------
    sizes: dict

    Returns
    -------
    tuple: which contain longest name of data operation and
    longest width of column
    """
    data_operation_width = len(sizes['widest_data_operation'])
    next_columns_width = 0
    data_amount = int(sizes['highest_data_amount'])
    time_value = int(sizes['highest_time_value'])

    if data_amount > time_value:
        next_columns_width = data_amount
    else:
        next_columns_width = time_value

    return data_operation_width, len(str(next_columns_width))


def from_sizes_get_table_height(sizes):
    """
    Parameters
    ----------
    sizes: dict

    Returns
    -------
    height: int
    """
    height = sizes['rows_number'] * 4 + 5

    return height


def print_board(board):
    """
    Parameters
    ----------
    board: list of nested lists

    Returns
    -------
    board: which contain list of nested lists
    """
    for row in board:
        for column in row:
            print(column, end='')
        print()


def modify_board(board):
    """Easy and fast modification :) otherway diffcult solution would be needed
    Parameters
    ----------
    board: list of nested lists

    Returns
    -------
    board: which contain list of nested lists
    """
    board[0][0] = '/'
    board[0][-1] = '\\'
    board[-1][0] = '\\'
    board[-1][-1] = '/'

    return board


def create_board(height, width, operation_width, column_width):
    """Creating board, if-elif ladder is used like priorities ladder
    Parameters
    ----------
    board: list of nested lists
    word: string to insert into board
    operation_width: int
    column_width: int

    Returns
    -------
    board: which contain list of nested lists
    """
    board = []

    for y in range(height):
        temp_storage = []

        for x in range(width+1):
            if y == 0 or y == height-1:
                temp_storage.append('-')
            elif x == 0:
                temp_storage.append('|')
            elif x > (operation_width+2) and (x-operation_width-3) % (3 + column_width) == 0:
                temp_storage.append('|')
            elif y % 4 == 0:
                temp_storage.append('-')
            else:
                temp_storage.append(' ')

        board.append(temp_storage)
    board = modify_board(board)

    return board


def next_columns_insert_tool(board, values_collector, first_column_range, column_width, jump=0):
    """Inserting a data into second, third, fourth and other greater than first column
    Parameters
    ----------
    board: list of nested lists
    word: string to insert into board
    operation_width: int
    column_width: int
    jump: int

    Returns
    -------
    board: which contain list of nested lists
    """
    values_start_point = first_column_range + 2
    column_width += 3
    k = 0
    next_column = column_width

    for number in values_collector:
        column_mid_point = int((column_width-len(number))/2) + 2
        inserting_start_point = values_start_point + (k*(next_column)) + column_mid_point

        for i in range(len(number)):
            board[2+jump][inserting_start_point+i] = number[i]

        k += 1

    return board


def first_column_insert_tool(board, word, operation_width, column_width, jump=0):
    """Inserting a data into just first column
    Parameters
    ----------
    board: list of nested lists
    word: string to insert into board
    operation_width: int
    column_width: int
    jump: int

    Returns
    -------
    board: which contain list of nested lists
    """
    first_column_range = operation_width
    inserting_start_point = int(((first_column_range+2)-len(word))/2)

    for i in range(len(word)):
        board[2+jump][inserting_start_point+i] = word[i]

    return board


def insert_table_description(board, data, operation_width, column_width):
    """Description manager function, here we have the sequence of inserting data into rows
    Parameters
    ----------
    data : dict : { key : tuple: (string, int), value : int }
    board: list of nested lists
    operation_width: int
    column_width: int

    Returns
    -------
    board: which contain list of nested lists
    """
    operations = []
    numbers = []

    for key in data:
        used_value = str(key[1])
        used_operation = key[0]

        if used_value not in numbers:
            numbers.append(used_value)

        if used_operation not in operations:
            operations.append(used_operation)

    board = first_column_insert_tool(board, 'Action', operation_width, column_width)
    board = next_columns_insert_tool(board, numbers, operation_width, column_width)

    values = [int(number) for number in numbers]
    values = bubble_sort(values)

    # k incremented by 4 is moving from start to the next ordered row
    k = 4
    for word in operations:
        board = first_column_insert_tool(board, word, operation_width, column_width, k)

        highscores = []
        for score in values:
            highscores.append(data[(word, score)])
        highscores = [str(score)+" ms" for score in highscores]

        board = next_columns_insert_tool(board, highscores, operation_width, column_width, k)
        k += 4

    return board


def print_computing_summary(computing_data):
    """Main function that manages the creation and modification of the board
    Parameters
    ----------
    computing_data : dict : { key : tuple: (string, int), value : int }

    Returns
    -------
    None
    """
    if computing_data:
        table_sizes = get_table_sizes(computing_data)
        operation_width, column_width = from_sizes_get_table_width(table_sizes)
        column_width += 3
        table_width = (operation_width + column_width * table_sizes['columns_number'] +
                        3 * (table_sizes['columns_number']+1))
        table_height = from_sizes_get_table_height(table_sizes)

        board = create_board(table_height, table_width, operation_width, column_width)
        board = insert_table_description(board, computing_data, operation_width, column_width)

        print_board(board)
    else:
        print("No data delivered.")
        exit()


def main():

    dictio = compute_data()

    print_computing_summary(dictio)


if __name__ == "__main__":
    main()
