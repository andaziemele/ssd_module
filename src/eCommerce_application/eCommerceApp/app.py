import json
from flask import Flask, jsonify
from threading import Thread
import time
from helper_funcs import get_data
from controllers import EShopController
import logging

logging.basicConfig(filename="app.log", encoding="utf-8", level=logging.DEBUG)
logger = logging.getLogger("EShopApp")


def start_api():
    app = Flask(__name__)
    with app.app_context():

        def get_orders_api():
            try:
                orders = get_data("orders")
                return jsonify(orders)
            except FileNotFoundError:
                return jsonify({"error": "Orders file not found"}), 404
            except json.JSONDecodeError:
                return jsonify({"error": "Invalid JSON format"}), 400

        # Add URL rules
        app.add_url_rule(
            "/api/orders", "get_orders_api", get_orders_api, methods=["GET"]
        )

        def run_flask():
            app.run(port=8000)

        Thread(target=run_flask).start()

        log = logging.getLogger("werkzeug")
        log.setLevel(logging.ERROR)


if __name__ == "__main__":
    # security enabling functionality
    secure = int(
        input(
            "Make application secure? Press [1] for YES, enter any other number to disable security.\n"
        )
    )

    if secure == 1:
        secure = True
    else:
        secure = False
    logger.info(f"Secure capability enabled: {secure}")
    # whilst the app is active
    while True:
        # email = input("Please enter your e-mail: \n")
        eshop_controller = EShopController(secure)
        start_api()
        # give the API time to start up
        time.sleep(1)

        email = input("Please enter your e-mail:\n")

        login_validated = eshop_controller.login(email)
        logger.info(f"Login for {email} validated: {login_validated}")

        while True:
            main_choice = int(
                input(
                    "What would you like to do? View/create/update/delete \n[1] Order(s) \n[2] Account\n"
                )
            )
            if main_choice == 1:
                sub_choice = int(
                    input(
                        "What would you like to do? \n[1] View own order \n[2] View all orders \n[3] Create order \n[4] Delete order\n"
                    )
                )
            elif main_choice == 2:
                sub_choice = int(
                    input(
                        "What would you like to do? \n[1] View own account \n[2] View all accounts \n[3] Delete account \n"
                    )
                )
            else:
                print("Wrong input. Try again.")
                sub_choice = False

            while sub_choice:
                if main_choice == 1:
                    if sub_choice == 1:
                        # view own order - all allowed
                        logger.info(f"Get order functionality requested.")
                        eshop_controller.get_order()
                        break
                    if sub_choice == 2:
                        # view all orders - only clerk and admin allowed
                        logger.info(f"Get all orders functionality requested.")
                        eshop_controller.get_all_orders()
                        break
                    if sub_choice == 3:
                        # create order - all allowed
                        logger.info(f"Create order functionality requested.")
                        eshop_controller.create_order()
                        break
                    if sub_choice == 4:
                        # delete order - only clerk allowed
                        logger.info(f"Delete order functionality requested.")
                        eshop_controller.delete_order()
                        break

                elif main_choice == 2:
                    # get current account - all allowed
                    if sub_choice == 1:
                        logger.info(f"Get account functionality requested.")
                        eshop_controller.get_account()
                        break
                    # get all accounts - only admin allowed
                    if sub_choice == 2:
                        logger.info(f"Get all accounts functionality requested.")
                        eshop_controller.get_all_accounts()
                        break
                    # delete account - only admin allowed
                    if sub_choice == 3:
                        logger.info(f"Delete account functionality requested.")
                        eshop_controller.delete_account()
                        break
                    else:
                        print("Wrong input. Try again.")
