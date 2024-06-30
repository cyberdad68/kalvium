import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape and parse HTML content
def scrape_election_results(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

# URL 1: Main page with links to state-wise results
url_main = "https://results.eci.gov.in/"
soup_main = scrape_election_results(url_main)

# Extracting state-wise result URLs
state_links = {}
state_items = soup_main.find_all('div', class_='state-item')

for item in state_items:
    state_name = item.find('h2').text.strip()
    state_url = item.find('a')['href']
    state_links[state_name] = state_url

# URL 2: Andhra Pradesh state results
url_andhra_pradesh = "https://results.eci.gov.in/AcResultGenJune2024/index.htm"
soup_andhra_pradesh = scrape_election_results(url_andhra_pradesh)

# Extract number of assembly constituencies
ac_count_ap = soup_andhra_pradesh.find('ul').find_all('span')[1].text.strip()

# Extract top five parties and their results for Andhra Pradesh
party_results_ap = []
party_boxes_ap = soup_andhra_pradesh.find_all('div', class_='pr-row')

for box in party_boxes_ap:
    party_name = box.find('div').text.strip()
    seats_won = box.find_all('div')[1].text.strip()
    party_results_ap.append({'State': 'Andhra Pradesh', 'Party': party_name, 'Seats Won': seats_won})

# URL 3: Odisha state results
url_odisha = "https://results.eci.gov.in/AcResultGenJune2024/index.htm" 
soup_odisha = scrape_election_results(url_odisha)

# Extract number of assembly constituencies (if available)
ac_count_odisha = soup_odisha.find('ul').find_all('span')[1].text.strip()

# Extract top five parties and their results for Odisha (example data)
party_results_odisha = []
party_boxes_odisha = soup_odisha.find_all('div', class_='pr-row')

for box in party_boxes_odisha:
    party_name = box.find('div').text.strip()
    seats_won = box.find_all('div')[1].text.strip()
    party_results_odisha.append({'State': 'Odisha', 'Party': party_name, 'Seats Won': seats_won})

# Create DataFrames for Andhra Pradesh and Odisha party-wise results
df_party_results_ap_odisha = pd.DataFrame(party_results_ap + party_results_odisha)

# URL 3: Bye elections results
url_bye_elections = "https://results.eci.gov.in/AcResultByeJune2024/"
soup_bye_elections = scrape_election_results(url_bye_elections)

# Extract results for bye elections
bye_elections_results = []
bye_elections_boxes = soup_bye_elections.find_all('div', class_='const-box')

for box in bye_elections_boxes:
    const_name = box.find('h3').text.strip()
    state_name = box.find('h4').text.strip()
    winner_name = box.find('h5').text.strip()
    party_name = box.find_all('h6')[0].text.strip()
    bye_elections_results.append({'Constituency': const_name, 'State': state_name, 'Winner': winner_name, 'Party': party_name})

# Create DataFrame for bye elections results
df_bye_elections_results = pd.DataFrame(bye_elections_results)

# URL 4: Arunachal Pradesh and Sikkim state results
url_arunachal_sikkim = "https://results.eci.gov.in/AcResultGen2ndJune2024/index.htm"
soup_arunachal_sikkim = scrape_election_results(url_arunachal_sikkim)

# Extracting data for Arunachal Pradesh
ap_state_box = soup_arunachal_sikkim.find('h2', text='Arunachal Pradesh').parent
ap_ac_count = ap_state_box.find('li').find_all('span')[1].text.strip()
ap_party_boxes = ap_state_box.find_all('div', class_='pr-row')

party_results_ap = []
for box in ap_party_boxes:
    party_name = box.find('div').text.strip()
    seats_won = box.find_all('div')[1].text.strip()
    party_results_ap.append({'State': 'Arunachal Pradesh', 'Party': party_name, 'Seats Won': seats_won})

# Extracting data for Sikkim
sikkim_state_box = soup_arunachal_sikkim.find('h2', text='Sikkim').parent
sikkim_ac_count = sikkim_state_box.find('li').find_all('span')[1].text.strip()
sikkim_party_boxes = sikkim_state_box.find_all('div', class_='pr-row')

party_results_sikkim = []
for box in sikkim_party_boxes:
    party_name = box.find('div').text.strip()
    seats_won = box.find_all('div')[1].text.strip()
    party_results_sikkim.append({'State': 'Sikkim', 'Party': party_name, 'Seats Won': seats_won})

# Create DataFrames for Arunachal Pradesh and Sikkim party-wise results
df_party_results_ap_sikkim = pd.DataFrame(party_results_ap + party_results_sikkim)

# Output DataFrames to CSV files
df_party_results_ap_odisha.to_csv('Andhra_Odisha_Party_Results.csv', index=False)
df_bye_elections_results.to_csv('Bye_Elections_Results.csv', index=False)
df_party_results_ap_sikkim.to_csv('Arunachal_Sikkim_Party_Results.csv', index=False)

print("CSV files saved successfully.")
