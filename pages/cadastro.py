import streamlit as st
from app import db

def atualizar_requisitos(cargo_id, exames, epis, integracoes):

    db.execute_query('DELETE FROM cargo_exame WHERE cargo_id = ?', (cargo_id,))
    db.execute_query('DELETE FROM cargo_epi WHERE cargo_id = ?', (cargo_id,))
    db.execute_query('DELETE FROM cargo_integracao WHERE cargo_id = ?', (cargo_id,))

    for exame_id in exames:
        db.execute_query('INSERT INTO cargo_exame (cargo_id, exame_id) VALUES (?, ?)', (cargo_id, exame_id))

    for epi_id, quantidade in epis:
        db.execute_query('INSERT INTO cargo_epi (cargo_id, epi_id, quantidade) VALUES (?, ?, ?)', (cargo_id, epi_id, quantidade))

    for integracao_id in integracoes:
        db.execute_query('INSERT INTO cargo_integracao (cargo_id, integracao_id) VALUES (?, ?)', (cargo_id, integracao_id))

def buscar_requisitos(cargo_id):
    exames_ids = db.get_exames_por_cargo(cargo_id)
    epis_ids = db.get_epis_por_cargo(cargo_id)
    integracoes_ids = db.get_integracoes_por_cargo(cargo_id)
    return exames_ids, epis_ids, integracoes_ids

st.sidebar.title('Atualizar Cargo')

cargos = db.get_cargos()
cargo_ids, cargo_nomes = zip(*cargos)

cargo_selecionado = st.sidebar.selectbox('Selecione o Cargo', cargo_nomes, key=1)

cargo_id = cargo_selecionado #cargo_ids[cargo_nomes.index(cargo_selecionado)]
exames_selecionados, epis_selecionados, integracoes_selecionadas = buscar_requisitos(cargo_id)

exames_disponiveis = db.get_exame()
epis_disponiveis = db.get_epi()
integracoes_disponiveis = db.get_integracao()

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.subheader('Exames')
    exames_checkbox = [st.checkbox(exame, value=(i+1 in exames_selecionados)) for i, exame in enumerate(exames_disponiveis)]

with col2:
    st.subheader('EPIs')

    epis_checkbox = []
    epis_quantidades = []

    epi_ids_selecionados = [epi_id for epi_id, _ in epis_selecionados]
    epi_quantidades_salvas = {epi_id: quantidade for epi_id, quantidade in epis_selecionados}

    for i, epi in enumerate(epis_disponiveis):
        epi_id = i + 1
        selected = st.checkbox(epi, value=(epi_id in epi_ids_selecionados))
        epis_checkbox.append(selected)

        if selected:
            quantidade_inicial = epi_quantidades_salvas.get(epi_id, 1)
            quantidade = st.number_input(f'Quantidade de {epi}', min_value=1, step=1, value=quantidade_inicial, key=f'quantidade_{i}')
        else:
            quantidade = 0
        epis_quantidades.append(quantidade)

with col3:
    st.subheader('Integrações')
    integracoes_checkbox = [st.checkbox(integracao, value=(i+1 in integracoes_selecionadas)) for i, integracao in enumerate(integracoes_disponiveis)]

if st.button('Atualizar'):
    exames_ids = [i+1 for i, checked in enumerate(exames_checkbox) if checked]   
    epis_ids_quantidades = [(i+1, quantidade) for i, (checked, quantidade) in enumerate(zip(epis_checkbox, epis_quantidades)) if checked]
    integracoes_ids = [i+1 for i, checked in enumerate(integracoes_checkbox) if checked]
    
    atualizar_requisitos(cargo_selecionado, exames_ids, epis_ids_quantidades, integracoes_ids)
    st.success('Informações atualizadas com sucesso!')
