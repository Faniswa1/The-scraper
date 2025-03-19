import requests
from bs4 import BeautifulSoup

def find_free_funds():
    # Example URL, you need to update this with actual URLs and logic to find funds
    url = 'https://example.com/free-funds'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    funds = []
    for fund in soup.find_all('div', class_='fund'):
        amount = fund.find('span', class_='amount').text
        description = fund.find('span', class_='description').text
        funds.append({
            'amount': amount,
            'description': description
        })

    return funds
