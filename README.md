# AURA-Quant-Pipeline 📊🏦
### Automated Relative Strength, Alpha-Beta Estimation & Risk Sizing Engine

[![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Frontend](https://img.shields.io/badge/frontend-Vanilla%20JS%20%2F%20CSS-orange.svg)](https://developer.mozilla.org/en-US/)

An automated end-to-end quantitative trading pipeline designed to identify, rank, and dynamically allocate capital to equities showing structurally significant momentum. The engine streams tick data across the Nifty universe, separates market tailwinds from stock-specific skill using rolling OLS regressions, filters statistical noise via Z-scores, and calculates execution risk metrics in a decoupled web architecture.

---

## 🏢 System Architecture

The pipeline decouples resource-heavy mathematical computations from the client network layer to bypass web timeout limits when processing large equity universes.

```text
[ Raw Market Ingestion (yfinance) ] 
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
[ Vanilla CSS/JS Dashboard (UI) ] ──► [ Client CSV Export Engine ]
```
<h2>🧪 Core Quantitative Methodology</h2>

<h3>1. Data Ingestion &amp; Additive Continuity</h3>
<p>Raw Open-High-Low-Close-Volume (OHLCV) datasets are ingested sequentially. To eliminate compounding scale asymmetry inherent in standard arithmetic percentage changes, returns are transformed into logarithmic time-series:</p>
$$r_t = \ln\left(\frac{P_t}{P_{t-1}}\right)$$

<h3>2. Idiosyncratic Alpha vs. Beta Systematic Separation</h3>
<p>To ensure the model captures genuine momentum rather than broader market buoyancy, the script evaluates a rolling linear regression model of the asset against the benchmark index ($^NSEI$):</p>
$$R_{\text{stock}} = \alpha + \beta R_{\text{Nifty}} + \epsilon$$
<ul>
  <li><strong>Beta ($\beta$):</strong> Represents systematic risk sensitivity (covariance of asset and market divided by market variance).</li>
  <li><strong>Alpha ($\alpha$):</strong> Represents true, isolated manager/asset outperformance independent of index behavior.</li>
</ul>

<h3>3. Statistical Significance Gating</h3>
<p>Relative Strength (Log RS) is tracked as a linear difference of cumulative logarithmic distributions. To pass the core filter, an asset's Log RS must deviate from its historical rolling mean ($\mu$) by a minimum standard deviation threshold ($\sigma$), eliminating short-term noise:</p>
$$Z = \frac{\text{RS} - \mu_{\text{RS}}}{\sigma_{\text{RS}}} > 1.5\sigma$$

<h3>4. Risk-Adjusted Allocation Sizing</h3>
<p>Surviving candidates are passed to a portfolio optimization engine. Capital allocation is scaled proportionally to its generated Alpha density, while being heavily penalized by systematic market risk exposure (Beta variance profile).</p>

<h3>5. Dynamic Trailing Drawdown Controls</h3>
<p>Risk management is asset-agnostic and volatility-adaptive. Instead of static percentage stops, a multi-period Average True Range (ATR) algorithm estimates active intraday expansion boundaries, mapping trailing stop losses to the equity's natural noise floor:</p>
$$\text{True Range (TR)} = \max\left[(H - L), |H - C_{\text{prev}}|, |L - C_{\text{prev}}|\right]$$
$$\text{Stop Level} = \text{Close} - (2 \times \text{ATR}_{14})$$

<hr />

<h2>🛠️ Tech Stack &amp; Optimization Engineering</h2>
<ul>
  <li><strong>Backend Mathematical Engine:</strong> Python 3.13, Pandas, NumPy, yfinance.</li>
  <li><strong>Server Architecture:</strong> FastAPI running asynchronous background workers (<code>BackgroundTasks</code>) via Uvicorn.</li>
  <li><strong>Web Caching:</strong> High-speed Time-to-Live (TTL) server-side cache window set to 30 minutes (1800 seconds) via dynamic file descriptor modification detection (<code>os.path.getmtime</code>).</li>
  <li><strong>Frontend Dashboard:</strong> Vanilla HTML5, Vanilla JavaScript, CSS custom variables (Dark Slate Fintech Theme).</li>
  <li><strong>Data Serialization &amp; Portability:</strong> Native Client-side CSV parser processing data chunks straight into dynamic system Blob structures for direct download.</li>
</ul>

<hr />

<h2>🚀 Installation &amp; Local Deployment</h2>

<h3>1. Backend Initialization</h3>
<p>Ensure your directory contains a verified list of active exchange assets inside <code>Symbols_NSE.txt</code>.</p>

<pre><code class="language-bash"># Clone the repository
git clone https://github.com/your-username/AURA-Quant-Pipeline.git
cd AURA-Quant-Pipeline/Backend

# Install required dependencies
pip install -r requirements.txt

# Launch the FastAPI production server
uvicorn api:app --reload</code></pre>

