import os
import random

ROWS = 6
COLS = 7
COL_LABELS = "ABCDEFG"
PLAYERS = ['X', 'O', 'V', 'H', 'M']    # Can have 2-5 players using these tokens

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print(" " + " ".join(COL_LABELS))  # Column headers
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLS * 2 + 1))  # Bottom border

def get_player_input(player, board):
    while True:
        choice = input(f"Player {player}, choose a column (A-G): ").upper()
        if choice not in COL_LABELS:
            print("Invalid column. Please enter a letter from A to G.")
            continue
        col = COL_LABELS.index(choice)
        if board[0][col] != ' ':
            print("That column is full. Try a different one.")
            continue
        return col

def drop_piece(board, col, player):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col

def check_win(board, player):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True
    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True
    # Check diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True
    # Check diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    # Ask number of players
    while True:
        try:
            num_players = int(input("Enter number of players (2-5): "))
            if 2 <= num_players <= 5:
                break
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input. Enter a number.")

    players = PLAYERS[:num_players]

    board = create_board()

    current_player_index = random.randint(0, num_players -1)

    while True:
        clear_screen()
        print_board(board)
        player = players[current_player_index]

        col = get_player_input(player, board)
        drop_piece(board, col, player)

        if check_win(board, player):
            clear_screen()
            print_board(board)
            print(f"Player {player} wins! Congratulations!")
            break
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
