import os
import random

# Constants (changeable for other dimensions/players as per instructions)
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_COUNT = 4 # Number in a row to win

def clear_screen():
    os.system('clear')  # (Linux/Unix), use 'cls' for Windows

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    # Print column headers
    col_headers = '  ' + '   '.join(chr(ord('A') + i) for i in range(COLUMNS))
    print(col_headers)
    print('+' + '---+'*COLUMNS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+'*COLUMNS)
   
def input_valid(column_input, board):
    if len(column_input) != 1:
        print("Invalid input. Please input a single column letter.")
        return False
    if not column_input.isalpha() or not column_input.isupper():
        print("Please enter an uppercase letter for the column.")
        return False
    index = ord(column_input) - ord('A')
    if index < 0 or index >= COLUMNS:
        print("Column out of range.")
        return False
    if board[0][index] != ' ':
        print("Column full. You lose your turn!")
        return 'FULL'
    return True

def drop_checker(board, column, checker):
    # Place 'checker' in the given column, at the lowest available space
    for row in reversed(range(ROWS)):
        if board[row][column] == ' ':
            board[row][column] = checker
            return row, column
    return None

def is_board_full(board):
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - WIN_COUNT + 1):
            if all(board[row][col+i] == checker for i in range(WIN_COUNT)):
                return True
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - WIN_COUNT + 1):
            if all(board[row+i][col] == checker for i in range(WIN_COUNT)):
                return True
    # Check positive diagonal
    for row in range(ROWS - WIN_COUNT + 1):
        for col in range(COLUMNS - WIN_COUNT + 1):
            if all(board[row+i][col+i] == checker for i in range(WIN_COUNT)):
                return True
    # Check negative diagonal
    for row in range(WIN_COUNT - 1, ROWS):
        for col in range(COLUMNS - WIN_COUNT + 1):
            if all(board[row-i][col+i] == checker for i in range(WIN_COUNT)):
                return True
    return False

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS-1)  # random starting player

    clear_screen()
    print_board(board)
    print(f"Player {players[current_player]}, you will start first.")

    while True:
        player_checker = players[current_player]
        while True:
            user_input = input(f"Player {player_checker}, please enter a column: ").strip()
            valid = input_valid(user_input, board)
            if valid == True:
                column = ord(user_input) - ord('A')
                break
            elif valid == 'FULL':
                # player loses their turn if column is full
                column = None
                break
            # else, continue asking (input not lost)
        
        clear_screen()
        if column is not None:
            drop_checker(board, column, player_checker)
        print_board(board)

        if column is not None and check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        if is_board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
