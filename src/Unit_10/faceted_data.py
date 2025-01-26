# Example script to demonstrate how data behaves differently based on who
# is viewing it, and how data gets partly concealed.

class DataViewer:
    """
    Class for storing data viewer attributes, including role upon which the viewer changes.
    """

    def __init__(self, role):
        self.role = role
        self.data = {
            'sales': [100.25, 200.99],
            'customer': ['Anna Smith', 'John Montgomery'],
            'email': ['annasmith@gmail.com', 'jmnt1995@yahoo.com'],
            'payment_card': ['3875-4030-9821-1051', '2901-4023-4092-0701']
        }

    def view_data(self):
        """
        Returns a view of data based on role attribute.
        :return data: a view of data based on user role.
        """
        if self.role == 'admin':
            return {
                'sales': self.data['sales'],
                'customer': self.data['customer'],
                'email': self.data['email'],
                'payment_card': self.data['payment_card']
            }
        elif self.role == 'clerk':
            return {
                'sales': self.data['sales'],
                'customer': self.data['customer'],
                'email': self.data['email'],
                'payment_card': self._partial_mask("payment_card", self.data['payment_card'])
            }
        elif self.role == 'user':
            return {
                'sales': sum(self.data['sales']),
                'customer': self._partial_mask("customer", self.data['customer']),
                'email': self._partial_mask("email", self.data['email']),
                'payment_card': self._partial_mask("payment_card", self.data['payment_card'])
            }
        else:
            return {'message': 'Unauthorised.'}

    def _partial_mask(self, field, value):
        """
        Mask for concealing certain types of info
        :param field: name of info field
        :param value: data to be concealed
        :return: concealed data
        """
        if field == 'email':
            return 'xxxxx' + str(value)[-4:]
        if field == 'customer':
            return 'xxxxx' + str(value)[-1:]
        elif field == 'payment_card':
            return '****-****-****-' + str(value)[-4:]
        return value


if __name__ == "__main__":
    admin = DataViewer('admin')
    clerk = DataViewer('clerk')
    user = DataViewer('user')
    guest = DataViewer('guest')

    print("Admin view:", admin.view_data())
    print("Clerk view:", clerk.view_data())
    print("User view:", user.view_data())
    print("Guest view:", guest.view_data())
