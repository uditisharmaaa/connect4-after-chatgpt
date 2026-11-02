import os
import random

# ----- CONSTANTS -----
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_CHARS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2  # Change to 3, 4, 5, etc. to support more players
CONNECT_N = 4

# ----- FUNCTIONS -----

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    column_headers = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(column_headers))
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def get_lowest_empty_row(board, col):
    for r in reversed(range(len(board))):
        if board[r][col] == " ":
            return r
    return None

def is_valid_column(board, col):
    return 0 <= col < len(board[0]) and board[0][col] == " "

def get_column_from_input(inp, col_count):
    if len(inp) != 1 or not inp.isalpha():
        return None
    col = ord(inp.upper()) - ord('A')
    if 0 <= col < col_count:
        return col
    else:
        return None

def board_full(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def check_win(board, row, col, player_char):
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # current checker
        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == player_char:
            count += 1
            r += dr
            c += dc
        # Check the other direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == player_char:
            count += 1
            r -= dr
            c -= dc
        if count >= CONNECT_N:
            return True
    return False

def choose_start_player(num_players):
    return random.randint(0, num_players-1)

# ----- MAIN GAME LOOP -----
def main():
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_CHARS[:NUM_PLAYERS]
    current_player = choose_start_player(NUM_PLAYERS)
    print_board(board)
    
    while True:
        player_char = players[current_player]
        print(f"Player {player_char}, please enter a column:")
        col_input = input().strip()
        
        col = get_column_from_input(col_input, COLUMNS)
        if col is None:
            print("Invalid input. Please enter a valid column letter (e.g., A, B, ...).")
            continue
        if not is_valid_column(board, col):
            print(f"Column {chr(col + ord('A'))} is full or invalid. You lose your turn!")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        # Place checker
        row = get_lowest_empty_row(board, col)
        board[row][col] = player_char
        print_board(board)
        
        # Check for a win
        if check_win(board, row, col, player_char):
            print(f"Player {player_char} won!")
            break
        # Check for a draw
        if board_full(board):
            print("The game is a draw!")
            break
        
        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
