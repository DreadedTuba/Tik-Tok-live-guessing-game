

from xml.dom import xmlbuilder
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent, LikeEvent, FollowEvent, ViewerCountUpdateEvent, GiftEvent
from numpy import append
from pandas import array
from pyparsing import FollowedBy

def test():
    client: TikTokLiveClient = TikTokLiveClient(unique_id="@dev_kuro")
   
    list_of_info = {
        'comments': '',
        'usrnames': '',
    }


    def on_comment(event: CommentEvent):
    
        user_name = event.user.nickname
        comment_sent = event.comment

        list_of_info['usrnames'] = user_name
        list_of_info['comments'] = comment_sent
    
        
    client.add_listener("comment", on_comment)
    
    client.run()


    print(list_of_info)


cv = test()

