import unittest
from unittest.mock import patch
from accounts import Account, get_share_price


class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account("12345", 1000.0)
    
    def test_initialization(self):
        self.assertEqual(self.account.account_id, "12345")
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(self.account.initial_deposit, 1000.0)
        self.assertEqual(self.account.holdings, {})
        self.assertEqual(self.account.transactions, [])
    
    def test_deposit_funds(self):
        self.account.deposit_funds(500.0)
        self.assertEqual(self.account.balance, 1500.0)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0], ("deposit", 500.0))
    
    def test_withdraw_funds_success(self):
        result = self.account.withdraw_funds(500.0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 500.0)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0], ("withdraw", 500.0))
    
    def test_withdraw_funds_failure(self):
        result = self.account.withdraw_funds(1500.0)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(len(self.account.transactions), 0)
    
    @patch('accounts.get_share_price', return_value=150.0)
    def test_buy_shares_success(self, mock_get_share_price):
        result = self.account.buy_shares("AAPL", 5)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 1000.0 - (150.0 * 5))
        self.assertEqual(self.account.holdings, {"AAPL": 5})
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0], ("buy", "AAPL", 5, 150.0))
    
    @patch('accounts.get_share_price', return_value=150.0)
    def test_buy_shares_failure(self, mock_get_share_price):
        result = self.account.buy_shares("AAPL", 10)  # 1500 > 1000 balance
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(self.account.holdings, {})
        self.assertEqual(len(self.account.transactions), 0)
    
    @patch('accounts.get_share_price', return_value=150.0)
    def test_sell_shares_success(self, mock_get_share_price):
        self.account.buy_shares("AAPL", 10)  # Setup holdings
        result = self.account.sell_shares("AAPL", 5)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 1000.0 - (150.0 * 10) + (150.0 * 5))
        self.assertEqual(self.account.holdings, {"AAPL": 5})
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[1], ("sell", "AAPL", 5, 150.0))
    
    @patch('accounts.get_share_price', return_value=150.0)
    def test_sell_shares_failure_not_enough_shares(self, mock_get_share_price):
        result = self.account.sell_shares("AAPL", 5)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(self.account.holdings, {})
        self.assertEqual(len(self.account.transactions), 0)
    
    @patch('accounts.get_share_price', return_value=150.0)
    def test_calculate_portfolio_value(self, mock_get_share_price):
        self.account.buy_shares("AAPL", 5)
        expected_value = (1000.0 - (150.0 * 5)) + (150.0 * 5)
        self.assertEqual(self.account.calculate_portfolio_value(), expected_value)
    
    def test_get_holdings(self):
        self.assertEqual(self.account.get_holdings(), {})
    
    def test_get_transactions(self):
        self.assertEqual(self.account.get_transactions(), [])
    
    @patch('accounts.get_share_price', return_value=150.0)
    def test_get_profit_or_loss(self, mock_get_share_price):
        self.account.buy_shares("AAPL", 5)
        current_value = (1000.0 - (150.0 * 5)) + (150.0 * 5)
        expected_profit = current_value - 1000.0
        self.assertEqual(self.account.get_profit_or_loss(), expected_profit)


class TestGetSharePrice(unittest.TestCase):
    def test_get_share_price_existing(self):
        self.assertEqual(get_share_price("AAPL"), 150.0)
        self.assertEqual(get_share_price("TSLA"), 700.0)
        self.assertEqual(get_share_price("GOOGL"), 2800.0)
    
    def test_get_share_price_non_existing(self):
        self.assertEqual(get_share_price("UNKNOWN"), 0.0)


if __name__ == "__main__":
    unittest.main()