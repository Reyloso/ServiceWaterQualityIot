#pubnub packages
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub


class pubnubClient():

    def __init__(self):
        self.pnconfig = PNConfiguration()
        self.CHANNEL = ''
        self.pubnub = object
        self.status = False


    def pubnub_connection(self, subscribe_key, publish_key, uuid, CHANNEL):
        """ function to open connection to pubnub """ 

        try:
            self.pnconfig.subscribe_key = subscribe_key
            self.pnconfig.publish_key = publish_key
            self.pnconfig.uuid = uuid
            self.CHANNEL = CHANNEL
            self.pubnub = PubNub(self.pnconfig)
            self.status = True
            return self.pubnub
        except Error:
            print('pubnub connection error occurred: %s' %Error)

    def pubnub_publish(self, data):
        """ function to open connection to pubnub """ 

        the_message = data
        envelope = self.pubnub.publish().channel(self.CHANNEL).message(data).sync()

        if envelope.status.is_error():
            print("[PUBLISH: fail]")
            print("error: %s" % status.error)
        else:
            print("[PUBLISH: sent]")
            print("timetoken: %s" % envelope.result.timetoken)
        
        



