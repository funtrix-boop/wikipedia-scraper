from io import StringIO
from warnings import filterwarnings

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


# converts an HTML table into a dataframe
def html_to_df(html: str) -> pd.DataFrame:
    html_stringio = StringIO(html)
    df = pd.read_html(html_stringio)
    return df[0]


def main() -> None:
    filterwarnings("ignore", category=UserWarning)
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
        html = element.get_attribute("outerHTML")

    # convert table into pandas dataframe, and get first 30 columns
    df = html_to_df(html)
    df = df.iloc[1:31, 1:3]

    # matplotlib plot settings
    fig, ax = plt.subplots()
    ax.set_xticklabels(df.Location, rotation=90)
    ax.yaxis.set_major_locator(MultipleLocator(50_000_000))
    ax.yaxis.offsetText.set_visible(False)
    plt.ticklabel_format(axis="y", style="sci", scilimits=(6, 6))

    # plot the data
    plt.title("Top 30 countries by population")
    plt.ylabel("Population (millions)")
    plt.grid(axis="y", linestyle="--")
    plt.bar(df.Location, df.Population,
            width=0.6, color="teal")
    plt.show()


if __name__ == "__main__":
    main()
