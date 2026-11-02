import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

NUM_PLAYERS = 3  # Change between 2 and 5 here

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print("  " + " ".join(COLUMN_LABELS))
    for row in board:
        print(" |" + "|".join(row) + "|")
    print(" +" + "-+" * COLS)

def get_valid_column_input(current_player):
    while True:
        user_input = input(f"Player {current_player}, choose column (A-G): ").upper()
        if user_input in COLUMN_LABELS:
            col = COLUMN_LABELS.index(user_input)
            return col
        else:
            print("Invalid input. Please enter a column between A and G.")

def is_column_full(board, col):
    return board[0][col] != ' '

def drop_piece(board, col, player):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col

def check_winner(board, player, row, col):
    # Directions: horizontal, vertical, diagonal /
    directions = [(0,1), (1,0), (1,1), (1,-1)]

    for dr, dc in directions:
        count = 1

        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    assert 2 <= NUM_PLAYERS <= 5, "NUM_PLAYERS must be between 2 and 5."
    players = PLAYERS[:NUM_PLAYERS]
    board = create_board()
    
    current_index = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        clear_screen()
        print_board(board)
        current_player = players[current_index]

        col = get_valid_column_input(current_player)

        if is_column_full(board, col):
            print("Column is full! Try another one.")
            input("Press Enter to continue...")
            continue

        row, col = drop_piece(board, col, current_player)

        if check_winner(board, current_player, row, col):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} wins! Congratulations!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break
        
        current_index = (current_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
