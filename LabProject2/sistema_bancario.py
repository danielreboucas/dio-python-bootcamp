def deposit(value, balance, bank_statement, /):
    balance += value
    bank_statement.append(value)
    print(f'''---\nNovo saldo: R$ {balance:.2f}\n---\n''')
    return balance
    
def withdraw(*, withdraw_value, balance, withdraws_number, limit, bank_statement):    
    if withdraws_number == 3:
        print('\nNúmero limite de saques diários atingido')
    else:
        if withdraw_value <= 500:
            if balance - withdraw_value < 0:
                print(f'\nNão é possível sacar o valor de {withdraw_value} pois é maior que o saldo da conta')
            else:
                balance -= withdraw_value
                bank_statement.append(withdraw_value * -1)
                withdraws_number += 1
                print(f'''\n---\nNovo saldo: R$ {balance:.2f}\n---\n''')
                return balance, withdraws_number
        else:
            print(f'\nQuantidade a ser sacada é maior que o limite permitido ({limit})')
        
def statement(balance, /, *, bank_statement):
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
        users.append({
            "username": username,
            "cpf": cpf,
            "birth_date": birth_date,
            "address": address
        })
        print(f'\nUsuário {username} criado com sucesso!')
    else:
        print(f'Usuário já existente!')

def create_account(accounts, agency, users):
    cpf = input('\nInforme o CPF do usuario (Apenas numeros): ')
    user = filter_users(cpf, users)
    if user:
        account_number = len(accounts) + 1
        accounts.append({
            "agency": agency,
            "account_number": account_number,
            "user": user
        })
        print(f'\Conta de número {account_number} criada com sucesso!')
    else:
        print(f'Usuário de CPF {cpf} não existe')
    
def filter_users(cpf, users):
    filtered_users = [user if user['cpf'] == cpf else None for user in users]
    return filtered_users[0] if filtered_users else None

def main():
    AGENCY = '0001'
    LIMIT = 500
    
    balance = 0
    withdraws_number = 0
    bank_statement = []
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
            print('\nQuanto deseja depositar?')
            deposit_value = float(input('Valor: '))
            balance = deposit(deposit_value, balance, bank_statement)
            
        elif option == '2':
            print(f'\nQuanto deseja sacar? (Limite: {LIMIT})')
            withdraw_value = float(input('Valor: '))
            balance, withdraws_number = withdraw(
                withdraw_value=withdraw_value,
                balance=balance,
                withdraws_number=withdraws_number,
                limit=LIMIT,
                bank_statement=bank_statement
            )

        elif option == '3':
            statement(balance, bank_statement=bank_statement)
            
        elif option == '4':
            create_user(users)
            
        elif option == '5':
            create_account(accounts, AGENCY, users)
            
        elif option == '6':
            break
        
        else:
            print('\nSelecione uma das opções.')
            
main()