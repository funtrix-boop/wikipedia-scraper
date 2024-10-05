# lets fucking go it works
from io import StringIO

import matplotlib.pyplot as plt
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


def main() -> None:
    # set firefox options
    options = Options()
    options.add_argument("--headless")

    url = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"
    xpath = (
        "//table[@class='wikitable sortable sticky-header sort-under "
        "mw-datatable col2left col6left jquery-tablesorter']"
    )
    # open wikipedia page with firefox
    with webdriver.Firefox(options=options) as driver:
        driver.get(url)
        # get HTML of wikipedia table
        element = driver.find_element(By.XPATH, xpath)
        html = StringIO(element.get_attribute("outerHTML"))

    # convert table into pandas dataframe
    df = pd.read_html(html)[0]
    df = df.iloc[:, 1:3][1:31]

    # matplotlib plot settings
    fig, ax = plt.subplots()
    ax.set_title("Top 30 countries by population")
    ax.set_xticklabels(df.Location, rotation=90)
    ax.set_ylabel("Population (millions)")
    ax.grid(axis="y", linestyle="--")
    ax.yaxis.offsetText.set_visible(False)
    plt.ticklabel_format(axis="y", style="sci", scilimits=(6, 6))

    # plot the data
    plt.bar(df.Location, df.Population)
    plt.show()

if __name__ == "__main__":
    main()
