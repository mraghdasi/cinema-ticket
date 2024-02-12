import json
from secrets import compare_digest

from src.utils.custom_exceptions import UsernameValidationError, EmailValidationError, PhoneNumberValidationError, \
    PasswordValidationError, DateValidationError
from src.utils.custom_validators import Validator
from src.utils.utils import hash_string, clear_terminal


def main(client):
    while True:
        request_data = json.dumps({
            'payload': {},
            'url': 'show_profile'
        })
        client.send(request_data.encode('utf-8'))
        response = client.recv(5 * 1024).decode('utf-8')
        response = json.loads(response)

        if response['status_code'] == 200:
            user = response['user']
        else:
            print(response['msg'])
            continue


        print(
            f'1.Username: {user["username"]}\n2.Email: {user["email"]}\n3.Phone Number: {user["phone_number"]}\n4.Password: Can\'t be shown due to security reasons\n5.Birth Date: {user["birthday"]}\n6.Quit')

        select_option = input("Which Setting Do You Want To Change ?: ").lower().strip()
        payload = {}
        try:
            if select_option == '6' or select_option == 'quit':
                print("\nExiting program...")
                break

            elif select_option == '1' or select_option == 'username':
                new_username = input("Enter New Username: ")
                Validator.username_validator(new_username)
                payload['username'] = new_username

            elif select_option == '2' or select_option == 'email':
                new_email = input("Enter New Email: ").lower().strip()
                Validator.email_validator(new_email)
                payload['email'] = new_email

            elif select_option == '3' or select_option == 'phone number':
                new_phone_number = input('Enter New Phone Number :')
                Validator.phone_number_validator(new_phone_number)
                payload['phone_number'] = new_phone_number

            elif select_option == '4' or select_option == 'password':
                password = input("Enter Current Password: ")
                new_password = input("Enter New Password: ")
                confirm_new_password = input("Confirm New Password: ")
                if (new_password == confirm_new_password) and (compare_digest(hash_string(password), user['password'])):
                    Validator.password_validator(new_password)
                    payload['password'] = hash_string(new_password)
                else:
                    print("Password could not be updated due to invalid inputs or verification error.")
                    continue
            elif select_option == '5' or select_option == 'birth date':
                birth_date = input("Enter New Birth Date: ")
                Validator.date_format_validator(birth_date)
                payload['birthday'] = birth_date
        except UsernameValidationError:
            clear_terminal()
            print("Invalid username format.")
            continue
        except EmailValidationError:
            clear_terminal()
            print("Invalid email format.")
            continue
        except PhoneNumberValidationError:
            clear_terminal()
            print("Invalid phone number format.")
            continue
        except PasswordValidationError:
            clear_terminal()
            print("Invalid password format.")
            continue
        except DateValidationError:
            clear_terminal()
            print("Invalid Birth Date Format.")
            continue
        except Exception:
            clear_terminal()
            print('Client Error')
            continue

        request_data = json.dumps({
            'payload': payload,
            'url': 'user_modification'
        })
        client.send(request_data.encode('utf-8'))
        response = client.recv(5 * 1024).decode('utf-8')
        response = json.loads(response)

        if response['status_code'] == 200:
            print("User information has been updated successfully!")
            break
        else:
            print(response['msg'])
            continue


if __name__ == '__main__':
    main()
