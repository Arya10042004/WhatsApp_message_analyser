from collections import Counter

import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
import emoji
extract=URLExtract()
def fetch_stats(selected_user, df):
    if selected_user == 'Overall':
        # Use the entire DataFrame
        filtered_df = df
    else:
        # Filter DataFrame for the selected user
        filtered_df = df[df['user'] == selected_user]

    # Number of messages
    num_messages = filtered_df.shape[0]

    # Count words in messages
    words = []
    for message in filtered_df['message']:
        words.extend(message.split())

    # Count media messages
    num_media_messages = filtered_df[filtered_df['message'] == '<Media omitted>\n'].shape[0]

    links=[]
    for message in filtered_df['message']:
        links.extend(extract.find_urls(message))




    return num_messages, len(words), num_media_messages,len(links)
def most_busy_users(filtered_df):

    x=filtered_df['user'].value_counts().head()
    df=round((filtered_df['user'].value_counts()/filtered_df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})

    return x,df
def create_wordcloud(selected_user,df):
    if selected_user == 'Overall':
        # Use the entire DataFrame
        filtered_df = df
    else:
        # Filter DataFrame for the selected user
        filtered_df = df[df['user'] == selected_user]

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc=wc.generate(filtered_df['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    if selected_user == 'Overall':
        # Use the entire DataFrame
        filtered_df = df
    else:
        # Filter DataFrame for the selected user
        filtered_df = df[df['user'] == selected_user]
    words = []
    for message in filtered_df['message']:
        words.extend(message.split())


    from collections import Counter

    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user == 'Overall':
        # Use the entire DataFrame
        filtered_df = df
    else:
        # Filter DataFrame for the selected user
        filtered_df = df[df['user'] == selected_user]
    emojis = []
    for message in filtered_df['message']:
        if isinstance(message, str):  # Ensure message is a string
            emojis.extend([c for c in message if emoji.is_emoji(c)])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user == 'Overall':
        # Use the entire DataFrame
        filtered_df = df
    else:
        # Filter DataFrame for the selected user
        filtered_df = df[df['user'] == selected_user]
    timeline = filtered_df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user == 'Overall':
        # Use the entire DataFrame
        filtered_df = df
    else:
        # Filter DataFrame for the selected user
        filtered_df = df[df['user'] == selected_user]
    daily = filtered_df.groupby('only-date').count()['message'].reset_index()
    return daily

def week_activity_map(selected_user,df):
    if selected_user == 'Overall':
        # Use the entire DataFrame
        filtered_df = df
    else:
        # Filter DataFrame for the selected user
        filtered_df = df[df['user'] == selected_user]
    return filtered_df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user == 'Overall':
        # Use the entire DataFrame
        filtered_df = df
    else:
        # Filter DataFrame for the selected user
        filtered_df = df[df['user'] == selected_user]
    return filtered_df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user == 'Overall':
        # Use the entire DataFrame
        filtered_df = df
    else:
        # Filter DataFrame for the selected user
        filtered_df = df[df['user'] == selected_user]
    user_heatmap=  filtered_df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)

    return user_heatmap














