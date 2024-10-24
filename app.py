from model import Database
import streamlit as st
from gerador_pdf import EPI_PDF, ASO_PDF

st.set_page_config(layout='wide', initial_sidebar_state='auto')

def cpf_validate(numbers):
    #  Obtém os números do CPF e ignora outros caracteres
    cpf = [int(char) for char in numbers if char.isdigit()]

    #  Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    #  Verifica se o CPF tem todos os números iguais, ex: 111.111.111-11
    #  Esses CPFs são considerados inválidos mas passam na validação dos dígitos
    #  Antigo código para referência: if all(cpf[i] == cpf[i+1] for i in range (0, len(cpf)-1))
    if cpf == cpf[::-1]:
        return False

    #  Valida os dois dígitos verificadores
    for i in range(9, 11):
        value = sum((cpf[num] * ((i+1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return False
    return True

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

dados_cnpj = {
    'TECA SERVICOS E EMPREENDIMENTOS FLORESTAIS LTDA':{
        'rua':'R PRIMEIRO DE MAIO',
        'numero':'3 B',
        'complemento':'',
        'bairro':'JARDIM BOM JESUS',
        'municipio':'AGUA CLARA',
        'cep':'79.680-000',
        'uf':'MS',
        'telefone':'(67) 3239-1403',
        'email':'TECAFLORESTAL@UOL.COM.BR',
        'cnpj':'96.504.642.0001.05'
    },
    'G A BARBOZA LEITE LTDA':{
        'rua':'R RAIMUNDO DA COSTA',
        'numero':'SN',
        'complemento':'',
        'bairro':'SUBURBANO 3º ETAPA',
        'municipio':'NOVO ACORDO',
        'cep':'77.610-000',
        'uf':'TO',
        'telefone':'(63) 3215-3194',
        'email':'AUGUSTO.DAPLAN@GMAIL.COM',
        'cnpj':'43.962.797.0001.10'
    },
    'ALEXANDRE TADEU A. B. LEITE LTDA':{
        'rua':'R FRANCISCO VIEIRA',
        'numero':'159',
        'complemento':'ANDAR A',
        'bairro':'JARDIM PRIMAVERA',
        'municipio':'AGUA CLARA',
        'cep':'79.680-000',
        'uf':'MS',
        'telefone':'(67) 3239-1403',
        'email':'TECAFLORESTAL@UOL.COM.BR',
        'cnpj':'20.754.464.0001.09'
    }
}

db = Database()
pdf_epi = EPI_PDF()
pdf_aso = ASO_PDF(dados_cnpj)

st.title('Sistema de Gestão de Admissões')

cargos = db.get_cargos()
cargo_ids, cargo_nomes = zip(*cargos)
empresas = dados_cnpj.keys()

funcionario = {
    'nome': st.text_input('Nome do Colaborador'),
    'cpf': st.text_input('CPF do Colaborador', max_chars=11),
    'matricula': int(st.number_input('Matricula do colaborador', format="%0.0f")),
    'data_nascimento': st.date_input('Data de nascimento', format="DD/MM/YYYY"),
    'data_admissao': st.date_input('Data de Admissão', format="DD/MM/YYYY"),
    'cargo': st.selectbox('Selecione o Cargo', cargo_nomes),
    'empresa': st.selectbox('Selecione a empresa', empresas)
}

if cpf_validate(funcionario['cpf']):
    if st.button('Consultar'):
        cargo_id = funcionario['cargo']  # cargo_ids[cargo_nomes.index(cargo)]
        exames, epis, integracoes = buscar_requisitos(cargo_id)
        
        st.subheader('Exames Necessários')
        st.write(', '.join(exames))

        st.subheader('EPIs Necessários')
        st.write(epis)

        st.subheader('Integrações Necessárias')
        st.write(', '.join(integracoes))

        pdf_aso.create_pdf(funcionario, exames)
        pdf_epi.criar_pdf(funcionario,epis)

        with open("exemple.pdf", "rb") as f:
            if st.download_button(
                        label="Baixar Ficha de EPI PDF",
                        data=f,
                        file_name=f"relatorio_{funcionario['nome']}.pdf",
                        mime='application/pdf'
                    ):
                st.success('Relatório gerado com sucesso!')


        with open("aso_relatorio.pdf", "rb") as f:
            if st.download_button(
                        label="Baixar ASO PDF",
                        data=f,
                        file_name=f"ASO_{funcionario['nome']}.pdf",
                        mime='application/pdf'
                    ):
                st.success('Relatório gerado com sucesso!')