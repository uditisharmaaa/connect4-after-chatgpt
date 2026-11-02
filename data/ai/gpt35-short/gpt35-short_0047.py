import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players

def clear_screen():
    os.system('clear')  # For Unix/Linux/macOS; for Windows use 'cls'

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Print column labels
    print('  ' + ' '.join(COLUMN_LABELS))
    for r in range(ROWS):
        print('| ' + ' '.join(board[r]) + ' |')
    print('+' + '--'*COLS + '+')

def get_player_count():
    while True:
        try:
            count = int(input(f"Enter number of players (2-{len(PLAYER_SYMBOLS)}): "))
            if 2 <= count <= len(PLAYER_SYMBOLS):
                return count
            else:
                print(f"Please enter a number between 2 and {len(PLAYER_SYMBOLS)}.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_column_choice(current_player):
    while True:
        choice = input(f"Player {current_player} - Choose a column (A-G): ").upper()
        if choice in COLUMN_LABELS:
            return COLUMN_LABELS.index(choice)
        else:
            print("Invalid column. Please enter a letter from A to G.")

def is_valid_move(board, col):
    return board[0][col] == ' '

def apply_move(board, col, player):
    # Place player piece in the lowest empty slot
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col

def check_win(board, row, col, player):
    # Directions: horizontal, vertical, diagonal /
    # and diagonal \
    directions = [
        [(0, 1), (0, -1)],   # Horizontal
        [(1, 0), (-1, 0)],   # Vertical
        [(1, 1), (-1, -1)],  # Diagonal \
        [(1, -1), (-1, 1)]   # Diagonal /
    ]

    for direction in directions:
        count = 1  # current piece counts as 1
        for dr, dc in direction:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def check_draw(board):
    # If top row is full (no spaces)
    return all(cell != ' ' for cell in board[0])

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    player_count = get_player_count()
    players = PLAYER_SYMBOLS[:player_count]

    current_index = random.randint(0, player_count -1)
    current_player = players[current_index]

    board = create_board()

    while True:
        clear_screen()
        print_board(board)
        print(f"Players: {', '.join(players)}")
        print(f"Current player: {current_player}")

        col = get_column_choice(current_player)
        if not is_valid_move(board, col):
            print("Column is full. Try again.")
            input("Press Enter to continue...")
            continue

        row, col = apply_move(board, col, current_player)

        if check_win(board, row, col, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} wins! Congratulations!")
            break

        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw! No more moves possible.")
            break

        # Move to next player
        current_index = (current_index + 1) % player_count
        current_player = players[current_index]

if __name__ == "__main__":
    main()
