"""
Standalone test for myrtpos.com reorder_custom2.fwx
Tests ONLY: login -> navigate -> generate -> detect data -> export -> download
Run this independently to debug without waiting for full T-Mobile scraper.

Usage:
    python test_rtpos.py

Credentials are hardcoded below for testing. Remove after confirming it works.
"""

import os
import time
import logging
from glob import glob
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# ── CONFIG ────────────────────────────────────────────────────────────────────
REPORT_USER_ID  = "adil.iot"
REPORT_PASSWORD = "Batman786!"
DOWNLOAD_DIR    = os.path.join(os.getcwd(), "test_downloads")
LOG_FILE        = "test_rtpos.log"
# ──────────────────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)


def make_download_dir():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    return os.path.abspath(DOWNLOAD_DIR)


def init_driver():
    dl_dir = make_download_dir()

    is_ci = os.getenv("CI") == "true" or os.getenv("GITHUB_ACTIONS") == "true" or not os.environ.get("DISPLAY")

    prefs = {
        "download.default_directory": dl_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }

    # Try undetected_chromedriver first, fall back to plain Selenium
    try:
        import undetected_chromedriver as uc
        opts = uc.ChromeOptions()
        if is_ci:
            opts.add_argument("--headless=new")
            opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-gpu")
        opts.add_experimental_option("prefs", prefs)
        driver = uc.Chrome(options=opts)
        log.info("Undetected Chrome initialized")
    except Exception as e:
        log.warning(f"Undetected Chrome failed ({e}), falling back to Selenium")
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        opts = Options()
        if is_ci:
            opts.add_argument("--headless=new")
            opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-gpu")
        opts.add_experimental_option("prefs", prefs)
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        driver = webdriver.Chrome(options=opts)
        log.info("Selenium Chrome initialized")

    if is_ci:
        try:
            driver.execute_cdp_cmd("Page.setDownloadBehavior", {
                "behavior": "allow",
                "downloadPath": dl_dir
            })
            log.info(f"CDP download path set: {dl_dir}")
        except Exception as cdp_err:
            log.warning(f"CDP set failed (non-fatal): {cdp_err}")

    driver.set_page_load_timeout(120)
    driver.implicitly_wait(10)
    return driver


def wait_for_element(driver, xpath, timeout=15):
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
    except TimeoutException:
        log.warning(f"Timeout waiting for: {xpath}")
        return None


def wait_for_download(dl_dir, timeout=120):
    log.info(f"Waiting for download in: {dl_dir}")
    end = time.time() + timeout
    while time.time() < end:
        partials = glob(os.path.join(dl_dir, "*.crdownload")) + glob(os.path.join(dl_dir, "*.tmp"))
        if partials:
            time.sleep(2)
            continue
        xlsxs = sorted(glob(os.path.join(dl_dir, "*.xlsx")), key=os.path.getmtime, reverse=True)
        if xlsxs and os.path.getsize(xlsxs[0]) > 0:
            log.info(f"Download complete: {xlsxs[0]} ({os.path.getsize(xlsxs[0])} bytes)")
            return xlsxs[0]
        time.sleep(2)
    log.error(f"Download timed out. Files in dir: {os.listdir(dl_dir)}")
    return None


def take_screenshot(driver, name):
    try:
        path = os.path.join(DOWNLOAD_DIR, f"{name}_{datetime.now().strftime('%H%M%S')}.png")
        driver.save_screenshot(path)
        log.info(f"Screenshot saved: {path}")
    except Exception as e:
        log.warning(f"Screenshot failed: {e}")


