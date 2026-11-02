import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2  # Change this for more players up to 5
CHECKERS = ["X", "O", "V", "H", "M"]

def print_board(board):
    os.system('clear')
    column_labels = "  ".join([chr(i + 65) for i in range(COLUMNS)])
    print("  " + column_labels)
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def init_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def get_next_empty_row(board, column_index):
    for row in range(ROWS-1, -1, -1):
        if board[row][column_index] == " ":
            return row
    return None

def check_for_win(board, player_checker):
    # Check horizontal, vertical, and diagonal directions for a win
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (col <= COLUMNS - 4 and all(board[row][col+i] == player_checker for i in range(4))):
                return True
            if (row <= ROWS - 4 and all(board[row+i][col] == player_checker for i in range(4))):
                return True
            if (row <= ROWS - 4 and col <= COLUMNS - 4 and all(board[row+i][col+i] == player_checker for i in range(4))):
                return True
            if (row >= 3 and col <= COLUMNS - 4 and all(board[row-i][col+i] == player_checker for i in range(4))):
                return True
    return False

def check_for_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = init_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, PLAYERS - 1)
    player_checkers = CHECKERS[:PLAYERS]

    while True:
        print_board(board)
        player_checker = player_checkers[current_player_index]
        print(f"Player {player_checker}, please enter a column:")

        while True:
            entry = input().upper()
            if not entry or len(entry) != 1 or not entry.isalpha() or ord(entry) - 65 >= COLUMNS:
                print("Invalid input. Please enter a valid column letter:")
                continue
            
            column_index = ord(entry) - 65
            row_index = get_next_empty_row(board, column_index)
            
            if row_index is None:
                print("Column is full. Please enter a different column:")
            else:
                board[row_index][column_index] = player_checker
                break
        
        if check_for_win(board, player_checker):
            print_board(board)
            print(f"Player {player_checker} won!")
            break
        
        if check_for_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
