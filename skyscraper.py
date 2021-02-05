'''
This module contains functions. 
'''
def read_input(path: str):
    """
    Read game board file from path.
    Return list of str.

    >>> read_input("check.txt")
    ['***21**', '452453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***']
    """
    with open(path, "r", encoding="utf-8") as file:
        lst = file.readlines()
        for i in range(len(lst)):
            if lst[i][-1] == "\n":
                lst[i] = lst[i][:-1]
        return lst


def left_to_right_check(input_line: str, pivot: str):
    """
    Check row-wise visibility from left to right.
    Return True if number of building from the left-most hint is visible looking to the right,
    False otherwise.

    input_line - representing board row.
    pivot - number on the left-most hint of the input_line.

    >>> left_to_right_check("412453*", 4)
    True
    >>> left_to_right_check("412453*", 5)
    False
    """
    if input_line[0] == "*":
        return True
    else:
        pivot = int(pivot)
        lst = list(input_line)[1:]
        if pivot > lst.index("5")+1:
            return False
        elif pivot < lst.index("5")+1:
            lost = lst.index("5")+1 - pivot
            counter = 0
            for i in range(lst.index("5")-1):
                try:
                    if (int(lst[i+1]) - int(lst[i]) < 0
                    or int(lst[i+1]) - int(lst[i-1])):
                        counter +=1
                except:
                    continue
            if counter == lost:
                return True
            return False
        else:
            for i in range(lst.index("5")-1):
                if int(lst[i+1]) - int(lst[i]) < 0:
                    return False
            return True


def check_not_finished_board(board: list):
    """
    Check if skyscraper board is not finished, i.e., '?' present on the game board.

    Return True if finished, False otherwise.

    >>> check_not_finished_board(['***21**', '4?????*', '4?????*', '*?????5', '*?????*', '*?????*', '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*5?3215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    lst = list(" ".join(board))
    if "?" in lst:
        return False
    return True


def check_uniqueness_in_rows(board: list):
    """
    Check buildings of unique height in each row.

    Return True if buildings in a row have unique length, False otherwise.

    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*553215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    for i in range(1,len(board)-1):
        lst = list(board[i])
        for j in range(1,len(lst)-1):
            if lst[j] != "*" and lst[1:-1].count(lst[j]) != 1:
                return False
    return True

def check_horizontal_visibility(board: list):
    """
    Check row-wise visibility (left-right and vice versa)

    Return True if all horizontal hints are satisfiable,
     i.e., for line 412453* , hint is 4, and 1245 are the four buildings
      that could be observed from the hint looking to the right.

    >>> check_horizontal_visibility(['***21**', '412453*', '412354*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    for i in range(1,len(board)-1):
        if ((not left_to_right_check(board[i], board[i][0]))
        or (not left_to_right_check(board[i][::-1], board[i][-1]))):
            return False
    return True

    

def check_columns(board: list):
    """
    Check column-wise compliance of the board for uniqueness (buildings of unique height) and visibility (top-bottom and vice versa).

    Same as for horizontal cases, but aggregated in one function for vertical case, i.e. columns.

    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_columns(['***21**', '412153*', '423445*', '*543215', '*35214*', '*41232*', '*2*1***'])
    False
    >>> check_columns(['***21**', '412553*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """

    lst = []
    for i in range(len(board)):
        lst.extend(list(board[i]))
    i = 0
    while i < 7:
        line = ''
        for j in range(i,len(lst),7):
            line+=lst[j]
        board[i] = line
        i +=1
    if check_uniqueness_in_rows(board):
        return check_horizontal_visibility(board)
    return False


def check_skyscrapers(input_path: str):
    """
    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.

    >>> check_skyscrapers("check.txt")
    False
    """
    board = read_input(input_path)
    if (check_not_finished_board(board) and check_uniqueness_in_rows(board)
    and check_horizontal_visibility(board) and check_columns(board)):
        return True
    return False


if __name__ == "__main__":
    print(check_skyscrapers("check.txt"))