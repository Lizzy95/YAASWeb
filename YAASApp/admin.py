from django.contrib import admin
from .models import Auction
from .models import Bidders
import djmoney_rates

admin.site.register(Auction)
admin.site.register(Bidders)