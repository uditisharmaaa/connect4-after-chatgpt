import os
import random

ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(i) for i in range(65, 65 + COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(col_input):
    if len(col_input) == 1 and 'A' <= col_input <= 'G':
        return True
    return False

def find_empty_row(board, col):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            return row
    return -1

def place_checker(board, col, player):
    row = find_empty_row(board, col)
    if row != -1:
        board[row][col] = player
        return True
    return False

def check_win(board, player):
    for r in range(ROWS):
        for c in range(COLS):
            if (c + 3 < COLS and all(board[r][c + i] == player for i in range(4))) or \
               (r + 3 < ROWS and all(board[r + i][c] == player for i in range(4))) or \
               (r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == player for i in range(4))) or \
               (r - 3 >= 0 and c + 3 < COLS and all(board[r - i][c + i] == player for i in range(4))):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    board = create_board()
    current_player_index = random.randint(0, 1)
    
    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        col_input = input(f"Player {current_player}, please enter a column (A-G): ").upper()

        if not is_valid_input(col_input):
            print("Invalid input. Please enter a valid column letter (A-G).")
            continue
            
        col = ord(col_input) - 65
        
        if place_checker(board, col, current_player):
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break
            current_player_index = (current_player_index + 1) % len(PLAYERS)
        else:
            print("Column is full. Try another column.")

if __name__ == '__main__':
    main()
