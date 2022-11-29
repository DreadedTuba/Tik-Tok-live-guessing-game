
from threading import Thread
import random, json, time, socketserver
from http.server import HTTPServer, BaseHTTPRequestHandler
from httpcore import ConnectError
from random_words import RandomWords
from helpers import get_data, set_data

# https://isaackogan.github.io/TikTokLive/
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, GiftEvent, ShareEvent, FollowEvent, ViewerCountUpdateEvent
from TikTokLive.types.errors import LiveNotFound


# use txttovoice library and make the comments to voice

def randomize_words(): # function gets a random word and tells the code needed info
    rw = RandomWords()

    rand_word = rw.random_words(count=1) # gets random word
    
    print(f"[!] Word Chosen ==> {rand_word[0]}")

    str_rand_word = str(rand_word[0])

    len_of_word = len(str_rand_word) # gets the lenght of chars in word
    print(f"[!] Word Length ==> {len_of_word}")

    if len_of_word == 3:
        question_mark_num = 1
        word_level = "easy" # fix this bullshit
    elif len_of_word == 4:
        question_mark_num = 1
        word_level = "easy"
    elif len_of_word == 5:
        question_mark_num = 2
        word_level = "easy"
    elif len_of_word == 6:
        question_mark_num = 2
        word_level = "medium"
    elif len_of_word == 7:
        question_mark_num = 3
        word_level = "medium"
    elif len_of_word == 8:
        question_mark_num = 3
        word_level = "medium"
    elif len_of_word == 9:
        question_mark_num = 3
        word_level = "medium"
    elif len_of_word == 10:
        question_mark_num = 4
        word_level = "hard"
    elif len_of_word == 11:
        question_mark_num = 4
        word_level = "hard"
    elif len_of_word == 12:
        question_mark_num = 5
        word_level = "hard"
    elif len_of_word == 13:
        question_mark_num = 5
        word_level = "hard"
    elif len_of_word == 14:
        question_mark_num = 5
        word_level = "hard" 
    elif len_of_word == 15:
        question_mark_num = 6
        word_level = "super hard" 
    elif len_of_word == 16:
        question_mark_num = 6
        word_level = "super hard"  
 
    rand_char_num = random.randint(0, len_of_word)

    word = str_rand_word
    for _ in range(question_mark_num):  # Credit to DropOut#3301 who helped make this!
        pos = random.randint(0, len(word)-1)
        question_word = word.replace(word[pos], "?", 3)

    return {"unsensored_word": str_rand_word, "hidden_word": question_word, "length_of_word": len_of_word,"word_level": word_level }
    

class TiKTokClient(TikTokLiveClient):
    def __init__(self, unique_id: str, debug: bool = False, **options):
        # Prevents calling previous cached comments
        options['process_initial_data'] = False
        super().__init__(unique_id, debug, **options)
        self.add_listener("comment", self.on_comment)

    def _comment_check(self, user: str, comment: str) -> None:
        '''
        Checks users comment for right word response then
        saves data to local json file.

        :param user: commenters username
        :param comment: comment of user
        :return: None
        '''
        data = get_data()
        if not data['active_word']:
            return
        if data['word_data']['unsensored_word'] in str(comment).lower():
            data['winner'] = str(user)
            set_data(data)

    async def on_comment(self, event: CommentEvent):
        user_name = event.user.nickname
        comment_sent = event.comment
        # Call comment checking
        self._comment_check(user_name, comment_sent)
        print(f'[+] user -> {user_name}, comment -> {comment_sent}')

    async def on_gift(self, event: GiftEvent):
        user_name = event.user.nickname
        gift_given = event.gift
        json_gift_info = {"username": user_name, "gift_sent": gift_given}
        return json.dumps(json_gift_info)


class Server_necs(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def _get_winner(self) -> json:
        '''
        Checks if there are any current winners then
        resets all data for next word game.

        Note: Passed bool type "winner" key as an additional
              check so you can use via front-end side to display
              winner html if chosen too.

        :return: Json
        '''
        data = get_data()
        if not data['winner']:
            return json.dumps( # Check if winner is listed
                {"username_list": data['word_data']['hidden_word'], "winner": False})
        # Save winner to var
        winner = data['winner']
        # Reset data
        data['winner'] = ''
        data['active_word'] = False
        set_data(data) # Save json data
        return json.dumps({"username_list": winner, "winner": True})

    def do_GET(self): # getting the usernames
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        message = str(self._get_winner())
        print(f'[+] winner data -> {message}')
        self.wfile.write(bytes(message, "utf8"))
    
    def _get_random_word(self) -> json:
        '''
        Assigns current word if none.

        :return: Json
        '''
        data = get_data()
        if data['active_word']:
            return json.dumps(data['word_data'])
        data['active_word'] = True
        data['word_data'] = randomize_words()
        set_data(data)
        return json.dumps(data['word_data'])

    def do_POST(self): # gettnig the word
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        message = str(self._get_random_word())
        print(f'[+] word data -> {message}')
        self.wfile.write(bytes(message, "utf8"))

def run_server(addr="localhost", port=8000, server_class=HTTPServer, handler_class=Server_necs):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()

def main() -> None:
    # Init threads
    oTik: TiKTokClient = TiKTokClient('@dev_kuro')
    tik = Thread(target=oTik.run)
    server = Thread(target=run_server, args=("127.0.0.1", 8080,))

    # Begin both threads
    tik.start()
    server.start()
    
    # Join both threads
    tik.join()
    server.join()

if __name__ == "__main__":
    main()
