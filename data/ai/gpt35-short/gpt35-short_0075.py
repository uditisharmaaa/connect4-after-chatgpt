import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print("  " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLS * 2 + 1))

def get_num_players():
    while True:
        try:
            n = int(input("Enter number of players (2-5): "))
            if 2 <= n <= 5:
                return n
            print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input, please enter a number.")

def get_player_move(player_token, board):
    while True:
        col = input(f"Player {player_token}, choose a column (A-G): ").upper()
        if col not in COLUMN_LABELS:
            print("Invalid column. Choose between A and G.")
            continue
        col_idx = COLUMN_LABELS.index(col)
        if board[0][col_idx] != ' ':
            print("Column is full, choose another.")
            continue
        return col_idx

def drop_token(board, col, token):
    # Place the token in the lowest available row in the column
    for row in range(ROWS -1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = token
            return row, col

def check_winner(board, token, row, col):
    # Directions: horizontal, vertical, diagonal /
    directions = [
        [(0, -1), (0, 1)],      # Horizontal
        [(-1, 0), (1, 0)],      # Vertical
        [(-1, -1), (1, 1)],     # Diagonal \
        [(-1, 1), (1, -1)]      # Diagonal /
    ]
    
    for direction in directions:
        count = 1  # count the placed token
        for dr, dc in direction:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == token:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    clear_screen()
    print("Welcome to Connect 4!\n")
    num_players = get_num_players()
    players = PLAYER_TOKENS[:num_players]
    current_player_index = random.randint(0, num_players - 1)
    board = create_board()
    
    while True:
        clear_screen()
        print_board(board)
        current_token = players[current_player_index]
        col = get_player_move(current_token, board)
        row, col = drop_token(board, col, current_token)
        
        if check_winner(board, current_token, row, col):
            clear_screen()
            print_board(board)
            print(f"Player {current_token} wins! Congratulations!")
            break
        
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break
        
        # Next player's turn
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
