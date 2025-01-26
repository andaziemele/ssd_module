import json
import re
import getpass
import jwt
import logging

logger = logging.getLogger("EShopApp")


def create_jtw(login_activity):
    """
    Creates JSON web token based on login activities to ensure uniqueness.
    :param login_activity: dict containing login name, date and role.
    """
    return jwt.encode(
        login_activity, get_secret_key("jwt_secret_key"), algorithm="HS256"
    )


def validate_email(email_address, debug=False):
    """
    Checks if an email exists in the database when validating registration.
    :param email_address: inputted email address
    :param debug: debugging flag for testing
    """
    if debug is False:
        file = "data/accounts.json"
    else:
        file = "tests/test_data/test_accounts.json"

    with open(file) as f:
        d = json.load(f)
        if not any(account["email"] == email_address for account in d):
            return False
        else:
            return True


def check_password_strength(password, secure):
    """
    Checks if password matches required strength attributes.
    :param password: inputted password
    :param secure: secure flag to bypass strength checks
    """
    pass_length = 8
    upper_pattern = r"[A-Z]"
    lower_pattern = r"[a-z]"
    char_pattern = r"@|!|\$|&|\."
    digit_pattern = r"\d"

    if secure:
        upper_match = re.search(upper_pattern, password)
        lower_match = re.search(lower_pattern, password)
        char_match = re.search(char_pattern, password)
        digit_match = re.search(digit_pattern, password)
        if (
            upper_match
            and lower_match
            and char_match
            and len(password) >= pass_length
            and digit_match
        ):
            return True
        else:
            return False
    else:
        return True


def check_email_pattern(email, secure):
    """
    Checks if email matches an expected pattern.
    Regex source for safe pattern: GeeksForGeeks https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
    Regex source for evil pattern: DZone https://dzone.com/articles/regular-expressions-denial
    :param email: email address string
    :param secure: secure bool
    :return: boolean if pattern valid or not
    """
    if secure:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    else:
        pattern = r"^([0-9a-za-z]([-.\w]*[0-9a-za-z])*@([0-9a-za-z][-\w]*[0-9a-za-z]\.)+[a-za-z]{2,9})$"
    # validates entered e-mail address structure
    if re.fullmatch(pattern, email):
        return True
    else:
        return False


def request_new_password(message, secure):
    """
    Requests new password. Checks if new password created is strong.
    :param message: message sent to user
    :param secure: secure boolean value
    """

    while True:
        password = str(getpass.getpass(message))
        password_check = check_password_strength(password, secure)
        if password_check:
            return password
        else:
            print("Password does not match the requirements. Please try again.")


def create_address_object(line1, line2, postcode):
    """
    Creates an address object to store in the account model.
    :param line1: first line of address
    :param line2: second line of address
    :param postcode: postcode of address
    :return: dict object of address
    """
    address = {"line1": line1, "line2": line2, "postcode": postcode}
    return address


def get_secret_key(key_type, debug=False):
    """
    Fetches secret keys for activities.
    In normal circumstances, these would be stored in a highly secured environment.
    :param debug: debug value for testing
    :param key_type: type of key required (jwt or encryption)
    :return key: returns key for encoding/decoding activities
    """
    if not debug:
        f = open("no_secrets_here/keys.json")
        data = json.load(f)
        key = data[0].get(key_type)
        f.close()
    else:
        f = open("tests/test_data/test_keys.json")
        data = json.load(f)
        key = data[0].get(key_type)
        f.close()
    return key


def get_data(data_type, debug=False):
    """
    Loads accounts from json file.
    :param data_type: type of data required to be loaded
    :param debug: debug flag for testing
    :return dicts: read list of dicts for further data processing
    """
    if data_type == "accounts":
        if debug is False:
            file = "data/accounts.json"
        else:
            file = "tests/test_data/test_accounts.json"
    elif data_type == "inventory":
        if debug is False:
            file = "data/inventory.json"
        else:
            file = "test_inventory.json"
    elif data_type == "orders":
        if debug is False:
            file = "data/orders.json"
        else:
            file = "test_orders.json"
    else:
        raise ValueError("No such data exists.")

    with open(file) as f:
        dicts = json.load(f)
        return dicts


def generate_account_number():
    """
    Generates an account number for a given Account instance.
    Checks for latest account number and adds +1 to increase value.
    :return: new updated account number
    """
    accounts = get_data("accounts")
    new_account_number = max(int(account["account_number"]) for account in accounts) + 1
    return new_account_number


def generate_order_number():
    """
    Generates an order number for a given Order instance.
    Checks for latest order number and adds +1 to increase value.
    :return: new updated order number
    """
    orders = get_data("orders")
    new_order_number = max(int(order["order_id"]) for order in orders) + 1
    return new_order_number


def load_brute_passwords():
    """
    Loads a list of passwords from txt file to demonstrate a brute-force attack.
    """
    password_file = "data/known_weak_passwords.txt"
    with open(password_file, "r") as file:
        passwords_list = file.read().splitlines()
    return passwords_list
