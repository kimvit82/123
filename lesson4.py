class BankAccount:
    def __init__(self, account_holder, balance=0):
        self.account_holder = account_holder
        self.__balance = balance

    def get_balance(self):
        print("Текущий баланс равен", self.__balance)

    def to_deposit(self, money=0):
        self.__balance = self.__balance + money
        print(f"Баланс {self.account_holder} был успешно пополнен на {money}")

    def withdraw_money(self, money=0):
        self.__balance = self.__balance - money
        print(f"С счета {self.account_holder} списано {money}")

    def transfer_money(self, account, money=0):
        self.__balance = self.__balance - money
        account.to_deposit(money)

    def __calculate_interest(self, percent):
        return self.__balance*(percent/100)

    def add_interest(self, percent):
        self.__balance = self.__balance + self.__calculate_interest(percent)

Ivan_account = BankAccount("Иван Иванов", 500)
Ivan_account.to_deposit(500)
Ivan_account.get_balance()
Ivan_account.withdraw_money(400)
Ivan_account.get_balance()

Sergey = BankAccount("Сергей", 500)
Ivan_account.transfer_money(Sergey, 400)

Ivan_account.get_balance()
Ivan_account.add_interest(60)
Ivan_account.get_balance()