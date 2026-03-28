import bs4
import requests
import pandas
from datetime import datetime
import json

logDictionary = {
    "PROCESSES_STATUS": {
        "API_REQUEST": "",
        "HTML_PARSING": "",
        "GETTING_CARDS": "",
        "APPENDING_DATA": "",
    },
    "ROWS_INGESTED": 0,
    "ERRORS": [],
    "TIME": {"START_TIME": "", "END_TIME": ""},
    "TECH_USED": "Python",
}

jobsListData = {
    "JOB_TITLE": [],
    "COMPANY_NAME": [],
    "LOCATION": [],
    "APPLY_LINK": [],
    "LEARN_LINK": [],
    "POST_DATE": [],
    "RUN_DATE": [],
}


def getHtmlText(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        htmlText = response.text
        logDictionary["PROCESSES_STATUS"]["API_REQUEST"] = "PASSED"
        return htmlText
    except Exception as e:
        logDictionary["PROCESSES_STATUS"]["API_REQUEST"] = "FAILED"
        logDictionary["ERRORS"].append({"getHtmlText": str(e).strip()})


def createdSoupObject(htmlText: str) -> bs4.BeautifulSoup:
    try:
        soup = bs4.BeautifulSoup(htmlText, "html.parser")
        logDictionary["PROCESSES_STATUS"]["HTML_PARSING"] = "PASSED"
        return soup
    except Exception as e:
        logDictionary["PROCESSES_STATUS"]["HTML_PARSING"] = "FAILED"
        logDictionary["ERRORS"].append({"createdSoupObject": str(e).strip()})


def getAllCards(soup: bs4.BeautifulSoup) -> list:
    try:
        cardsList = soup.find_all("div", class_="card-content")
        logDictionary["PROCESSES_STATUS"]["GETTING_CARDS"] = "PASSED"
        return cardsList
    except Exception as e:
        logDictionary["PROCESSES_STATUS"]["GETTING_CARDS"] = "FAILED"
        logDictionary["ERRORS"].append({"getAllCards": str(e).strip()})


def appendHtmlDataToDict(cards: list) -> None:
    currentDateTime = datetime.now().isoformat()
    try:
        for card in cards:
            jobsListData["JOB_TITLE"].append(
                card.find("h2", class_="title is-5").text.strip()
            )
            jobsListData["COMPANY_NAME"].append(
                card.find("h3", class_="subtitle is-6 company").text.strip()
            )
            jobsListData["LOCATION"].append(
                card.find("p", class_="location").text.strip()
            )
            jobsListData["POST_DATE"].append(card.find("time").text.strip())
            jobsListData["RUN_DATE"].append(currentDateTime)
            for anchor in card.find_all("a"):
                if anchor.text.strip().lower() == "learn":
                    jobsListData["LEARN_LINK"].append(anchor.get("href").strip())
                elif anchor.text.lower() == "apply":
                    jobsListData["APPLY_LINK"].append(anchor.get("href").strip()) 
        logDictionary["PROCESSES_STATUS"]["APPENDING_DATA"] = "PASSED"
    except Exception as e:
        logDictionary["PROCESSES_STATUS"]["APPENDING_DATA"] = "FAILED"
        logDictionary["ERRORS"].append({"appendHtmlDataToDict": str(e).strip()})


def saveToCsv(jobsListData: dict) -> None:
    df = pandas.DataFrame(jobsListData)
    df.to_csv("data/job_listing_data.csv", index=False)
    logDictionary["ROWS_INGESTED"] = len(df)


def saveLogfile() -> None:
    with open("data/logs.json", "w") as j_file:
        json.dump(logDictionary, j_file, indent=4)


def main():

    logDictionary["TIME"]["START_TIME"] = datetime.now().isoformat()
    url = "https://realpython.github.io/fake-jobs/"

    htmlText = getHtmlText(url)
    soup = createdSoupObject(htmlText)
    cards = getAllCards(soup)

    appendHtmlDataToDict(cards)
    saveToCsv(jobsListData)
    logDictionary["TIME"]["END_TIME"] = datetime.now().isoformat()
    saveLogfile()


if __name__ == "__main__":
    main()
