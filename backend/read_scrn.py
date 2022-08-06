
import random, json, time
from http.server import HTTPServer, BaseHTTPRequestHandler
from httpcore import ConnectError
from random_words import RandomWords
# https://isaackogan.github.io/TikTokLive/
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, GiftEvent, ShareEvent, FollowEvent, ViewerCountUpdateEvent


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
    for u in range(question_mark_num):  # Credit to DropOut#3301 who helped make this!
        pos = random.randint(0, len(word)-1)
        question_word = word.replace(word[pos], "?", 3)

    
    response = {"unsensored_word": str_rand_word, "hidden_word": question_word, "length_of_word": len_of_word,"word_level": word_level }
    return json.dumps(response)
    
def scrape_tt_info():
    
    client: TikTokLiveClient = TikTokLiveClient(unique_id="@dev_kuro")
    
    def clean_info(comment_sent, user_name):
        on_comment()
        json_comment_info = {"username_list": user_name, "comment_list": comment_sent}
        return json_comment_info
    
    @client.on("comment")
    async def on_comment(event: CommentEvent):
        user_name = event.user.nickname
        comment_sent = event.comment
        clean_info(comment_sent, user_name)
        
        
       
        
        
        
        
        
        
        
    @client.on("gift")
    async def on_gift(event: GiftEvent):
        user_name = event.user.nickname
        gift_given = event.gift
        json_gift_info = {"username": user_name, "gift_sent": gift_given}
        return json.dumps(json_gift_info)
        
    client.add_listener("comment", on_comment)
    #client.add_listener("gift", on_gift)
    client.run()





class Server_necs(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()


    def do_GET(self): # getting the usernames
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        ret_info = scrape_tt_info()
        message = str(ret_info)
        self.wfile.write(bytes(message, "utf8"))
  
    
    def do_POST(self): # gettnig the word
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        array_of_info = randomize_words()   
        message = str(array_of_info)

        self.wfile.write(bytes(message, "utf8"))


def run(server_class=HTTPServer, handler_class=Server_necs, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run(addr="127.0.0.1", port=8080)
    
