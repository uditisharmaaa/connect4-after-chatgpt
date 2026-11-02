import random
import os

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    print('+' + '---+' * COLS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLS)

def is_valid_move(board, col):
    return 0 <= col < COLS and board[0][col] == ' '

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            break

def check_win(board, checker):
    for r in range(ROWS):
        for c in range(COLS):
            if (c + 3 < COLS and all(board[r][c + j] == checker for j in range(4))) or \
               (r + 3 < ROWS and all(board[r + j][c] == checker for j in range(4))) or \
               (r + 3 < ROWS and c + 3 < COLS and all(board[r + j][c + j] == checker for j in range(4))) or \
               (r - 3 >= 0 and c + 3 < COLS and all(board[r - j][c + j] == checker for j in range(4))):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column:")
        user_input = input().strip().upper()
        
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input, please enter a letter A-G.")
            continue
        
        col = ord(user_input) - 65

        if not is_valid_move(board, col):
            print("Column is full or invalid, try again.")
            continue

        place_checker(board, col, current_player)
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
