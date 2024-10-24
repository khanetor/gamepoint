import streamlit as st
import polars as pl

st.title("Game Point")

if "df" not in st.session_state:
    st.session_state["df"] = pl.DataFrame(schema={
        "name": pl.String,
        "phone": pl.String,
    })

if "cost" not in st.session_state:
    st.session_state["cost"] = 10

with st.form("price"):
    st.header("Price")
    price = st.number_input("Price", min_value=0, value=st.session_state["cost"])

    submitted = st.form_submit_button("Set", type="primary")

    if submitted:
        st.session_state["cost"] = price

with st.form("registration"):
    st.header("Sign up")

    name = st.text_input("Name")
    phone = st.text_input("MobilePay")

    submitted = st.form_submit_button("Sign up", type="primary")

    if submitted:
        st.session_state["df"] = st.session_state["df"].vstack(
            pl.DataFrame({"name": name, "phone": phone})
        ).unique()

if st.session_state["df"].shape[0] > 0:
    split = st.session_state["cost"] / st.session_state["df"].shape[0]
    st.dataframe(st.session_state["df"].with_columns(
        pl.lit(split).cast(pl.Decimal(4, 2)).alias("pay")
    ),
    use_container_width=True)
