import pandas as pd
import re

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[AP]M'

    message= re.split(pattern,data)[1:]
    date= re.findall(pattern,data)

    df = pd.DataFrame({'user_message': message, 'date': date})

    df['date'] = pd.to_datetime(df['date'])

    df['date'] = df['date'].dt.strftime('%d-%m-%Y %H:%M')

    users = []
    messages_1 = []
    for i in df['user_message']:
        entry = re.split('([\w\W]+?):\s', i)
        if entry[1:]:
            users.append(entry[1])
            messages_1.append(entry[2])

        else:
            users.append('group notification')
            messages_1.append(entry[0])

    df['users'] = users
    df['messages'] = messages_1
    df.drop(columns=['user_message'], inplace=True)

    df['date'] = pd.to_datetime(df['date'])
    df['users'] = df['users'].str.replace('-', '')
    df['users'] = df['users'].str.strip(' ')
    # df['message_date'] = pd.to_datetime(df['message_date'])
    # df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    # df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    # df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
