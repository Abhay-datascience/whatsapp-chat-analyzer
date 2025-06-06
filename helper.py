from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
extract= URLExtract()

def fetch_stats(selected_user,df):

    if selected_user!='Overall':
        df = df[df['users'] == selected_user]

    num_messages= df.shape[0]
    words = []

    for i in df['messages']:
        words.extend(i.split())

    num_of_media_messages= df[df['messages']=='<Media omitted>\n'].shape[0]

    links=[]
    for i in df['messages']:
        links.extend((extract.find_urls(i)))

    return num_messages,len(words),num_of_media_messages,len(links)

def most_busy_user(df):
    x= df['users'].value_counts().head()
    df= round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns= {'users':'name','count':'percent'})

    return x,df


def creat_wordcloud(selected_user,df):

    if selected_user!='Overall':
        df = df[df['users'] == selected_user]

    wc= WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc= wc.generate(df['messages'].str.cat(sep= " "))
    return df_wc


def most_common_words(selected_user,df):

    f= open('stop_hinglish.txt','r')
    stop_words= f.read()

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    words = []
    for i in temp['messages']:
        for word in i.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df= pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    emojis = []

    for i in df['messages']:
        emojis.extend([c for c in i if emoji.is_emoji(c)])

    emoji_df= pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts()

def monthly_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)

    return user_heatmap





















