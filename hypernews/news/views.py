from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from collections import OrderedDict
from datetime import datetime
import json
import os
import itertools
from operator import itemgetter
from hypernews.settings import NEWS_JSON_PATH
from django.shortcuts import redirect
import random


articles = []

articles_dict = {}


def open_json(json_list):
    with open(NEWS_JSON_PATH, 'r') as json_file:
        json_list = json.load(json_file)
    return json_list


def group_articles(some_dict, art_list):

    for article in art_list:
        some_dict[article['link']] = article  # dict link: news

    # sort by date desc
    sorted_articles = sorted(art_list, key=itemgetter('created'), reverse=True)
    grouped_by_date = {key: list(group)
                       for key, group in itertools.groupby(sorted_articles, key=lambda x: x['created'][0:10])}
    return grouped_by_date


class MyView(View):
    def get(self, request, *args, **kwargs):
        # return render(request, 'news/index.html')
        return HttpResponseRedirect('/news')


class NewsView(View):
    def get(self, request, *args, **kwargs):
        search_dict = {}
        needed_articles = []
        articles_1 = []
        articles_1 = open_json(articles_1)
        if not request.GET.get('q'):
            return render(request, 'news/news_file.html',
                          context={'articles': group_articles(articles_dict, open_json(articles))})
        else:
            for element in articles_1:
                if request.GET.get('q') in element['title']:
                    needed_articles.append(element)
                    # group_articles(search_dict, articles_1)
            return render(request, 'news/news_file.html',
                          context={'articles': group_articles(search_dict, needed_articles)})


class JsonView(View):
    def get(self, request, id, *args, **kwargs):
        # open_json(articles)
        group_articles(articles_dict, open_json(articles))
        article = articles_dict[id]
        return render(request, 'news/news1.html', article)


class CreateView(View):
    def get(self, request):
        return render(request, 'news/create_news.html')

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        text = request.POST.get('text')
        link = random.randint(10, 1000000)
        articles.append({'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'text': text, 'title': title,
                         'link': str(link)})
        with open(NEWS_JSON_PATH, 'ab') as file:
            file.seek(-1, os.SEEK_END)
            file.truncate()
        with open(NEWS_JSON_PATH, 'a') as file:
            file.write(', {"created": "' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '", "text": "' + text +
                       '", "title": "' + title + '", "link": ' + str(link) + '}]')
        return redirect('/news/')


class SearchView(View):
    def get(self, request):
        search_dict = {}
        needed_articles = []
        articles_1 = []
        articles_1 = open_json(articles_1)
        for element in articles_1:
            if request.GET.get('q') in element['title']:
                needed_articles.append(element)
                # group_articles(search_dict, articles_1)
        return render(request, 'news/search.html',
                      context={'articles': group_articles(search_dict, needed_articles)})



