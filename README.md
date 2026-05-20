<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>README - AURA Quant Pipeline</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
            line-height: 1.6;
            color: #c9d1d9;
            background-color: #0d1117;
            max-width: 850px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }
        h1, h2, h3 {
            color: #58a6ff;
            border-bottom: 1px solid #21262d;
            padding-bottom: 0.3em;
        }
        h1 {
            font-size: 2.25rem;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        h3 {
            border-bottom: none;
            color: #c9d1d9;
            margin-top: 1.5rem;
        }
        .subtitle {
            font-size: 1.25rem;
            color: #8b949e;
            margin-top: 0;
            margin-bottom: 1.5rem;
            font-weight: 400;
        }
        a {
            color: #58a6ff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        hr {
            height: 0.25em;
            padding: 0;
            margin: 24px 0;
            background-color: #21262d;
            border: 0;
        }
        code, pre {
            font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
            font-size: 85%;
            background-color: #161b22;
            border-radius: 6px;
        }
        code {
            padding: 0.2em 0.4em;
        }
        pre {
            padding: 16px;
            overflow: auto;
            line-height: 1.45;
        }
        pre code {
            padding: 0;
            background-color: transparent;
            font-size: 100%;
            word-break: normal;
            white-space: pre;
            color: #e6edf3;
        }
        ul, ol {
            padding-left: 2em;
        }
        li {
            margin-top: 0.25em;
        }
        .badge-container {
            margin-bottom: 1.5rem;
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        .badge {
            display: inline-block;
            padding: 4px 8px;
            font-size: 0.75rem;
            font-weight: 600;
            color: #ffffff;
            border-radius: 20px;
            text-decoration: none !important;
        }
        .badge-python { background-color: #3776AB; }
        .badge-fastapi { background-color: #009688; }
        .badge-js { background-color: #F7DF1E; color: #000000; }
        .math-block {
            background-color: #161b22;
            border-left: 4px solid #388bfd;
            padding: 12px 16px;
            margin: 16px 0;
            font-family: "Times New Roman", Times, serif;
            font-size: 1.15rem;
            color: #e6edf3;
            overflow-x: auto;
        }
        .math-block i {
            font-family: "Times New Roman", Times, serif;
            font-style: italic;
        }
        .math-block sub {
            font-size: 0.75rem;
        }
        .footer {
            margin-top: 3rem;
            padding-top: 1.5rem;
            border-top: 1px solid #21262d;
            font-size: 0.85rem;
            color: #8b949e;
            text-align: center;
        }
    </style>
</head>
<body>

    <h1>AURA-Quant-Pipeline 📊</h1>
    <div class="subtitle">Automated Relative Strength, Alpha-Beta Estimation & Risk Sizing Engine</div>

    <div class="badge-container">
        <span class="badge badge-python">Python 3.13</span>
        <span class="badge badge-fastapi">FastAPI Backend</span>
        <span class="badge badge-js">Vanilla JS & CSS Frontend</span>
    </div>

    <p>An automated end-to-end quantitative trading pipeline designed to identify, rank, and dynamically allocate capital to equities showing structurally significant momentum. The engine streams tick data across the Nifty universe, separates market tailwinds from stock-specific skill using rolling OLS regressions, filters statistical noise via Z-scores, and calculates execution risk metrics in a decoupled web architecture.</p>

    <hr>

    <h2>🏢 System Architecture</h2>
    <p>The pipeline decouples resource-heavy mathematical computations from the client network layer to bypass web timeout limits when processing large equity universes.</p>

<pre><code>[ Raw Market Ingestion (yfinance) ] 
               │
               ▼
[ Quantitative Math Engine (main.py) ] ──(Generates Snapshots)──► [ latest_scan.json ]
               │                                                          ▲
               ▼                                                          │ (Direct I/O File Read)
[ Asynchronous Background Worker ]                                        │
               │                                                          │
   (Pings Status / Trigger)                                               │
               │                                                          │
               ▼                                                          │
[ FastAPI Production Gateway (api.py) ] ◄─────────────────────────────────┘
               ▲
               │ (Non-blocking Async Polling)
               ▼
[ Vanilla CSS/JS Dashboard (UI) ] ──► [ Client CSV Export Engine ]</code></pre>

    <hr>

    <h2>🧪 Core Quantitative Methodology</h2>

    <h3>1. Data Ingestion & Additive Continuity</h3>
    <p>Raw Open-High-Low-Close-Volume (OHLCV) datasets are ingested sequentially. To eliminate compounding scale asymmetry inherent in standard arithmetic percentage changes, returns are transformed into logarithmic time-series:</p>
    <div class="math-block">
        <i>r<sub>t</sub></i> = ln(<i>P<sub>t</sub></i> / <i>P<sub>t-1</sub></i>)
    </div>

    <h3>2. Idiosyncratic Alpha vs. Beta Systematic Separation</h3>
    <p>To ensure the model captures genuine momentum rather than broader market buoyancy, the script evaluates a rolling linear regression model of the asset against the benchmark index:</p>
    <div class="math-block">
        <i>R<sub>stock</sub></i> = <i>&alpha;</i> + <i>&beta;R<sub>Nifty</sub></i> + <i>&epsilon;</i>
    </div>
    <ul>
        <li><strong>Beta (<i>&beta;</i>):</strong> Represents systematic risk sensitivity (covariance of asset and market divided by market variance).</li>
        <li><strong>Alpha (<i>&alpha;</i>):</strong> Represents true, isolated asset outperformance independent of index behavior.</li>
    </ul>

    <h3>3. Statistical Significance Gating</h3>
    <p>Relative Strength (Log RS) is tracked as a linear difference of cumulative logarithmic distributions. To pass the core filter, an asset's Log RS must deviate from its historical rolling mean (&mu;) by a minimum standard deviation threshold (&sigma;), eliminating short-term noise:</p>
    <div class="math-block">
        <i>Z</i> = (RS &minus; <i>&mu;<sub>RS</sub></i>) / <i>&sigma;<sub>RS</sub></i> &gt; 1.5<i>&sigma;</i>
    </div>

    <h3>4. Risk-Adjusted Allocation Sizing</h3>
    <p>Surviving candidates are passed to a portfolio optimization engine. Capital allocation is scaled proportionally to its generated Alpha density, while being heavily penalized by systematic market risk exposure (Beta variance profile).</p>

    <h3>5. Dynamic Trailing Drawdown Controls</h3>
    <p>Risk management is asset-agnostic and volatility-adaptive. Instead of static percentage stops, a multi-period Average True Range (ATR) algorithm estimates active intraday expansion boundaries, mapping trailing stop losses to the equity's natural noise floor:</p>
    <div class="math-block">
        True Range (TR) = max[(<i>H</i> &minus; <i>L</i>), |<i>H</i> &minus; <i>C<sub>prev</sub></i>|, |<i>L</i> &minus; <i>C<sub>prev</sub></i>|]
        <br>
        Stop Level = Close &minus; (2 &times; ATR<sub>14</sub>)
    </div>

    <hr>

    <h2>🛠️ Tech Stack & Optimization Engineering</h2>
    <ul>
        <li><strong>Backend Mathematical Engine:</strong> Python 3.13, Pandas, NumPy, yfinance.</li>
        <li><strong>Server Architecture:</strong> FastAPI running asynchronous background workers (<code>BackgroundTasks</code>) via Uvicorn.</li>
        <li><strong>Web Caching:</strong> High-speed Time-to-Live (TTL) server-side cache window set to 30 minutes (1800 seconds) via dynamic file descriptor modification detection (<code>os.path.getmtime</code>).</li>
        <li><strong>Frontend Dashboard:</strong> Vanilla HTML5, Vanilla JavaScript, CSS custom variables (Dark Slate Fintech Theme).</li>
        <li><strong>Data Serialization & Portability:</strong> Native Client-side CSV parser processing data chunks straight into dynamic system <code>Blob</code> structures for direct download.</li>
    </ul>

    <hr>

    <h2>🚀 Installation & Local Deployment</h2>

    <h3>1. Backend Initialization</h3>
    <p>Ensure your directory contains a verified list of active exchange assets inside <code>Symbols_NSE.txt</code>.</p>
<pre><code># Clone the repository
git clone https://github.com/your-username/AURA-Quant-Pipeline.git
cd AURA-Quant-Pipeline/Backend

# Install required dependencies
pip install -r requirements.txt

# Launch the FastAPI production server
uvicorn api:app --reload</code></pre>

    <h3>2. Frontend Interface Mount</h3>
    <p>Since the UI is built utilizing native, optimized browser APIs, you don't need any complex compilation scripts or heavy Node module overhead:</p>
    <ul>
        <li>Open the <code>Frontend/</code> folder.</li>
        <li>Launch <code>index.html</code> via VS Code's <strong>Live Server</strong> plugin or click directly on the layout file.</li>
        <li>Click <strong>Deploy Live Scanner</strong> to kick off background market calculations.</li>
    </ul>

    <hr>

    <h2>💾 System Snapshot Sample Output</h2>
<pre><code>{
  "status": "success",
  "data": [
    {
      "Ticker": "HALEOSLABS.NS",
      "Close_Price": 1556.50,
      "Alpha": 0.00457,
      "Beta": 0.29,
      "Log_RS": 0.0804,
      "Alpha_Weight_%": 100.00,
      "Beta_Weight_%": 100.00,
      "Stop_Loss": 1383.62
    }
  ]
}</code></pre>

    <div class="footer">
        Developed by <strong>Manit Arora</strong> – Focused on Algorithmic Execution, Portfolio Sizing Strategy, and Quantitative Systems Architecture.
    </div>

</body>
</html>
