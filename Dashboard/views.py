from django.shortcuts import render,redirect

# Create your views here.
from django.views.generic import TemplateView,CreateView,UpdateView,View
from .forms import SignUpForm
from .models import Trade,Trader,MetaTraderAccount
import time
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Name: AYOMIDE ADEKOYA
# Server: MetaQuotes-Demo
# Type: Forex Hedged USD
# Login: 5015385110
# Password: cl2iaktf
# Investor: 5hpsxxew
# Create your views here.
# Name: AYOMIDE ADEKOYA
# Server: MetaQuotes-Demo
# Type: Forex Hedged USD
# Login: 5015393214
# Password: lf2bglvb
# Investor: mqzfps4n
# Name: AYOMIDE ADEKOYA
# Server: MetaQuotes-Demo
# Type: Forex Hedged USD
# Login: 5015393524
# Password: iifbv2yt
# Investor: ecx1dqka
# Create your views here.
class SignUp(CreateView):
    template_name = "registration/signup.html"
    form_class= SignUpForm
    success_url='/'

class IndexView(LoginRequiredMixin,TemplateView):
    template_name = "index.html"
    def get(self, request, *args, **kwargs):
        
            # Redirect to the index pa
        context = self.get_context_data(**kwargs)
        
        return self.render_to_response(context)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        
        active_account = MetaTraderAccount.objects.filter(user=self.request.user, is_active=True).first()
        Trades = Trade(trader=self.request.user,trade_account=active_account)
        
        trader = self.request.user
        Trades = Trade(trader=self.request.user,trade_account=active_account)
        time_data=self.get_time_data()
        total_profit_loss=Trade.get_total_profit_loss(trader)
        # random_trades = generate_random_trades_periodically.delay(self, minutes=1.0)
        total_trade_count = Trade.get_total_trade(trader)
        profit_loss_data = self.get_profit_loss_data()
        balance_data = self.get_balance_data()
        equity_data = self.get_equity_data()
        total_balance = 0
        total_equity = 0
        percentage_increase, percentage_decrease = self.calculate_percentage_changes(profit_loss=total_profit_loss, balance=total_balance)
        percentage_increase_balance, percentage_decrease_balance = self.calculate_percentage_changes_balance(total_balance=total_balance)
        accounts = MetaTraderAccount.objects.filter(user=trader)
        active_account = accounts.filter(is_active=True).first()

        

        if active_account:
            total_balance = active_account.balance
            total_equity = active_account.equity
            
    
        context={
            'Trades':Trades,'profit_loss_data':profit_loss_data,
            'time_data':time_data,'total_profit_loss':total_profit_loss,
            'total_balance':total_balance,'total_trade_count':total_trade_count,
            'percentage_increase':percentage_increase,'percentage_decrease':percentage_decrease,
            'percentage_increase_balance':percentage_increase_balance,'percentage_decrease_balance':percentage_decrease_balance,
            'balance_data':balance_data,'equity_data':equity_data,'accounts': accounts,
            'active_account': active_account,
            'total_equity':total_equity,
            }
        
        return context
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            # Retrieve form data and create a new MetaTraderAccount instance
            account = request.POST.get('account')
            password = request.POST.get('password')
            server = request.POST.get('server')
            account = MetaTraderAccount(user=request.user, server=server, account=account, password=password)
            account.save()
            # account.connect_mt5()
            # Redirect to the index view
            

            return self.get(request, *args, **kwargs)
    def get_profit_loss_data(self):
        trader = self.request.user
        trades = Trade.objects.filter(trader=trader)
        data = [float( trade.profit_loss) for trade in trades]
        return data
    def get_balance_data(self):
        active_account = MetaTraderAccount.objects.filter(user=self.request.user, is_active=True).first()
        trades = Trade.objects.filter(trade_account=active_account)
        data = [float( trade.trade_balance) for trade in trades]
        return data
    def get_equity_data(self):
        active_account = MetaTraderAccount.objects.filter(user=self.request.user, is_active=True).first()
        trades = Trade.objects.filter(trade_account=active_account)
        data = [float( trade.trade_equity) for trade in trades]
        return data
    def get_time_data(self):
        active_account = MetaTraderAccount.objects.filter(user=self.request.user, is_active=True).first()
        trades = Trade.objects.filter(trade_account=active_account)
        # trader = self.request.user
        # trades = Trade.objects.filter(trader=trader)
        data = [( trade.timestamp.strftime('%m/%d %H:%M')) for trade in trades]
        return data
    def calculate_percentage_changes(self, profit_loss, balance=100000):
        if balance == 0:
            return 0.0, 0.0
        percentage_increase = round((profit_loss / balance) * 100, 2)
        percentage_decrease = round(((balance - profit_loss) / balance) * 100, 2)
        return percentage_increase, percentage_decrease
    
    def calculate_percentage_changes_balance(self, total_balance):
        account_balance = 100000 # Get the initial account balance
        if account_balance == 0:
            return 0.0, 0.0
        percentage_increase = round(((total_balance - account_balance) / account_balance) * 100, 2)
        percentage_decrease = round(((account_balance - total_balance) / account_balance) * 100, 2)
        return percentage_increase, percentage_decrease
    
    def update_account_balance(self):
        active_account = MetaTraderAccount.objects.filter(user=self.request.user, is_active=True).first()
        trade = Trade(trader=self.request.user,trade_accout=active_account)
        new_equity=Trade.trade_equity
        # trade_balance=
        trade.trade_balance=new_equity
        trade.save()
        return trade
    def update_account_equity(self):
        active_account = MetaTraderAccount.objects.filter(user=self.request.user, is_active=True).first()
        trade = Trade(trader=self.request.user,trade_accout=active_account)
        new_equity=Trade.trade_equity
        # trade_balance=
        trade.trade_balance=new_equity
        trade.save()
        return trade
    

    def generate_random_trades_periodically(self, minutes):
        trade=0
        while True:
            trade=self.update_account_balance()
            trade1=self.update_account_equity()
            time.sleep(minutes * 60)
            return trade,trade1
    def get_equity_periodically(self, minutes):
        trade=0
        while True:

            # trade=self.update_account_balance()
            trade=self.update_account_equity()
            time.sleep(minutes * 60)
            return trade
