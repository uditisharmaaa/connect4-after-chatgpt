import os
import random

# Constants
ROWS = 6
COLS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Players: max 5 players, pick number of players here
ALL_PLAYERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 3  # Change between 2 and 5 (inclusive)

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print("  " + " ".join(COL_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("=" * (COLS * 2 + 1))

def get_next_player(current_index, num_players):
    return (current_index + 1) % num_players

def col_label_to_index(label):
    label = label.upper()
    if label in COL_LABELS:
        return COL_LABELS.index(label)
    return -1

def is_valid_move(board, col):
    return board[0][col] == ' '

def make_move(board, col, player):
    # drop token in the lowest empty row in the column
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col
    return None  # Should never happen if checked before

def check_win(board, player, row, col):
    # Directions: horizontal, vertical, diag /
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    
    for dr, dc in directions:
        count = 1  # count the placed token
        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        # Check opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def check_draw(board):
    # Draw if no spaces in top row
    return all(cell != ' ' for cell in board[0])

def get_player_input(player, board):
    while True:
        user_input = input(f"Player {player}, choose column (A-G): ").strip()
        col = col_label_to_index(user_input)
        if col == -1:
            print("Invalid column. Choose a letter from A to G.")
            continue
        if not is_valid_move(board, col):
            print(f"Column {user_input.upper()} is full. Choose another.")
            continue
        return col

def main():
    board = create_board()
    players = ALL_PLAYERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS -1)
    
    while True:
        clear_screen()
        print_board(board)
        current_player = players[current_player_index]
        
        col = get_player_input(current_player, board)
        row, col = make_move(board, col, current_player)
        
        if check_win(board, current_player, row, col):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} wins! Congratulations!")
            break
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more moves possible.")
            break
        current_player_index = get_next_player(current_player_index, NUM_PLAYERS)

if __name__ == "__main__":
    main()
