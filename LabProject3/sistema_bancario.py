from abc import ABC, abstractmethod

class Account:
    def __init__(self, client, account_num):
        self._client = client
        self._account_num = account_num
        self._balance = 0
        self._agency = '0001'
        self._bank_statement = BankStatement()

    @classmethod
    def new_account(cls, client, account_num):
        return cls(client, account_num)
    
    @property
    def client(self):
        return self._client
    
    @property
    def account_num(self) -> int:
        return self._account_num
    
    @property
    def balance(self):
        return self._balance
    
    @property
    def agency(self):
        return self._agency
    
    @property
    def bank_statement(self):
        return self._bank_statement
    
    def deposit(self, value):
        self._balance += value
        self._bank_statement.add_statement(value)
        print(f'''---\nNovo saldo: R$ {self._balance:.2f}\n---\n''')
        return True
    
    def withdraw(self, value):
        if self._balance - value < 0:
            print('\nSaldo Insuficiente!')
            return False
        else:
            self._balance -= value
            self._bank_statement.add_statement(value * -1)
            print(f'''\n---\nNovo saldo: R$ {self._balance:.2f}\n---\n''')
            return True
      
class CheckingAccount(Account):
    def __init__(self, client, account_num):
        super().__init__(client, account_num)
        self._limit = 500
        self._withdraws_number = 0
        self._withdraws_number_limit = 3
        
    def deposit(self, value):
        super().deposit(value)

    def withdraw(self, value):
        if self._withdraws_number == self._withdraws_number_limit:
            print('\nNúmero limite de saques diários atingido')
            return False
        else:
            if value <= self._limit:
                super().withdraw(value)
                self._withdraws_number += 1
                return True
            else:
                print(f'\nQuantidade a ser sacada é maior que o limite permitido ({self._limit})')
                return False

class Client:
    def __init__(self, address):
        self._address = address
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)
    
    def transaction(self, account, transaction):
        transaction.add_transaction(account)
    
class Individual(Client):
    def __init__(self, address, cpf, name, birth_date):
        super().__init__(address)
        self.cpf = cpf
        self.name = name
        self.birth_date = birth_date
        
        
class BankStatement:
    def __init__(self):
        self._statements = []
    
    def add_statement(self, statement):
        self._statements.append(statement)

    @property
    def statements(self):
        return self._statements

class Transaction(ABC):
    @property 
    @abstractmethod
    def value(self):
        pass
    
    @classmethod
    @abstractmethod
    def add_transaction(self, account):
        pass
    
class Deposit(Transaction):
    def __init__(self, value):
        self._value = value
    
    @property
    def value(self):
        return self._value
    
    def add_transaction(self, account):
        account.deposit(self._value)
        
class Withdraw(Transaction):
    def __init__(self, value):
        self._value = value
    
    @property
    def value(self):
        return self._value
    
    def add_transaction(self, account):
        account.withdraw(self._value)
    
    
    
def deposit(users):
    cpf = input('Em qual CPF deseja depositar? ')
    client = filter_users(cpf, users)
    if not client:
        print(f'\nUsuário de CPF: {cpf} não existe')
        return None
    else:
        print('\nQuanto deseja depositar?')
        deposit_value = float(input('Valor: '))
        deposit = Deposit(deposit_value)
        account = client.accounts[0]
        client.transaction(account, deposit)

def withdraw(users):    
    cpf = input('De qual CPF deseja sacar? ')
    client = filter_users(cpf, users)
    if not client:
        print(f'\nUsuário de CPF: {cpf} não existe')
        return None
    else:
        print(f'\nQuanto deseja sacar?')
        withdraw_value = float(input('Valor: '))
        withdraw = Withdraw(withdraw_value)
        account = client.accounts[0]
        client.transaction(account, withdraw)

        
def statement(users):
    cpf = input('De qual CPF deseja visualizar o extrato? ')
    client = filter_users(cpf, users)
    if not client:
        print(f'\nUsuário de CPF: {cpf} não existe')
        return None
    else:
        bank_statement = client.accounts[0].bank_statement.statements
        balance = client.accounts[0].balance
        if len(bank_statement) == 0:
            print('\nNão foram realizadas movimentações.')
        else:
            print('\n--- Extrato ---')
            for statement in bank_statement:
                print(f'R$ {statement:.2F} \n')
            print(f'Saldo: R$ {balance:.2F}')
            print('---------------')
        
def create_user(users):
    username = input('\nInforme o nome completo do usuario: ')
    cpf = input('\nInforme o CPF do usuario (Apenas numeros): ')
    user = filter_users(cpf, users)
    if not user:
        birth_date = input('\nInforme a data de nascimento do usuario (DD-MM-AA): ')
        address = input('\nInforme o endereço do usuario (Logradouro, número - bairro - cidade/estado) : ')
        
        new_user = Individual(address, cpf, username, birth_date)
        users.append(new_user)
        print(f'\nUsuário {username} criado com sucesso!')
    else:
        print(f'\nUsuário já existente!')

def create_account(accounts, users):
    cpf = input('\nInforme o CPF do usuario (Apenas numeros): ')
    user = filter_users(cpf, users)
    if user:
        account_number = len(accounts) + 1
        new_account = CheckingAccount(user, account_number)
        accounts.append(new_account)
        user.accounts.append(new_account)
        print(f'\nConta de número {account_number} criada com sucesso!')
    else:
        print(f'\nUsuário de CPF: {cpf} não existe')
    
def filter_users(cpf, users):
    filtered_users = [user if user.cpf == cpf else None for user in users]
    return filtered_users[0] if filtered_users else None

def main():
    users = []
    accounts = []

    while True:
        print(
        '''
        Escolha uma das opções abaixo: 

        1: Depositar
        2: Sacar
        3: Extrato
        4: Criar Usuário
        5: Criar Conta Corrente
        6: Sair
        '''
        )
        option = input('Opção: ')
        
        if option == '1':
            deposit(users)
            
        elif option == '2':
            withdraw(users)

        elif option == '3':
            statement(users)
            
        elif option == '4':
            create_user(users)
            
        elif option == '5':
            create_account(accounts, users)
            
        elif option == '6':
            break
        
        else:
            print('\nSelecione uma das opções.')
            
main()