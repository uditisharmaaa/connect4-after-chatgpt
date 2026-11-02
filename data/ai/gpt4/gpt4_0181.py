import os
import random

# Constants
ROWS, COLS = 6, 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(i) for i in range(ord('A'), ord('A') + COLS)))
    print(("+" + "---+" * COLS))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print(("+" + "---+" * COLS))

def is_valid_input(column, board):
    if column not in range(COLS):
        return False
    return board[0][column] == " "

def drop_checker(board, column, symbol):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = symbol
            break

def check_win(board, symbol):
    # Horizontal check
    for y in range(ROWS):
        for x in range(COLS - 3):
            if all(board[y][x + i] == symbol for i in range(4)):
                return True
    # Vertical check
    for x in range(COLS):
        for y in range(ROWS - 3):
            if all(board[y + i][x] == symbol for i in range(4)):
                return True
    # Diagonal (\) check
    for y in range(ROWS - 3):
        for x in range(COLS - 3):
            if all(board[y + i][x + i] == symbol for i in range(4)):
                return True
    # Diagonal (/) check
    for y in range(3, ROWS):
        for x in range(COLS - 3):
            if all(board[y - i][x + i] == symbol for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def get_column_input():
    while True:
        inp = input("Please enter a column: ").strip().upper()
        if len(inp) == 1 and 'A' <= inp <= 'G':
            return ord(inp) - ord('A')
        print("Invalid input. Try again.")

def main():
    random.seed()
    board = create_board()
    num_players = 2
    players = PLAYER_SYMBOLS[:num_players]
    current_player = random.choice(players)
    
    print_board(board)
    
    while True:
        print(f"Player {current_player}'s turn.")
        column = get_column_input()
        
        if is_valid_input(column, board):
            drop_checker(board, column, current_player)
            print_board(board)
            
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            if is_draw(board):
                print("The game is a draw!")
                break
            
            current_player = players[(players.index(current_player) + 1) % num_players]
        else:
            print("Column is full. Try again.")

if __name__ == "__main__":
    main()
