# Trading-Bot
Built a simplified trading bot in Python that places MARKET and LIMIT orders on Binance Futures Testnet via CLI. Designed with a clean, modular structure — separating the API client, validation, order logic, and logging — with proper error handling for invalid inputs and failed API calls.

Setup & Run Instructions
1. Get Binance Testnet API keys

Go to https://testnet.binancefuture.com
Log in with GitHub, activate a Futures Testnet account
Generate an API Key and Secret from the dashboard

2. Open the project in VS Code

Unzip trading_bot.zip
File → Open Folder → select the outer trading_bot folder (must show bot/, README.md, requirements.txt in Explorer)

3. Open terminal in VS Code

Ctrl + ` (or Terminal → New Terminal)
Make sure prompt shows trading_bot> (not trading_bot\bot>)

4. (Optional but recommended) Create a virtual environment
python -m venv venv
venv\Scripts\activate
You should see (venv) appear in the prompt.
5. Install dependencies
pip install -r requirements.txt
6. Set your API keys (PowerShell)
$env:BINANCE_API_KEY="your_key_here"
$env:BINANCE_API_SECRET="your_secret_here"
(These only last for the current terminal session — you'll need to re-set them if you close and reopen the terminal.)
7. Run the bot
MARKET order:
python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
LIMIT order:
python -m bot.cli --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 60000
8. Check the logs
After running, check logs/trading_bot.log — this file gets created automatically and records every request/response/error. Save a sample from here since it's required for your submission.
Common errors:

ModuleNotFoundError: No module named 'bot' → you're in the wrong folder; run cd .. until prompt shows trading_bot>
API key/secret required → env variables weren't set correctly, or you closed/reopened the terminal after setting them
Order fails with a Binance error → check your testnet account has funds, and that the symbol/quantity meet Binance's minimum requirements
