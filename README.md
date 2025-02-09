<h1 align="center">Forex Trading Robot - SMA Crossover Strategy</h1>
<p align="center">
  <img src="https://github.com/user-attachments/assets/9bcc92a8-1bc1-409c-9125-dc26adb526f9" alt="GUI Screenshot" width="600">
</p><p>This is an <strong>automated Forex trading robot</strong> built using Python and MetaTrader 5. It implements a <strong>Simple Moving Average (SMA) Crossover Strategy</strong> to identify trading opportunities and execute trades automatically. The robot is designed to be simple, efficient, and customizable, making it suitable for both beginners and experienced traders.</p>

<h2>✨ Features</h2><ul>
  <li><strong>SMA Crossover Strategy</strong>: Uses a 10-period fast SMA and a 50-period slow SMA to generate buy/sell signals.</li>
  <li><strong>Risk Management</strong>: Built-in stop loss and take profit levels to protect trades.</li>
  <li><strong>User-Friendly Interface</strong>: Modern dark-themed GUI with rounded corners for easy configuration.</li>
  <li><strong>Real-Time Trading</strong>: Connects to MetaTrader 5 for real-time price data and trade execution.</li>
  <li><strong>Customizable</strong>: Easily modify SMA periods, stop loss, take profit, and other parameters.</li>
</ul>

<h2>🚀 How It Works</h2>
<ol>
  <li>The robot fetches real-time price data from MetaTrader 5.</li>
  <li>It calculates the 10-period fast SMA and 50-period slow SMA.</li>
  <li>When the fast SMA crosses above the slow SMA, it generates a buy signal.</li>
  <li>When the fast SMA crosses below the slow SMA, it generates a sell signal.</li>
  <li>The robot automatically executes trades based on these signals and manages open positions.</li>
</ol>

<h2>📦 Installation</h2>
<ol>
  <li><strong>Install Python</strong>: Ensure you have Python 3.8 or higher installed.</li>
  <li><strong>Install Required Libraries</strong>:
    <pre><code>pip install MetaTrader5 pandas tkinter</code></pre>
  </li>
  <li><strong>Set Up MetaTrader 5</strong>:
    <ul>
      <li>Install MetaTrader 5 from <a href="https://www.metatrader5.com/">MetaQuotes</a>.</li>
      <li>Create a demo account for testing.</li>
    </ul>
  </li>
  <li><strong>Clone the Repository</strong>:
    <pre><code>git clone https://github.com/your-username/forex-trading-robot.git
cd forex-trading-robot</code></pre>
  </li>
  <li><strong>Run the Robot</strong>:
    <pre><code>python KayTechRobot.py</code></pre>
  </li>
</ol>

<h2>🎯 Usage</h2>
<ol>
  <li>Launch the application.</li>
  <li>Configure the settings in the GUI:
    <ul>
      <li>Select a currency pair (e.g., EURUSD).</li>
      <li>Set the lot size or risk percentage.</li>
      <li>Choose a timeframe (e.g., M1, M5, H1).</li>
    </ul>
  </li>
  <li>Click <strong>"Start Trading"</strong> to begin.</li>
  <li>Monitor the logs for trade executions and errors.</li>
</ol>

<h2>📸 Screenshots</h2>
<p align="center">
  <img src="https://github.com/user-attachments/assets/9bcc92a8-1bc1-409c-9125-dc26adb526f9" alt="GUI Screenshot" width="600">
</p>
<p align="center"><em>The modern dark-themed GUI for configuring the robot.</em></p>

<h2>🤝 Contributing</h2>
<p>Contributions are welcome! If you'd like to improve this project, please:</p>
<ol>
  <li>Fork the repository.</li>
  <li>Create a new branch (<code>git checkout -b feature/YourFeature</code>).</li>
  <li>Commit your changes (<code>git commit -m 'Add some feature'</code>).</li>
  <li>Push to the branch (<code>git push origin feature/YourFeature</code>).</li>
  <li>Open a pull request.</li>
</ol>

<h2>📜 License</h2>
<p>This project is licensed under the <strong>MIT License</strong>. See the <a href="LICENSE">LICENSE</a> file for details.</p>

<h2>⚠️ Disclaimer</h2>
<p>This Forex trading robot is for <strong>educational purposes only</strong>. Trading in the Forex market involves significant risk, and you should only trade with money you can afford to lose. The developers are not responsible for any financial losses incurred while using this software.</p>

<h2>📞 Support</h2>
<p>If you have any questions or need help, feel free to open an issue on GitHub or contact me at <a href="mailto:your-email@example.com">your-email@example.com</a>.</p>
