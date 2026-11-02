import random
import os

# Constants
ROWS = 6
COLS =7PLAYERS = ['X', 'O']
CHECKER_COUNT_TO_WIN = 4

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    header = ' '.join([chr(65 + col) for col in range(len(board[0]))])
    print(f"  {header}")
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(row) + "+")

def get_player_input(player, board):
    while True:
        column = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(column) != 1 or not column.isalpha() or ord(column) < 65 or ord(column) >= 65 + COLS:
            print("Invalid input. Please enter a valid column letter.")
        elif board[0][ord(column) - 65] != ' ':
            print("This column is full. Please choose another column.")
        else:
            return ord(column) - 65

def place_checker(board, column, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = player
            break

def check_win(board, player):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - CHECKER_COUNT_TO_WIN + 1):
            if all(board[row][col + i] == player for i in range(CHECKER_COUNT_TO_WIN)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - CHECKER_COUNT_TO_WIN + 1):
            if all(board[row + i][col] == player for i in range(CHECKER_COUNT_TO_WIN)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - CHECKER_COUNT_TO_WIN + 1):
        for col in range(COLS - CHECKER_COUNT_TO_WIN + 1):
            if all(board[row + i][col + i] == player for i in range(CHECKER_COUNT_TO_WIN)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(CHECKER_COUNT_TO_WIN - 1, ROWS):
        for col in range(COLS - CHECKER_COUNT_TO_WIN + 1):
            if all(board[row - i][col + i] == player for i in range(CHECKER_COUNT_TO_WIN)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    board = create_board(ROWS, COLS)
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    print_board(board)

    while True:
        player = PLAYERS[current_player_index]
        column = get_player_input(player, board)
        place_checker(board, column, player)
        print_board(board)

        if check_win(board, player):
            print(f"Player {player} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
