import requests
from bs4 import BeautifulSoup


# ------- Home Page ------- #

# searchURL = "https://www.yelp.com/search?find_desc=thai%20food&find_loc=owings%20mills"
# example = "https://www.yelp.com/search?find_desc=sushi&find_loc=baltimore"


# find url from the user search input
def searchListURL(what, where):
    Yelp = "https://www.yelp.com/search?find_desc="
    what = what.replace(' ', '%20')
    where = '&find_loc=' + where.replace(' ', '%20')
    searchURL = Yelp + what + where
    # print(searchURL)
    return searchURL

# get code and build BeautifulSoup object


def runBeautifulSoup(url):
    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    return soup

# find all restaurants and their links(url) based on user searching input


def findSearchInfo(soup):
    restaurants = []
    links = []
    reviews = []
    info = []
    for h3 in soup.find_all('h3', class_="alternate__373c0__1uacp"):
        for a in h3.findChildren('a'):
            restaurant = a.text
            link = a.get('href')
            restaurants.append(restaurant)
            links.append(link)
    # BUGS when no review it skips, creates wrong matching numbers of reviews and restaurants
    for span in soup.find_all('span', class_="reviewCount__373c0__2r4xT"):
        review = span.text
        reviews.append(review)
    info.append(restaurants)
    info.append(links)
    info.append(reviews)
    return info

# print all restaurants' names and their links


def printAllInfo(info):
    i = 0
    while i < len(info):
        j = 1
        while j < len(info[i]):
            print(info[i][j])
            print()
            j += 1
        i += 1

# get all the links from user search input


def getAllLinks(info):
    j = 1
    links = []
    while j < len(info[1]):
        print(info[1][j])
        links.append(info[1][j])
        j += 1
    return links

# get all restaurants' names from user search input


def getAllNames(info):
    j = 1
    names = []
    while j < len(info[0]):
        print(j, info[0][j])
        names.append(info[1][j])
        j += 1
    return names

# get a specific link (when user choose a restaurant)


def getTheLink(info, index):
    print(info[1][index])
    return info[1][index]

# get a specific name of a restaurant (chosen restaurant)


def getTheName(info, index):
    print(info[0][index])
    return info[0][index]


def printNamesAndReviews(info):
    j = 1
    while j < len(info[0]):
        number = str(j)+"."
        review = info[2][j]
        reviews = "("+review+")"
        print(number, info[0][j], reviews)
        j += 1


# ------------------------------------------------------------------------------------------

# ------- Get the Reviews Page (The Chosen Restaurant Page) ------- #

def createThePlaceURL(link, find):
    # example = "https://www.yelp.com/biz/baltimore-built-bistro-b3-baltimore-3?start=1"
    Yelp = "https://www.yelp.com"
    toBeRemoved = -(len(find)+5)

    # print(toBeRemoved)
    link = link[:toBeRemoved]
    start1 = "?start=1"
    url = Yelp+link+start1
    print(url)
    return url

# find total pages (reviews)


def findTotalPages(soup):
    totalPages = ''
    for div in soup.find_all('div', class_="page-of-pages"):
        # print(div.text)
        pageOfPages = div.text.strip()
        # print(pageOfPages)
        # print(len(pageOfPages))
        totalPages = pageOfPages[10:]
        # print(pageOfPages)
        # print(totalPages)
        totalPages = int(totalPages)
    return totalPages

 # Scraping all reviews


def scrapeReviews(link, totalPages):
    link = link[:-1]
    page = 1
    countReviews = 1
    startAt = 1
    # startAt = start at review number(1,20,40,60,80) this is for the url
    while page <= totalPages:
        if page == 1:
            startAt = 1
        elif page > 1:
            startAt = (page-1)*20
        strStartAt = str(startAt)
        url = link+strStartAt
        pageOfPages = "(Page " + str(page) + " of " + str(totalPages) + ")"
        print(url, pageOfPages)
        soup = runBeautifulSoup(url)
        # print all reviews
        for p in soup.find_all('p', {"lang": "en"}):
            print(countReviews)
            print(p.text, '\n')
            countReviews += 1
        page += 1


def start():
    # Get user input
    find = input('What kind of food you are looking for: ')
    near = input('Location: ')

    # Get search URL (List of restaurants/Places Page)
    searchListUrl = searchListURL(find, near)

    # created BeautifulSoup object
    soup = runBeautifulSoup(searchListUrl)

    # get all 'info' (names, links(href), and numbers of reviews)
    # (scrape the 'info' of the places in the list (30 featured places), then store them into a list
    # the list (30 featured places) can be different, based on user input)
    info = findSearchInfo(soup)

    # Print all names and numbers of reviews for user to choose
    printNamesAndReviews(info)

    # User choose a place to find its reviews
    chosenPlace = int(input(
        "Enter the 'number' of the restaurant you want to see reviews: "))

    # get the href link from that chosen place
    theLink = getTheLink(info, chosenPlace)

    # create real/working url
    thePlaceURL = createThePlaceURL(theLink, find)

    # create Beautiful Soup object
    soup = runBeautifulSoup(thePlaceURL)

    # find Total pages of reviews
    totalPages = findTotalPages(soup)

    # scraping all reviews from all the pages
    scrapeReviews(thePlaceURL, totalPages)


# ------------------------------------------------------------------------------------------
# ------------------ Program starts here -------------------
start()
