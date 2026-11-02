import os
import random

# ----- CONSTANTS -----
ROWS = 6                  # Number of rows
COLS = 7                  # Number of columns (max 26)
NUM_PLAYERS = 2           # Number of players (2-5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Possible checkers for up to 5 players
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# ----- BOARD FUNCTIONS -----

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    # Print column letters
    print('  ' + '   '.join(ALPHABET[:COLS]))
    # Print top border
    print('+' + '---+' * COLS)
    # Print each row
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLS)

# ----- GAME LOGIC -----

def get_move(player, board):
    while True:
        move = input(f"Player {player}, please enter a column: ").strip().upper()
        # --- Validation ---
        if len(move) != 1 or move not in ALPHABET[:COLS]:
            print("Invalid input. Please enter a valid column letter.")
            continue
        col = ALPHABET.index(move)
        if board[0][col] != " ":
            print("Column is full. You lose your turn.")
            return None  # lose turn if full
        return col

def drop_checker(board, col, checker):
    # Place checker at the lowest available position in the given column
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col  # return the (row, col) placed
    # This should not happen due to earlier check for full column
    return None

def check_for_win(board, row, col, checker):
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Down-right diagonal
        (1, -1),  # Down-left diagonal
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    # Draw if no space in top row
    return all(cell != " " for cell in board[0])

# ----- MAIN LOOP -----

def main():
    board = create_board()
    player_checkers = CHECKERS[:NUM_PLAYERS]
    current = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    print(f"Player {player_checkers[current]} moves first!")

    while True:
        player = player_checkers[current]
        
        col = get_move(player, board)
        if col is None:
            # Player lost the turn (column full), go to next player
            current = (current + 1) % NUM_PLAYERS
            continue
        
        row, col_pos = drop_checker(board, col, player)
        print_board(board)
        
        if check_for_win(board, row, col_pos, player):
            print(f"Player {player} won!")
            break
        
        if is_draw(board):
            print("It's a draw!")
            break
        
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
