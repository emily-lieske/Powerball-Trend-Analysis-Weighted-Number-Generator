import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

# Define the date range
start_date = datetime.date(2025, 1, 23)
end_date = datetime.date(2026, 1, 5)

dates = []
for day in range((end_date - start_date).days + 1):
    date = start_date + datetime.timedelta(days = day)
    new_date = str(date)
    dates.append(new_date)

# Initialize an empty list to store extracted data
data = []

# Loop through each date
for date in dates:

    # Send request and parse HTML
    url = f"https://www.powerball.com/draw-result?gc=powerball&date={date}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract estimated jackpot
    jackpot_result = ""
    jackpot = soup.find("div", {"class": "estimated-jackpot"})
    for item in jackpot:
        item_text = item.get_text()
        if "Jackpot" not in item_text and '\n' not in item_text:
            jackpot_result = item_text

    # Extract winning numbers
    draw_results = []
    draw_results_raw = soup.find("div", {"class": "d-flex col-auto flex-nowrap game-ball-group mx-auto"})
    for result in draw_results_raw:
        item = result.get_text()
        if item != '\n':
            draw_results.append(result.get_text())

    winning_date = soup.find("h5", {"class": "title-date"}).get_text()
    # print(winning_date)

    # Extract winners & prizes data
    table = soup.find("table", {"class": "winners-table"})
    rows = table.find_all("tr")
    for row in rows:
        powerball_num_winners = [str(num.text.strip()) for num in row.find_all("td", {"data-label": "Powerball Winners"})]
        powerball_prizes = [str(num.text.strip()) for num in row.find_all("td", {"data-label": "Powerball Prize"})]
        data.append({
            "date": winning_date,
            "jackpot": jackpot_result,
            "numbers": draw_results,
            "num_winners": powerball_num_winners,
            "prizes": powerball_prizes
        })
    # print(data)

# Store extracted data in a CSV file
pd.DataFrame(data).to_csv("~/Desktop/Since-Last-Jackpot-2024-to-2025-powerball_data_1-6.csv", index=False)