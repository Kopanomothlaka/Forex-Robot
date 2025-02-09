
"""
SMA Crossover Forex Robot with Modern Dark GUI
"""

import tkinter as tk
from tkinter import ttk
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import time
import logging
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('strategy.log'), logging.StreamHandler()]
)

# Add Canvas extension methods for rounded rectangles
def _create_rounded_rect(self, x, y, w, h, r=25, **kwargs):
    points = (x+r, y, x+r, y, x+w-r, y, x+w-r, y, x+w, y, x+w, y+r, 
             x+w, y+r, x+w, y+h-r, x+w, y+h-r, x+w, y+h, x+w-r, y+h, 
             x+w-r, y+h, x+r, y+h, x+r, y+h, x, y+h, x, y+h-r, 
             x, y+h-r, x, y+r, x, y+r, x, y)
    return self.create_polygon(points, **kwargs, smooth=True)
tk.Canvas.create_rounded_rect = _create_rounded_rect

# Color Scheme
COLORS = {
    'background': '#1a1a1a',
    'secondary': '#2d2d2d',
    'accent': '#4CAF50',
    'text': '#ffffff',
    'highlight': '#404040',
    'border': '#333333'
}

class StrategyConfigGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Forex Strategy Config")
        self.root.configure(bg=COLORS['background'])
        self.root.resizable(False, False)
        
        # Create main canvas with rounded corners
        self.canvas = tk.Canvas(self.root, bg=COLORS['background'], 
                              highlightthickness=0, width=400, height=350)
        self.canvas.pack(padx=20, pady=20)
        self.canvas.create_rounded_rect(10, 10, 390, 340, 25, 
                                      fill=COLORS['secondary'], outline=COLORS['border'])
        
        # Configure styles
        self.configure_styles()
        
        # Create widgets
        self.create_widgets()
        self.set_default_values()
        self.center_window()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame style
        style.configure('TFrame', background=COLORS['secondary'])
        
        # Label style
        style.configure('TLabel', 
                       background=COLORS['secondary'],
                       foreground=COLORS['text'],
                       font=('Arial', 10))
        
        # Entry style
        style.configure('TEntry', 
                       fieldbackground=COLORS['highlight'],
                       foreground=COLORS['text'],
                       bordercolor=COLORS['accent'],
                       lightcolor=COLORS['accent'],
                       darkcolor=COLORS['accent'],
                       font=('Arial', 10))
        
        # Combobox style
        style.configure('TCombobox', 
                       fieldbackground=COLORS['highlight'],
                       foreground=COLORS['text'],
                       background=COLORS['secondary'],
                       selectbackground=COLORS['accent'],
                       font=('Arial', 10))
        
        # Button style
        style.configure('TButton', 
                       background=COLORS['accent'],
                       foreground=COLORS['text'],
                       borderwidth=0,
                       focuscolor=COLORS['secondary'],
                       font=('Arial', 10, 'bold'))
        style.map('TButton', 
                 background=[('active', '#45a049'), ('disabled', '#333333')])

    def create_widgets(self):
        # Main container
        self.main_frame = ttk.Frame(self.canvas, style='TFrame')
        self.canvas.create_window(200, 175, window=self.main_frame)

        # Widgets
        ttk.Label(self.main_frame, text="Currency Pair:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.symbol = ttk.Combobox(self.main_frame, width=18, style='TCombobox')
        self.symbol.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(self.main_frame, text="Lot Size:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.lot_size = ttk.Entry(self.main_frame, width=21, style='TEntry')
        self.lot_size.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Label(self.main_frame, text="Risk Percentage:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.risk_percent = ttk.Entry(self.main_frame, width=21, style='TEntry')
        self.risk_percent.grid(row=2, column=1, padx=10, pady=10)
        
        ttk.Label(self.main_frame, text="Timeframe:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.timeframe = ttk.Combobox(self.main_frame, 
                                    values=['M1', 'M5', 'M15', 'H1', 'H4', 'D1'], 
                                    width=18, style='TCombobox')
        self.timeframe.grid(row=3, column=1, padx=10, pady=10)
        
        self.start_btn = ttk.Button(self.main_frame, text="START TRADING", 
                                   style='TButton', command=self.start_strategy)
        self.start_btn.grid(row=4, column=0, columnspan=2, pady=20)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')

    def get_available_symbols(self):
        try:
            mt5.initialize()
            symbols = mt5.symbols_get()
            return [s.name for s in symbols][:30]
        except Exception as e:
            logging.error(f"Error getting symbols: {str(e)}")
            return ['EURUSD', 'GBPUSD', 'USDJPY', 'XAUUSD', 'BTCUSD']
        finally:
            mt5.shutdown()

    def set_default_values(self):
        self.symbol['values'] = self.get_available_symbols()
        self.symbol.set('EURUSD')
        self.lot_size.insert(0, '0.1')
        self.risk_percent.insert(0, '1.0')
        self.timeframe.set('H1')

    def validate_inputs(self):
        try:
            inputs = {
                'symbol': self.symbol.get(),
                'lot_size': float(self.lot_size.get()),
                'risk_percent': float(self.risk_percent.get()),
                'timeframe': self.timeframe.get()
            }
            
            if inputs['lot_size'] < 0 or inputs['risk_percent'] < 0:
                raise ValueError("Negative values not allowed")
                
            return inputs
        except ValueError as e:
            logging.error(f"Invalid input: {str(e)}")
            return None

    def start_strategy(self):
        inputs = self.validate_inputs()
        if inputs:
            self.root.destroy()
            strategy_thread = threading.Thread(target=run_strategy, args=(inputs,))
            strategy_thread.start()

# Strategy Core Functions ######################################################

def get_sma_crossover(symbol, timeframe, fast=10, slow=50):
    try:
        bars = mt5.copy_rates_from_pos(symbol, timeframe, 0, slow + 1)
        if bars is None or len(bars) < slow:
            logging.error("Not enough bars for SMA calculation")
            return 'neutral'

        df = pd.DataFrame(bars)
        df['fast_sma'] = df['close'].rolling(fast).mean()
        df['slow_sma'] = df['close'].rolling(slow).mean()

        last_fast = df['fast_sma'].iloc[-1]
        last_slow = df['slow_sma'].iloc[-1]
        prev_fast = df['fast_sma'].iloc[-2]
        prev_slow = df['slow_sma'].iloc[-2]

        if last_fast > last_slow and prev_fast <= prev_slow:
            return 'buy'
        elif last_fast < last_slow and prev_fast >= prev_slow:
            return 'sell'
        return 'neutral'

    except Exception as e:
        logging.error(f"SMA calculation error: {str(e)}")
        return 'neutral'

def calculate_position_size(symbol, risk_percent, sl_pips=20):
    try:
        account_info = mt5.account_info()
        if account_info is None:
            logging.error("Failed to get account info")
            return 0.0
        
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            logging.error(f"Failed to get symbol info for {symbol}")
            return 0.0

        balance = account_info.balance
        if balance <= 0:
            logging.error("Invalid account balance")
            return 0.0

        risk_amount = balance * (risk_percent / 100)
        point_value = symbol_info.point
        tick_value = symbol_info.trade_tick_value_profit

        if point_value == 0 or tick_value == 0:
            logging.error("Invalid point/tick value")
            return 0.0

        position_size = risk_amount / (sl_pips * point_value * tick_value)
        return round(position_size, 2)
    
    except Exception as e:
        logging.error(f"Position size calculation error: {str(e)}")
        return 0.0

def execute_trade(signal, args):
    try:
        symbol = args.symbol
        symbol_info = mt5.symbol_info(symbol)
        
        if args.lot_size > 0:
            position_size = args.lot_size
        else:
            position_size = calculate_position_size(symbol, args.risk_percent)
        
        if position_size <= 0:
            logging.error("Invalid position size")
            return

        tick = mt5.symbol_info_tick(symbol)
        sl_pips = 20  # Fixed stop loss
        tp_pips = 40  # Fixed take profit

        if signal == 'buy':
            order_type = mt5.ORDER_TYPE_BUY
            price = tick.ask
            sl_price = price - sl_pips * symbol_info.point
            tp_price = price + tp_pips * symbol_info.point
        else:
            order_type = mt5.ORDER_TYPE_SELL
            price = tick.bid
            sl_price = price + sl_pips * symbol_info.point
            tp_price = price - tp_pips * symbol_info.point

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": position_size,
            "type": order_type,
            "price": price,
            "sl": sl_price,
            "tp": tp_price,
            "deviation": 50,
            "magic": 234000,
            "comment": "SMA Strategy",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }

        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logging.error(f"Order failed: {result.comment}")
        else:
            logging.info(f"Order executed: {result}")
    
    except Exception as e:
        logging.error(f"Trade execution error: {str(e)}")

def manage_positions(current_signal, args):
    try:
        positions = mt5.positions_get(symbol=args.symbol)
        if positions is None:
            return

        for position in positions:
            if (position.type == mt5.ORDER_TYPE_BUY and current_signal == 'sell') or \
               (position.type == mt5.ORDER_TYPE_SELL and current_signal == 'buy'):
                close_position(position, args)
    
    except Exception as e:
        logging.error(f"Position management error: {str(e)}")

def close_position(position, args):
    try:
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": position.symbol,
            "volume": position.volume,
            "type": mt5.ORDER_TYPE_SELL if position.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY,
            "position": position.ticket,
            "price": mt5.symbol_info_tick(position.symbol).bid if position.type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(position.symbol).ask,
            "deviation": 50,
            "magic": 234000,
            "comment": "Close position",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }

        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logging.error(f"Close position failed: {result.comment}")
        else:
            logging.info(f"Position closed: {result}")
    
    except Exception as e:
        logging.error(f"Position closing error: {str(e)}")

def run_strategy(params):
    TIMEFRAME_MAP = {
        'M1': mt5.TIMEFRAME_M1,
        'M5': mt5.TIMEFRAME_M5,
        'M15': mt5.TIMEFRAME_M15,
        'H1': mt5.TIMEFRAME_H1,
        'H4': mt5.TIMEFRAME_H4,
        'D1': mt5.TIMEFRAME_D1,
    }

    class StrategyParams:
        def __init__(self, params):
            self.symbol = params['symbol']
            self.lot_size = params['lot_size']
            self.risk_percent = params['risk_percent']
            self.timeframe = params['timeframe']
            self.fast_sma = 10
            self.slow_sma = 50
            self.max_positions = 5
            self.deviation = 50
            self.magic_number = 234000

    args = StrategyParams(params)
    
    if not mt5.initialize():
        logging.error("Failed to initialize MT5")
        return

    logging.info(f"Strategy started with parameters: {params}")

    try:
        while True:
            current_signal = get_sma_crossover(
                args.symbol,
                TIMEFRAME_MAP[args.timeframe],
                args.fast_sma,
                args.slow_sma
            )

            manage_positions(current_signal, args)
            positions = mt5.positions_get(symbol=args.symbol)
            open_positions = len(positions) if positions else 0

            if open_positions < args.max_positions and current_signal != 'neutral':
                execute_trade(current_signal, args)

            # Sleep until next candle
            sleep_time = 60 - datetime.now().second
            time.sleep(max(1, sleep_time))

    except KeyboardInterrupt:
        logging.info("Strategy stopped by user")
    except Exception as e:
        logging.error(f"Critical error: {str(e)}")
    finally:
        mt5.shutdown()
        logging.info("MT5 connection closed")

if __name__ == '__main__':
    root = tk.Tk()
    app = StrategyConfigGUI(root)
    root.mainloop()