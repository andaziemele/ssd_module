import bcrypt
from cryptography.fernet import Fernet
from helper_funcs import (
    get_secret_key,
    generate_account_number,
    get_data,
    generate_order_number,
    check_email_pattern,
    create_address_object,
    create_jtw,
    request_new_password,
    load_brute_passwords,
)
import datetime
import logging
import json
import getpass

logger = logging.getLogger("EShopApp")

cipher_suite = Fernet(get_secret_key("data_encryption_key").encode("utf-8"))


class Item:
    def __init__(self):
        self.item_id = ""
        self.brand = ""
        self.name = ""
        self.price = ""
        self.quantity = ""
        self.category_id = ""


class InventoryModel:
    """
    Class to manage inventory functionalities.
    """

    def __init__(self):
        """
        Holds loaded inventory list.
        """
        self.inventory = None

    def load_inventory(self):
        """
        Loads data for the inventory.
        """
        self.inventory = get_data("inventory")

    def search_inventory(self, search_keyword):
        """
        Very simple sequential search algorithm for the purposes of demonstrating functionality.
        Ensures casing is the same for
        :param search_keyword: keyword to search by
        :return: found items in the inventory
        """
        return [
            item
            for item in self.inventory
            if search_keyword.lower() in item.get("name", "").lower()
        ]


class OrderModel:
    """
    Order class to store and update order attributes.
    """
    def __init__(self):
        self.account_number = ""
        self.order_id = ""
        self.date = ""
        self.status = ""
        self.total = ""
        self.order_items = []

    def create_order(self, account_number, order_id, date, status, total):
        """
        Creates and assigns attributes to Order object as user creates an order.
        :param account_number:
        :param order_id:
        :param date:
        :param status:
        :param total:
        :return:
        """
        self.account_number = account_number
        self.order_id = order_id
        self.date = date
        self.status = status
        self.total = total

    def add_product_to_order(self, item_id, quantity):
        """
        Appends an item to an order based on its ID value.
        :param item_id: item id value of item
        :param quantity: number of items required
        """
        self.order_items.append({"item_id": item_id, "quantity": quantity})

    def update_order_status(self, order_status):
        """
        Updates Order status attribute where necessary.
        :param order_status: updated status
        """
        self.status = order_status


