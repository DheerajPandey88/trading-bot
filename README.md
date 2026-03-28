# Binance Futures Testnet Trading Bot

## Setup

1. Clone repo
2. Install dependencies:
   pip install -r requirements.txt

3. Create .env file:
   BINANCE_API_KEY=your_key
   BINANCE_API_SECRET=your_secret

4. Run examples:

### Market Order
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

### Limit Order
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 60000

## Features
- Market & Limit Orders
- BUY / SELL support
- CLI input validation
- Logging to file
- Error handling

5.* 🌄 **Screenshots**
<h2 align="center">📱 App Preview</h2>

<p align="center">
  <img src="https://github.com/DheerajPandey88/trading-bot/blob/8a91cb24224fd264c192cc6f99d3e39e715cdd3f/Screenshot%202026-03-29%20010148.png" width="250">
</p>


## Logs
Check logs in:
logs/bot.log

## Assumptions
- Using Binance Futures Testnet
- API keys already created