def run_test():
    log.info("=" * 60)
    log.info("TEST: myrtpos reorder_custom2.fwx")
    log.info("=" * 60)

    driver = init_driver()

    try:
        # ── STEP 1: Login ──────────────────────────────────────────
        log.info("STEP 1: Navigating to myrtpos login page...")
        driver.get("https://www.myrtpos.com/newbdi/index.fwx")
        time.sleep(4)
        take_screenshot(driver, "01_login_page")

        user_field = wait_for_element(driver, '//input[@name="secUserID"]')
        pass_field = wait_for_element(driver, '//input[@name="secPassword"]')
        login_btn  = wait_for_element(driver, '//input[@value="Login"]')

        if not user_field or not pass_field or not login_btn:
            log.error("Login form elements not found - check screenshot")
            return False

        user_field.clear()
        user_field.send_keys(REPORT_USER_ID)
        pass_field.clear()
        pass_field.send_keys(REPORT_PASSWORD)
        login_btn.click()
        time.sleep(4)
        take_screenshot(driver, "02_after_login")
        log.info("Login submitted")

        # ── STEP 2: Navigate to reorder_custom2 ───────────────────
        log.info("STEP 2: Navigating directly to reorder_custom2.fwx...")
        driver.get("https://www.myrtpos.com/newbdi/reorder_custom2.fwx")
        time.sleep(5)
        take_screenshot(driver, "03_reorder_page")
        log.info(f"Page title: {driver.title}")
        log.info(f"Current URL: {driver.current_url}")

        # ── STEP 3: Set days field ─────────────────────────────────
        log.info("STEP 3: Looking for Days field...")
        days_field = wait_for_element(driver, '//input[@name="frmDays"]', timeout=10)
        if days_field:
            days_field.click()
            days_field.clear()
            days_field.send_keys("7")
            log.info("Days set to 7")
        else:
            log.warning("Days field not found - may not be needed on new page")

        # ── STEP 4: Click Generate ─────────────────────────────────
        log.info("STEP 4: Looking for Generate button...")
        generate_btn = wait_for_element(driver, '//span[contains(text(),"Generate")]', timeout=10)
        if not generate_btn:
            generate_btn = wait_for_element(driver, '//*[contains(text(),"Generate")]', timeout=5)

        if not generate_btn:
            take_screenshot(driver, "04_no_generate_btn")
            log.error("Generate button NOT found - check screenshot 04")
            # Log all visible buttons to help debug
            buttons = driver.find_elements(By.XPATH, '//button | //input[@type="button"] | //input[@type="submit"] | //span')
            log.info(f"Found {len(buttons)} button-like elements on page")
            for b in buttons[:20]:
                try:
                    txt = b.text.strip()
                    if txt:
                        log.info(f"  Element: <{b.tag_name}> text='{txt}'")
                except Exception:
                    pass
            return False

        log.info("Clicking Generate...")
        try:
            generate_btn.click()
        except Exception:
            driver.execute_script("arguments[0].click();", generate_btn)

        take_screenshot(driver, "05_after_generate")

        # ── STEP 5: Poll for data ──────────────────────────────────
        log.info("STEP 5: Waiting for report data to appear...")
        max_wait = 60  # only wait 60s in test - it loads in ~5s now
        poll = 2
        elapsed = 0

        while elapsed < max_wait:
            # Check for data rows using multiple possible selectors
            selectors = [
                '//tr[contains(@class,"dx-row dx-data-row")]',
                '//td[contains(@class,"dx-cell")]',
                '//div[contains(@class,"dx-datagrid-rowsview")]//tr',
                '//table//tr[position()>1]',
            ]
            row_count = 0
            for sel in selectors:
                try:
                    rows = driver.find_elements(By.XPATH, sel)
                    if rows:
                        row_count = len(rows)
                        log.info(f"  Found {row_count} rows using selector: {sel}")
                        break
                except Exception:
                    pass

            if row_count > 0:
                log.info(f"Data detected after {elapsed}s - {row_count} rows found")
                take_screenshot(driver, "06_data_loaded")
                break

            if elapsed % 10 == 0:
                log.info(f"  Still waiting... {elapsed}s elapsed")
                take_screenshot(driver, f"06_waiting_{elapsed}s")

            time.sleep(poll)
            elapsed += poll
        else:
            log.error("No data rows detected after 60 seconds")
            take_screenshot(driver, "06_timeout_no_data")
            # Dump page source snippet for debugging
            try:
                src = driver.page_source[:3000]
                log.info(f"Page source snippet:\n{src}")
            except Exception:
                pass
            return False

        # ── STEP 6: Find and click export button ──────────────────
        log.info("STEP 6: Looking for Excel export button...")
        export_selectors = [
            '//i[@class="dx-icon dx-icon-export-excel-button"]',
            '//*[contains(@class,"dx-icon-export-excel-button")]',
            '//*[contains(@title,"Export") or contains(@aria-label,"Export")]',
        ]

        export_btn = None
        for sel in export_selectors:
            try:
                btns = driver.find_elements(By.XPATH, sel)
                visible = [b for b in btns if b.is_displayed()]
                if visible:
                    export_btn = visible[0]
                    log.info(f"Export button found using: {sel}")
                    break
            except Exception:
                pass

        if not export_btn:
            take_screenshot(driver, "07_no_export_btn")
            log.error("Export button NOT found - check screenshot 07")
            # Log all icons on the page
            icons = driver.find_elements(By.XPATH, '//i | //*[contains(@class,"dx-icon")]')
            log.info(f"Icons on page: {len(icons)}")
            for ic in icons[:30]:
                try:
                    cls = ic.get_attribute("class")
                    if cls:
                        log.info(f"  icon class: '{cls}'")
                except Exception:
                    pass
            return False

        take_screenshot(driver, "07_export_btn_found")
        log.info("Clicking export button...")
        try:
            export_btn.click()
        except Exception:
            driver.execute_script("arguments[0].click();", export_btn)

        time.sleep(3)

        # ── STEP 7: Wait for download ──────────────────────────────
        log.info("STEP 7: Waiting for file download...")
        dl_dir = make_download_dir()
        result = wait_for_download(dl_dir)

        if result:
            log.info(f"SUCCESS! File downloaded: {result}")
            take_screenshot(driver, "08_success")
            return True
        else:
            log.error("Download did not complete")
            take_screenshot(driver, "08_download_failed")
            return False

    except Exception as e:
        log.error(f"Unexpected error: {e}")
        import traceback
        log.error(traceback.format_exc())
        take_screenshot(driver, "error")
        return False

    finally:
        driver.quit()
        log.info("Browser closed")


if __name__ == "__main__":
    success = run_test()
    log.info("=" * 60)
    log.info(f"TEST RESULT: {'PASSED' if success else 'FAILED'}")
    log.info("=" * 60)
    import sys
    sys.exit(0 if success else 1)
