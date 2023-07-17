from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone
import MetaTrader5 as mt5
import random

# Create your models here.
class Trader(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return str(self.name)
    

class MetaTraderAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,max_length=225)
    account = models.BigIntegerField(unique=True)
    password = models.CharField(max_length=255)
    server = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    equity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True) 
    def __str__(self):
        return str(self.account)

    def connect_mt5(self):
        if not mt5.initialize():
            raise ValueError("Failed to initialize MetaTrader5")

        # Connect to the MetaTrader server
        server = self.server
        account = self.account
        password = self.password
        print(account)
        login_result = mt5.login(server=server, login=account, password=password)

        if not login_result:
            raise ValueError("Failed to connect to MetaTrader server")

    def disconnect_mt5(self):
        mt5.shutdown()

    def update_account_info(self):
        if not mt5.account_info():
            raise ValueError("Failed to retrieve account information")

        # Update the balance and equity fields
        self.is_active=True
        self.balance = mt5.account_info().balance
        self.equity = mt5.account_info().equity
        self.save()
    
    def set_active(self):
        # Method to set the account as active
        self.is_active = True
        self.save()

    def deactivate(self):
        # Method to deactivate the account
        self.is_active = False
        self.save()

class Trade(models.Model):
    trader = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    profit_loss = models.FloatField(default=0)
    trade_account=models.ForeignKey(MetaTraderAccount, on_delete=models.CASCADE, related_name='trades')
    trade_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    trade_equity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def save(self, *args, **kwargs):
        active_account = MetaTraderAccount.objects.filter(user=self.trader, is_active=True).first()
        if active_account:
            self.trade_account=active_account
            self.trade_balance = active_account.balance
            self.trade_equity = active_account.equity
        super(Trade, self).save(*args, **kwargs)

    
    
    

    @staticmethod
    def get_total_profit(user):
        total_profit = Trade.objects.filter(trader=user).aggregate(profit=Sum('profit_loss', filter=models.Q(profit_loss__gt=0)))['profit']
        return total_profit or 0

    @staticmethod
    def get_total_loss(user):
        total_loss = Trade.objects.filter(trader=user).aggregate(loss=Sum('profit_loss', filter=models.Q(profit_loss__lt=0)))['loss']
        return total_loss or 0

    @staticmethod
    def get_total_profit_loss(user):
        total_profit = Trade.get_total_profit(user)
        total_loss = Trade.get_total_loss(user)
        total_profit_loss = total_profit + total_loss
        return total_profit_loss

    # @staticmethod
    # def get_total_balance(user):
    #     total_profit_loss=Trade.get_total_profit_loss(user)
    #     acct_balance=Trade.trade_balance
    #     total_balance = (float(total_profit_loss) + float(acct_balance))
    #     return total_balance or 0
    
    def get_total_trade(user):
        return Trade.objects.filter(trader=user).count()

