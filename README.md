import os
from dotenv import load_dotenv

load_dotenv()

# Configuration Telegram
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Configuration Trading Forex
FOREX_PAIRS = [
    'GBP/USD',
    'EUR/USD', 
    'EUR/JPY'
]

# Symboles pour l'API
FOREX_SYMBOLS = {
    'GBPUSD': 'GBP/USD',
    'EURUSD': 'EUR/USD',
    'EURJPY': 'EUR/JPY'
}

# Timeframes disponibles
TIMEFRAMES = {
    '5m': '5m',
    '15m': '15m',
    '30m': '30m',
    '1h': '1h',
    '4h': '4h',
    '1d': '1d'
}

# Configuration SMC spécifique Forex
SMC_CONFIG = {
    'order_block_lookback': 50,
    'fair_value_gap_threshold': 0.05,  # Plus petit pour le Forex
    'liquidity_sweep_lookback': 20,
    'breaker_block_threshold': 0.03,
    'bos_lookback': 10,
    'choch_lookback': 15,
    'premium_discount_threshold': 0.5,
    'volume_threshold': 1.2,  # Volume moins important en Forex
    'pip_threshold': 10,  # Seuil en pips pour les signaux
}

# Paramètres de risque Forex
RISK_CONFIG = {
    'max_risk_per_trade': 2.0,  # % du capital
    'max_daily_risk': 5.0,  # % du capital
    'rr_ratio': 2.0,  # Ratio risque/récompense
    'max_open_positions': 3,
    'stop_loss_atr_multiplier': 1.5,
    'default_position_size': 0.1,  # Lots standard
    'pip_value': {
        'GBPUSD': 10,  # $ par pip pour 1 lot standard
        'EURUSD': 10,
        'EURJPY': 8.5  # Approximatif, dépend du taux JPY/USD
    }
}

# Sessions de trading Forex (UTC)
TRADING_SESSIONS = {
    'london': {'open': 7, 'close': 16},
    'new_york': {'open': 12, 'close': 21},
    'tokyo': {'open': 23, 'close': 8},
    'sydney': {'open': 21, 'close': 6}
}

# News économiques importantes
ECONOMIC_NEWS = {
    'high_impact': ['NFP', 'CPI', 'GDP', 'Interest Rate Decision', 'FOMC'],
    'medium_impact': ['PMI', 'Retail Sales', 'Unemployment Rate', 'Trade Balance']
}# Trading-assistant-
