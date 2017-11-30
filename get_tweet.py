#!/usr/bin/env python
# -*- coding:utf-8 -*-
import TweetsGetter
import os
import urllib.request
import json
import collections as cl
from datetime import datetime as dt

if __name__ == '__main__':

    #キーワードで取得
    keyword_getter = TweetsGetter.TweetsGetter.bySearch('Tokyo, trip')
    cnt = 0
    tweetid_list = []
    user_list = []
    tweet_list =[]

    for tweet in keyword_getter.collect(total = 2):
        cnt += 1
        print('------ %d ------'  % cnt)
        # ユーザーを指定して取得 （screen_name）
        user_list.append(tweet['user']['screen_name'])
        user_getter = TweetsGetter.TweetsGetter.byUser(tweet['user']['screen_name'])
        temp = []
        for tweet1 in user_getter.collect(total = 5):
            if tweet1['id'] not in tweetid_list:
                child_tweet_list = []
                print(tweet1['user']['screen_name'])

                created_at = tweet1['created_at']
                created_at = created_at.replace('+0000','')
                created_at = dt.strptime(created_at, '%a %b %d %H:%M:%S %Y')
                print(created_at)

                child_tweet_list.append(str(created_at))
                print(tweet1['text'])

                child_tweet_list.append(tweet1['text'])
                try:
                    print(tweet1['entities']['media'][0]['media_url_https'])
                    child_tweet_list.append(tweet1['entities']['media'][0]['media_url_https'])
                    # url = tweet1['entities']['media'][0]['media_url_https']
                    # any_url_obj = urllib.request.urlopen(url)
                    # local = open(os.path.basename(url), 'wb')
                    # local.write(any_url_obj.read())
                except:
                    print('mediaなし')
                    child_tweet_list.append('None')
                try:
                    print(tweet1['geo']['coordinates'])
                    child_tweet_list.append(tweet1['geo']['coordinates'])
                except:
                    print('geoなし')
                    child_tweet_list.append('None')

                print(' ')
                print('='*100)
                tweetid_list.append(tweet1['id'])
                temp.append(child_tweet_list)
        tweet_list.append(temp)

    print(user_list)
    print(tweet_list)
    print('*'*100)
    for i in tweet_list:
        print(i)
        print('='*100)
        '''
        jsonへの整形
        '''

    ys = cl.OrderedDict()
    for i in range(len(user_list)):
        data = cl.OrderedDict()
        data["tweets"] = tweet_list[i]
        ys[user_list[i]] = data

    fw = open('myu_s.json','w')
    #ココ重要！！
    # json.dump関数でファイルに書き込む
    json.dump(ys,fw,indent=4)
