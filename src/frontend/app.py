import pandas as pd
import requests
import streamlit as st

API_URL = 'http://backend:8000/api'


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
    if response.status_code == 200:
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

st.sidebar.title('Menu')
menu_options = {
    'Ver Itens': 'view_items',
    'Adicionar Item': 'add_item',
    'Atualizar Item': 'update_item',
    'Deletar Item': 'delete_item',
    'Histórico de Movimentação': 'view_movement_history',
}

# Inicializa o estado da sessão
if 'choice' not in st.session_state:
    st.session_state.choice = None

# Função para definir a escolha do menu
def set_choice(choice):
    st.session_state.choice = choice


# Cria os botões do menu
for option, value in menu_options.items():
    if st.sidebar.button(option, on_click=set_choice, args=(value,)):
        st.session_state.choice = value

choice = st.session_state.choice

if choice == 'view_items':
    st.subheader('Ver Itens')
    item_id = st.number_input('Busar item por ID', min_value=1, format='%d')
    if st.button('Buscar'):
        item = get_item(item_id)
        if item:
            df = pd.DataFrame([item])
            st.write(df.to_html(index=False), unsafe_allow_html=True)
    else:
        items = get_items()
        if items:
            df = pd.DataFrame(items)
            st.write(df.to_html(index=False), unsafe_allow_html=True)

elif choice == 'add_item':
    st.subheader('Adicionar Item')
    produto = st.text_input('Nome do Produto')
    unidade_medida = st.selectbox('Unidade de Medida', ['litro', 'metro', 'quilograma', 'metro_cubico', 'quantidade'])
    custo_medio = st.number_input('Custo Médio', min_value=0.0, format='%.2f')
    valor_venda = st.number_input('Valor de Venda', min_value=0.0, format='%.2f')
    if unidade_medida == 'quantidade':
        estoque = st.number_input('Estoque', min_value=0, format='%d')
    else:
        estoque = st.number_input('Estoque', min_value=0.0, format='%.2f')

    if st.button('Adicionar'):
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
            st.write(df.to_html(index=False), unsafe_allow_html=True)

elif choice == 'update_item':
    st.subheader('Atualizar Item')
    item_id = st.number_input('ID do Item', min_value=1, format='%d')
    if st.button('Buscar'):
        item = get_item(item_id)
        if item:
            st.session_state.item_to_update = item

    if 'item_to_update' in st.session_state:
        item = st.session_state.item_to_update
        produto = st.text_input('Nome do Produto', value=item['produto'])
        unidade_medida = st.selectbox(
            'Unidade de Medida',
            ['litro', 'metro', 'quilograma', 'metro_cubico', 'quantidade'],
            index=['litro', 'metro', 'quilograma', 'metro_cubico', 'quantidade'].index(item['unidade_medida']),
        )
        custo_medio = st.number_input('Custo Médio', min_value=0.0, format='%.2f', value=item['custo_medio'])
        valor_venda = st.number_input('Valor de Venda', min_value=0.0, format='%.2f', value=item['valor_venda'])
        if unidade_medida == 'quantidade':
            estoque = st.number_input('Estoque', min_value=0, format='%d', value=int(item['estoque']))
        else:
            estoque = st.number_input('Estoque', min_value=0.0, format='%.2f', value=item['estoque'])

        if st.button('Atualizar'):
            data = {
                'produto': produto,
                'unidade_medida': unidade_medida,
                'custo_medio': custo_medio,
                'valor_venda': valor_venda,
                'estoque': estoque,
            }
            updated_item = update_item(item_id, data)
            if updated_item:
                st.success('Item atualizado com sucesso')
                df = pd.DataFrame([updated_item])
                st.write(df.to_html(index=False), unsafe_allow_html=True)

elif choice == 'delete_item':
    st.subheader('Deletar Item')
    item_id = st.number_input('ID do Item', min_value=1, format='%d')

    if st.button('Deletar'):
        item = delete_item(item_id)
        if item:
            st.success('Item deletado com sucesso')

elif choice == 'view_movement_history':
    st.subheader('Ver Histórico de Movimentação')
    product_id = st.number_input('ID do Produto', min_value=1, format='%d')
    if st.button('Buscar'):
        movements = get_movement_history(product_id)
        if movements:
            df = pd.DataFrame(movements)
            st.write(df.to_html(index=False), unsafe_allow_html=True)
