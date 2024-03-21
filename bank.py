""" вас есть банковская карта с начальным балансом равным 0 у.е.
Вы хотите управлять этой картой, выполняя следующие операции, для
выполнения которых необходимо написать следующие функции:
check_multiplicity(amount): Проверка кратности суммы при пополнении и
снятии.
deposit(amount): Пополнение счёта.
withdraw(amount): Снятие денег.
exit(): Завершение работы и вывод итоговой информации о состоянии
счета и проведенных операциях.
"""
import decimal
import logging
import sys

MULTIPLICITY = 50
PERCENT_REMOVAL = decimal.Decimal(15) / decimal.Decimal(1000)
MIN_REMOVAL = decimal.Decimal(30)
MAX_REMOVAL = decimal.Decimal(600)
PERCENT_DEPOSIT = decimal.Decimal(3) / decimal.Decimal(100)
RICHNESS_PERCENT = decimal.Decimal(10) / decimal.Decimal(100)
RICHNESS_SUM = decimal.Decimal(10_000_000)
bank_account = decimal.Decimal(0)
count = 0
operations = []
FORMAT = '{asctime} - {levelname} - {funcName}() - {msg} '


def check_multiplicity(amount: int) -> bool:
    """проверяет, кратна ли сумма amount заданному множителю MULTIPLICITY."""
    if not isinstance(amount, int):
        logging.error(f'Некорректное значение. Должно быть целое int, введено {type(amount)}')
        raise ValueError(f'Введено некорректное значение {amount}.')
    if amount < 0:
        logging.error(f'Некорректное значение. {amount} должно быть > 0.')
        raise ValueError(f'Введено некорректное значение {amount}.')

    if amount % MULTIPLICITY != 0:
        logging.info(f'Сумма должна быть кратной {MULTIPLICITY} у.е.')
        return False
    return True


def deposit(amount: int) -> None:
    """позволяет клиенту пополнять свой счет на
       определенную сумму. Пополнение счета возможно только на сумму,
       которая кратна MULTIPLICITY."""
    if check_multiplicity(amount):
        logging.info(f'Cчет пополнен на сумму {amount}')
        global bank_account
        bank_account += amount
        operations.append(
            f'Пополнение карты на {amount} у.е. Итого {bank_account} у.е.')


def withdraw(amount: int) -> None:
    """позволяет клиенту снимать средства со счета.
       Сумма снятия также должна быть кратной MULTIPLICITY. При снятии средств
       начисляется комиссия в процентах от снимаемой суммы, которая может
       варьироваться от MIN_REMOVAL до MAX_REMOVAL."""
    if not isinstance(amount, int):
        logging.error(f'Некорректное значение. Должно быть целое int, введено {type(amount)}')
        raise ValueError(f'Введено некорректное значение: {amount}.')
    if amount < 0:
        logging.error(f'Некорректное значение. {amount} должно быть > 0.')
        raise ValueError(f'Введено некорректное значение {amount}.')

    global bank_account
    res = amount * PERCENT_REMOVAL
    res = max(res, MIN_REMOVAL)
    res = min(res, MAX_REMOVAL)
    if bank_account < amount:
        logging.info('Недостаточно средств.')
        operations.append(
            f'Недостаточно средств. Сумма с комиссией {int(amount + res)} у.е. '
            f'На карте {bank_account} у.е.')
    if check_multiplicity(amount):
        if bank_account > amount:
            logging.info('Снятие с карты прошло успешно.')
            bank_account = bank_account - amount - res
            operations.append(
                f'Снятие с карты {amount} у.е. Процент за снятие {int(res)} у.е.. '
                f'Итого {int(bank_account)} у.е.')


def bank_exit() -> None:
    """Завершает работу с банковским счетом. Перед завершением,
    если на счету больше RICHNESS_SUM, начисляется налог на богатство в
    размере RICHNESS_PERCENT процентов."""
    global bank_account
    if bank_account > RICHNESS_SUM:
        percent = bank_account * RICHNESS_PERCENT
        bank_account -= percent
        operations.append(
            f'Вычтен налог на богатство {RICHNESS_PERCENT}% в сумме {percent} '
            f'у.е. Итого {bank_account} у.е.')
    operations.append(f'Возьмите карту на которой {bank_account} у.е.')
    logging.info('Работа с банковским счетом завершена.')


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.INFO,
        format=FORMAT, style='{',
        handlers=[
            logging.FileHandler(__file__[:-3] + '.log', encoding='utf-8', mode='w'),
            logging.StreamHandler(sys.stdout)])

    try:
        deposit(500)
        withdraw(100)
        withdraw(50)
        deposit(100)
        withdraw(250)
        bank_exit()
    except ValueError as e:
        print(e)