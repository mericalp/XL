# # business_logic/WebSocket/consumers.py
# from channels.generic.websocket import WebsocketConsumer
# from asgiref.sync import async_to_sync
# import json

# class NotificationConsumer(WebsocketConsumer):
#     def connect(self):
#         self.group_name = "admin_notifications"
#         async_to_sync(self.channel_layer.group_add)(
#             self.group_name,
#             self.channel_name
#         )
#         self.accept()

#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.group_name,
#             self.channel_name
#         )

#     def receive(self, text_data):
#         data = json.loads(text_data)
#         async_to_sync(self.channel_layer.group_send)(
#             self.group_name,
#             {
#                 "type": "send_notification",
#                 "message": data.get('message', '')
#             }
#         )

#     def send_notification(self, event):
#         self.send(text_data=json.dumps({
#             "type": "notification",
#             "message": event["message"]
#         }))