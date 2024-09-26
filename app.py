from model import Database
import streamlit as st
from fpdf import FPDF

db = Database()

def buscar_requisitos(cargo_id):
    exames_response = db.execute_query('SELECT nome FROM exames WHERE id IN (SELECT exame_id FROM cargo_exame WHERE cargo_id = ?)', (cargo_id,))
    exames = [row[0] for row in exames_response]

    epis_response = db.execute_query('SELECT nome FROM epis WHERE id IN (SELECT epi_id FROM cargo_epi WHERE cargo_id = ?)', (cargo_id,))
    epis = [row[0] for row in epis_response]

    integracoes_response = db.execute_query('SELECT nome FROM integracoes WHERE id IN (SELECT integracao_id FROM cargo_integracao WHERE cargo_id = ?)', (cargo_id,))
    integracoes = [row[0] for row in integracoes_response]

    return exames, epis, integracoes

def gerar_pdf(nome, data_admissao, cargo, exames, epis, integracoes):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)

    pdf.cell(200, 10, txt=f'Relatório de Admissão de {nome}', ln=True, align='C')
    pdf.cell(200, 10, txt=f'Data de Admissão: {data_admissao}', ln=True)
    pdf.cell(200, 10, txt=f'Cargo: {cargo}', ln=True)
    
    pdf.cell(200, 10, txt='Exames Necessários:', ln=True)
    for exame in exames:
        pdf.cell(200, 10, txt=f'- {exame}', ln=True)

    pdf.cell(200, 10, txt='EPIs Necessários:', ln=True)
    for epi in epis:
        pdf.cell(200, 10, txt=f'- {epi}', ln=True)

    pdf.cell(200, 10, txt='Integrações Necessárias:', ln=True)
    for integracao in integracoes:
        pdf.cell(200, 10, txt=f'- {integracao}', ln=True)

    pdf.output("example.pdf")

    return pdf

# Interface principal com Streamlit
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
    pdf = gerar_pdf(nome, data_admissao, cargo, exames, epis, integracoes)

    with open("example.pdf", "rb") as f:
        if st.download_button(
                    label="Baixar Relatório PDF",
                    data=f,
                    file_name=f"relatorio_{nome}.pdf",
                    mime='application/pdf'
                ):
            st.success('Relatório gerado com sucesso!')