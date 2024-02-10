import json

from prettytable import PrettyTable

from src.utils.utils import clear_terminal


def show_user_comments(client, movie):
    while True:
        request_data = json.dumps({
            'payload': {
                'movie_id': movie['id'],
            },
            'url': 'get_user_comments'
        })
        client.send(request_data.encode('utf-8'))
        response = client.recv(5 * 1024).decode('utf-8')
        response = json.loads(response)
        if response['status_code'] == 200:
            comments = response['comments']
        else:
            clear_terminal()
            print(response['msg'])
            continue

        table = PrettyTable(['Id', 'Description', 'Reply To', 'Created At'])

        for comment in comments:
            table.add_row([comment['id'], comment['description'][:15] + '...', comment['reply_to'] if comment['reply_to'] else None, comment['created_at']])
        print(table)

        selected_comment = input('Enter Id of Comment: ')
        if selected_comment in map(str, [comment['id'] for comment in comments]):
            return selected_comment
        elif selected_comment == 'quit':
            break
        else:
            clear_terminal()
            print('Invalid Comment ID')
            continue


def main(client, movie):
    while True:
        print("comments and id of comments")

        user_input = input(
            '\n1. Add comment\n2. Delete comment\n3. Update comment\n4. Reply to comment\n5. Quit\n\n:').strip().lower()

        if user_input == '5' or user_input == 'quit':
            clear_terminal()
            break
        elif user_input == '1' or user_input == 'add comment':
            while True:
                description = input("Enter a description: ").strip().lower()

                request_data = json.dumps({
                    'payload': {
                        'description': description,
                        'movie_id': movie['id'],
                    },
                    'url': 'add_comment'
                })
                client.send(request_data.encode('utf-8'))
                response = client.recv(5 * 1024).decode('utf-8')
                response = json.loads(response)
                if response['status_code'] == 200:
                    comment = response['comment']
                    print("Comment Added!")
                    print(
                        f"Comment ID: {comment['id']} \nDescription: {comment['description'][:15]}...\nCreated At: {comment['created_at']}")
                    break
                else:
                    clear_terminal()
                    print(response['msg'])
                    continue

        elif user_input == '2' or user_input == 'delete comment':
            while True:
                selected_comment = show_user_comments(client, movie)
                if not selected_comment:
                    break

                request_data = json.dumps({
                    'payload': {
                        'comment_id': selected_comment,
                    },
                    'url': 'delete_comment'
                })
                client.send(request_data.encode('utf-8'))
                response = client.recv(5 * 1024).decode('utf-8')
                response = json.loads(response)
                if response['status_code'] == 200:
                    print('Comment Deleted Successfully')
                    break
                else:
                    clear_terminal()
                    print(response['msg'])
                    continue

        elif user_input == '3' or user_input == 'update comment':
            while True:
                selected_comment = show_user_comments(client, movie)
                if not selected_comment:
                    break
                new_description = input('Enter New Description: ')

                if not new_description:
                    clear_terminal()
                    print('Invalid Description')
                    continue

                request_data = json.dumps({
                    'payload': {
                        'comment_id': selected_comment,
                        'new_description': new_description
                    },
                    'url': 'update_comment'
                })
                client.send(request_data.encode('utf-8'))
                response = client.recv(5 * 1024).decode('utf-8')
                response = json.loads(response)
                if response['status_code'] == 200:
                    print('Comment Updated Successfully')
                    break
                else:
                    clear_terminal()
                    print(response['msg'])
                    continue

        elif user_input == '4' or user_input == 'reply to comment':
            while True:
                selected_comment = show_user_comments(client, movie)
                if not selected_comment:
                    break
                description = input("Enter a description: ").strip().lower()

                request_data = json.dumps({
                    'payload': {
                        'description': description,
                        'movie_id': movie['id'],
                        'reply_to': selected_comment,
                    },
                    'url': 'add_comment_reply'
                })
                client.send(request_data.encode('utf-8'))
                response = client.recv(5 * 1024).decode('utf-8')
                response = json.loads(response)
                if response['status_code'] == 200:
                    comment = response['comment']
                    print("Comment Added!")
                    print(
                        f"Comment ID: {comment['id']} \nDescription: {comment['description'][:15]}...\nCreated At: {comment['created_at']}")
                    break
                else:
                    clear_terminal()
                    print(response['msg'])
                    continue


if __name__ == "__main__":
    main()
