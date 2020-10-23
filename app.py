from streamlit_session_state import get, reset
import streamlit as st
import pandas as pd
import numpy as np


st.beta_set_page_config('Pizza Time', page_icon=":pizza:", layout="wide")


session_state = get(dfs={})
num_comps = st.sidebar.slider("Number of Comparisons", min_value=2, max_value=10, step=1)

st.header("Pizza Compare")
compared_data = st.empty()

cols = st.beta_columns(num_comps)

dfs  = session_state.dfs


for idx, c in enumerate(cols):
    idx = str(idx)
    with c:
        diameter = st.number_input("Diameter?", key=f"{idx}diameter")
        price = st.number_input("Price?", key=f"{idx}price", min_value=0.01)
        quantity = st.number_input("Quantity?", key=f"{idx}quantity", min_value=1, step=1)

        diameter = round(diameter, 2)
        price = round(price, 2)


        submit = st.button("add pizza", key=idx)
        if submit:
            if any(dfs.get(idx, [False])):
                dfs[idx] = dfs[idx].append({
                    'diameter': diameter, 
                    'price': price,
                    'pizza place': idx,
                    'area per $ per pizza': np.pi * diameter**2 / price,
                    'area per $': quantity * np.pi * diameter**2 / price,
                    }, 
                    ignore_index=True)
            else:
                dfs[idx] = pd.DataFrame(
                        {
                            'diameter': [diameter], 
                            'price': [price],
                            'pizza place': [idx],
                            'area per $ per pizza': np.pi * diameter**2 / price,
                            'area per $': quantity * np.pi * diameter**2 / price,
                        }, 
                        index=None)

        st.text(f'pizza place #{idx}')


if any(dfs):
    combined_df = pd.concat(dfs).reset_index(drop=True).sort_values('area per $ per pizza', ascending=False)
    compared_data.write(combined_df)
    st.write(combined_df.groupby(by='pizza place')['area per $'].sum())



session_state = get(dfs=dfs)



