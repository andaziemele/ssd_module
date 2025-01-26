from models import EShopModel
from views import EShopView
from functools import wraps
from helper_funcs import get_data
import requests
import logging

logger = logging.getLogger("EShopApp")


class EShopController:
    """
    Controller to implement EShop capabilities and manage interactions between Model(s) and View.
    """
    def __init__(self, secure):
        self.model = EShopModel()
        self.view = EShopView()
        self.secure = secure

    def login(self, email):
        """
        Login feature implemented for controller. Sets email address using the necessary validations.
        :param email: user-inputted email address
        """
        self.model.account.secure = self.secure
        self.model.account.email = email
        while True:
            login_validated = self.model.login(self.secure)
            if login_validated:
                logger.info(f"Successful login with {email}")
                break

    def role_required(roles):
        """
        Custom Python decorator to implement Role-based Access Control.
        Decorates certain functions and fetches loaded account role.
        Source: https://medium.com/@subhamx/role-based-access-control-in-django-the-right-features-to-the-right-users-9e93feb8a3b1
        :return:
        """
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.model.account.role in roles:
                    return func(self, *args, **kwargs)
                else:
                    print("You're not allowed to do this!")
                    logger.error(f"Unauthorised access to {func}")

            return wrapper

        return decorator

    def create_order(self):
        """
        Enables user to search for items to add to order and creates an order based on user inputs of item IDs.
        """
        while True:
            search_keyword = str(
                input("Enter the search keyword of items you'd like to add to order.\n")
            )
            results = self.model.search_inventory(search_keyword)
            if results:
                self.view.list_inventory_items(results)
            else:
                print("Nothing found for your search term.")
            while results:
                item_id = str(input("Enter item ID of item to add to cart."))
                quantity = int(input("Enter quantity of items required."))
                self.model.add_to_order(item_id, quantity)
                current_order = self.model.get_current_order()
                self.view.list_order(current_order)
                more = int(input("Any more to add? [1] YES [2] NO"))
                if more == 1:
                    pass
                else:
                    break
            break

    def get_order(self):
        """
        Search for orders associated to current account and list them.
        """
        order = self.model.search_orders()
        self.view.list_order(order)

    @role_required(["admin", "clerk"])
    def get_all_orders(self):
        """
        Gets all orders via an API request. Only admin and clerk are allowed to do this.
        """
        response = requests.get("http://localhost:8000/api/orders", timeout=10)
        if response.status_code == 200:
            self.view.list_all_orders(response)
            return response.json()
        return None

    @role_required(["clerk"])
    def delete_order(self):
        """
        Deletes an order. Only clerk is allowed to do this.
        :return:
        """
        orders = get_data("orders")
        self.view.list_all_orders(orders)
        order_id = str(input("Enter order ID of order for deletion."))
        for i, d in enumerate(orders):
            if d.get("order_id") == order_id:
                # pop order from list based on index
                orders.pop(i)
                break
        logger.info(f"Order with the ID {order_id} is deleted.")
        self.get_all_orders()

    def get_account(self):
        """
        Get current account details. No user permissions.
        """
        account = self.model.account
        self.view.list_account_details(account)

    @role_required(["admin", "clerk"])
    def get_all_accounts(self):
        """
        View all accounts. Only admins and clerks are allowed this.
        """
        accounts = get_data("accounts")
        self.view.list_accounts(accounts)

    @role_required(["admin"])
    def delete_account(self):
        """
        Delete an account. Only admins are allowed this.
        """
        accounts = get_data("accounts")
        account_id = str(input("Enter account ID of order for deletion."))
        for i, d in enumerate(accounts):
            if d.get("account_id") == account_id:
                # pop account from list based on index
                accounts.pop(i)
                break
        logger.info(f"Account with the ID {account_id} is deleted.")
        self.get_all_accounts()
