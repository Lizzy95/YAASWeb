"""YAAS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from YAASApp.views import *
from YAASApp.views_server import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^yaas/$', show_home),

                       #User urls
                       (r'^yaas/createuser/', createUser),
                       (r'^yaas/loginuser/', loginUser),
                       (r'^yaas/logoutuser/$', logoutUser),
                       (r'^yaas/edituser/$', editUser),

                       #URLs for auction
                       (r'^yaas/createauction/$', createAuction),
                       (r'^yaas/saveaucconf/', saveAucConf),
                       (r'^yaas/view/(?P<idItem>\w+)/$',     show_Auction),
                       (r'^yaas/editauction/(?P<idItem>\w+)/$', edit_auction),
                       (r'^yaas/bid/(?P<idItem>\w+)/$', bid_auction),
                       (r'^yaas/banauction/(?P<idItem>\w+)/$', ban_auction),

                       #URLs for search
                       (r'^yaas/searchauction/$', searchAuction),
                       #URL for browse
                       (r'^yaas/browseauction/$', auctionBrowse),

                       #URLs for the server
                       (r'^yaas/browseauctionServer/$', auction_list),
                       (r'^yaas/searchauctionServer/(?P<pk>[0-9]+)/$', auction_detail),


                       #URLs to edit
                       (r'^editpassword/', editPassword),
                       (r'^editemail/', editEmail),

                       (r'^setlanguage/(?P<lang_code>\w+)/$', set_language),
                       (r'^admin/', include(admin.site.urls)),
                    )