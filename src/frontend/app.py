import pandas as pd
import requests
import streamlit as st

API_URL = 'http://controller:8000/api'


def get_items():
    """Fetch all items from the API.

    Returns:
        list: A list of items if the request is successful, otherwise an empty list.
    """
    response = requests.get(f'{API_URL}/items')
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f'Erro: {response.status_code} - {response.text}')
        return []


def get_item(item_id):
    """Fetch a single item by ID from the API.

    Args:
        item_id (int): The ID of the item to fetch.

    Returns:
        dict: The item data if the request is successful, otherwise None.
    """
    response = requests.get(f'{API_URL}/items/{item_id}')
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f'Erro: {response.status_code} - {response.text}')
        return None


def create_item(data):
    """Create a new item via the API.

    Args:
        data (dict): The item data to create.

    Returns:
        dict: The created item data if the request is successful, otherwise None.
    """
    response = requests.post(f'{API_URL}/items', json=data)
    if response.status_code == 201:
        return response.json()
    else:
        st.error(f'Erro: {response.status_code} - {response.text}')
        return None


def update_item(item_id, data):
    """Update an existing item via the API.

    Args:
        item_id (int): The ID of the item to update.
        data (dict): The updated item data.

    Returns:
        dict: The updated item data if the request is successful, otherwise None.
    """
    response = requests.put(f'{API_URL}/items/{item_id}', json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f'Erro: {response.status_code} - {response.text}')
        return None


def delete_item(item_id):
    """Delete an item by ID via the API.

    Args:
        item_id (int): The ID of the item to delete.

    Returns:
        dict: The deleted item data if the request is successful, otherwise None.
    """
    response = requests.delete(f'{API_URL}/items/{item_id}')
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f'Erro: {response.status_code} - {response.text}')
        return None


def get_movement_history(product_id):
    """Fetch the movement history for a product by ID from the API.

    Args:
        product_id (int): The ID of the product to fetch the movement history for.

    Returns:
        list: A list of movement history records if the request is successful, otherwise an empty list.
    """
    response = requests.get(f'{API_URL}/movements/{product_id}')
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f'Erro: {response.status_code} - {response.text}')
        return []


st.title('Gestão de Inventário')

menu = ['Ver Itens', 'Ver Item', 'Adicionar Item', 'Atualizar Item', 'Deletar Item', 'Ver Histórico de Movimentação']
choice = st.sidebar.selectbox('Menu', menu)

if choice == 'Ver Itens':
    st.subheader('Ver Itens')
    items = get_items()
    if items:
        df = pd.DataFrame(items)
        st.dataframe(df)

elif choice == 'Ver Item':
    st.subheader('Ver Item')
    item_id = st.number_input('ID do Item', min_value=1, format='%d')
    if st.button('Ver Item'):
        item = get_item(item_id)
        if item:
            df = pd.DataFrame([item])
            st.dataframe(df)

elif choice == 'Adicionar Item':
    st.subheader('Adicionar Item')
    produto = st.text_input('Nome do Produto')
    unidade_medida = st.selectbox('Unidade de Medida', ['litro', 'metro', 'quilograma', 'metro_cubico', 'quantidade'])
    custo_medio = st.number_input('Custo Médio', min_value=0.0, format='%.2f')
    valor_venda = st.number_input('Valor de Venda', min_value=0.0, format='%.2f')
    estoque = st.number_input('Estoque', min_value=0, format='%d')

    if st.button('Adicionar Item'):
        data = {
            'produto': produto,
            'unidade_medida': unidade_medida,
            'custo_medio': custo_medio,
            'valor_venda': valor_venda,
            'estoque': estoque,
        }
        item = create_item(data)
        if item:
            st.success('Item adicionado com sucesso')
            df = pd.DataFrame([item])
            st.dataframe(df)

elif choice == 'Atualizar Item':
    st.subheader('Atualizar Item')
    item_id = st.number_input('ID do Item', min_value=1, format='%d')
    produto = st.text_input('Nome do Produto')
    unidade_medida = st.selectbox('Unidade de Medida', ['litro', 'metro', 'quilograma', 'metro_cubico', 'quantidade'])
    custo_medio = st.number_input('Custo Médio', min_value=0.0, format='%.2f')
    valor_venda = st.number_input('Valor de Venda', min_value=0.0, format='%.2f')
    estoque = st.number_input('Estoque', min_value=0, format='%d')

    if st.button('Atualizar Item'):
        data = {
            'produto': produto,
            'unidade_medida': unidade_medida,
            'custo_medio': custo_medio,
            'valor_venda': valor_venda,
            'estoque': estoque,
        }
        item = update_item(item_id, data)
        if item:
            st.success('Item atualizado com sucesso')
            df = pd.DataFrame([item])
            st.dataframe(df)

elif choice == 'Deletar Item':
    st.subheader('Deletar Item')
    item_id = st.number_input('ID do Item', min_value=1, format='%d')

    if st.button('Deletar Item'):
        item = delete_item(item_id)
        if item:
            st.success('Item deletado com sucesso')

elif choice == 'Ver Histórico de Movimentação':
    st.subheader('Ver Histórico de Movimentação')
    product_id = st.number_input('ID do Produto', min_value=1, format='%d')
    if st.button('Ver Histórico de Movimentação'):
        movements = get_movement_history(product_id)
        if movements:
            df = pd.DataFrame(movements)
            st.dataframe(df)
