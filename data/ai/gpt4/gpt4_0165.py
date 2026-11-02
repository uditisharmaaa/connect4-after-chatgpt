import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def valid_column(column, board):
    return column in range(COLUMNS) and board[0][column] == " "

def place_checker(board, column, symbol):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = symbol
            return

def check_direction(board, start_row, start_col, dr, dc, symbol):
    count = 0
    row, col = start_row, start_col
    while 0 <= row < ROWS and 0 <= col < COLUMNS and board[row][col] == symbol:
        count += 1
        row += dr
        col += dc
    return count

def check_win(board, symbol):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == symbol:
                if (check_direction(board, row, col, 0, 1, symbol) >= 4 or  # Horizontal
                    check_direction(board, row, col, 1, 0, symbol) >= 4 or  # Vertical
                    check_direction(board, row, col, 1, 1, symbol) >= 4 or  # Diagonal \
                    check_direction(board, row, col, 1, -1, symbol) >= 4):  # Diagonal /
                    return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    board = create_board()
    players = PLAYER_SYMBOLS[:2]  # Adjust for num players
    current_player = random.randint(0, len(players) - 1)
    
    print_board(board)
    while True:
        symbol = players[current_player]
        print(f"Player {symbol}, please enter a column:")
        
        while True:
            try:
                user_input = input().strip().upper()
                column = ord(user_input) - 65
                if valid_column(column, board):
                    place_checker(board, column, symbol)
                    break
                else:
                    print("Invalid input. Try again:")
            except (ValueError, IndexError):
                print("Invalid input. Try again:")
        
        print_board(board)
        
        if check_win(board, symbol):
            print(f"Player {symbol} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % len(players)

if __name__ == "__main__":
    main()
