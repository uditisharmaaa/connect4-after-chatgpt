import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = "ABCDEFG"
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column labels
    print('  ' + ' '.join(COLUMN_LABELS))
    # Print board rows from top to bottom
    for row in board:
        print('| ' + ' '.join(row) + ' |')
    print('-' * (COLS * 2 + 3))

def is_valid_column(col):
    return 0 <= col < COLS

def is_column_not_full(board, col):
    return board[0][col] == ' '

def drop_piece(board, col, player):
    # Drop piece in the lowest available row
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col

def check_win(board, player):
    # Check horizontal locations for win
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == player for i in range(4)):
                return True

    # Check vertical locations for win
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == player for i in range(4)):
                return True

    # Check positively sloped diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == player for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i][c+i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    # If top row is full for all columns, it's a draw
    return all(board[0][c] != ' ' for c in range(COLS))

def get_player_input(player):
    while True:
        user_input = input(f"Player {player}, choose a column (A-G): ").strip().upper()
        if user_input in COLUMN_LABELS:
            col = COLUMN_LABELS.index(user_input)
            return col
        else:
            print("Invalid input. Please enter a letter from A to G.")

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    
    # Choose number of players
    while True:
        try:
            num_players = int(input(f"Enter number of players (2 to {len(PLAYERS)}): "))
            if 2 <= num_players <= len(PLAYERS):
                break
            else:
                print("Invalid number of players.")
        except ValueError:
            print("Please enter a valid integer.")

    players = PLAYERS[:num_players]

    board = create_board()
    current_player_index = random.randint(0, num_players - 1)
    game_over = False

    while not game_over:
        print_board(board)
        print(f"It's {players[current_player_index]}'s turn.")

        col = get_player_input(players[current_player_index])

        if not is_column_not_full(board, col):
            print("That column is full, try a different one.")
            continue

        row, col = drop_piece(board, col, players[current_player_index])

        if check_win(board, players[current_player_index]):
            print_board(board)
            print(f"Player {players[current_player_index]} wins! Congrats!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("Game over! It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % num_players

    print("Thanks for playing!")

if __name__ == '__main__':
    main()
