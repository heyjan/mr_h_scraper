import requests
from bs4 import BeautifulSoup
import csv
import time


def scrape_mr_hanf(page_limit=None):
    base_url = "https://mr-hanf.de/samen-shop/alle-hanfsamen/"
    page = 1
    elements_count = 0

    # Open the CSV file for writing
    with open('full_data.csv', mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'THC']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        while True:
            url = base_url + f"?page={page}"
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to fetch page {page}. Status code: {response.status_code}")
                break

            soup = BeautifulSoup(response.content, 'html.parser')
            product_rows = soup.find_all('div', class_='row product-image')

            if not product_rows:
                print("No more product rows found. Exiting.")
                break

            for row in product_rows:
                # Get strain name
                strain_name = row.find('h2', class_='lr_title').text.strip()

                # Get THC percentage if available
                thc_info = row.find('td', text='THC')
                if thc_info:
                    thc_percentage = thc_info.find_next_sibling('td').text.strip()
                else:
                    thc_percentage = "N/A"
                    continue  # Skip to the next product if THC info is not available

                print(f"Strain: {strain_name}, THC: {thc_percentage}")

                # Write data to CSV
                writer.writerow({'Name': strain_name, 'THC': thc_percentage})

                # Increment elements count
                elements_count += 1

                # Check if we reached the limit of 50 elements
                if elements_count >= 50:
                    print("Reached element limit. Pausing for 30 seconds.")
                    time.sleep(30)
                    elements_count = 0

            if page_limit and page >= page_limit:
                print(f"Reached page limit of {page_limit}. Exiting.")
                break

            page += 1


# To scrape all pages, call the function without any arguments
scrape_mr_hanf()

# To scrape a specific number of pages, specify the page limit
# scrape_mr_hanf(page_limit=5)
