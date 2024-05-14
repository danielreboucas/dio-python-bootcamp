balance = 0
withdraws_number = 0
bank_statement = []
LIMIT = 500

while True:
    print(
    '''
    Escolha uma das opções abaixo: 

    1: Depositar
    2: Sacar
    3: Extrato
    4: Sair
    '''
    )
    option = input('Opção: ')
    
    if option == '1':
        print('\nQuanto deseja depositar?')
        deposit_value = float(input('Valor: '))
        balance += deposit_value
        bank_statement.append(deposit_value)
        print(f'''---\nNovo saldo: R$ {balance:.2f}\n---\n''')
        
    elif option == '2':
        print(f'\nQuanto deseja sacar? (Limite: {LIMIT})')
        withdraw_value = float(input('Valor: '))
        
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
            else:
                print(f'\nQuantidade a ser sacada é maior que o limite permitido ({LIMIT})')
    
    elif option == '3':
        if len(bank_statement) == 0:
            print('\nNão foram realizadas movimentações.')
        else:
            print('\n--- Extrato ---')
            for statement in bank_statement:
                print(f'R$ {statement:.2F} \n')
            print(f'Saldo: R$ {balance:.2F}')
            print('---------------')
    elif option == '4':
        break
    
    else:
        print('\nSelecione uma das opções.')