import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')  # Use 'cls' on Windows if necessary

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Column labels
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_column(column, board):
    return column.isalpha() and 'A' <= column < chr(65 + COLS) and board[0][ord(column) - 65] == " "

def drop_checker(column, board, checker):
    col_idx = ord(column) - 65
    for row in reversed(range(ROWS)):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx

def check_win(board, player, row, col):
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for dr, dc in directions:
        count = 1
        for i in range(1, 4):  # Check forward direction
            r, c = row + dr * i, col + dc * i
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                count += 1
            else:
                break
        for i in range(1, 4):  # Check backward direction
            r, c = row - dr * i, col - dc * i
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                count += 1
            else:
                break
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def main():
    clear_screen()
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)
    
    print_board(board)
    print(f"Player {current_player} goes first!\n")
    
    while True:
        print_board(board)
        column = input(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        
        if not is_valid_column(column, board):
            print("Invalid input. Please try again.")
            continue
        
        row, col = drop_checker(column, board, current_player)
        if check_win(board, current_player, row, col):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_index = players.index(current_player)
        current_player = players[(current_index + 1) % PLAYERS]

if __name__ == "__main__":
    main()
