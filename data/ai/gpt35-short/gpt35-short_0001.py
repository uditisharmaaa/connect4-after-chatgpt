import random
import os

ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # max 5 players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print('  ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('| ' + ' '.join(row) + ' |')
    print('+-----------------+')

def get_player_count():
    while True:
        try:
            n = int(input("How many players (2-5)? "))
            if 2 <= n <= 5:
                return n
            else:
                print("Please choose between 2 and 5 players.")
        except ValueError:
            print("Please enter a valid integer.")

def get_column_choice(player):
    while True:
        choice = input(f"Player {player}'s turn. Choose column (A-G): ").upper()
        if choice in COLUMN_LABELS:
            col = COLUMN_LABELS.index(choice)
            return col
        else:
            print("Invalid column. Choose a letter from A to G.")

def is_valid_move(board, col):
    return board[0][col] == ' '

def make_move(board, col, player):
    # Place the player's marker in the lowest empty row of the column
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = player
            return r, col  # Return the position where piece was placed

def check_direction(board, start_r, start_c, dr, dc, player):
    count = 0
    r, c = start_r, start_c
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
        count += 1
        r += dr
        c += dc
    return count

def check_win(board, r, c, player):
    # Check all 4 directions for 4 in a row:
    # horizontal, vertical, diagonal /
    # and diagonal \
    
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # count the piece just placed
        # count in positive direction
        count += check_direction(board, r+dr, c+dc, dr, dc, player)
        # count in negative direction
        count += check_direction(board, r-dr, c-dc, -dr, -dc, player)
        if count >= 4:
            return True
    return False

def is_board_full(board):
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    num_players = get_player_count()
    players = PLAYERS[:num_players]
    board = create_board()
    current_player_idx = random.randint(0, num_players -1)
    
    while True:
        clear_screen()
        print_board(board)
        player = players[current_player_idx]
        
        # get valid move
        col = get_column_choice(player)
        if not is_valid_move(board, col):
            print("That column is full! Try again.")
            input("Press Enter to continue...")
            continue
        
        r, c = make_move(board, col, player)
        
        if check_win(board, r, c, player):
            clear_screen()
            print_board(board)
            print(f"Player {player} wins! Congratulations!")
            break
        
        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more moves possible.")
            break
        
        # next player's turn
        current_player_idx = (current_player_idx +1) % num_players

if __name__ == "__main__":
    main()
