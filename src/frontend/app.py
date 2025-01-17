import pandas as pd
import requests
import streamlit as st

API_URL = 'http://controller:8000/api'


def get_items():
    response = requests.get(f'{API_URL}/items')
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f'Error: {response.status_code} - {response.text}')
        return []


def get_item(item_id):
    response = requests.get(f'{API_URL}/items/{item_id}')
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f'Error: {response.status_code} - {response.text}')
        return None


def create_item(data):
    response = requests.post(f'{API_URL}/items', json=data)
    if response.status_code == 201:
        return response.json()
    else:
        st.error(f'Error: {response.status_code} - {response.text}')
        return None


def update_item(item_id, data):
    response = requests.put(f'{API_URL}/items/{item_id}', json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f'Error: {response.status_code} - {response.text}')
        return None


def delete_item(item_id):
    response = requests.delete(f'{API_URL}/items/{item_id}')
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f'Error: {response.status_code} - {response.text}')
        return None


def get_movement_history(product_id):
    response = requests.get(f'{API_URL}/movements/{product_id}')
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f'Error: {response.status_code} - {response.text}')
        return []


st.title('Inventory Management')

menu = ['View Items', 'View Item', 'Add Item', 'Update Item', 'Delete Item', 'View Movement History']
choice = st.sidebar.selectbox('Menu', menu)

if choice == 'View Items':
    st.subheader('View Items')
    items = get_items()
    if items:
        df = pd.DataFrame(items)
        st.dataframe(df)

elif choice == 'View Item':
    st.subheader('View Item')
    item_id = st.number_input('Item ID', min_value=1, format='%d')
    if st.button('View Item'):
        item = get_item(item_id)
        if item:
            df = pd.DataFrame([item])
            st.dataframe(df)
        else:
            st.error('Item not found')

elif choice == 'Add Item':
    st.subheader('Add Item')
    produto = st.text_input('Product Name')
    unidade_medida = st.selectbox('Unit of Measure', ['litro', 'metro', 'quilograma', 'metro_cubico', 'quantidade'])
    custo_medio = st.number_input('Average Cost', min_value=0.0, format='%.2f')
    valor_venda = st.number_input('Sale Value', min_value=0.0, format='%.2f')
    estoque = st.number_input('Stock', min_value=0, format='%d')

    if st.button('Add Item'):
        data = {
            'produto': produto,
            'unidade_medida': unidade_medida,
            'custo_medio': custo_medio,
            'valor_venda': valor_venda,
            'estoque': estoque,
        }
        item = create_item(data)
        if item:
            st.success('Item added successfully')
            df = pd.DataFrame([item])
            st.dataframe(df)

elif choice == 'Update Item':
    st.subheader('Update Item')
    item_id = st.number_input('Item ID', min_value=1, format='%d')
    produto = st.text_input('Product Name')
    unidade_medida = st.selectbox('Unit of Measure', ['litro', 'metro', 'quilograma', 'metro_cubico', 'quantidade'])
    custo_medio = st.number_input('Average Cost', min_value=0.0, format='%.2f')
    valor_venda = st.number_input('Sale Value', min_value=0.0, format='%.2f')
    estoque = st.number_input('Stock', min_value=0, format='%d')

    if st.button('Update Item'):
        data = {
            'produto': produto,
            'unidade_medida': unidade_medida,
            'custo_medio': custo_medio,
            'valor_venda': valor_venda,
            'estoque': estoque,
        }
        item = update_item(item_id, data)
        if item:
            st.success('Item updated successfully')
            df = pd.DataFrame([item])
            st.dataframe(df)

elif choice == 'Delete Item':
    st.subheader('Delete Item')
    item_id = st.number_input('Item ID', min_value=1, format='%d')

    if st.button('Delete Item'):
        item = delete_item(item_id)
        if item:
            st.success('Item deleted successfully')

elif choice == 'View Movement History':
    st.subheader('View Movement History')
    product_id = st.number_input('Product ID', min_value=1, format='%d')
    if st.button('View Movement History'):
        movements = get_movement_history(product_id)
        if movements:
            df = pd.DataFrame(movements)
            st.dataframe(df)
        else:
            st.error('No movement history found for this product')
