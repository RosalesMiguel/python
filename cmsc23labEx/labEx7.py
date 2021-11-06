from abc import ABC, abstractmethod


def actionUnsuccesfull() -> str:
    return 'Action not completed\nReason:'


class BankAccount(ABC):
    @abstractmethod
    def __init__(self, balance: int, owner: str):
        self.balance = int(balance)
        self.owner = str(owner)
        self.status = True

    def withdraw(self, amount: int):
        if self.status == True:
            amount = int(amount)
            if amount <= self.balance:
                self.balance -= amount
                return True
            elif amount < 0:
                print(actionUnsuccesfull(), 'Invalid value')
                return False
            else:
                print(actionUnsuccesfull(),
                      'Account balance is insufficient to withdraw', amount, 'Php')
                return False
        else:
            print("Account is inactive")
            return False

    def activate(self):
        if self.status == True:
            print("Account is already active.")
        else:
            self.status = not self.status

    def deactivate(self):
        if self.status == False:
            print("Account is already inactive.")
        else:
            self.status = not self.status

    def balanceReport(self):
        print('Account balance:', self.balance, 'Php')

    def accountInfo(self):
        if self.status == True:
            status = 'Active'
        else:
            status = 'Inactive'
        print(
            f'Owner: {self.owner}\nAccount type: {type(self).__name__}\nStatus: {status}')

    def appylChanges(self):
        pass


class Payroll(BankAccount):
    def __init__(self, balance: int, owner: str):
        super().__init__(balance, owner)


class Debit(BankAccount):
    def __init__(self, balance: int, owner: str):
        super().__init__(balance, owner)

    def fundTransfer(self, amount: int, account: BankAccount):
        if self.status and account.status == True:
            amount = int(amount)
            if amount < 0:
                print(actionUnsuccesfull(), 'Invalid value')
                return False
            elif amount > self.balance:
                print(actionUnsuccesfull(),
                      'Account balance is insuffiecient to transfer', amount, 'Php')
                return False
            else:

                if str(type(account).__name__) == 'Debit':
                    if self.withdraw(amount) == True:
                        account.deposit(amount)
                        return True
                elif str(type(account).__name__) == 'Credit':
                    if account.remaining <= 0:
                        print(actionUnsuccesfull, 'Invalid value')
                        return False
                    elif amount > account.balance:
                        print(actionUnsuccesfull,
                              "Amount is greater than the account's credit balance")
                        return False
                    else:
                        if self.withdraw(amount) == True:
                            account.deposit(amount)
                            return True
                        else:
                            return False
                elif str(type(account).__name__) == 'Payroll':
                    if self.withdraw(amount) == True:
                        account.balance += amount
                        return True
                    else:
                        return False
        else:
            print("Account is inactive")
            return False

    def deposit(self, amount: int):
        if self.status == True:
            amount = int(amount)
            if amount < 0:
                print(actionUnsuccesfull(), 'Invalid value')
                return False
            else:
                self.balance += amount
                return True
        else:
            print("Account is inactive")
            return False

    def appylChanges(self):
        if self.status == True:
            interestRate = 0.02
            if self.balance < 100:
                self.status = False
            else:
                self.balance = int(self.balance * (1 + interestRate))


class Credit(BankAccount):
    def __init__(self, balance: int, owner: str):
        super().__init__(balance, owner)
        self.creditLimit = 200000
        self.remaining = self.creditLimit - self.balance

    def withdraw(self, amount: int):
        if self.status == True:
            amount = int(amount)
            if self.balance >= self.creditLimit:
                print(actionUnsuccesfull(),
                      'Account balance is at its credit limit')
                return False
            elif amount < 0:
                print(actionUnsuccesfull(), 'Invalid Value')
                return False
            elif amount <= self.remaining:
                self.balance += amount
                return True
            elif amount > self.remaining:
                print(actionUnsuccesfull(), 'Withdrawing',
                      amount, 'Php will exceed credit limit')
                return False
        else:
            print("Account is inactive")
            return False

    def deposit(self, amount: int):
        if self.status == True:
            amount = int(amount)
            if amount < 0:
                print(actionUnsuccesfull(), 'Invalid value')
                return False
            elif amount > self.balance:
                print(actionUnsuccesfull,
                      'Amount is greater than the credit balance')
                return False
            else:
                self.balance -= amount
                return True
        else:
            print("Account is inactive")
            return False

    def fundTransfer(self, amount: int, account: BankAccount):
        if self.status and account.status == True:
            amount = int(amount)
            if amount < 0:
                print(actionUnsuccesfull(), 'Invalid value')
                return False
            elif amount > self.remaining:
                print(actionUnsuccesfull(),
                      'Account balance will exceed the credit limit', amount, 'Php')
                return False
            else:

                if str(type(account).__name__) == 'Debit':
                    self.withdraw(amount)
                    account.deposit(amount)
                    return True
                elif str(type(account).__name__) == 'Credit':
                    if account.remaining <= 0:
                        print(actionUnsuccesfull, 'Invalid value')
                        return False
                    elif amount > account.balance:
                        print(actionUnsuccesfull,
                              "Amount is greater than the account's credit balance")
                        return False
                    else:
                        if self.withdraw(amount) == True:
                            account.deposit(amount)
                            return True
                        else:
                            return False
                elif str(type(account).__name__) == 'Payroll':
                    if self.withdraw(amount) == True:
                        account.balance += amount
                        return True
                    else:
                        return False
        else:
            print("Account is inactive")
            return False

    def appylChanges(self):
        if self.status == True:
            interestRate = 0.02
            if self.balance >= self.creditLimit:
                self.status = False
            else:
                self.balance = int(self.balance * (1 + interestRate))
                if self.balance >= self.creditLimit:
                    self.status = False
