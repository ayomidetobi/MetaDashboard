# import json
# from django.contrib.auth.models import AnonymousUser
# from django.contrib.sessions.models import Session
# from django.contrib.auth import get_user_model
# from channels.db import database_sync_to_async
# from channels.generic.websocket import AsyncWebsocketConsumer
# from .mt5 import get_balance,get_equity
# from .views import IndexView
# from .models import Trade,Trader
# import time
# import requests
# import websocket
# import asyncio
# from django.contrib.auth.mixins import LoginRequiredMixin
# from asgiref.sync import sync_to_async


# class ChartConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
        
#             # Proceed with WebSocket connection
#             await self.accept()
#         # Start updating and sending data periodically
#             asyncio.ensure_future(self.update_data())
#     @database_sync_to_async
#     def get_session(self, session_token):
#         try:
#             session = Session.objects.get(session_key=session_token)
#             return session
#         except Session.DoesNotExist:
#             return None

#     # @database_sync_to_async
#     # def get_user(self, user_id):
#     #     User = get_user_model()
#     #     try:
#     #         user = User.objects.get(id=user_id)
#     #         return user
#     #     except User.DoesNotExist:
#     #         return AnonymousUser()

#     async def disconnect(self, close_code):
#         # Stop updating and sending data
#         pass

#     async def receive(self, text_data):
#         # Handle incoming messages from the client, if needed
#         pass

#     async def update_data(self):
#         while True:
#             user = await sync_to_async(self.get_user)()
#             await self.get_equity_periodically(minutes=1)
#             await self.generate_balance_periodically()
#             balance_data = await sync_to_async(self.get_balance_data)()
#             equity_data = await sync_to_async(self.get_equity_data)()
#             time_data = await sync_to_async(self.get_time_data)()
#             # Get the latest data from your view
#             data = {
#                 'balance': balance_data,
#                 'equity': equity_data,
#                 'time_data': time_data,
#             }
#             print(data)
#             # Send the data to the client
#             await self.send(text_data=json.dumps(data))

#             # Sleep for the desired interval before the next update
#             await asyncio.sleep(60)  # Update every 60 seconds
        
#     def get_balance_data(self):
#         trader_id = self.scope['user'].id 
#         trades = Trade.objects.filter(trader_id=trader_id)
#         data = []
#         # print(type(data))

#         for trade in trades:
#             balance = get_balance()  # Replace with your actual logic to get the trade balance
#             data.append(float(balance))

#             return data

#     def get_equity_data(self):
#         trader_id = self.scope['user'].id
#         trades = Trade.objects.filter(trader_id=trader_id)
#         data = [float(trade.trade_equity) for trade in trades]
#         return data

#     def get_time_data(self):
#         trader_id = self.scope['user'].id
#         trades = Trade.objects.filter(trader_id=trader_id)
#         data = [trade.timestamp.strftime("%m/%d %H:%M") for trade in trades]
#         return data

#     def update_account_balance(self):
#         trader = self.user
#         new_balance = get_balance()  # Replace with your actual logic to get the balance
#         trader.trade_balance = new_balance
        
#         self.balance_data.append(new_balance)  # Store the new balance in the array
#         return trader

#     def update_account_equity(self):
#         trader = self.scope["user"]
#         new_equity = get_equity()  # Replace with your actual logic to get the equity
#         trader.trade_equity = new_equity
        
#         # self.get_equity_data.join(new_equity)  # Store the new equity in the array
#         return trader

#     def generate_balance_periodically(self, minutes):
#         trade = 0
#         trade = self.update_account_balance()
#         time.sleep(minutes * 60)
#         return trade

#     def get_equity_periodically(self, minutes):
#         trade = 0
        
#         trade = self.update_account_equity()
#         time.sleep(minutes * 60)
#         return trade
#     def get_user(self):
#         User = get_user_model()
#         return User.objects.get(id=self.scope['user'].id)