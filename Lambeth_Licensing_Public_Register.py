from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from selenium.common.exceptions import StaleElementReferenceException

# URL template for base search
base_url = "https://hmolicensing.lambeth.gov.uk/public-register"

# Set up Selenium WebDriver (using Chrome)
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Function to extract data from each href page
def extract_link_data(href):
    driver.get(href)
    time.sleep(3)  # Wait for the page to load

    # Extract title from the linked page
    try:
        title = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div/h1').text
    except:
        title = "N/A"

    # Extract License Type
    try:
        license_type = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div/div/p[1]/span').text
    except:
        license_type = "N/A"

    # Extract License Reference Number
    try:
        license_reference_number = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div/div/p[2]/span').text
    except:
        license_reference_number = "N/A"

    # Extract License Starting Date
    try:
        license_start_date = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div/div/p[4]/span').text
    except:
        license_start_date = "N/A"

    # Extract License Ending Date
    try:
        license_end_date = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div/div/p[5]/span').text
    except:
        license_end_date = "N/A"

    # Return all extracted data as a dictionary
    return {
        "Title": title,
        "License Type": license_type,
        "License Reference Number": license_reference_number,
        "License Starting Date": license_start_date,
        "License Ending Date": license_end_date
    }

def scrape_pages(start_page, end_page):
    data = []

    # Visit the base URL and search for 'SE5'
    driver.get(base_url)
    time.sleep(3)  # Wait for the page to load

    # Locate the search box and input 'SE5'
    search_box = driver.find_element(By.NAME, "search[query]")
    search_box.clear()
    search_box.send_keys("SE5")
    search_box.send_keys(Keys.RETURN)  # Press Enter to start the search
    time.sleep(3)  # Wait for search results to load

    for page in range(start_page, end_page + 1):
        print(f"Scraping Page {page}...")

        # Check if the page number exists in the URL or needs to be updated
        if page > 1:
            url = f"{base_url}?pagination%5Bpage%5D={page}&pagination%5Bsize%5D=15&search%5B_token%5D=8.AHDvA0kNcGeQfOCd6nPlmaRIkcE-L4zc-zrs-guGTMc.WROeVQRhSFGhHtXe3kCRz-Ms8PJMY9SZj02jq03JCbQ5SYlnLWE1JNoqjw&search%5Bquery%5D=SE5&search%5Brecaptcha%5D%5BrecaptchaV2%5D=&search%5Brecaptcha%5D%5BrecaptchaV3%5D=03AFcWeA4p0Hh_AkPdkiEsqf_cMSTiagnJ1J5-N44NycG_vuOdPXv_H2bLnkrDSDUa1Sq1BumzYlHdn6N2kO30zGLLaTkNLdQH_CZRjMGM3BzchQgQI-T4ZNblAgrIst7LXkrFesW-PWn1KEqU3DfChB32uF27Xit-rlXabbSTeGhF9JinCcKhiLh8r0_k5-YKbhQhf4Eh4-7bqt5CKjfmCcr28HDZMxRTpBbcjKNauqb8gYbb9hqMwRvK1FRa6bef8z78AlryIIInwq68tFTNC-NvIz7Drxnk3XKPRe1VopqeVg1Mj0PZ5zq8yzKqfdnHPNeD3as2M1MTUio7sUifFjeWrFSLgxCgW7PD95pnaeoG7LVLe8BHh57985WuTKnn16mVUGyc0Y9a2ObHYAkl6s122BLLb_FRq674wzWVZv-06PZYydTE5gAPdibTG2dbEEoD_h9K_bb7QDWH63eA7IDFIjlUVr2xaotzSiJA2PUGGmWhgzGF2R932PpQAvOgpx6tqQWr7JVw0IqkKOBantkQRmMqA8Pvq-h0GwuIhHUDgBCZ_22TOZutQmjT4dkjnZJEfYZMRl2P4PV4GPq0tVu7v7ws6z_HfVOz49fzjYxAY-ziGwHcZ-z0ob_ZMvwoHplVb9_3wsEw_kXKcXjx4eHmsT5uM58SI3pLDFIZP9Dm59JHPhuBePRC25ZgLCF5qt47ILK_e6QdE4gbZgOvf23g3vk0d001o1Cg5XEjc5BAwXY6_oCoN3JxB2scxeCCmqXrguSMT5oN1u6YHaAwe81FDIt8I3KmqOSdCEffsxYcj2qQLftI5n044NBeeHRhGVCVgSdiSxQ2GwbI2Z-ftcmaecYrCISyHtVYGZxeUiqQAOa0CT5bLg0"
            driver.get(url)
            time.sleep(3)  # Wait for page to load

        # Extract h2 tags (titles) and <p> tags (holder names)
        h2_tags = driver.find_elements(By.TAG_NAME, "h2")
        p_tags = driver.find_elements(By.XPATH, '//*[@id="main-content"]/div[2]/div/p')

        # Extract data for each entry on the page
        for i, h2 in enumerate(h2_tags):
            try:
                title = h2.text if h2.text else "N/A"
                holder_name = p_tags[i].text if i < len(p_tags) else "N/A"
                href = "N/A"
                
                # Try to find the link inside the h2 tag
                try:
                    link_element = h2.find_element(By.XPATH, './/a')
                    href = link_element.get_attribute("href")
                except:
                    pass

                # Extract link data from the next page (if exists)
                link_data = {"Title": "N/A", "License Type": "N/A", "License Reference Number": "N/A", 
                             "License Starting Date": "N/A", "License Ending Date": "N/A"}

                if href != "N/A":
                    link_data = extract_link_data(href)
                    driver.back()  # Go back to the search results page

                # Append the result to the data list
                data.append({
                    "S.No": len(data) + 1,
                    "Main Title": title,
                    "Holder Name": holder_name,
                    "Link": href,
                    **link_data
                })
            except StaleElementReferenceException:
                print(f"Stale element encountered on page {page}, retrying...")
                time.sleep(1)  # Pause for a moment and retry extracting the element
                h2_tags = driver.find_elements(By.TAG_NAME, "h2")
                p_tags = driver.find_elements(By.XPATH, '//*[@id="main-content"]/div[2]/div/p')

        print(f"Completed Page {page}")
    
    # Create a DataFrame and export to Excel
    df = pd.DataFrame(data)
    df.to_excel("extracted_data_multiple_pages.xlsx", index=False)
    print("Data has been written to extracted_data_e_pages.xlsx")

# Take user input for the range of pages
start_page = int(input("Enter the starting page number: "))
end_page = int(input("Enter the ending page number: "))

# Call the scrape_pages function with user input
scrape_pages(start_page=start_page, end_page=end_page)

# Close the browser after scraping
driver.quit()
