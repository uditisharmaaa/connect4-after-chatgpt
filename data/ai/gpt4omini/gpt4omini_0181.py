import os
import random

WIDTH = 7
HEIGHT = 6
PLAYERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2

def create_board():
    return [[' ' for _ in range(WIDTH)] for _ in range(HEIGHT)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(WIDTH)))
    print("+" + "---+" * WIDTH)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * WIDTH)

def is_valid_input(col):
    if len(col) != 1 or not col.isalpha():
        return False
    col_index = ord(col.upper()) - 65
    return 0 <= col_index < WIDTH

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal, vertical and two diagonal wins
    for r in range(HEIGHT):
        for c in range(WIDTH):
            if c + 3 < WIDTH and all(board[r][c + i] == checker for i in range(4)):
                return True
            if r + 3 < HEIGHT and all(board[r + i][c] == checker for i in range(4)):
                return True
            if r + 3 < HEIGHT and c + 3 < WIDTH and all(board[r + i][c + i] == checker for i in range(4)):
                return True
            if r - 3 >= 0 and c + 3 < WIDTH and all(board[r - i][c + i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        print_board(board)
        player = PLAYERS[current_player_index]
        col = input(f"Player {player}, please enter a column: ").upper()
        
        while not is_valid_input(col):
            col = input("Invalid input. Please enter a valid column: ").upper()
        
        col_index = ord(col) - 65
        if not drop_checker(board, col_index, player):
            print("Column is full. Your turn is lost.")
        else:
            if check_win(board, player):
                print_board(board)
                print(f"Player {player} won!")
                break
            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break
            
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
