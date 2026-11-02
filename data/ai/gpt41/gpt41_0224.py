import os
import random
import string

# ----------- CONSTANTS -----------

ROWS = 6            # Number of rows of the board
COLS = 7            # Number of columns of the board (max 26)
NUM_PLAYERS = 2     # Change this value to allow for 2-5 players

# Allowed player symbols
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# ----------- FUNCTIONS -----------

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Print column letters
    col_labels = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(col_labels))
    print('+' + '---+' * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print('+' + '---+' * cols)

def get_player_symbols(num_players):
    return PLAYER_SYMBOLS[:num_players]

def is_valid_column(input_str, cols):
    return (len(input_str) == 1 and input_str in string.ascii_uppercase[:cols])

def column_is_full(board, col_idx):
    return board[0][col_idx] != ' '

def get_valid_column_input(current_player, cols, board):
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if not is_valid_column(user_input, cols):
            print(f"Invalid input. Please enter a letter between A and {string.ascii_uppercase[cols-1]}.")
            continue
        col_idx = string.ascii_uppercase.index(user_input)
        if column_is_full(board, col_idx):
            print("Column is full. You lose your turn!")
            return None  # Return None to indicate a lost turn
        return col_idx

def place_checker(board, col_idx, player_symbol):
    # Place in the lowest available row in column col_idx
    for row in reversed(range(len(board))):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = player_symbol
            return row, col_idx
    return None  # Should not happen if checked for a full column

def check_win(board, player_symbol, last_row, last_col):
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal /
        (1, -1),  # Diagonal \
    ]

    rows = len(board)
    cols = len(board[0])

    for drow, dcol in directions:
        count = 1
        # Check in the positive direction
        r, c = last_row + drow, last_col + dcol
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == player_symbol:
            count += 1
            r += drow
            c += dcol
        # Check in the negative direction
        r, c = last_row - drow, last_col - dcol
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == player_symbol:
            count += 1
            r -= drow
            c -= dcol
        if count >= 4:
            return True
    return False

def is_draw(board):
    # The game is a draw if there are no empty spaces in the top row
    return all(cell != ' ' for cell in board[0])

# ----------- MAIN GAME LOOP -----------

def main():
    # Set up player symbols for selected number of players
    num_players = NUM_PLAYERS
    player_symbols = get_player_symbols(num_players)
    rows, cols = ROWS, COLS

    board = create_board(rows, cols)
    
    # Pick random player to start
    current_player_idx = random.randrange(num_players)
    
    clear_screen()
    print_board(board)
    
    while True:
        current_player_symbol = player_symbols[current_player_idx]
        print()
        col_idx = get_valid_column_input(current_player_symbol, cols, board)
        if col_idx is not None:
            # Place checker
            row_idx, _ = place_checker(board, col_idx, current_player_symbol)
            clear_screen()
            print_board(board)
            
            # Check win
            if check_win(board, current_player_symbol, row_idx, col_idx):
                print(f"Player {current_player_symbol} won!")
                break
            
            # Check draw
            if is_draw(board):
                print("The game is a draw!")
                break
        else:
            # Player loses turn if column input but column is full
            pass
        
        # Next player's turn
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
