import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    # Print column headers
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    # Print the board
    for row in board:
        print('+---+' * COLS)
        print('| ' + ' | '.join(cell for cell in row) + ' |')
    print('+---+' * COLS)

def is_valid_move(board, col):
    return 0 <= col < COLS and board[0][col] == ' '

def drop_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row][col+1] == checker and 
                board[row][col+2] == checker and 
                board[row][col+3] == checker):
                return True
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == checker and 
                board[row+1][col] == checker and 
                board[row+2][col] == checker and 
                board[row+3][col] == checker):
                return True
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row+1][col+1] == checker and 
                board[row+2][col+2] == checker and 
                board[row+3][col+3] == checker):
                return True
    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row-1][col+1] == checker and 
                board[row-2][col+2] == checker and 
                board[row-3][col+3] == checker):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS-1)
    game_over = False
    
    while not game_over:
        print_board(board)
        print(f"Player {CHECKERS[current_player]}, please enter a column: ")
        
        while True:
            try:
                col = input().upper()
                if len(col) != 1:
                    raise ValueError
                col_num = ord(col) - ord('A')
                if not is_valid_move(board, col_num):
                    raise ValueError
                break
            except ValueError:
                print("Invalid input. Please enter a valid column (A-" + chr(65 + COLS - 1) + "):")
        
        if drop_checker(board, col_num, CHECKERS[current_player]):
            if check_win(board, CHECKERS[current_player]):
                print_board(board)
                print(f"Player {CHECKERS[current_player]} won!")
                game_over = True
            elif is_draw(board):
                print_board(board)
                print("It's a draw!")
                game_over = True
            else:
                current_player = (current_player + 1) % PLAYERS
        else:
            current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
