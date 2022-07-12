from bs4 import BeautifulSoup
import requests
import pandas as pd


def extract(page):
    """
    Extracts the data from the web URL
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }

    url = f"https://in.indeed.com/jobs?q=react%20js%20developer&start={page}"

    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup
    # return r.status_code


def transform(soup):
    divs = soup.find_all("div", class_="job_seen_beacon")
    print(f"📃 Number of Jobs on Page : {len(divs)}")

    for div in divs:
        title = div.find("a").text.strip()
        print(title)

        companyName = div.find("span", class_="companyName").text.strip()
        print(f"🏢 organization: {companyName}")
        try:
            temp = div.find("div", class_="metadata salary-snippet-container")
            salary = temp.find("div", class_="attribute_snippet").text.strip()
            print(f"💰 salary: {salary}")
        except:
            salary = ""
            print(f"💰 salary: {salary}")

        summary = div.find("div", class_="job-snippet").text.strip().replace("\n", "")
        print(summary)

        job = {
            "title": title,
            "company": companyName,
            "salary": salary,
            "summary": summary,
        }
        jobList.append(job)
    return


if __name__ == "__main__":
    jobList = []

    """
    the pagination is of 10 as of now on the website we are scrapping.
    """
    for i in range(0, 50, 10):
        s = extract(i)
        transform(s)
        print(len(jobList))
        print(f"👞 Jobs: \n {jobList}")

        df = pd.DataFrame(jobList)

        df.head()

        df.to_csv("react jobs.csv")
