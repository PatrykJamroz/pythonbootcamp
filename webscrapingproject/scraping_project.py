import requests
from bs4 import BeautifulSoup
from random import choice


def get_quotes():
    quotes = []
    is_fetching = True
    base_url = 'https://quotes.toscrape.com/page/'
    page_num = 1

    print("Fetching the game data...")

    while is_fetching:
        r = requests.get(f"{base_url}{page_num}")
        html_string = r.text
        soup = BeautifulSoup(html_string, 'html.parser')
        found_quotes = soup.find_all(class_='quote')
        formatted_quotes = [{"quote": item.find(class_='text').get_text(), "author": item.find(
            class_='author').get_text(), "bio_url": item.find('a', string='(about)').get('href')} for item in found_quotes]
        quotes.extend(formatted_quotes)

        if soup.find(class_='next'):
            page_num += 1
        else:
            is_fetching = False

    return quotes


def game():
    quotes = get_quotes()
    random_quote = get_random_quote(quotes)
    bio = get_authors_bio(random_quote['bio_url'])
    tries_left = 4

    print(f"Here is a quote:\n\n{random_quote['quote']}\n\n")
    # TODO remove when app ready
    print('resp: ', random_quote['author'])

    while tries_left > 0:
        response = get_response(tries_left)
        if response == random_quote['author']:
            print("You guessed it correctly! Congratulations!")
            is_playing_again = input("Would you like to play again (y/n)?")
            if is_playing_again == 'y':
                random_quote = get_random_quote(quotes)
                bio = get_authors_bio(random_quote['bio_url'])
                tries_left = 4
                print("Great here we go again...\n\n")
                print(f"Here is a quote:\n\n{random_quote['quote']}\n\n")
                print('resp: ', random_quote['author'])
            else:
                return
        else:
            tries_left -= 1
            get_tip(tries_left, random_quote, bio)

    is_playing_again = input("Would you like to play again (y/n)?")
    if is_playing_again == 'y':
        # TODO inefficent - data is fetched again
        game()
    else:
        return


def get_random_quote(quotes):
    return choice(quotes)


def get_authors_bio(url):
    r = requests.get(f"https://quotes.toscrape.com{url}")
    html_string = r.text
    soup = BeautifulSoup(html_string, 'html.parser')
    return {'born': soup.find(class_='author-born-date').get_text(), 'born_loc': soup.find(class_='author-born-location').get_text()}


def get_response(tries_left):
    response = input(f"Who said this? Guesses remaining: {tries_left} ")
    return response


def get_tip(tries_left, quote, bio):
    base_text = "Here's a hint:"
    if tries_left == 3:
        print(
            f"{base_text} The author was born in {bio['born']}, {bio['born_loc']}.")
    elif tries_left == 2:
        print(
            f"{base_text} The author's first name starts with {quote['author'].split()[0][0]}")
    elif tries_left == 1:
        print(
            f"{base_text} The author's last name starts with {quote['author'].split()[0][1]}")
    else:
        print(
            f"Sorry you've run out guesses. The answer was {quote['author']}")


game()
