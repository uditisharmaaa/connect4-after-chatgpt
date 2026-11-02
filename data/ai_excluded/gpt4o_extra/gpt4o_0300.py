import os
import random

ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print('   ' + '   '.join([chr(i) for i in range(65, 65 + len(board[0]))]))
    print('+' + '---+' * len(board[0]))
    for row in board:
        print('|' + '|'.join(f' {col} ' for col in row) + '|')
        print('+' + '---+' * len(board[0]))

def get_column_index(choice):
    return ord(choice.upper()) - 65

def is_valid_choice(choice, cols):
    if not choice or len(choice) != 1:
        return False
    index = get_column_index(choice)
    return 0 <= index < cols

def is_column_full(board, col_index):
    return board[0][col_index] != ' '

def place_checker(board, col_index, checker):
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = checker
            return

def check_line(line, checker):
    return any(line[i:i+4] == [checker]*4 for i in range(len(line) - 3))

def check_win(board, checker):
    # Check horizontal win
    for row in board:
        if check_line(row, checker):
            return True

    # Check vertical win
    for col in range(len(board[0])):
        if check_line([board[row][col] for row in range(len(board))], checker):
            return True

    # Check diagonal win (/ and \)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row+i][col+i] == checker for i in range(4)) or \
               all(board[row+3-i][col+i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(len(board[0])))

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)
    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        choice = input().strip()
        if not is_valid_choice(choice, COLUMNS):
            print("Invalid input. Please try again.")
            continue
        col_index = get_column_index(choice)
        if is_column_full(board, col_index):
            print("Column full. You lose your turn.")
            current_player = players[(players.index(current_player) + 1) % PLAYERS]
            continue
        place_checker(board, col_index, current_player)
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print_board(board)
            print("Game is a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    main()
