__author__ = 'lizzycruz'


from django_cron import CronJobBase, Schedule
from django.shortcuts import get_object_or_404
from YAASApp.models import Auction
from YAASApp.models import Bidders
from datetime import datetime
from forms import EditEmailForm

from django.core.mail import send_mail

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1
    RETRY_AFTER_FAILURE_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS,retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'blogApp.my_cron_job'    # a unique code

    def do(self):
         auction_lists = Auction.objects.all()
         todayDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
         for nAuc in auction_lists:
             if nAuc.deadLine == todayDate:
                 nAuc.resolve = "resolve"
                 from_email = 'noreply@yaas.com'
                 bidders = Bidders.objects.all()
                 emailBidders = []
                 for bider in bidders:
                     emailBidders.append(bider.bidderEmail)
                 emailBidders.append(nAuc.authoremail)
                 send_mail('New bid add', 'The item '+str(nAuc.titleAuc)+"has been resolved", from_email ,
                            emailBidders, fail_silently=False)
                 send_mail('New bid add', 'The item '+str(nAuc.titleAuc)+"is yours", from_email ,
                            nAuc.bidderemail, fail_silently=False)