class AccountModel:
    """
    Class to manage account functionalities.
    """

    def __init__(self):
        """
        Initialises empty Account object.
        """
        self.email_address = ""
        self.account_number = ""
        self.secure_password = ""
        self.insecure_password = ""
        self.name = ""
        self.surname = ""
        self.address = ""
        self.phone = ""
        self.role = "user"
        self.jwt = ""
        self.secure = True

    @property
    def email(self):
        """
        Enables setter to be used for updating the email attribute.
        """
        return self.email_address

    @email.setter
    def email(self, value, debug=False):
        """
        Checks if an email exists in the database when validating registration and sets the updated attribute.
        Additionally, checks if matches valid regex pattern.
        Source: https://www.pythontutorial.net/tkinter/tkinter-mvc/
        :param value: e-mail address value
        :param debug: bool True enables unit testing of the method
        """

        # validates entered e-mail address structure, and also assesses if system secure/insecure for ReDoS attack
        if check_email_pattern(value, secure=self.secure):
            # opens account json files and checks if email exists already
            accounts = get_data("accounts", debug)
            if any(account["email_address"] == value for account in accounts):
                logger.error(f"E-mail already registered: {value}")
                self.email_address = value
            else:
                # assigns e-mail to the new account model
                logger.error(f'Account with e-mail "{value}" requires registration.')
                self.email_address = value
        else:
            raise ValueError(f"Invalid email address: {value}")

    def load_account_details(self, secure, email):
        """
        Loads account details stored in the JSON file.
        :param secure: bool to enable insecure demonstration of how a password is stored
        :param email: account is loaded based on inputted email address
        :return: bool if account loaded
        """
        accounts = get_data("accounts")
        account = [d for d in accounts if d.get("email_address") == email]
        if account:
            self.name = account[0].get("name")
            self.surname = account[0].get("surname")
            self.account_number = account[0].get("account_number")
            # demonstrating security functionality for securely/insecurely storing passwords
            if secure:
                self.secure_password = account[0].get("secure_password")
            else:
                self.insecure_password = account[0].get("insecure_password")
            self.phone = account[0].get("phone")
            self.address = account[0].get("address")
            if secure:
                self.role = account[0].get("role")
            else:
                # if insecure, assign admin role by default
                self.role = "admin"
            return True
        else:
            return False

    def save_account(self):
        """
        Fetches attribute information from newly updated Account class object,
        transforms into a dict and saves to JSON file.
        """
        accounts = get_data("accounts")
        account = self.__dict__
        accounts.append(account)
        with open("data/accounts.json", mode="w") as f:
            f.write(json.dumps(accounts, indent=2))
        logger.info(f"Account saved.")

    def register_account(self, secure):
        """
        Captures required inputs as part of registration and saves the account as JSON.
        Secure and insecure saving of details enabled.
        """
        self.request_password(secure, existing_account=False)
        if secure:
            self.name = cipher_suite.encrypt(
                input("Please enter your name. \n").encode("utf-8")
            ).decode("utf-8")
            self.surname = cipher_suite.encrypt(
                input("Please enter your surname. \n").encode("utf-8")
            ).decode("utf-8")
            line1 = cipher_suite.encrypt(
                input("Please enter the first line of your address. \n").encode("utf-8")
            ).decode("utf-8")
            line2 = cipher_suite.encrypt(
                input("Please enter the second line of your address. \n").encode(
                    "utf-8"
                )
            ).decode("utf-8")
            postcode = cipher_suite.encrypt(
                input("Please enter your postcode. \n").encode("utf-8")
            ).decode("utf-8")
            self.address = create_address_object(line1, line2, postcode)
            self.phone = cipher_suite.encrypt(
                input("Please enter your phone number. \n").encode("utf-8")
            ).decode("utf-8")
        else:
            self.name = input("Please enter your name. \n")
            self.surname = input("Please enter your surname. \n")
            line1 = input("Please enter the first line of your address. \n")
            line2 = input("Please enter the second line of your address. \n")
            postcode = input("Please enter your postcode. \n")
            self.address = create_address_object(line1, line2, postcode)
            self.phone = input("Please enter your phone number. \n")
        self.account_number = generate_account_number()

        # save account
        self.save_account()
        logger.info(f"Account registered.")

    def request_password(self, secure, existing_account=True, brute_password=None):
        """
        Requests password to user in a secure and insecure way, and adjusts functionality based on
        whether the account is a new or an existing account. This includes checking the password against
        existing database, and where a password is newly created (existing_account=False), makes sure it's strong.
        Additionally, enables brute force password demonstration attack.
        :param brute_password: pre-inputted password from a text file of known insecure passwords.
        :param existing_account: bool if account already exists/does not exist.
        :param secure: secure functionality bool.
        :return:
        """
        if secure:
            if existing_account:
                # if account already exists
                message = "Enter your password: \n"
                pass_phrase = str(getpass.getpass(message))
                validated = bcrypt.checkpw(
                    pass_phrase.encode("utf-8"), self.secure_password.encode("utf-8")
                )

            else:
                # new registration
                logger.info(f"Registration required.")
                message = "Enter your password: \nIt must \n* Be at least 8 characters \n* Contain at least one uppercase and one lowercase character \n *Contain at least one numeric character \n*Contain at least one of these characters @!$&.\n"
                pass_phrase = request_new_password(message, secure)
                self.secure_password = bcrypt.hashpw(
                    pass_phrase.encode("utf-8"), bcrypt.gensalt()
                ).decode("utf-8")
                validated = False
        else:  # all insecure paths
            if brute_password:
                # brute entry with pre-listed passwords
                pass_phrase = brute_password
            else:
                message = "Enter your password: \n"
                pass_phrase = input(message)
            if existing_account:
                # check against database
                return self.insecure_password == pass_phrase
            else:
                self.insecure_password = pass_phrase
                validated = False

        return validated


