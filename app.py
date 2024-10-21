from model import Database
import streamlit as st
from gerador_pdf import PDF

db = Database()
pdf = PDF()

st.set_page_config(layout='wide', initial_sidebar_state='auto')

def buscar_requisitos(cargo_id):
    exames_response = db.execute_query('SELECT nome FROM exames WHERE id IN (SELECT exame_id FROM cargo_exame WHERE cargo_id = ?)', (cargo_id,))
    exames = [row[0] for row in exames_response]

    epis_response = db.execute_query('''
        SELECT  
            epis.nome, 
            epis.unidade,
            cargo_epi.quantidade
        FROM 
            epis
        INNER JOIN
            cargo_epi ON cargo_epi.epi_id = epis.id
        WHERE 
            cargo_epi.cargo_id = ?
    ''', (cargo_id,))

        # Formatar resposta dos EPIs como uma lista de dicionários
    epis = [{'nome': row[0], 'unidade': row[1], 'quantidade': row[2]} for row in epis_response]

    integracoes_response = db.execute_query('SELECT nome FROM integracoes WHERE id IN (SELECT integracao_id FROM cargo_integracao WHERE cargo_id = ?)', (cargo_id,))
    integracoes = [row[0] for row in integracoes_response]

    return exames, epis_response, integracoes


st.title('Sistema de Gestão de Admissões')

cargos = db.get_cargos()
cargo_ids, cargo_nomes = zip(*cargos)

nome = st.text_input('Nome do Colaborador')
data_admissao = st.date_input('Data de Admissão', format="DD/MM/YYYY")
cargo = st.selectbox('Selecione o Cargo', cargo_nomes)

if st.button('Consultar'):
    cargo_id = cargo  # cargo_ids[cargo_nomes.index(cargo)]
    exames, epis, integracoes = buscar_requisitos(cargo_id)
    
    st.subheader('Exames Necessários')
    st.write(', '.join(exames))

    st.subheader('EPIs Necessários')
    st.write(epis)

    st.subheader('Integrações Necessárias')
    st.write(', '.join(integracoes))
    pdf.criar_pdf(nome, cargo, data_admissao, epis)

    with open("exemple.pdf", "rb") as f:
        if st.download_button(
                    label="Baixar Relatório PDF",
                    data=f,
                    file_name=f"relatorio_{nome}.pdf",
                    mime='application/pdf'
                ):
            st.success('Relatório gerado com sucesso!')