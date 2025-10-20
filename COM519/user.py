
class User:
    """ 
    user class to hold all common data values. To be extended by child classes (Customer/Staff)
    """
    def __init__(
            self, account_cre_date: str, name: str, address: str, post_code: str,
            email: str, phone_no: int|None, user_name: str, password: str, access_code: str          
            ):
        self.account_cre_date = account_cre_date
        self.name = name
        self.address = address
        self.post_code = post_code
        self.email = email
        self.phone_no = phone_no
        self.user_name = user_name
        self.password = password
        self.access_code = access_code
        self.account_cre_date = account_cre_date

    def login_check():
        pass


class Customer(User):
    """ 
    extension to the user class to hold all customer specific data values
    """
    def __init__(
            self, account_cre_date: str, name: str, address: str, post_code: str,
            email: str, phone_no: int|None, user_name: str, password: str, access_code: str,
            customer_id: str, membership_id: str|None
            ):
        super().__init__(account_cre_date, name, address, post_code, email, phone_no, user_name, password, access_code)
        self.customer_id = customer_id
        self.membership_id = membership_id

    def update_account_details():
        pass


class Staff(User):
    """ 
    extension to the user class to hold all staff specific data values
    """
    def __init__(
            self, account_cre_date: str, name: str, address: str, post_code: str,
            email: str, phone_no: int|None, user_name: str, password: str, access_code: str,
            staff_id: str, staff_type: str, mechanic_id: str|None, primary_garage: str        
            ):
        super().__init__(account_cre_date, name, address, post_code, email, phone_no, user_name, password, access_code)
        self.staff_id = staff_id
        self.membership_id = staff_id
        self.staff_type = staff_type
        self.mechanic_id = mechanic_id
        self.primary_garage = primary_garage

    def update_account_details():
        pass

    def update_customer_account_details():
        pass