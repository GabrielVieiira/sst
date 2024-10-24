from fpdf import FPDF
from model import Database

db = Database()

class EPI_PDF(FPDF):

    def __init__(self):
        super().__init__()
        self.add_font('Calibri', '', 'fonts/calibri.ttf', uni=True)
        self.add_font('Calibri', 'B', 'fonts/calibrib.ttf', uni=True)
        self.add_font('Calibri', 'I', 'fonts/calibrii.ttf', uni=True)

    def header(self):
        self.image('logo_teca.png', 10, 8, 33)
        
        self.set_font('Calibri', 'B', 12)
        
        self.cell(84, 10, '', 0, 0, 'C')
        
        self.multi_cell(94, 10, 'TECA SERVIÇOS FLORESTAIS\nÚltima Revisão: 25/05/2024    Revisão Nº: 003', 0, 'C')
        
        self.set_xy(188, 8)
        self.multi_cell(94, 10, 'CAUTELA DE CONTROLE DE EQUIPAMENTO DE PROTEÇÃO INDIVIDUAL\nPORTARIA 3.214/78 NR 06', 0, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Calibri', 'I', 8)
        self.cell(0, 10, 'Página %s' % self.page_no(), 0, 0, 'C')

    def basic_info(self, funcionario):
        nome = funcionario['nome']
        cpf = funcionario['cpf']
        matricula = str(funcionario['matricula'])
        cargo = funcionario['cargo']
        data_admissao = funcionario['data_admissao'].strftime('%d/%m/%Y')


        self.set_font('Calibri', 'B', 11)
        self.cell(270/4, 6, 'NOME:', 1)
        self.set_font('Calibri', '', 11)
        self.cell(270/4, 6, nome, 1)

        self.set_font('Calibri', 'B', 11)
        self.cell(270/4, 6, 'CPF:', 1)
        self.set_font('Calibri', '', 11)
        self.cell(270/4, 6, cpf, 1, 1)

        self.set_font('Calibri', 'B', 11)
        self.cell(270/4, 6, 'MATRÍCULA:', 1)
        self.set_font('Calibri', '', 11)
        self.cell(270/4, 6, matricula, 1)

        self.set_font('Calibri', 'B', 11)
        self.cell(270/4, 6, 'FUNÇÃO:', 1)
        self.set_font('Calibri', '', 11)
        self.cell(270/4, 6, cargo, 1, 1)

        self.set_font('Calibri', 'B', 10)
        self.cell(270/4, 6, 'ADMISSÃO:', 1)
        self.set_font('Calibri', '', 10)
        self.cell(270/4, 6, data_admissao, 1)

        self.set_font('Calibri', 'B', 10)
        self.cell(135, 6, 'DATA DE TRANSFERÊNCIA E/OU DEMISSÃO:', 1, 1)

        self.ln(5)

    def term_of_responsibility(self):
        self.set_font('Calibri', '', 10)
        term = (
            "Declaro para todos os efeitos legais, que estou ciente das obrigações que passo a assumir com relação aos EPIs, "
            "constantes na Norma Regulamentadora 06 da Portaria 3.214/78 inscritas no subitem 6.6.1, a saber:\n"
            "a) usar o fornecido pela organização, observado o disposto no item 6.5.2;\n"
            "b) utilizar apenas para a finalidade a que se destina;\n"
            "c) responsabilizar-se pela limpeza, guarda e conservação;\n"
            "d) comunicar à organização quando extraviado, danificado ou qualquer alteração que o torne impróprio para uso; e\n"
            "e) cumprir as determinações da organização sobre o uso adequado.\n\n"
        )
        self.multi_cell(277, 5, term, 1)
        
        self.set_font('Calibri', 'B', 10)
        self.multi_cell(277, 6, 'Me encontro ciente da disposição legal constante na NR 01, principalmente do subitem 1.9.1 de que constitui ato faltoso a recusa injustificada de usar EPI fornecido pela empresa, incorrendo nas penalidades previstas pela lei.', 1)

        self.set_font('Calibri', '', 10)
        self.multi_cell(277, 6, 'Declaro ter RECEBIDO gratuitamente da empresa TECA SERVIÇOS FLORESTAIS os Equipamentos de Proteção Individual descritos abaixo, conforme relata o artigo 166 da seção IV do capítulo V da CLT e recebi ORIENTAÇÃO quanto ao uso correto, de higienização e conservação conforme NR 06. E que estou CIENTE da obrigatoriedade do seu USO CORRETO para proteção da minha integridade física, comprometendo-me a devolvê-lo a empresa, no término do meu contrato de trabalho e pedido de demissão, assim como a indenização em caso de dano ou perda.', 1)

        self.ln(5)

    def sign_section(self,data_admissao):
        data = data_admissao.strftime('%d/%m/%Y')
        self.set_font('Calibri', 'B', 12)
        self.cell(0, 6, f'Local: Campo Grande / MS        Data: {data}        Assinatura: ', 1, 1)

    def table_header(self):
        self.set_font('Calibri', 'B', 10)
        
        self.cell(20, 8, 'DATA', 1, 0, 'C')
        self.cell(10, 8, 'UND', 1, 0, 'C') 
        self.cell(25, 8, 'QUANTIDADE', 1, 0, 'C')
        self.cell(75, 8, 'DESCRIÇÃO DO EPI', 1, 0, 'C')
        self.cell(15, 8, 'CA', 1, 0, 'C')
        self.cell(15, 8, 'MOTIVO', 1, 0, 'C')
        self.cell(45, 8, 'ASS. COLABORADOR (A)', 1, 0, 'C')
        self.cell(35, 8, 'DATA DEVOLUÇÃO', 1, 0, 'C')
        self.cell(37, 8, 'ASS. RECEPTOR (A)', 1, 1, 'C')

    def table_rows(self, epis, data_admissao):
        self.set_font('Calibri', '', 8)
        for epi in epis:
            self.cell(20, 8, data_admissao.strftime('%d/%m/%Y'), 1, align='C')
            self.cell(10, 8, epi[1], 1, align='C')
            self.cell(25, 8, str(epi[2]), 1, align='C')
            self.cell(75, 8, epi[0], 1, align='C')
            self.cell(15, 8, '', 1, align='C')
            self.cell(15, 8, '', 1, align='C')
            self.cell(45, 8, '', 1, align='C')
            self.cell(35, 8, '', 1, align='C')
            self.cell(37, 8, '', 1, align='C')
            self.ln()

    def observation_and_signatures(self):
        self.set_font('Calibri', '', 10)
        self.cell(138, 8, 'Assinatura SESTR / RH:', 1)
        self.cell(139, 8, 'Assinatura do Colaborador (a):', 1, 1)
        self.cell(277, 8, 'Observação CA - Certificado de Aprovação do EPI pelo Mtb:', 1, 1)

    def criar_pdf(self, funcionario, epis):
        data_admissao = funcionario['data_admissao']
        self.add_page(orientation='L')
        self.basic_info(funcionario)
        self.term_of_responsibility()
        self.sign_section(data_admissao)
        self.table_header()
        self.table_rows(epis, data_admissao)
        self.observation_and_signatures()
        self.output("exemple.pdf")


class ASO_PDF(FPDF):

    def __init__(self, cnpj_info):
        super().__init__()
        self.add_font('Calibri', '', 'fonts/calibri.ttf', uni=True)
        self.add_font('Calibri', 'B', 'fonts/calibrib.ttf', uni=True)
        self.add_font('Calibri', 'I', 'fonts/calibrii.ttf', uni=True)
        self.cnpj_info = cnpj_info

    def header(self):
        # Cabeçalho com logo e título
        # self.image('logo.png', 10, 8, 33)
        self.set_font('Calibri', 'B', 12)
        self.cell(0, 10, 'ASO - ATESTADO DE SAUDE OCUPACIONAL', ln=True, align='C')
        self.ln(10)

    def footer(self):
        # Rodapé com número da página
        self.set_y(-15)
        self.set_font('Calibri', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def add_company_section(self, empresa):
        # Recupera os dados da empresa selecionada
        dados_empresa = self.cnpj_info.get(empresa)
        
        if dados_empresa:
            # Seção de empresa
            self.set_font('Calibri', 'B', 11)
            self.cell(0, 10, 'Empresa', ln=True)
            self.set_font('Calibri', '', 10)
            
            # Preenche as informações da empresa a partir do dicionário
            razao_social = empresa
            cnpj = dados_empresa['cnpj']
            endereco = f"{dados_empresa['rua']}, {dados_empresa['numero']} {dados_empresa['complemento']}".strip()
            bairro = dados_empresa['bairro']
            cidade = dados_empresa['municipio']
            uf = dados_empresa['uf']
            cep = dados_empresa['cep']
            telefone = dados_empresa['telefone']
            email = dados_empresa['email']
            
            # Imprime as informações no PDF
            self.cell(0, 10, f'Razão Social: {razao_social}', ln=True)
            self.cell(0, 10, f'CNPJ: {cnpj}', ln=True)
            self.cell(0, 10, f'Endereço: {endereco}, Bairro: {bairro}', ln=True)
            self.cell(0, 10, f'Cidade / UF: {cidade} / {uf}  CEP: {cep}', ln=True)
            self.cell(0, 10, f'Telefone: {telefone}  Email: {email}', ln=True)
        else:
            self.cell(0, 10, 'Empresa não encontrada!', ln=True)

    def add_employee_section(self, funcionario):
        # Seção de informações do funcionário
        self.ln(10)
        self.set_font('Calibri', 'B', 11)
        self.cell(0, 10, 'Funcionário', ln=True)
        
        self.set_font('Calibri', '', 10)
        nome = funcionario.get('nome', 'N/A')
        matricula = funcionario.get('matricula', 'N/A')
        cpf = funcionario.get('cpf', 'N/A')
        data_nascimento = funcionario.get('data_nascimento', 'N/A').strftime('%d/%m/%Y') if funcionario.get('data_nascimento') else 'N/A'
        cargo = funcionario.get('cargo', 'N/A')
        
        # Imprimindo as informações no PDF
        self.cell(0, 10, f'Nome: {nome}', ln=True)
        self.cell(0, 10, f'Código: {matricula}  CPF: {cpf}', ln=True)
        self.cell(0, 10, f'Data de Nascimento: {data_nascimento}', ln=True)
        self.cell(0, 10, f'Função: {cargo}', ln=True)

    def add_doctor_section(self,):
        # Seção de médico responsável
        self.ln(10)
        self.set_font('Calibri', 'B', 11)
        self.cell(0, 10, 'Médico Responsável pelo PCMSO', ln=True)
        self.set_font('Calibri', '', 10)
        self.cell(0, 10, f'Nome: IVAN LUCIO COSTA OLAIA', ln=True)
        self.cell(0, 10, f'CRM: 3877PSP', ln=True)
        self.cell(0, 10, f'Endereço: Praça 20 de Setembro, 122, Piso Superior', ln=True)
        self.cell(0, 10, f'Bairro: Centro', ln=True)
        self.cell(0, 10, f'Cidade/UF: Itapeva/SP', ln=True)
        self.cell(0, 10, f'Telefone: (15) 3521-4169', ln=True)

    def add_risks_section(self):
        riscos = (
            'Físicos: Radiações não ionizantes, Ruído Abaixo do Nível de Ação.\n'
            'Químicos: Flumioxazina, Glifosato, Imazapyr, Sulfuramida.\n'
            'Ergonômicos: Aspectos Ergonomicos - Leves.\n'
            'Acidentes: Ataque de animal peçonhento ou insetos, colisão...'
        )

        self.ln(10)
        self.set_font('Calibri', 'B', 11)
        self.cell(0, 10, 'Perigos / Fatores de Risco', ln=True)
        self.set_font('Calibri', '', 10)
        self.multi_cell(0, 10, riscos)

    def add_exam_section(self, exames):
        # Seção de avaliação clínica e exames
        self.ln(10)
        self.set_font('Calibri', 'B', 11)
        self.cell(0, 10, 'Avaliação Clínica e Exames Realizados', ln=True)
        
        self.set_font('Calibri', '', 10)
        
        # Iterando sobre a lista de exames
        for exame in exames:
            self.cell(0, 10, f'____/____/____ {exame}', ln=True)

    def add_final_section(self,):
        apto,inapto = ['Sim', 'Não']

        self.ln(10)
        self.set_font('Calibri', 'B', 11)
        self.cell(0, 10, 'Parecer', ln=True)
        self.set_font('Calibri', '', 10)
        apto_inapto = f'Apto Para Função: {apto}  Inapto Para Função: {inapto}'
        self.multi_cell(0, 10, apto_inapto)

    def create_pdf(self, funcionario, exames):
        self.add_page()
        self.add_company_section(funcionario['empresa'])
        self.add_employee_section(funcionario)
        self.add_doctor_section()
        self.add_risks_section()
        self.add_exam_section(exames)
        self.add_final_section()
        self.output('aso_relatorio.pdf')