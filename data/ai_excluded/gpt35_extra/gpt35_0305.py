import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Maximum 5 players, we only use first PLAYERS elements
WIN_CONDITION = 4

def clear_screen():
    os.system('clear')

def create_board():
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board

def print_board(board):
    clear_screen()
    # Print column labels
    labels = "  "
    for i in range(COLUMNS):
        labels += " " + chr(ord('A') + i) + "  "
    print(labels)
    # Print board rows
    for r in range(ROWS):
        print("+---" * COLUMNS + "+")
        line = "|"
        for c in range(COLUMNS):
            line += " " + board[r][c] + " |"
        print(line)
    print("+---" * COLUMNS + "+")

def get_valid_column_input(player_checker):
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(col_input) != 1:
            print("Invalid input! Please enter a single letter representing a column.")
            continue
        if col_input < 'A' or col_input >= chr(ord('A') + COLUMNS):
            print("Invalid input! Column out of range.")
            continue
        col = ord(col_input) - ord('A')
        return col

def place_checker(board, col, player_checker):
    # Place the checker in the lowest empty spot in the column
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return row, col
    # Column full
    return None, None

def check_win(board, row, col, player_checker):
    # Directions: horizontal, vertical, diagonal /
    directions = [
        (0,1), # horizontal right
        (1,0), # vertical down
        (1,1), # diagonal down-right
        (1,-1) # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_checker:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_CONDITION:
            return True
    return False

def board_full(board):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    players_checkers = CHECKERS[:PLAYERS]
    
    # Randomly select first player
    current_player_index = random.randint(0, PLAYERS -1)
    
    print_board(board)
    
    while True:
        player_checker = players_checkers[current_player_index]
        col = get_valid_column_input(player_checker)
        row, placed_col = place_checker(board, col, player_checker)
        if row is None:
            # Column full => player loses turn
            print(f"Column {chr(ord('A')+col)} is full! Player {player_checker} loses the turn.")
        else:
            print_board(board)
            if check_win(board, row, placed_col, player_checker):
                print(f"Player {player_checker} won!")
                break
            if board_full(board):
                print("The game is a draw!")
                break
        # Next player's turn
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
