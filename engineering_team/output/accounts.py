class Account:
    def __init__(self, account_id: str, initial_deposit: float) -> None:
        self.account_id = account_id
        self.initial_deposit = initial_deposit
        self.balance = initial_deposit
        self.holdings = {}
        self.transactions = []

    def deposit_funds(self, amount: float) -> None:
        self.balance += amount
        self.transactions.append(("deposit", amount))

    def withdraw_funds(self, amount: float) -> bool:
        if amount <= self.balance:
            self.balance -= amount
            self.transactions.append(("withdraw", amount))
            return True
        return False

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        share_price = get_share_price(symbol)
        total_price = share_price * quantity
        if total_price <= self.balance:
            self.balance -= total_price
            if symbol in self.holdings:
                self.holdings[symbol] += quantity
            else:
                self.holdings[symbol] = quantity
            self.transactions.append(("buy", symbol, quantity, share_price))
            return True
        return False

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        if symbol in self.holdings and self.holdings[symbol] >= quantity:
            share_price = get_share_price(symbol)
            total_price = share_price * quantity
            self.balance += total_price
            self.holdings[symbol] -= quantity
            if self.holdings[symbol] == 0:
                del self.holdings[symbol]
            self.transactions.append(("sell", symbol, quantity, share_price))
            return True
        return False

    def calculate_portfolio_value(self) -> float:
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def get_holdings(self) -> dict:
        return self.holdings

    def get_transactions(self) -> list:
        return self.transactions

    def get_profit_or_loss(self) -> float:
        current_value = self.calculate_portfolio_value()
        return current_value - self.initial_deposit


def get_share_price(symbol: str) -> float:
    prices = {"AAPL": 150.0, "TSLA": 700.0, "GOOGL": 2800.0}
    return prices.get(symbol, 0.0)

# Example code to demonstrate usage
if __name__ == "__main__":
    account = Account("001", 10000.0)
    account.deposit_funds(2000)
    account.buy_shares("AAPL", 10)
    account.sell_shares("AAPL", 5)
    account.withdraw_funds(500)
    print("Holdings:", account.get_holdings())
    print("Transactions:", account.get_transactions())
    print("Portfolio Value:", account.calculate_portfolio_value())
    print("Profit/Loss:", account.get_profit_or_loss())
