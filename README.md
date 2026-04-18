# 🛍️ Streamlit Myntra Scraper

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An **ultra-fast**, interactive web application to scrape product data from Myntra.com using Selenium, visualize insights, and export results as CSV.

---

## ✨ Features

- **⚡ Ultra‑Fast Scraping** – Collects data directly from search result pages (no per‑product page visits) – up to **2000 products** in seconds.
- **📊 Interactive Visualizations** – Choose from bar charts, pie charts, line plots, and price histograms.
- **📥 One‑Click CSV Export** – Download scraped data for further analysis.
- **🎨 Modern UI** – Gradient header, hover animations, and responsive layout.
- **📈 Real‑time Progress** – Live progress bar and status updates.
- **🔍 Smart Data Cleaning** – Automatically converts `1.2k` ratings → `1200`, handles missing values.
- **🚫 No Deprecation Warnings** – Fully compatible with latest Streamlit (uses `width='stretch'`).

---

## 🛠️ Technologies Used

| Technology                                                              | Purpose                                 |
|-------------------------------------------------------------------------|-----------------------------------------|
| [Streamlit](https://streamlit.io/)                                      | Frontend UI & app framework             |
| [Selenium](https://www.selenium.dev/)                                   | Web automation for dynamic content      |
| [WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager) | Automatic ChromeDriver management       |
| [Pandas](https://pandas.pydata.org/)                                    | Data manipulation & cleaning            |
| [Plotly Express](https://plotly.com/python/plotly-express/)             | Interactive charts & graphs             |
| [Requests](https://docs.python-requests.org/)                           | HTTP handling (indirectly via Selenium) |

---

## 📋 Scraped Data Fields

| Column         | Description                                 |
|----------------|---------------------------------------------|
| `product_type` | Name of the product (e.g., "Kurta for Men") |
| `brand`        | Brand name (e.g., "Wrogn", "US Polo Assn.") |
| `price`        | Price in Indian Rupees (integer)            |
| `rating`       | Average rating (float, 0–5)                 |
| `total_rating` | Number of user ratings (cleaned integer)    |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** installed
- **Google Chrome** browser (latest version)
- **pip** package manager

### Installation

1. **Clone the repository** (or download the `myntra_scraper.py` file)
   ```bash
   git clone https://github.com/abuawaish/streamlit-myntra-scraper.git
   cd streamlit-myntra-scraper
   ```

2. **Install required packages**
    ```bash
    pip install streamlit pandas selenium webdriver-manager plotly
    ```

3. **Run the app**
    ```bash
   streamlit run myntra_scraper.py
   ```

4. **Open your browser at http://localhost:8501**

### 🎮 How to Use

1. Enter a product keyword – e.g., `"kurta for men"`, `"shirts"`, `"sneakers"`
2. Set the number of products – 5 to 2000 (depending on search results)
3. Click `"Start Scraping"` – Watch the progress bar fill up.
4. Explore the results:
   - View the data table
   - Check key metrics (avg price, avg rating, total reviews)
   - Switch between chart types (Bar / Pie / Line)
5. Download CSV – Save the data for offline analysis.
6. Search again – Use the button to start a new search.

### 📊 Visualization Options


| Chart Type   | What it shows                              |
|--------------|--------------------------------------------|
| `Bar Chart`  | Top 10 brands by number of products        |
| `Pie Chart`  | Distribution of ratings (Poor → Excellent) |
| `price`      | Price in Indian Rupees (integer)           |
| `Line Chart` | Average price vs. product rating           |
| `Histogram`  | Price range distribution                   |

- **All charts are interactive – hover, zoom, pan.**

### 🧠 How It Works (Technical Overview)

- Headless Chrome launches and navigates to Myntra.
- Search keyword is entered and submitted.
- Product elements are extracted from the search results page (not individual product pages).
- Pagination automatically clicks `"Next"` until the requested number of products is collected.
- Data cleaning:
  - `"1.2k"` → `1200` (total ratings)
  - `"No Rating"` → 0.0
  - Price stripped of `"Rs"` and `commas` → integer.

- Results are displayed in a Streamlit data table and visualized with Plotly.
- CSV is generated on‑the‑fly for download.

**Why is it fast?**
- Traditional scrapers visit each product's detail page (slow). This app extracts all needed info from the search result cards, making it ~10x faster.

### ⚠️ Important Notes & Ethics

- `Respect robots.txt` – Myntra allows indexing of product pages. However, excessive requests may get your IP temporarily blocked.
- `Use responsibly` – This tool is for educational and personal use only. Do not use for commercial data harvesting without permission.
- `Rate limiting` – The code includes time.sleep() delays to avoid overloading the server.
- `Headless mode` – Runs in background; you won't see a browser window.

### 🐛 Troubleshooting


| Issue                                                                | Solution                                                                     |
|----------------------------------------------------------------------|------------------------------------------------------------------------------|
| `WebDriverException: Message: unknown error: Chrome failed to start` | Ensure Google Chrome is installed and up‑to‑date.                            |
| `No products found`                                                  | Try a more specific keyword (e.g., "men cotton shirts" instead of "shirts"). |
| `TimeoutException`                                                   | 	Increase the wait times in the code (or check your internet connection).    |
| `Line Chart`                                                         | Average price vs. product rating                                             |
| `DeprecationWarning`                                                 | Already fixed – use the code provided above.                                 |


### 📁 Project Structure

```text
streamlit-myntra-scraper/
├── myntra_scraper.py          # Main application
├── requirements.txt           # Dependencies
├── .gitignore                 # exclude files or directories 
├──  package.txt               # System Dependencies
└── README.md                  # This file
```

### 📦 requirements.txt

**Create a `requirements.txt` file with:**

```text
streamlit>=1.28.0
pandas>=2.0.0
selenium>=4.15.0
webdriver-manager>=4.0.0
plotly>=5.17.0
```
**Install all at once:**

```bash
pip install -r requirements.txt
```

### 🤝 Contributing

1. Contributions are welcome! Please open an issue or submit a pull request.
2. Fork the repository
3. Create a feature branch (git checkout -b feature/amazing-feature)
4. Commit your changes (git commit -m 'Add some amazing feature')
5. Push to the branch (git push origin feature/amazing-feature)
6. Open a Pull Request

### 📄 License
- **Distributed under the MIT License. See LICENSE file for more information.**

### 🙏 Acknowledgements

- Myntra for providing product data (we love shopping there!)
- Streamlit team for the amazing framework
- Selenium & WebDriver Manager contributors

### 📬 Contact
- Abu Awaish – [LinkedIn](https://www.linkedin.com/in/abu-awaish-a6523b258/)

### Happy Scraping! 🛍️📊