from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(100, 10, 'TECA SERVIÇOS FLORESTAIS', 0, 0, 'C')
        self.cell(90, 10, 'CAUTELA DE CONTROLE DE EPI', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 10, 'Última Revisão: 25/05/2024    Revisão Nº: 003    PORTARIA 3.214/78 NR 06', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Página %s' % self.page_no(), 0, 0, 'C')

    def basic_info(self, nome, cargo, data_admissao):
        self.set_font('Arial', 'B', 10)
        self.cell(40, 6, 'NOME:', 1)
        self.cell(60, 6, nome, 1)
        self.cell(30, 6, 'CPF:', 1)
        self.cell(60, 6, '', 1, 1)

        self.cell(40, 6, 'MATRÍCULA:', 1)
        self.cell(60, 6, '', 1)
        self.cell(30, 6, 'FUNÇÃO:', 1)
        self.cell(60, 6, cargo, 1, 1)

        self.cell(40, 6, 'ADMISSÃO:', 1)
        self.cell(60, 6, data_admissao.strftime('%d/%m/%Y'), 1)
        self.cell(90, 6, 'DATA DE TRANSFERÊNCIA E/OU DEMISSÃO:', 1, 1)

        self.ln(5)

    def term_of_responsibility(self):
        self.set_font('Arial', '', 9)
        term = (
            "Declaro para todos os efeitos legais, que estou ciente das obrigações que passo a assumir com relação aos EPIs, "
            "constantes na Norma Regulamentadora 06 da Portaria 3.214/78 inscritas no subitem 6.6.1, a saber:\n"
            "a) usar o fornecido pela organização, observado o disposto no item 6.5.2;\n"
            "b) utilizar apenas para a finalidade a que se destina;\n"
            "c) responsabilizar-se pela limpeza, guarda e conservação;\n"
            "d) comunicar à organização quando extraviado, danificado ou qualquer alteração que o torne impróprio para uso; e\n"
            "e) cumprir as determinações da organização sobre o uso adequado.\n\n"
            "Me encontro ciente da disposição legal constante na NR 01..."
        )
        self.multi_cell(0, 5, term)
        self.ln(5)

    def sign_section(self):
        self.set_font('Arial', '', 10)
        self.cell(0, 6, 'Local: Chapadão do Céu / GO        Data: 14/05/2024        Assinatura: ', 1, 1)

    def table_header(self):
        self.set_font('Arial', 'B', 10)
        self.cell(20, 8, 'DATA', 1, 0, 'C')
        self.cell(15, 8, 'UND', 1, 0, 'C')
        self.cell(20, 8, 'QUANT', 1, 0, 'C')
        self.cell(65, 8, 'DESCRIÇÃO DO EPI', 1, 0, 'C')
        self.cell(20, 8, 'CA', 1, 0, 'C')
        self.cell(25, 8, 'MOTIVO', 1, 0, 'C')
        self.cell(35, 8, 'ASS. COLABORADOR (A)', 1, 0, 'C')
        self.cell(20, 8, 'DATA DEVOL.', 1, 0, 'C')
        self.cell(35, 8, 'ASS. RECEPTOR (A)', 1, 1, 'C')

    def table_rows(self, epis):
        self.set_font('Arial', '', 10)
        for epi in epis:
            self.cell(20, 8, '', 1)
            self.cell(15, 8, '', 1)
            self.cell(20, 8, '', 1)
            self.cell(65, 8, epi, 1)
            self.cell(20, 8, '', 1)
            self.cell(25, 8, '', 1)
            self.cell(35, 8, '', 1)
            self.cell(20, 8, '', 1)
            self.cell(35, 8, '', 1)
            self.ln()

    def observation_and_signatures(self):
        self.set_font('Arial', '', 10)
        self.cell(140, 8, 'Assinatura SESTR / RH:', 1)
        self.cell(90, 8, 'Assinatura do Colaborador (a):', 1, 1)
        self.cell(0, 8, 'Observação CA - Certificado de Aprovação do EPI pelo Mtb:', 1, 1)

    def criar_pdf(self, nome, cargo, data_admissao, epis):
        self.add_page()
        self.basic_info(nome, cargo, data_admissao)
        self.term_of_responsibility()
        self.sign_section()
        self.table_header()
        self.table_rows(epis)
        self.observation_and_signatures()
        self.output("exemple.pdf")