import random
import os

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:2]  # Modify slice for number of players

def clear_screen():
    os.system('clear')  # Use 'cls' for Windows

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    header = '  ' + '   '.join(chr(ord('A') + i) for i in range(COLUMNS))
    print(header)
    for row in board:
        print('+---' * COLUMNS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * COLUMNS + '+')

def is_valid_move(column, board):
    return column >= 0 and column < COLUMNS and board[0][column] == ' '

def make_move(board, column, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = checker
            return True
    return False

def check_winner(board, checker):
    # Check horizontal, vertical, and both diagonal wins
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal (/)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal (\)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def play_game():
    board = create_board()
    current_player = random.choice(range(len(CHECKERS)))
    print_board(board)
    
    while True:
        checker = CHECKERS[current_player]
        while True:
            move = input(f"Player {checker}, please enter a column: ").strip().upper()
            if len(move) == 1 and 'A' <= move <= chr(ord('A') + COLUMNS - 1):
                column = ord(move) - ord('A')
                if is_valid_move(column, board):
                    break
            print("Invalid input. Please try again.")

        make_move(board, column, checker)
        print_board(board)

        if check_winner(board, checker):
            print(f"Player {checker} won!")
            break
        elif check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % len(CHECKERS)

if __name__ == "__main__":
    play_game()
