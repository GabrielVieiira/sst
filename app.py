from model import Database
import streamlit as st
# from fpdf import FPDF
from gerador_pdf import PDF

db = Database()
pdf = PDF()

def buscar_requisitos(cargo_id):
    exames_response = db.execute_query('SELECT nome FROM exames WHERE id IN (SELECT exame_id FROM cargo_exame WHERE cargo_id = ?)', (cargo_id,))
    exames = [row[0] for row in exames_response]

    epis_response = db.execute_query('SELECT nome FROM epis WHERE id IN (SELECT epi_id FROM cargo_epi WHERE cargo_id = ?)', (cargo_id,))
    epis = [row[0] for row in epis_response]

    integracoes_response = db.execute_query('SELECT nome FROM integracoes WHERE id IN (SELECT integracao_id FROM cargo_integracao WHERE cargo_id = ?)', (cargo_id,))
    integracoes = [row[0] for row in integracoes_response]

    return exames, epis, integracoes


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
    st.write(', '.join(epis))

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