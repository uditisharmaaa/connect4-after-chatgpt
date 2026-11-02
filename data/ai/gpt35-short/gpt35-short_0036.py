import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print(" " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLS * 2 + 1))

def get_num_players():
    while True:
        try:
            n = int(input("Enter number of players (2-5): "))
            if 2 <= n <= 5:
                return n
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_move(player):
    while True:
        move = input(f"Player {player}, choose a column (A-G): ").upper()
        if move in COLUMN_LABELS:
            return COLUMN_LABELS.index(move)
        else:
            print("Invalid column. Please enter a letter from A to G.")

def is_valid_move(board, col):
    return board[0][col] == ' '

def make_move(board, col, player):
    # Drop piece to lowest empty row in column
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col

def check_winner(board, row, col, player):
    # Check all directions: horizontal, vertical, both diagonals

    def count_consecutive(r_step, c_step):
        count = 0
        r, c = row + r_step, col + c_step
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += r_step
            c += c_step
        return count

    directions = [
        (0, 1),  # Horizontal right
        (1, 0),  # Vertical down
        (1, 1),  # Diagonal down-right
        (1, -1), # Diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # Count the current piece
        count += count_consecutive(dr, dc)
        count += count_consecutive(-dr, -dc)
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(cell != ' ' for cell in board[0])

def next_player_index(current_index, total_players):
    return (current_index + 1) % total_players

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    num_players = get_num_players()
    players = PLAYERS[:num_players]

    board = create_board()
    current_player_index = random.randint(0, num_players - 1)

    while True:
        clear_screen()
        print_board(board)
        player = players[current_player_index]

        col = get_move(player)
        if not is_valid_move(board, col):
            print(f"Column {COLUMN_LABELS[col]} is full. Try again.")
            input("Press Enter to continue...")
            continue

        row, col = make_move(board, col, player)

        if check_winner(board, row, col, player):
            clear_screen()
            print_board(board)
            print(f"Player {player} wins!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        current_player_index = next_player_index(current_player_index, num_players)

    print("Game over.")

if __name__ == "__main__":
    main()
