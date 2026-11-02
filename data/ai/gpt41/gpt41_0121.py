import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2  # You can set this between 2 and 5

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    columns = len(board[0])
    # Print column labels
    labels = [chr(ord("A") + i) for i in range(columns)]
    print("  " + "   ".join(labels))
    # Print top border
    print("+---" * columns + "+")
    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * columns + "+")

def pick_random_player(num_players):
    return random.randint(0, num_players - 1)

def get_player_move(player_token, columns):
    while True:
        move = input(f"Player {player_token}, please enter a column: ")
        if len(move) != 1 or not move.isalpha() or not move.isupper():
            print("Invalid input. Enter a single uppercase letter for column.")
            continue
        col_index = ord(move) - ord("A")
        if 0 <= col_index < columns:
            return col_index
        else:
            print("Column out of range. Try again.")

def is_column_full(board, col):
    return board[0][col] != " "

def place_token(board, col, token):
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = token
            return row, col
    return None, None  # Should not happen if checked before

def is_board_full(board):
    return all(cell != " " for cell in board[0])

def check_winner(board, last_row, last_col, player_token):
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # Include the last placed token
        # Check one direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == player_token:
            count += 1
            r += dr
            c += dc
        # Check opposite direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == player_token:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def main():
    board = create_board(ROWS, COLUMNS)
    player_tokens = PLAYER_TOKENS[:NUM_PLAYERS]
    current_player_idx = pick_random_player(NUM_PLAYERS)
    clear_screen()
    print_board(board)
    game_over = False
    while not game_over:
        token = player_tokens[current_player_idx]
        col = get_player_move(token, COLUMNS)
        if is_column_full(board, col):
            print("Column is full. You lose your turn.")
            # Move to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue
        row, col = place_token(board, col, token)
        clear_screen()
        print_board(board)
        # Check for win
        if check_winner(board, row, col, token):
            print(f"Player {token} won!")
            game_over = True
            break
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            game_over = True
            break
        # Next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
