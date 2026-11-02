import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    # Column labels
    letters = string.ascii_uppercase[:len(board[0])]
    print('  ' + '   '.join(letters))
    # Board rows with separators
    for r in range(len(board)):
        print('+' + '---+' * len(board[0]))
        row_str = '|'.join(' ' + board[r][c] + ' ' for c in range(len(board[0])))
        print('|' + row_str + '|')
    print('+' + '---+' * len(board[0]))

def get_player_input(current_player, board):
    letters = string.ascii_uppercase[:len(board[0])]
    while True:
        choice = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if len(choice) != 1 or choice not in letters:
            # invalid input
            continue
        col = letters.index(choice)
        # Check if the column is full
        if board[0][col] != ' ':
            # Turn lost, column full
            return col, False
        return col, True

def place_checker(board, column, checker):
    # Place the checker at the lowest available space in the column
    for row in reversed(range(len(board))):
        if board[row][column] == ' ':
            board[row][column] = checker
            return row, column

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count >= WIN_COUNT:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count >= WIN_COUNT:
                    return True
            else:
                count = 0

    # Diagonal check (top-left to bottom-right)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            win = True
            for i in range(WIN_COUNT):
                if board[r + i][c + i] != checker:
                    win = False
                    break
            if win:
                return True

    # Diagonal check (bottom-left to top-right)
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            win = True
            for i in range(WIN_COUNT):
                if board[r - i][c + i] != checker:
                    win = False
                    break
            if win:
                return True

    return False

def check_draw(board):
    # If top row has no empty spaces, board is full
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_CHECKERS[:PLAYERS]

    current_player_index = random.randint(0, PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_index]

        col, valid_turn = get_player_input(current_checker, board)
        if not valid_turn:
            # Column full, turn lost
            current_player_index = (current_player_index + 1) % PLAYERS
            continue

        place_checker(board, col, current_checker)

        if check_win(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
