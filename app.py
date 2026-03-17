import streamlit as st
import serpapi
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    layout="centered", page_title="Price Compare", page_icon="🔎",
    initial_sidebar_state="collapsed")
# """--------------------------------------------------------------------------------------------------------------------------------------"""
def compare(name):
    params = {
    "engine": "google_shopping",
    "q": name,
    "api_key": "04de13f030079597572e63a7b2bbe0dcbd64d750817c2f6925215048a2679aa4",
    "gl" : "in"
    }

    search = serpapi.GoogleSearch(params)
    results = search.get_dict()
    shopping_results = results["shopping_results"]
    return(shopping_results)

# --------------------------------------------------------------------------------------------------------------------------------------"""

 #header
c1,c3 = st.columns(2)
c1.image("e_pharmacy.png", width= 200)
c3.header("E-Pharmacy Price compairsion system")

# """--------------------------------------------------------------------------------------------------------------------------------------"""
st.sidebar.title("Enter Name of Medicine:")
st.sidebar.markdown(" ")
st.sidebar.markdown(" ")

medicine_name=st.sidebar.text_input(
        "Enter Name here 👇"
    )
number=st.sidebar.text_input(
        "Enter Number of options here 👇"
    )
med_name=[]
med_price=[]
if medicine_name is not None:
    if st.sidebar.button("show compair"):
# """--------------------------------------------------------------------------------------------------------------------------------------"""
        inline_shopping_results=compare(medicine_name)
        st.sidebar.image(inline_shopping_results[0].get("thumbnail"))
        lowest_price=float(inline_shopping_results[0].get("price")[1:])
        lowest_price_index=0
# """--------------------------------------------------------------------------------------------------------------------------------------"""
        for i in range(int(number)):
            st.title(f"Option {i+1}")
            c1,c2 = st.columns(2)
            curent_price=float(inline_shopping_results[i].get("price")[1:])
            med_name.append(inline_shopping_results[i].get("source"))
            med_price.append(float((inline_shopping_results[i].get("price"))[1:10]))

            c1.write("Company ")
            c2.write(inline_shopping_results[i].get("source"))

            c1.write("Medicine Name")
            c2.write((inline_shopping_results[i].get("title"))[0:40])

            print(curent_price)
            print(lowest_price)
            lowest_price = min(curent_price,lowest_price)
            print(lowest_price)
            if curent_price <= lowest_price :
                lowest_price = curent_price
                print(lowest_price)
                lowest_price_index =i
                print(lowest_price_index)

            c1.write("Price")
            c2.write(inline_shopping_results[i].get("price"))

            url= inline_shopping_results[i].get("link")
            print(url)
            c1.write("BUY LINK ")
            c2.write("[link](%s)" % url)

            """-----------------------------------"""

        st.title("Best Option : ")
        i=lowest_price_index
        c1,c2 = st.columns(2)
        c1.write("Company ")
        c2.write(inline_shopping_results[i].get("source"))

        c1.write("Price")
        c2.write(inline_shopping_results[i].get("price"))

        url= inline_shopping_results[i].get("link")
        print(url)
        c1.write("BUY LINK ")
        c2.write("[link](%s)" % url)
        
        """-----------------------------------"""

        #graph comrasion 
        df=pd.DataFrame(med_price,med_name)
        st.title("Chart Comarasion : ")
        st.bar_chart(df)
        
        fig1, ax1 = plt.subplots()
        ax1.pie(med_price, labels=med_name,shadow=True, startangle=90)
        ax1.axis('equal') 
        st.pyplot(fig1)
