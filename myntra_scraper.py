import streamlit as st
import pandas as pd
import re
import time
import plotly.express as px
import subprocess
import sys
from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, WebDriverException

# ---------- Page Configuration ----------
st.set_page_config(
    page_title="Myntra Scraper Pro",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- Custom CSS (same as before) ----------
st.markdown("""
<style>
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .main { animation: fadeIn 0.6s ease-out; }
    .header-container {
        background: linear-gradient(135deg, #ff3f6c 0%, #ff6b8b 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    .header-container:hover { transform: scale(1.01); }
    .header-container h1 { font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; }
    .stButton > button {
        background-color: #ff3f6c;
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #e6355c;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255,63,108,0.3);
    }
    .stDownloadButton > button {
        background-color: #28a745;
        border: none;
        transition: all 0.3s;
    }
    .stDownloadButton > button:hover { transform: translateY(-2px); background-color: #218838; }
    .dataframe thead tr th { background-color: #ff3f6c; color: white; }
    .stProgress > div > div { background-color: #ff3f6c; }
</style>
""", unsafe_allow_html=True)

# ---------- Session State ----------
if 'scraped_df' not in st.session_state:
    st.session_state.scraped_df = None
if 'search_performed' not in st.session_state:
    st.session_state.search_performed = False

# ---------- Robust Driver Setup with Error Logging ----------
def get_driver():
    """Configure and return a Chrome driver that works on Streamlit Cloud."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Explicit binary location (installed by chromium package)
    options.binary_location = "/usr/bin/chromium"
    
    # Use the system chromedriver (installed by chromium-driver)
    service = Service(executable_path="/usr/bin/chromedriver")
    
    try:
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except WebDriverException as e:
        error_msg = f"WebDriverException: {str(e)}"
        # Log to stderr (appears in Streamlit logs)
        print(error_msg, file=sys.stderr)
        # Also try to get Chromium version for debugging
        try:
            result = subprocess.run(["/usr/bin/chromium", "--version"], capture_output=True, text=True)
            print(f"Chromium version: {result.stdout.strip()}", file=sys.stderr)
            error_msg += f"\nChromium version: {result.stdout.strip()}"
        except Exception as ver_e:
            print(f"Could not get Chromium version: {ver_e}", file=sys.stderr)
        st.error(error_msg)
        raise  # Re-raise so the calling function knows it failed

# ---------- Fast Scraping Function ----------
def scrape_myntra_fast(keyword: str, limit: int) -> Optional[pd.DataFrame]:
    url = "https://www.myntra.com/"
    driver = None
    try:
        driver = get_driver()
        driver.get(url)
        
        # Search for the keyword
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'desktop-query'))
        )
        search_bar = search_box.find_element(By.CLASS_NAME, 'desktop-searchBar')
        search_bar.clear()
        search_bar.send_keys(keyword)
        search_button = search_box.find_element(By.CLASS_NAME, 'desktop-submit')
        search_button.click()
        
        # Wait for products to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'product-base'))
        )
        
        product_type_list = []
        brand_list = []
        price_list = []
        rating_list = []
        total_rating_list = []
        
        progress_bar = st.progress(0, text="Scraping products...")
        status_text = st.empty()
        
        collected = 0
        while collected < limit:
            product_data = driver.find_elements(By.CLASS_NAME, 'product-base')
            if not product_data:
                break
                
            for data in product_data:
                if collected >= limit:
                    break
                try:
                    prod_type = data.find_elements(By.CLASS_NAME, 'product-product')
                    product_type_list.append(prod_type[0].text if prod_type else "Unknown")
                    
                    brand_name = data.find_elements(By.CLASS_NAME, 'product-brand')
                    brand_list.append(brand_name[0].text if brand_name else "Unknown")
                    
                    prod_price = data.find_elements(By.CLASS_NAME, 'product-price')
                    if prod_price:
                        price_text = prod_price[0].text.replace('Rs', '').replace('.', '').strip()
                        price_numbers = re.findall(r'\d+', price_text)
                        price = int(price_numbers[0]) if price_numbers else 0
                    else:
                        price = 0
                    price_list.append(price)
                    
                    prod_rating = data.find_elements(By.CLASS_NAME, 'product-ratingsContainer')
                    rating = prod_rating[0].text.split('\n')[0] if prod_rating else "No Rating"
                    rating_list.append(rating)
                    
                    total_rate = data.find_elements(By.CLASS_NAME, 'product-ratingsCount')
                    if total_rate:
                        rate_text = total_rate[0].text.split('\n')
                        total_rating_list.append(rate_text[1] if len(rate_text) > 1 else "0")
                    else:
                        total_rating_list.append("0")
                    
                    collected += 1
                    progress_bar.progress(int(collected / limit * 100))
                    status_text.text(f"Collected {collected} of {limit} products...")
                    
                except StaleElementReferenceException:
                    continue
            
            if collected >= limit:
                break
                
            # Pagination: click next button
            try:
                next_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, 'pagination-next'))
                )
                driver.execute_script("arguments[0].scrollIntoView();", next_button)
                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(2)
            except TimeoutException:
                st.info("No more pages available.")
                break
        
        progress_bar.empty()
        status_text.empty()
        
        df = pd.DataFrame({
            'product_type': product_type_list,
            'brand': brand_list,
            'price': price_list,
            'rating': rating_list,
            'total_rating': total_rating_list
        })
        
        def convert_rating_count(s):
            s = str(s).lower().strip()
            if 'k' in s:
                num = float(s.replace('k', ''))
                return int(num * 1000)
            else:
                return int(s) if s.isdigit() else 0
        
        df['total_rating'] = df['total_rating'].apply(convert_rating_count)
        df['rating'] = df['rating'].apply(lambda x: float(x) if x.replace('.', '', 1).isdigit() else 0.0)
        
        return df
        
    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)
        st.error(f"Scraping error: {error_type}: {error_msg}")
        # Log full details to console (visible in Streamlit logs)
        print(f"Full exception: {error_type}: {error_msg}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return None
    finally:
        if driver:
            driver.quit()

# ---------- UI Layout ----------
st.markdown("""
<div class="header-container">
    <h1>🛍️ Myntra Product Scraper Pro</h1>
    <p>Ultra‑fast scraping from search results | Interactive insights & visualizations</p>
</div>
""", unsafe_allow_html=True)

with st.container():
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        keyword = st.text_input("🔍 Product Keyword", placeholder="e.g., kurta for men, shirts, shoes")
    with col2:
        limit = st.number_input("📊 Number of Products", min_value=5, max_value=2000, value=100, step=10)
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        search_clicked = st.button("🚀 Start Scraping", width='stretch')

if search_clicked and keyword:
    st.session_state.search_performed = True
    with st.spinner("Initializing scraper..."):
        df = scrape_myntra_fast(keyword.strip(), limit)
        st.session_state.scraped_df = df

# ---------- Results & Visualizations ----------
if st.session_state.search_performed and st.session_state.scraped_df is not None:
    df = st.session_state.scraped_df
    
    # Metrics
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📦 Total Products", len(df))
    with col2:
        avg_price = df['price'].mean()
        st.metric("💰 Average Price", f"₹{avg_price:,.0f}")
    with col3:
        avg_rating = df['rating'].mean()
        st.metric("⭐ Average Rating", f"{avg_rating:.2f}")
    with col4:
        total_reviews = df['total_rating'].sum()
        st.metric("🗣️ Total Reviews", f"{total_reviews:,}")
    
    st.markdown("---")
    st.subheader("📋 Scraped Data")
    st.dataframe(df, width='stretch', hide_index=True)
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", data=csv, file_name=f"myntra_{keyword}.csv", mime="text/csv", width='stretch')
    
    # Visualizations
    st.markdown("---")
    st.subheader("📊 Data Insights & Visualizations")
    
    plot_type = st.selectbox(
        "Select chart type",
        options=["Bar Chart (Top Brands)", "Pie Chart (Rating Distribution)", "Line Chart (Price vs Rating)"],
        index=0
    )
    
    if plot_type == "Bar Chart (Top Brands)":
        brand_counts = df['brand'].value_counts().head(10).reset_index()
        brand_counts.columns = ['Brand', 'Count']
        fig = px.bar(brand_counts, x='Brand', y='Count', title="Top 10 Brands by Product Count",
                     color='Count', color_continuous_scale='Viridis')
        fig.update_layout(showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig, width='stretch')
        
    elif plot_type == "Pie Chart (Rating Distribution)":
        def rating_category(r):
            if r == 0: return "No Rating"
            elif r < 2: return "Poor (0-2)"
            elif r < 3: return "Average (2-3)"
            elif r < 4: return "Good (3-4)"
            else: return "Excellent (4-5)"
        df['rating_cat'] = df['rating'].apply(rating_category)
        rating_counts = df['rating_cat'].value_counts().reset_index()
        rating_counts.columns = ['Rating Category', 'Count']
        fig = px.pie(rating_counts, values='Count', names='Rating Category',
                     title="Product Rating Distribution", hole=0.4,
                     color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, width='stretch')
        
    else:
        df['rating_rounded'] = df['rating'].round(1)
        price_by_rating = df.groupby('rating_rounded')['price'].mean().reset_index()
        fig = px.line(price_by_rating, x='rating_rounded', y='price',
                      title="Average Price vs Product Rating",
                      markers=True)
        fig.update_traces(line_color='#ff3f6c', marker_color='#ff3f6c')
        st.plotly_chart(fig, width='stretch')
    
    st.subheader("💰 Price Distribution")
    fig_hist = px.histogram(df, x='price', nbins=30, title="Price Range Distribution",
                            labels={'price': 'Price (₹)'}, color_discrete_sequence=['#ff3f6c'])
    fig_hist.update_layout(bargap=0.1)
    st.plotly_chart(fig_hist, width='stretch')
    
    if st.button("🔄 Search Again", width='stretch'):
        st.session_state.scraped_df = None
        st.session_state.search_performed = False
        st.rerun()
        
elif st.session_state.search_performed and st.session_state.scraped_df is None:
    st.info("💡 No data available. Please try a different keyword or adjust your parameters.")

st.markdown("---")
st.caption("⚠️ For educational purposes only. Please respect Myntra's robots.txt and terms of service.")