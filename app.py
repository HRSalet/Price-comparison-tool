import serpapi
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="centered", page_title="Price Compare", page_icon="🔎",initial_sidebar_state="collapsed")

def compare_price(medicine_name):
    params = {
        "engine": "google_shopping",
        "q": medicine_name,
        "api_key": "04de13f030079597572e63a7b2bbe0dcbd64d750817c2f6925215048a2679aa4",
        "gl": "in"
    }
    search = serpapi.GoogleSearch(params)
    results = search.get_dict()
    shopping_results = results["shopping_results"]
    return shopping_results

c1,c2 = st.columns(2)
c1.image("e-pharmacy.jpg", width=300)
c2.header("E-pharmacy Price Comparison System")

st.sidebar.title("Enter name of medicine:")
medicine_name = st.sidebar.text_input("Enter name hear:")
numbers = st.sidebar.text_input("Enter number of options to show:")

medicine_company_list = []
medicine_price_list = []

if medicine_name is not None:
    if st.sidebar.button("Price Compare"):
        shopping_results = compare_price(medicine_name)
        lowest_price_str = (shopping_results[0].get("price"))[1:]
        lowest_price_float = float(lowest_price_str.replace(',',''))
        lowest_price_index = 0
        st.sidebar.image(shopping_results[0].get("thumbnail"), width=300)
        for i in range(int(numbers)):
            current_price_string = (shopping_results[i].get("price"))[1:]
            current_price_float = float(current_price_string.replace(',',''))

            medicine_company_list.append(shopping_results[i].get("source"))
            medicine_price_list.append(current_price_float)

            st.title(f"Option {i+1}")
            c1,c2 = st.columns(2)
            c1.write("Company")
            c2.write(shopping_results[i].get("source"))

            c1.write("Medicine Name")
            c2.write(shopping_results[i].get("title")[:30])

            c1.write("Price")
            c2.write(shopping_results[i].get("price"))

            url = shopping_results[i].get("product_link", "")
            c1.write("Buy Link:")
            if url:
                c2.markdown(f'<a href="{url}" target="_blank">Link</a>', unsafe_allow_html=True)
            else:
                c2.write("No link available")

            """______________________________________________________________"""
            
            if current_price_float < lowest_price_float:
                lowest_price_float = current_price_float
                lowest_price_index = i

        st.title("Best Option")
        c1,c2 = st.columns(2)
        c1.write("Company")
        c2.write(shopping_results[lowest_price_index].get("source"))

        c1.write("Name")
        c2.write(shopping_results[lowest_price_index].get("title"))

        c1.write("Price")
        c2.write(shopping_results[lowest_price_index].get("price"))

        url = shopping_results[lowest_price_index].get("product_link", "")
        c1.write("Buy Link:")
        if url:
            c2.markdown(f'<a href="{url}" target="_blank">Link</a>', unsafe_allow_html=True)
        else:
            c2.write("No link available")

        df = pd.DataFrame(medicine_price_list,medicine_company_list)
        st.title("Chart Comparison")
        st.bar_chart(df)

        fig1, ax1 = plt.subplots()
        ax1.pie(medicine_price_list, labels=medicine_company_list, startangle=90)
        ax1.axis("equal")
        st.pyplot(fig1)