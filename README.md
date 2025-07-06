# 🚀 NQ Strategy Hunter - AI-Powered Trading Strategy Discovery

<div align="center">

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.3+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
![GitHub issues](https://img.shields.io/github/issues/Hezi12/strategy-hunter)
![GitHub stars](https://img.shields.io/github/stars/Hezi12/strategy-hunter)

**🎯 Autonomous Trading Strategy Discovery for NQ Futures**

[🌐 **Try Live Demo**](https://your-domain.com) • [📖 **Documentation**](docs/) • [🇮🇱 **Hebrew Docs**](WEB_README.md)

</div>

## 🌟 Features

- 🤖 **Autonomous Strategy Discovery** - AI-powered genetic algorithm that runs 24/7
- 📊 **Advanced Analytics** - RSI, MACD, Bollinger Bands, Price Action analysis
- 🌐 **Beautiful Web Interface** - No terminal required, modern responsive UI
- 📈 **Real-time Monitoring** - Live strategy performance tracking
- 🔬 **Comprehensive Backtesting** - Historical data testing with 355K+ data points
- 🎯 **Strict Risk Management** - Stop loss, position sizing, drawdown control
- 📱 **Mobile-Friendly** - Works on desktop, tablet, and mobile devices
- 🔒 **Privacy-First** - All processing happens locally, no cloud dependencies

## 🚀 Quick Start

### 🌐 Web Interface (Recommended)
```bash
# Clone the repository
git clone https://github.com/Hezi12/strategy-hunter.git
cd strategy-hunter

# Install dependencies
pip install -r web/requirements.txt

# Launch web interface
python3 run_website.py
```

**That's it!** The web interface will open automatically at `http://localhost:5001`

### 🖥️ Command Line Interface
```bash
# Autonomous strategy discovery
python3 run_autonomous.py

# Interactive dashboard
python3 run_dashboard.py

# Data analysis tools
python3 run_analysis.py
```

## 📊 What It Does

The system uses a **genetic algorithm** to discover profitable trading strategies for NQ (Nasdaq Futures) by:

1. **Analyzing 355K+ data points** from NQ historical data
2. **Creating 100 random strategies** each generation
3. **Testing each strategy** against strict performance criteria
4. **Evolving the best performers** through crossover and mutation
5. **Finding winning strategies** that meet all profitability requirements

## 🎯 Winning Strategy Criteria

The AI discovers strategies that meet **ALL** these strict criteria:

### 📊 Performance Requirements
- **Minimum Trades**: 200+ trades annually
- **Profit Factor**: 1.7+ (gross profit / gross loss)
- **Sharpe Ratio**: 1.5+ (risk-adjusted returns)
- **Win Rate**: 50%+ success rate
- **Average Trade**: $30+ per trade

### 🛡️ Risk Management
- **Max Drawdown**: Under $10,000
- **Consecutive Losses**: Maximum 6 trades
- **Total Return**: Must be positive
- **Consistency**: Stable performance across time periods

## 🏗️ Project Structure

```
nq-strategy-hunter/
├── 🌐 web/                 # Modern web interface
│   ├── app.py             # Flask server
│   ├── templates/         # HTML templates
│   └── requirements.txt   # Web dependencies
├── 🤖 autonomous/         # Autonomous AI system
│   ├── autonomous_strategy_hunter.py
│   └── show_results.py
├── 📊 strategies/         # Strategy discovery engines
├── 🔍 analysis/           # Data analysis tools
├── 📈 data/               # Market data (NQ 2018-2024)
├── 📋 results/            # Generated strategies & reports
├── 🎛️ dashboard/          # Streamlit dashboard
├── 📚 docs/               # Documentation
└── 🚀 run_*.py            # Quick launch scripts
```

## 💻 Web Interface Features

### 🏠 Main Dashboard
- **🟢 Start System** - Launch autonomous strategy discovery
- **🔴 Stop System** - Halt the discovery process
- **📊 View Results** - Browse discovered strategies
- **🚦 Status Monitor** - Real-time system monitoring

### 📈 Results Dashboard
- **Interactive Charts** - Strategy performance visualization
- **Strategy Comparison** - Side-by-side strategy analysis
- **Best Strategy Details** - Complete winning parameters
- **Auto-Refresh** - Live updates every 60 seconds

## 🔧 Installation & Setup

### Local Development
```bash
# 1. Clone repository
git clone https://github.com/Hezi12/strategy-hunter.git
cd strategy-hunter

# 2. Install dependencies
pip install -r web/requirements.txt

# 3. Launch web interface
python3 run_website.py
```

### Docker Deployment
```bash
# Build image
docker build -t nq-strategy-hunter .

# Run container
docker run -p 5001:5001 nq-strategy-hunter
```

### Production Deployment
See **[WEB_DEPLOYMENT.md](WEB_DEPLOYMENT.md)** for detailed instructions on:
- VPS deployment
- Nginx configuration
- SSL certificate setup
- Domain configuration
- Cloud platform deployment (Heroku, Railway, Render)

## 📊 Sample Results

```
🏆 Winning Strategy Discovered!
═══════════════════════════════════════
📊 Generation: 5
💰 Total Return: $133,764
📈 Win Rate: 59.6%
🎯 Fitness Score: 433.8
📱 Total Trades: 30,121
⚡ Average Trade: $44.32
🛡️ Max Drawdown: $8,450
```

## 🧬 How the AI Works

### 1. **Data Processing**
- Loads NQ futures data (2018-2024)
- Calculates technical indicators (RSI, MACD, Volume, etc.)
- Prepares market microstructure data

### 2. **Genetic Algorithm**
- Initializes population of 100 random strategies
- Each strategy has 20+ parameters (entry/exit rules)
- Evaluates fitness based on backtesting results

### 3. **Evolution Process**
- Selects top 20% performers (elitism)
- Creates new generation through crossover
- Applies random mutations (15% rate)
- Repeats until winning strategy found

### 4. **Strategy Validation**
- Tests against all winning criteria
- Validates risk management parameters
- Exports complete strategy details

## 🌐 Deployment Options

### Quick Deploy (1-Click)
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
[![Deploy to Railway](https://railway.app/button.svg)](https://railway.app/new)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Self-Hosted Options
- **VPS Deployment**: Full control, custom domain
- **Docker**: Containerized deployment
- **Local Network**: Run on home server

## 🛡️ Security & Disclaimers

### 🔒 Security Features
- **Local Processing**: All AI runs on your machine
- **No Cloud Dependencies**: Data never leaves your computer
- **Privacy First**: No external API calls required
- **Secure Deployment**: Production-ready security configs

### ⚠️ Important Disclaimers
- **Research Tool**: For educational and research purposes only
- **Historical Data**: Past performance doesn't guarantee future results
- **Risk Warning**: Trading involves substantial risk of loss
- **Due Diligence**: Always validate strategies before live trading

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with modern Python web technologies
- Genetic algorithm inspired by financial research
- Technical indicators based on industry standards
- UI/UX designed for professional traders

## 📞 Support & Community

- 📧 **Email**: [support@your-domain.com](mailto:support@your-domain.com)
- 💬 **Discord**: [Join our community](https://discord.gg/nq-strategy-hunter)
- 🐛 **Issues**: [GitHub Issues](https://github.com/Hezi12/strategy-hunter/issues)
- 📖 **Documentation**: [Full Documentation](docs/)
- 🐦 **Twitter**: [@NQStrategyBot](https://twitter.com/NQStrategyBot)

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Hezi12/strategy-hunter&type=Date)](https://star-history.com/#Hezi12/strategy-hunter&Date)

---

<div align="center">

**Made with ❤️ for the trading community**

If this project helps you discover profitable strategies, please consider giving it a ⭐️!

[🌟 **Star on GitHub**](https://github.com/Hezi12/strategy-hunter) • [🐦 **Follow on Twitter**](https://twitter.com/NQStrategyBot) • [💬 **Join Discord**](https://discord.gg/nq-strategy-hunter)

</div> 