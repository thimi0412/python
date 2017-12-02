#!/usr/bin/env python
# -*- coding:utf-8 -*-
import TweetsGetter
import os
import urllib.request
import json
import collections as cl
from datetime import datetime as dt
import datetime

if __name__ == '__main__':

    '''
    キーワードで検索
    '''
    keyword_getter = TweetsGetter.TweetsGetter.bySearch('Tokyo, trip')

    '''
    cnt:ツイートの連番
    tweetid_list:ツイートの重複を避けるためのリスト(tweet_idを格納する)
    '''
    cnt = 0
    tweetid_list = []

    '''
    jsonを作成するためのリスト
    user_list:screen_nameを格納
    tweets_list:ユーザ別のtweetを格納(複数)
    '''
    user_list = []
    tweet_result_list =[]

    '''
    取得したツイートのユーザからタイムラインを取得
    '''
    for tweet1 in keyword_getter.collect(total = 5):
        cnt += 1 #連番の算
        user_list.append(tweet1['user']['screen_name']) #screen_nameを追加

        '''
        タイムラインを取得
        '''
        user_getter = TweetsGetter.TweetsGetter.byUser(tweet1['user']['screen_name'])

        '''
        複数のツイートを格納するリスト
        '''
        tweet_list = []

        '''
        タイムラインを回す
        '''
        for tweet2 in user_getter.collect(total = 5):
            '''
            ツイートの重複チェック、ツイートのidが既に存在しているかで判定
            '''
            if tweet2['id'] not in tweetid_list:

                '''
                ツイートの情報を格納するリスト
                '''
                tweet_info_list = []

                #取得した時刻(文字列)をDate型に整形
                created_at = tweet2['created_at']
                created_at = created_at.replace('+0000','')
                created_at = dt.strptime(created_at, '%a %b %d %H:%M:%S %Y')
                #日本時刻にするため9時間加算
                created_at = created_at + datetime.timedelta(hours=9)

                #時刻とテキストをtweet_info_listに格納
                tweet_info_list.append(str(created_at))
                tweet_info_list.append(tweet2['text'])

                '''
                デバック文
                '''
                print('screen_name:{}'.format(tweet2['user']['screen_name']))
                print('created_at:{}'.format(created_at))
                print('text:{}'.format(tweet2['text']))

                '''
                位置情報(latlong)、画像URL(media_url)の処理
                存在しない場合は'None'を格納
                '''
                try: #画像、画像のダウンロードは今後考える
                    print('media_url:{}'.format(tweet2['entities']['media'][0]['media_url_https']))
                    tweet_info_list.append(tweet2['entities']['media'][0]['media_url_https'])
                    # url = tweet1['entities']['media'][0]['media_url_https']
                    # any_url_obj = urllib.request.urlopen(url)
                    # local = open(os.path.basename(url), 'wb')
                    # local.write(any_url_obj.read())
                except:
                    print('media_url:mediaなし')
                    tweet_info_list.append('None')

                try: #位置情報
                    print('位置情報:{}'.format(tweet2['geo']['coordinates']))
                    tweet_info_list.append(tweet2['geo']['coordinates'])
                except:
                    print('位置情報:geoなし')
                    tweet_info_list.append('None')

                print(' ')
                print('='*100)

                tweetid_list.append(tweet2['id']) #重複チェックのためidを格納

                tweet_list.append(tweet_info_list) #tweets_listに格納

        tweet_result_list.append(tweet_list)

    print(user_list)
    print(tweet_result_list)

    '''
    jsonへの整形
    '''

    ys = cl.OrderedDict()
    for i in range(len(user_list)):
        data = cl.OrderedDict()
        data["tweets"] = tweet_result_list[i]
        ys[user_list[i]] = data

    fw = open('myu_s.json','w')
    json.dump(ys,fw,indent=4,ensure_ascii=False)
