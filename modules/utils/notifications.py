import firebase_admin.messaging

class FCMNotifier:
    '''
    Firebase Cloud Messaging notifier.
    '''

    def __init__(self):
        self.app = firebase_admin.initialize_app()

    def send_message(self, payload, topic=None, token=None):
        '''
        Send a message to all devices subscribed to a given topic.
        '''
        message = firebase_admin.messaging.Message(data=payload,topic=topic,token=token)
        firebase_admin.messaging.send(message, app=self.app)

    def subscribe_to_topic(self, token, topic):
        '''
        Subscribe a device to a topic.
        '''
        firebase_admin.messaging.subscribe_to_topic(token, topic, app=self.app)

    def unsubscribe_from_topic(self, token, topic):
        '''
        Subscribe a device to a topic.
        '''
        firebase_admin.messaging.unsubscribe_from_topic(token, topic, app=self.app)

