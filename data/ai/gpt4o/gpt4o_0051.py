import random
import os

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
PLAYER_COUNT = 2

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]

def print_board(board):
    clear_screen()
    print('  ' + '   '.join(chr(ord('A') + c) for c in range(COLUMN_COUNT)))
    print('+' + '---+' * COLUMN_COUNT)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLUMN_COUNT)

def is_valid_column(column, board):
    return column in range(COLUMN_COUNT) and board[0][column] == ' '

def get_next_open_row(column, board):
    for r in range(ROW_COUNT - 1, -1, -1):
        if board[r][column] == ' ':
            return r
    return None

def drop_checker(board, row, column, checker):
    board[row][column] = checker

def winning_move(board, checker):
    # Check horizontal locations
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if board[r][c] == checker and all(board[r][c+i] == checker for i in range(1, 4)):
                return True
    
    # Check vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == checker and all(board[r+i][c] == checker for i in range(1, 4)):
                return True
    
    # Check positively sloped diagonals
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if board[r][c] == checker and all(board[r+i][c+i] == checker for i in range(1, 4)):
                return True
    
    # Check negatively sloped diagonals
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if board[r][c] == checker and all(board[r-i][c+i] == checker for i in range(1, 4)):
                return True

    return False

def is_draw(board):
    return all(board[0][c] != ' ' for c in range(COLUMN_COUNT))

def main():
    board = create_board()
    print_board(board)
    
    turn = random.randint(0, PLAYER_COUNT - 1)
    print(f"Player {PLAYER_SYMBOLS[turn]} starts.")
    
    game_over = False

    while not game_over:
        print_board(board)
        column_choice = input(f"Player {PLAYER_SYMBOLS[turn]}, please enter a column: ").strip().upper()

        if column_choice.isalpha() and ord(column_choice) - ord('A') < COLUMN_COUNT:
            column = ord(column_choice) - ord('A')
            if is_valid_column(column, board):
                row = get_next_open_row(column, board)
                drop_checker(board, row, column, PLAYER_SYMBOLS[turn])
                
                if winning_move(board, PLAYER_SYMBOLS[turn]):
                    print_board(board)
                    print(f"Player {PLAYER_SYMBOLS[turn]} won!")
                    game_over = True
                elif is_draw(board):
                    print_board(board)
                    print("The game is a draw!")
                    game_over = True
                
                turn = (turn + 1) % PLAYER_COUNT
            else:
                print("Invalid column choice. Try again.")
        else:
            print("Invalid input. Try again.")

if __name__ == "__main__":
    main()
