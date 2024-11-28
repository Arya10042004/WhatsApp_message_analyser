import re
import pandas as pd


def preprocess(data):
    # Regular expression to extract date-time patterns
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'

    # Splitting messages and extracting dates
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Creating the DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Correcting the datetime format
    df['message_date'] = pd.to_datetime(df['message_date'], format="%d/%m/%Y, %H:%M - ")

    # Renaming the column for consistency
    df.rename(columns={"message_date": "date"}, inplace=True)

    # Extracting users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("Group Notification")
            messages.append(entry[0])

    # Adding the extracted data to the DataFrame
    df['user'] = users
    df['message'] = messages

    # Dropping the combined user-message column
    df.drop(columns='user_message', inplace=True)

    # Adding additional date-time features
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['only-date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period=[]
    for hour in df[['day_name','hour']]['hour']:
        if hour== 23:
            period.append(str(hour)+'-'+str('00'))
        elif hour==0:
            period.append(str('00')+'-'+str(hour+1))
        else:
            period.append(str(hour)+'-'+str(hour+1))
    df['period']=period

    # Returning the processed DataFrame
    return df
