import os

from src.utils.utils import clear_terminal

# incoming : all the comments and replies to comments for specified movie
# outgoing : any update for comments

def main(user_info, movie):
    while True:
        print("comments and id of comments")

        # input('1.add comment 2.reply to')

        # if input == 1 ...
        # if input == 2 ...

        user_input = input('\n1. Add comment\n2. Delete comment\n3. Update comment\n4.Reply to comment\n5. Quit\n\n:').strip().lower()

        if user_input == '6' or user_input == 'quit':
            clear_terminal()
            break
        elif user_input == '1' or user_input == 'add comment':
            ...
        elif user_input == '2' or user_input == 'delete comment':
            ...
        elif user_input == '3' or user_input == 'update comment':
            ...
        elif user_input == '4' or user_input == 'reply to comment':
            ...


if __name__ == "__main__":
    main('m', 'spiderman')
