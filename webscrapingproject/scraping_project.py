import requests
from bs4 import BeautifulSoup
from random import choice


def game():
    quotes = get_quotes()
    game_state = setup_game_state(quotes)
    print_quote(game_state['quote']['text'])

    # TODO remove when app ready
    print('resp: ', game_state['quote']['author'])

    while game_state['tries_left'] > 0:
        response = get_response(game_state['tries_left'])

        if response == game_state['quote']['author']:
            print("You guessed it correctly! Congratulations!")

            if ask_if_playing_again():
                game_state = setup_game_state(quotes)
                print_quote(game_state['quote']['text'])
                print('resp: ', game_state['quote']['author'])
            else:
                print('See you soon!')
                return
        else:
            game_state['tries_left'] -= 1

            if game_state['tries_left'] == 0:
                get_tip(game_state)

                if ask_if_playing_again():
                    game_state = setup_game_state(quotes)
                    print_quote(game_state['quote']['text'])
                    print('resp: ', game_state['quote']['author'])
                else:
                    print('See you soon!')
                    return

            get_tip(game_state)


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
        formatted_quotes = [{"text": item.find(class_='text').get_text(), "author": item.find(
            class_='author').get_text(), "bio_url": item.find('a', string='(about)').get('href')} for item in
                            found_quotes]
        quotes.extend(formatted_quotes)

        if soup.find(class_='next'):
            page_num += 1
        else:
            is_fetching = False

    return quotes


def setup_game_state(quotes):
    random_quote = get_random_quote(quotes)
    return {'quote': random_quote, 'bio': get_authors_bio(random_quote['bio_url']), 'tries_left': 4}


def print_quote(text, is_playing_again=False):
    if is_playing_again:
        print("Great here we go again...\n\n")
    print(f"Here is a quote:\n\n{text}\n")


def get_random_quote(quotes):
    return choice(quotes)


def get_authors_bio(url):
    r = requests.get(f"https://quotes.toscrape.com{url}")
    html_string = r.text
    soup = BeautifulSoup(html_string, 'html.parser')
    return {'born': soup.find(class_='author-born-date').get_text(),
            'born_loc': soup.find(class_='author-born-location').get_text()}


def get_response(tries_left):
    response = input(f"Who said this? Guesses remaining: {tries_left} ")
    return response


def ask_if_playing_again():
    return True if input("Would you like to play again (y/n)?") == 'y' else False


def get_tip(game_state):
    base_text = "Here's a hint:"
    tries_left = game_state['tries_left']
    author = game_state['quote']['author']
    if tries_left == 3:
        print(
            f"{base_text} The author was born in {game_state['bio']['born']}, {game_state['bio']['born_loc']}.")
    elif tries_left == 2:
        print(
            f"{base_text} The author's first name starts with {author.split()[0][0]}")
    elif tries_left == 1:
        print(
            f"{base_text} The author's last name starts with {author.split()[1][0]}")
    else:
        print(
            f"Sorry you've run out guesses. The answer was {author}")


if __name__ == "__main__":
    game()
