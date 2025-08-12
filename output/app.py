import gradio as gr
from accounts import Account, get_share_price

account = None

def create_account(account_id: str, initial_deposit: float):
    global account
    account = Account(account_id, initial_deposit)
    return f"Account {account_id} created with initial deposit ${initial_deposit:.2f}"

def deposit(amount: float):
    if account is None:
        return "Please create an account first"
    account.deposit_funds(amount)
    return f"Deposited ${amount:.2f}. New balance: ${account.balance:.2f}"

def withdraw(amount: float):
    if account is None:
        return "Please create an account first"
    if account.withdraw_funds(amount):
        return f"Withdrew ${amount:.2f}. New balance: ${account.balance:.2f}"
    else:
        return "Insufficient funds for withdrawal"

def buy_shares(symbol: str, quantity: int):
    if account is None:
        return "Please create an account first"
    if account.buy_shares(symbol, quantity):
        return f"Bought {quantity} shares of {symbol}. New balance: ${account.balance:.2f}"
    else:
        return "Insufficient funds for purchase"

def sell_shares(symbol: str, quantity: int):
    if account is None:
        return "Please create an account first"
    if account.sell_shares(symbol, quantity):
        return f"Sold {quantity} shares of {symbol}. New balance: ${account.balance:.2f}"
    else:
        return "Insufficient shares to sell"

def get_portfolio():
    if account is None:
        return "Please create an account first"
    holdings = account.get_holdings()
    portfolio_value = account.calculate_portfolio_value()
    profit_loss = account.get_profit_or_loss()
    
    holdings_str = "\n".join([f"{k}: {v} shares" for k, v in holdings.items()]) if holdings else "No holdings"
    
    return (f"Current Holdings:\n{holdings_str}\n\n"
            f"Portfolio Value: ${portfolio_value:.2f}\n"
            f"Profit/Loss: ${profit_loss:.2f}")

def get_transaction_history():
    if account is None:
        return "Please create an account first"
    transactions = account.get_transactions()
    if not transactions:
        return "No transactions yet"
    
    history = []
    for t in transactions:
        if t[0] == "deposit":
            history.append(f"Deposit: +${t[1]:.2f}")
        elif t[0] == "withdraw":
            history.append(f"Withdrawal: -${t[1]:.2f}")
        elif t[0] == "buy":
            history.append(f"Buy: {t[2]} shares of {t[1]} @ ${t[3]:.2f}")
        elif t[0] == "sell":
            history.append(f"Sell: {t[2]} shares of {t[1]} @ ${t[3]:.2f}")
    
    return "\n".join(history)

with gr.Blocks() as demo:
    gr.Markdown("# Trading Simulation Platform")
    
    with gr.Tab("Account"):
        with gr.Row():
            account_id = gr.Textbox(label="Account ID", value="001")
            initial_deposit = gr.Number(label="Initial Deposit", value=10000.0)
            create_btn = gr.Button("Create Account")
        create_output = gr.Textbox(label="Account Status")
        
        with gr.Row():
            deposit_amount = gr.Number(label="Deposit Amount")
            deposit_btn = gr.Button("Deposit")
        with gr.Row():
            withdraw_amount = gr.Number(label="Withdraw Amount")
            withdraw_btn = gr.Button("Withdraw")
        deposit_output = gr.Textbox(label="Transaction Status")
    
    with gr.Tab("Trading"):
        with gr.Row():
            symbol = gr.Dropdown(label="Stock Symbol", choices=["AAPL", "TSLA", "GOOGL"])
            quantity = gr.Number(label="Quantity", value=1)
        with gr.Row():
            buy_btn = gr.Button("Buy")
            sell_btn = gr.Button("Sell")
        trade_output = gr.Textbox(label="Trade Status")
    
    with gr.Tab("Portfolio"):
        portfolio_btn = gr.Button("Refresh Portfolio")
        portfolio_output = gr.Textbox(label="Portfolio Summary", lines=10)
    
    with gr.Tab("Transactions"):
        transactions_btn = gr.Button("Refresh Transactions")
        transactions_output = gr.Textbox(label="Transaction History", lines=10)
    
    create_btn.click(create_account, inputs=[account_id, initial_deposit], outputs=create_output)
    deposit_btn.click(deposit, inputs=deposit_amount, outputs=deposit_output)
    withdraw_btn.click(withdraw, inputs=withdraw_amount, outputs=deposit_output)
    buy_btn.click(buy_shares, inputs=[symbol, quantity], outputs=trade_output)
    sell_btn.click(sell_shares, inputs=[symbol, quantity], outputs=trade_output)
    portfolio_btn.click(get_portfolio, outputs=portfolio_output)
    transactions_btn.click(get_transaction_history, outputs=transactions_output)

if __name__ == "__main__":
    demo.launch()