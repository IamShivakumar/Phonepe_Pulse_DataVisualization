import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import mysql.connector as sql
connect = sql.connect(
host = "localhost",
user = "root",
password = "mysql1234",
database = "phonepe_pulse"
)
mycursor = connect.cursor(buffered=True)

st.set_page_config(page_title= "Phonepe Pulse Data Visualization",
                  # page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created by *Shiva*!
                                        Data has been cloned from Phonepe Pulse Github Repo"""})

with st.sidebar:
        selected = option_menu(None,
                           options=["Home","Top Charts","Explore Data"],
                           icons=["house-door-fill","tools","card-text"],
                           styles={"nav-link-selected": {"background-color": "purple"}},
                           default_index=0)

if selected=="Home":
 st.title(":violet[Phonepe_Pulse]")
 st.markdown(":violet[Welcome to the PhonePe Pulse Dashboard ,This PhonePe Pulse Data Visualization and Exploration dashboard is a user-friendly tool designed to provide insights and information about the data in the PhonePe Pulse GitHub repository. This dashboard offers a visually appealing and interactive interface for users to explore various metrics and statistics.]")

if selected=="Top Charts":
      st.title(":violet[Top Charts]")
      Type=st.sidebar.selectbox("Type",("Transaction","Users"))
      column1,column2= st.columns([1,1.5],gap="large")
      with column1:
        Year = st.selectbox("Year", ("2018","2019","2020","2021","2022","2023"))
        Year=int(Year)
        Quarter = st.selectbox("Quarter", ('1','2','3','4'))
        Quarter=int(Quarter)
      with column2:
        st.info(
                """
                #### From this menu we can get insights like :
                - Top 10 State, District based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """,icon="🔍"
                ) 
      if Type == "Transaction":
         col1,col2 = st.columns([1,1],gap="medium")
         with col1:
            st.markdown("### :violet[State]")
            mycursor.execute(f"select state, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_transaction where year = {Year} and quarter = {Quarter} group by state order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

         with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"select district , sum(Transaction_Count) as Total_Count, sum(Transaction_Amount) as Total_Amount from map_transaction where year = {Year} and quarter = {Quarter} group by district order by Total_Amount desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transaction_Count','Transaction_Amount'])
            fig = px.pie(df, values='Transaction_Amount',
                             names='District',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transaction_Count'],
                             labels={'Transaction_Count':'Transaction_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

      if Type=='Users':         
          column1,column2,column3 = st.columns([2,2,2],gap="small")   
          with column1:
            st.markdown("### :violet[Brands]")
            if Year == 2023 and Quarter in [3,4]:
                st.markdown("#### Sorry No Data to Display for 2022 Quarter 3 and 4")
            else:
                mycursor.execute(f"select Mobile_model, sum(Transaction_Count) as Total_Count, avg(Transaction_percentage)*100 as Avg_Percentage from agg_user where year = {Year} and quarter = {Quarter} group by Mobile_model order by Total_Count desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Mobile Model', 'Total_Users','Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10',
                             x="Total_Users",
                             y="Mobile Model",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)
          with column2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"select district, sum(Registered_User) as Total_Users, sum(app_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)   
          with column3:
            st.markdown("### :violet[State]")
            mycursor.execute(f"select state, sum(Registered_User) as Total_Users, sum(app_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="State",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)   

if selected=="Explore Data":
      st.title(":violet[Explore]")
      Type=st.sidebar.selectbox("Type",("Transaction","Users"))
      column1,column2= st.columns([2,2],gap="large")
      Year = st.sidebar.selectbox("Year", ("2018","2019","2020","2021","2022","2023"))
      Year=int(Year)
      Quarter = st.sidebar.selectbox("Quarter", ('1','2','3','4'))
      Quarter=int(Quarter)
      if Type=="Transaction":
       with column1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            mycursor.execute(f"select state, sum(Transaction_Count) as Total_Transactions, sum(Transaction_Amount) as Total_amount from map_transaction where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            # df2 = pd.read_csv('Statenames.csv')
            # df1.State = df2
            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_amount',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
       with column2:
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            mycursor.execute(f"select state, sum(Transaction_Count) as Total_Transactions, sum(Transaction_Amount) as Total_amount from map_transaction where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            # df2 = pd.read_csv('Statenames.csv')
            df1.Total_Transactions = df1.Total_Transactions.astype(int)
            # df1.State = df2
            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_Transactions',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            st.markdown("## :violet[Top Payment Type]")
            mycursor.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from agg_transaction where year= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])
            fig = px.bar(df,
                     title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=False)
# BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
       with column1:
            st.markdown("## :violet[Select any State to explore more]")
            selected_state = st.selectbox("",
                             ("Andaman & Nicobar","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh","Dadra & Nagar Haveli & Daman & Diu","Delhi","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu & Kashmir","Jharkhand","Karnataka","Kerala","Ladakh","Lakshadweep","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"),index=30)
         
            mycursor.execute(f"select State, District,year,quarter, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from map_transaction where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by state,district")
        
            df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
            fig = px.bar(df1,
                     title=selected_state,
                     x="Total_Transactions",
                     y="District",
                     orientation='h',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)
      if Type=="Users":
          column1,column2= st.columns([2,2],gap="large")
          with column1:
              mycursor.execute(f"SELECT sum(Registered_user) FROM phonepe_pulse.map_user where year<={Year} and Quarter<={Quarter}")
              Total_users=mycursor.fetchone()
              totalUsers=format(Total_users[0],",")
              st.write(f"###l :violet[Registered Phonepe users till Q{Quarter} {Year} : {totalUsers}]")
                      # Overall State Data - TOTAL APPOPENS - INDIA MAP
              st.markdown("## :violet[Overall Country Data - User App opening frequency]")
              mycursor.execute(f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by state")
              df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
              df1.Total_Appopens = df1.Total_Appopens.astype(float)
              fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                  featureidkey='properties.ST_NM',
                  locations='State',
                  color='Total_Appopens',
                  color_continuous_scale='sunset')
              fig.update_geos(fitbounds="locations", visible=False)
              st.plotly_chart(fig,use_container_width=True)
          with column2:
              mycursor.execute(f"SELECT sum(App_opens) FROM phonepe_pulse.map_user where year={Year} and Quarter={Quarter}")
              Total_appOpens=mycursor.fetchone()
              totalappOpens=format(Total_appOpens[0],",")
              st.markdown(f"### :violet[Phonepe app opens in Q{Quarter} {Year} : {totalappOpens}]")
              st.markdown("## :violet[Select any State to explore more]")
              selected_state = st.selectbox("",("Andaman & Nicobar","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh","Dadra & Nagar Haveli & Daman & Diu","Delhi","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu & Kashmir","Jharkhand","Karnataka","Kerala","Ladakh","Lakshadweep","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"),index=30)
              mycursor.execute(f"select State,year,quarter,District,sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,year,quarter order by state,district")
              df = pd.DataFrame(mycursor.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
              df.Total_Users = df.Total_Users.astype(int)
              fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
              st.plotly_chart(fig,use_container_width=True)         
