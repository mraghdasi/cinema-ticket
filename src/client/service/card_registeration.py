import sys
from src.utils.custom_validators import Validator
import sys


def get_input(prompt, validation_func):
    while True:
        user_input = input(prompt)
        if validation_func(user_input):
            return user_input
        print("Invalid input. Please try again.")

def validate_card_number(card_number):
    return Validator.validate(card_number, (Validator.len_validator, 16, Validator.value_validator, 0))

def validate_cvv2(cvv2):
    return Validator.validate(cvv2, (Validator.len_validator, 3, Validator.value_validator, 0))

def validate_year(year):
    return year.isdigit() and 0 <= int(year) <= 99

def validate_month(month):
    return month in {'01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'}


def main(user_info):
    card_list = []
    # outgoing : creat the card in db



       # card registration stuff

    # card registration stuff


    # returns user info

    # ========================= Please Check The Code ======================
    # ✔    for quiting the program in this file use KeyboardInterruptError

    # ✔     use the validations from custom_validations.py

    # ✔    if we type card number correct but write for example cvv2 wrong the program should not take card num from us again
    # (check registration.py for my approach)


    # ✔   the program should close if everything runs correct



    print('fill the fields')
    card_number = get_input("Enter card number (16 digits): ", validate_card_number)

    cvv2 = get_input("Enter CVV2 code (3-4 digits): ", validate_cvv2)

    year = get_input("Enter card expiration year (2 digits, e.g. 22): ", validate_year)

    month = get_input("Enter card expiration month (2 digits, e.g. 01): ", validate_month)

    card_info = (card_number, cvv2, year, month)

    if card_info in card_list:
        print("The card {} has already been registered.".format(card_number))
        raise KeyboardInterrupt

    card_list.append(card_info)
    print("The card {} has been successfully registered.".format(card_number))
    print("The card information: {}".format(card_info))
    print("List of registered cards: {}".format(card_list))


if __name__ == '__main__':
    try:
        main(user_info=0)
    except KeyboardInterrupt:
        print('Exiting the program...')
        sys.exit(0)

    # the program should close if everything runs correct

    while True:
        print('fill the fields')
        card_number = input("Enter card number (16 digits): ")
        if card_number == 'q':
            print('Exiting the program...')
            break
        elif len(card_number) != 16:
            print("Invalid card number. Please try again.")
            continue
        cvv2 = input("Enter CVV2 code (3-4 digits): ")
        if cvv2 == 'q':
            print('Exiting the program...')
            break
        elif len(cvv2) not in {3, 4}:
            print("Invalid CVV2 code. Please try again.")
            continue
        year = input("Enter card expiration year (e.g. 2022): ")
        if year == 'q':
            print('Exiting the program...')
            break
        month = input("Enter card expiration month (2 digits, e.g. 01): ")
        if month == 'q':
            print('Exiting the program...')
            break
        elif month not in {'01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'}:
            print("Invalid month. Please try again.")
            continue
        card_info = (card_number, cvv2, year, month)
        card_list.append(card_info)
        print(f"The card {card_number} has been successfully registered.")
        print(f"The card information: {card_info}")
        print(f"List of registered cards: {card_list}")


if __name__ == '__main__':
    main(user_info=0)

