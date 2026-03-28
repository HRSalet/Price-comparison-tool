import streamlit as st
import serpapi
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    layout="centered", page_title="Price Compare", page_icon="🔎",
    initial_sidebar_state="collapsed")

def compare(name):
    params = {
        "engine": "google_shopping",
        "q": name,
        "api_key": "04de13f030079597572e63a7b2bbe0dcbd64d750817c2f6925215048a2679aa4",
        "gl": "in"
    }

    search = serpapi.GoogleSearch(params)
    results = search.get_dict()
    shopping_results = results["shopping_results"]
    return shopping_results

c1, c3 = st.columns(2)
c1.image("shopping.png", width=200)
c3.header("Price Comparison System")

st.sidebar.title("Enter Name of Product:")
st.sidebar.markdown(" ")
st.sidebar.markdown(" ")

product_name = st.sidebar.text_input("Enter Name here")
number = st.sidebar.text_input("Enter Number of options here")

prod_name = []
prod_price = []

if product_name is not None:
    if st.sidebar.button("Show Price Compare"):

        inline_shopping_results = compare(product_name)
        st.sidebar.image(inline_shopping_results[0].get("thumbnail"))
        lowest_price = float(inline_shopping_results[0].get("price").replace("₹","").replace(",",""))
        lowest_price_index = 0

        for i in range(int(number)):
            st.title(f"Option {i + 1}")
            c1, c2 = st.columns(2)
            current_price = float(inline_shopping_results[i].get("price").replace("₹","").replace(",",""))
            prod_name.append(inline_shopping_results[i].get("source"))
            prod_price.append(float(inline_shopping_results[i].get("price").replace("₹","").replace(",","")))

            c1.write("Company ")
            c2.write(inline_shopping_results[i].get("source"))

            c1.write("Product Name")
            c2.write((inline_shopping_results[i].get("title"))[0:40])

            print(current_price)
            print(lowest_price)
            lowest_price = min(current_price, lowest_price)
            print(lowest_price)
            if current_price <= lowest_price:
                lowest_price = current_price
                print(lowest_price)
                lowest_price_index = i
                print(lowest_price_index)

            c1.write("Price")
            c2.write(inline_shopping_results[i].get("price"))

            url = inline_shopping_results[i].get("product_link")
            print(url)
            c1.write("Buy Link")
            c2.markdown(f'<a href="{url}" target="_blank">LINK</a>', unsafe_allow_html=True)

        st.title("Best Option : ")
        i = lowest_price_index
        c1, c2 = st.columns(2)
        c1.write("Company ")
        c2.write(inline_shopping_results[i].get("source"))

        c1.write("Price")
        c2.write(inline_shopping_results[i].get("price"))

        url = inline_shopping_results[i].get("product_link")
        print(url)
        c1.write("Buy Link")
        c2.markdown(f'<a href="{url}" target="_blank">LINK</a>', unsafe_allow_html=True)

        df = pd.DataFrame(prod_price, prod_name)
        st.title("Chart Comparison : ")
        st.bar_chart(df)

        fig1, ax1 = plt.subplots()
        ax1.pie(prod_price, labels=prod_name, startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)