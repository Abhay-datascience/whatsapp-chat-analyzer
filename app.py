import streamlit as st
from numpy.f2py.cb_rules import cb_map

import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data= bytes_data.decode('utf-8')
    df= preprocessor.preprocess(data)


    # fetch unique users
    users_list= df['users'].unique().tolist()
    users_list.remove('group notification')
    users_list.sort()
    users_list.insert(0,'Overall')

    selected_user= st.sidebar.selectbox("show analysis wrt",users_list)

    if st.sidebar.button('Show Analysis'):

        num_messages,words, num_of_media_messages,links= helper.fetch_stats(selected_user,df)

        st.title("Top Statistics")

        col1, col2, col3, col4= st.columns(4)

        with col1:
            st.write("Total Messages")
            st.title(num_messages)

        with col2:
            st.write("Total Words")
            st.title(words)

        with col3:
            st.write("Media Shared")
            st.title(num_of_media_messages)

        with col4:
            st.write("Links Shared")
            st.title(links)

        # Timeline

        st.title("Monthly Timeline")
        timeline= helper.monthly_timeline(selected_user, df)
        fig,ax= plt.subplots()
        ax.plot(timeline['time'], timeline['messages'],color= 'green')
        plt.xticks(rotation= 'vertical')
        st.pyplot(fig)

        # activity map

        st.title('Activity Map')

        col1, col2= st.columns(2)

        with col1:
            st.header('Most busy day')
            busy_day= helper.week_activity_map(selected_user, df)
            fig,ax= plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color= 'c')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header('Most busy month')
            busy_month = helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color= 'c')
            plt.xticks(rotation= 'vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        # finding the busiest user in the group

        if selected_user=='Overall':
            st.title('Most Busy Users')
            x,new_df= helper.most_busy_user(df)

            fig, ax= plt.subplots()

            col1, col2= st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color= 'red')
                plt.xticks(rotation= 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # Wordcloud

        st.title('WordCloud')
        df_wc= helper.creat_wordcloud(selected_user, df)
        fig,ax= plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Most Common Words

        most_common_df= helper.most_common_words(selected_user, df)

        fig,ax= plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')


        st.title('Most Common Words')
        st.pyplot(fig)

        # Emoji analysis

        emoji_df= helper.emoji_helper(selected_user, df)
        st.title('Emoji Analysis')

        col1, col2= st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct='%1.2f%%')
            st.pyplot(fig)


















