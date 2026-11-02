import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    print("  " + "   ".join(chr(65 + col) for col in range(len(board[0]))))
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def is_valid_column(board, col):
    return 0 <= col < len(board[0]) and board[0][col] == " "

def get_column_input(board):
    while True:
        col_input = input("Please enter a column: ").strip()
        if len(col_input) == 1 and col_input.isalpha():
            col = ord(col_input.upper()) - 65
            if is_valid_column(board, col):
                return col
        print("Invalid column. Try again.")

def drop_checker(board, col, token):
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = token
            return row, col

def check_winner(board, last_row, last_col, token):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for step in (-1, 1):
            r, c = last_row, last_col
            while True:
                r += dr * step
                c += dc * step
                if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == token:
                    count += 1
                else:
                    break
            if count >= 4:
                return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(len(board[0])))

def main():
    clear_screen()
    board = create_board(ROWS, COLUMNS)
    num_players = 2  # Fixed for this assignment
    players = PLAYER_TOKENS[:num_players]
    current_player = random.randint(0, num_players - 1)
    
    print("Welcome to Connect 4!")
    print_board(board)
    
    while True:
        print(f"Player {players[current_player]}'s turn.")
        col = get_column_input(board)
        
        row, col = drop_checker(board, col, players[current_player])
        clear_screen()
        print_board(board)
        
        if check_winner(board, row, col, players[current_player]):
            print(f"Player {players[current_player]} won!")
            break
        elif is_draw(board):
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