def switch_metatrader_account(request, account_id):
        MetaTraderAccount.objects.filter(user=request.user).update(is_active=False)
        account = MetaTraderAccount.objects.get(id=account_id)

        try:
            account.connect_mt5()
            account.update_account_info()
            print(account.is_active)
            request.user.active_account = account
            request.user.save()
        finally:
            account.disconnect_mt5()
        
        return redirect('index')        
   
class UpdateChartDataView(View):
    def update_account_balance(self):
        trader = Trade(trader=self.request.user)
        new_balance=Trade.trade_balance
        # trade_balance=Trade.trade_balance
        trader.trade_balance=new_balance
        trader.save()
        return trader
    def update_account_equity(self):
        trader = Trade(trader=self.request.user)
        new_equity=Trade.trade_equity
        # trade_balance=
        trader.trade_balance=new_equity
        trader.save()
        return trader
    def get(self, request, *args, **kwargs):
        view = IndexView.as_view()
        response = view(request, *args, **kwargs)
        self.update_account_balance()
        self.update_account_equity()
        IndexView.get_equity_periodically(self ,minutes=1.0)
        IndexView.generate_random_trades_periodically(self, minutes=1.0)
        new_balance_data = response.context_data['balance_data']
        new_equity_data = response.context_data['equity_data']
        time_data = response.context_data['time_data']
        
        context={
            'new_balance_data': new_balance_data, 
            'time_data': time_data,
            'new_equity_data':new_equity_data,
            }
        
        return JsonResponse(context, content_type="application/json")

# class ChartDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Trade
#         fields = ('profit_loss', 'timestamp')
    

class ProfileView(LoginRequiredMixin,View):
    template_name = "users-profile.html"
    model =Trader
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    fields= ('name')

class FAQ(TemplateView):
    template_name='pages-faq.html'


def error_404_view(request, exception):
    data = {}
    # we add the path to the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, '404.html',data)

def error_500(request):
        data = {}
        response= render(request,'404.html', data)
        response.status_code = 404
        return response

@login_required         
def add_metatrader_account(request):
    if request.method == 'POST':
        # Retrieve form data and create a new MetaTraderAccount instance
        account = request.POST.get('account')
        password = request.POST.get('password')
        server = request.POST.get('server')
        account = MetaTraderAccount(user=request.user, account=account, password=password, server=server)
        account.connect_mt5()
        account.save()
        return redirect('index.html')# Redirect to account list view
    else:
        return render(request, 'add_metatrader_account.html')
    

def account_list(request):
    
    accounts = MetaTraderAccount.objects.filter(user=request.user)
    active_account = accounts.filter(is_active=True).first()

    balance = None
    equity = None

    if active_account:
        balance = active_account.balance
        equity = active_account.equity
    
    return render(request, 'account_list.html', {'accounts': accounts, 'active_account': active_account, 'balance': balance, 'equity': equity})