class EShopModel:
    """
    Initialise EShop Model, which initialises the child models InventoryMode, OrderModel and AccountModel.
    """
    def __init__(self):
        self.inventory = InventoryModel()
        self.order = OrderModel()
        self.account = AccountModel()

    def login(self, secure):
        """
        Enables secure/insecure logging in feature, including login limits and brute-force entry.
        :param secure: bool if secure or not secure
        :return: returns bool true if login successful
        """
        self.account.secure = secure
        email = self.account.email
        account_status = self.account.load_account_details(secure, email)
        logger.info(f"Account with email {email} found: {account_status}")
        logins = 0
        if secure:
            login_limit = 4
            brute_force = False
        else:
            # insecure - increase login limit to 1000
            login_limit = 1000
            brute_force = int(
                input(
                    "Would you like to use a brute-force attack to enter the account? \n[1] YES \n[2] NO\n"
                )
            )

        if brute_force == 1:  # if user would like to enter via brute-force
            logger.warning(f"Brute entry executed by {email}")
            passwords = load_brute_passwords()
            for password in passwords:
                print(f"Trying weak password: {password}")
                passed = self.account.request_password(
                    secure, existing_account=account_status, brute_password=password
                )
                if account_status:
                    if passed:
                        logger.info("Login successful.")
                        login_info = {
                            "user_email": email,
                            "role": self.account.role,
                            "time": str(datetime.datetime.now()),
                        }
                        self.account.jwt = create_jtw(login_info)
                        print(
                            "Save this important token for future logins:",
                            self.account.jwt,
                        )
                        return True
                    else:
                        while logins < login_limit - 1:
                            logins += 1
                            logger.error(
                                f"Password incorrect, try again. Attempts remaining: {login_limit - logins}"
                            )
                            passed = self.account.request_password(
                                secure,
                                existing_account=account_status,
                                brute_password=password,
                            )
                            if passed:
                                login_info = {
                                    "user_email": email,
                                    "role": self.account.role,
                                    "time": str(datetime.datetime.now()),
                                }
                                self.account.jwt = create_jtw(login_info)
                                print(
                                    "Save this important token for future logins:",
                                    self.account.jwt,
                                )
                                return True
                            break
        else:
            passed = self.account.request_password(
                secure, existing_account=account_status
            )

        if account_status:
            if passed:
                logger.info("Login successful.")
                login_info = {
                    "user_email": email,
                    "role": self.account.role,
                    "time": str(datetime.datetime.now()),
                }
                self.account.jwt = create_jtw(login_info)
                print("Save this important token for future logins:", self.account.jwt)
                return True
            else:
                while logins < login_limit - 1:
                    logins += 1
                    logger.error(
                        f"Password incorrect, try again. Attempts remaining: {login_limit - logins}"
                    )
                    passed = self.account.request_password(secure)
                    if passed:
                        login_info = {
                            "user_email": email,
                            "role": self.account.role,
                            "time": str(datetime.datetime.now()),
                        }
                        self.account.jwt = create_jtw(login_info)
                        print(
                            "Save this important token for future logins:",
                            self.account.jwt,
                        )
                        return True
        elif not account_status:
            self.account.register_account(secure)
            return False

    def search_inventory(self, search_keyword):
        """
        Loads and searches inventory for order updating.
        :return results: found inventory items.
        """
        self.inventory.load_inventory()
        logger.info(f"Inventory loaded.")
        results = self.inventory.search_inventory(search_keyword)

        return results

    def search_orders(self):
        """
        Search orders based on the logged-in account's account number.
        :return: list of found orders.
        """
        orders = get_data("orders")
        return [
            d for d in orders if d.get("account_number") == self.account.account_number
        ]

    def add_to_order(self, item_id, quantity):
        """
        Creates new order and allows input of item ids to add order items.
        :param item_id:
        :param quantity:
        """
        order_id = generate_order_number()
        date = datetime.datetime.now()
        status = "created"
        total = "0.00"
        self.order.create_order(
            self.account.account_number, order_id, date, status, total
        )
        self.order.add_product_to_order(item_id, quantity)
        logger.info(f"Products added to order.")

    def get_current_order(self):
        """
        Gets and returns current order in progress.
        :return current_order: returns the newly created order.
        """
        current_order = self.order.__dict__
        return current_order
