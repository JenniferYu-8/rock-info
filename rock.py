import requests
from bs4 import BeautifulSoup
import csv
import json

# Fetch the main webpage
url = 'https://www.last.fm/tag/rock/artists'
response = requests.get(url)

# Parse the content with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Extract artist names and number of listeners
artists = soup.select('.big-artist-list-title a')
num_listeners = soup.select('.big-artist-list-listeners')
listeners_text = [listener.get_text(strip=True)[0:-9] for listener in num_listeners]

# Create a list to hold all artist information for JSON
artists_info = []

# Create or open a CSV file for writing
with open('artists_info.csv', mode='w', newline='', encoding='utf-8') as csvfile:
    # Define the CSV writer and the column headers
    writer = csv.writer(csvfile)
    writer.writerow(['Artist', 'Listeners', 'Years Active', 'Members', 'URL'])  # Write headers

    # Loop over artists and extract additional info from their pages
    for artist, listeners in zip(artists, listeners_text):
        artist_name = artist.get_text(strip=True)
        artist_url = artist['href']
        
        # Make sure the URL is absolute (if it's relative, append the base URL)
        if not artist_url.startswith('http'):
            artist_url = 'https://www.last.fm' + artist_url

        # Print basic info
        print(f"Artist: {artist_name}")
        print(f"Listeners: {listeners}")
        
        # Visit the artist's page to extract more information
        artist_response = requests.get(artist_url)
        artist_soup = BeautifulSoup(artist_response.content, 'html.parser')
        
        # Extract "Years Active" information
        years_active = None
        detail_labels = artist_soup.find_all('dt')
        for label in detail_labels:
            if 'Years Active' in label.get_text():
                years_active = label.find_next_sibling('dd').get_text(strip=True)
                break
        if years_active:
            print(f"Years Active: {years_active}")
        else:
            years_active = "Not found"  # Handle case when not found
            print("Years Active info not found.")

        # Modify URL to visit the artist's wiki page
        wiki_url = artist_url + '/+wiki'
        
        # Visit the artist's wiki page to extract more information
        wiki_response = requests.get(wiki_url)
        wiki_soup = BeautifulSoup(wiki_response.content, 'html.parser')

        # Extract "Members" information
        members = None

        # Find the <h4> tag with "Members" text
        members_header = wiki_soup.find('h4', string='Members')

        if members_header:
            # Get the next sibling which should be the <ul> with members
            members_list = members_header.find_next_sibling('ul')
            
            if members_list:
                # Extract each member and ensure there's a space before any '('
                members = [member.get_text(strip=True).replace("(", " (") for member in members_list.find_all('li')]

        if members:
            # Join members into a single string, each member separated by a comma
            members_str = ", ".join(members)
            print("Members:", members_str)
        else:
            members_str = "Not found"
            print("Members info not found.")


        print(f"URL: {artist_url}")

        # Write artist information to CSV
        writer.writerow([artist_name, listeners, years_active, members_str, artist_url])  # Write a row

        # Prepare artist information for JSON
        artist_data = {
            'Artist': artist_name,
            'Listeners': listeners,
            'Years Active': years_active,
            'Members': members_str,
            'URL': artist_url
        }
        artists_info.append(artist_data)  # Add to the list

        print("-" * 40)

# Write the list of artist information to a JSON file
with open('artists_info.json', mode='w', encoding='utf-8') as jsonfile:
    json.dump(artists_info, jsonfile, indent=4, ensure_ascii=False)  # Write JSON with indentation

print("Data has been written to artists_info.csv and artists_info.json.")






