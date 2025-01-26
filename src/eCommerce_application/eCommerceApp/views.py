class EShopView:
    """
    View methods for EShop capabilities.
    """

    @staticmethod
    def list_inventory_items(items):
        print("Found items in inventory, printing details \n..........")
        for item in items:
            print(item)

    @staticmethod
    def list_all_orders(orders):
        print("Found orders, printing details \n..........")
        for order in orders:
            print(order)

    @staticmethod
    def list_order(order):
        print("Viewing order, printing details \n..........")
        print(order)

    @staticmethod
    def list_account_details(account):
        print("Found account, printing details \n..........")
        print(account)

    @staticmethod
    def list_accounts(accounts):
        print("Found accounts, printing details \n..........")
        for account in accounts:
            print(account)
