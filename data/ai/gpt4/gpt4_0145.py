import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    column_labels = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(column_labels)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(column, board):
    return column.isalpha() and 0 <= (column_index := ord(column.upper()) - ord('A')) < len(board[0]) and board[0][column_index] == " "

def drop_checker(column, checker, board):
    column_index = ord(column.upper()) - ord('A')
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = checker
            return True
    return False

def check_win(board, row, col):
    def count_consecutive(dx, dy):
        count = 0
        x, y = row + dx, col + dy
        while 0 <= x < ROWS and 0 <= y < COLUMNS and board[x][y] == board[row][col]:
            count += 1
            x += dx
            y += dy
        return count

    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dx, dy in directions:
        if count_consecutive(dx, dy) + count_consecutive(-dx, -dy) + 1 >= 4:
            return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    # Initialize game
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_CHECKERS[:2]  # Set number of players to 2 (can use up to `MAX_PLAYERS`)
    current_player = random.randint(0, len(players) - 1)  # Random starting player

    # Game loop
    while True:
        print_board(board)
        print(f"Player {players[current_player]}, it's your turn!")

        # Player input
        while True:
            column = input("Please enter a column: ").strip()
            if is_valid_column(column, board):
                break
            print("Invalid input. Please try again.")

        # Drop the checker
        if not drop_checker(column, players[current_player], board):
            print("Column is full. You lost your turn!")

        # Check if the player won or if it's a draw
        for row in range(ROWS):
            for col in range(COLUMNS):
                if board[row][col] == players[current_player] and check_win(board, row, col):
                    print_board(board)
                    print(f"Player {players[current_player]} won!")
                    return
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            return

        # Switch to the next player
        current_player = (current_player + 1) % len(players)

if __name__ == "__main__":
    main()
