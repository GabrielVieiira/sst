from fpdf import FPDF
from model import Database
import re

db = Database()


class EPI_PDF(FPDF):

    def __init__(self):
        super().__init__()
        self.add_font("Calibri", "", "fonts/calibri.ttf", uni=True)
        self.add_font("Calibri", "B", "fonts/calibrib.ttf", uni=True)
        self.add_font("Calibri", "I", "fonts/calibrii.ttf", uni=True)

    def header(self):
        self.image("logo_teca.png", 10, 8, 33)

        self.set_font("Calibri", "B", 12)

        self.cell(84, 10, "", 0, 0, "C")

        self.multi_cell(
            94,
            10,
            "TECA SERVIÇOS FLORESTAIS\nÚltima Revisão: 25/05/2024    Revisão Nº: 003",
            0,
            "C",
        )

        self.set_xy(188, 8)
        self.multi_cell(
            94,
            10,
            "CAUTELA DE CONTROLE DE EQUIPAMENTO DE PROTEÇÃO INDIVIDUAL\nPORTARIA 3.214/78 NR 06",
            0,
            "C",
        )

    def footer(self):
        self.set_y(-15)
        self.set_font("Calibri", "I", 8)
        self.cell(0, 10, "Página %s" % self.page_no(), 0, 0, "C")

    def basic_info(self, funcionario):
        nome = funcionario["nome"]
        cpf = funcionario["cpf"]
        cpf_formatado = re.sub(r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\4', cpf)
        matricula = str(funcionario["matricula"])
        cargo = funcionario["cargo"]
        data_admissao = funcionario["data_admissao"].strftime("%d/%m/%Y")

        self.set_font("Calibri", "B", 11)
        self.cell(270 / 4-50, 6, "NOME:",'LTB')
        self.set_font("Calibri", "", 11)
        self.cell(270 / 4+50, 6, nome, 'RTB')

        self.set_font("Calibri", "B", 11)
        self.cell(270 / 4-60, 6, "CPF:",'LTB')
        self.set_font("Calibri", "", 11)
        self.cell(270 / 4+60, 6, cpf_formatado, 'RTB', 1)

        self.set_font("Calibri", "B", 11)
        self.cell(270 / 4-40, 6, "MATRÍCULA:",'LTB')
        self.set_font("Calibri", "", 11)
        self.cell(270 / 4+40, 6, matricula, 'RTB')

        self.set_font("Calibri", "B", 11)
        self.cell(270 / 4-50, 6, "FUNÇÃO:",'LTB')
        self.set_font("Calibri", "", 11)
        self.cell(270 / 4+50, 6, cargo, 'RTB', 1)

        self.set_font("Calibri", "B", 10)
        self.cell(270 / 4-45, 6, "ADMISSÃO:",'LTB')
        self.set_font("Calibri", "", 10)
        self.cell(270 / 4+45, 6, data_admissao,'RTB')

        self.set_font("Calibri", "B", 10)
        self.cell(135, 6, "DATA DE TRANSFERÊNCIA E/OU DEMISSÃO:", 1, 1)

        self.ln(5)

    def term_of_responsibility(self):
        self.set_font("Calibri", "", 10)
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

        self.set_font("Calibri", "B", 10)
        self.multi_cell(
            277,
            6,
            "Me encontro ciente da disposição legal constante na NR 01, principalmente do subitem 1.9.1 de que constitui ato faltoso a recusa injustificada de usar EPI fornecido pela empresa, incorrendo nas penalidades previstas pela lei.",
            1,
        )

        self.set_font("Calibri", "", 10)
        self.multi_cell(
            277,
            6,
            "Declaro ter RECEBIDO gratuitamente da empresa TECA SERVIÇOS FLORESTAIS os Equipamentos de Proteção Individual descritos abaixo, conforme relata o artigo 166 da seção IV do capítulo V da CLT e recebi ORIENTAÇÃO quanto ao uso correto, de higienização e conservação conforme NR 06. E que estou CIENTE da obrigatoriedade do seu USO CORRETO para proteção da minha integridade física, comprometendo-me a devolvê-lo a empresa, no término do meu contrato de trabalho e pedido de demissão, assim como a indenização em caso de dano ou perda.",
            1,
        )

        self.ln(5)

    def sign_section(self, data_admissao):
        data = data_admissao.strftime("%d/%m/%Y")
        self.set_font("Calibri", "B", 12)
        self.cell(
            0,
            6,
            f"Local: Campo Grande / MS        Data: {data}        Assinatura: ",
            1,
            1,
        )

    def table_header(self):
        self.set_font("Calibri", "B", 10)

        self.cell(20, 8, "DATA", 1, 0, "C")
        self.cell(10, 8, "UND", 1, 0, "C")
        self.cell(25, 8, "QUANTIDADE", 1, 0, "C")
        self.cell(75, 8, "DESCRIÇÃO DO EPI", 1, 0, "C")
        self.cell(15, 8, "CA", 1, 0, "C")
        self.cell(15, 8, "MOTIVO", 1, 0, "C")
        self.cell(45, 8, "ASS. COLABORADOR (A)", 1, 0, "C")
        self.cell(35, 8, "DATA DEVOLUÇÃO", 1, 0, "C")
        self.cell(37, 8, "ASS. RECEPTOR (A)", 1, 1, "C")

    def table_rows(self, epis, data_admissao):
        self.set_font("Calibri", "", 8)
        for epi in epis:
            self.cell(20, 8, data_admissao.strftime("%d/%m/%Y"), 1, align="C")
            self.cell(10, 8, epi[1], 1, align="C")
            self.cell(25, 8, str(epi[2]), 1, align="C")
            self.cell(75, 8, epi[0], 1, align="C")
            self.cell(15, 8, "", 1, align="C")
            self.cell(15, 8, "", 1, align="C")
            self.cell(45, 8, "", 1, align="C")
            self.cell(35, 8, "", 1, align="C")
            self.cell(37, 8, "", 1, align="C")
            self.ln()

    def observation_and_signatures(self):
        self.set_font("Calibri", "", 10)
        self.cell(138, 8, "Assinatura SESTR / RH:", 1)
        self.cell(139, 8, "Assinatura do Colaborador (a):", 1, 1)
        self.cell(
            277, 8, "Observação CA - Certificado de Aprovação do EPI pelo Mtb:", 1, 1
        )

    def criar_pdf(self, funcionario, epis):
        data_admissao = funcionario["data_admissao"]
        self.add_page(orientation="L")
        self.basic_info(funcionario)
        self.term_of_responsibility()
        self.sign_section(data_admissao)
        self.table_header()
        self.table_rows(epis, data_admissao)
        self.observation_and_signatures()
        self.output("exemple.pdf")


class ASO_PDF(FPDF):

    def __init__(self, cnpj_info, funcoes_riscos):
        super().__init__()
        self.add_font("Verdana", "", "fonts/verdana.ttf", uni=True)
        self.add_font("Verdana", "B", "fonts/verdanab.ttf", uni=True)
        self.add_font("Verdana", "I", "fonts/verdanai.ttf", uni=True)
        self.cnpj_info = cnpj_info
        self.riscos = funcoes_riscos
        self.largura = 190

    def header(self):
        altura = 32
        self.image('logo_pcmso.png', 10, 8, 33)
        self.set_font("Verdana", "B", 10)
        self.cell(self.largura, altura, "ASO - ATESTADO DE SAUDE OCUPACIONAL",1,True,"C")
        self.ln(1)    

    def footer(self):
        # Rodapé com número da página
        self.set_y(-15)
        self.set_font("Verdana", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

    def add_company_section(self, empresa):
        altura = 4.3
        dados_empresa = self.cnpj_info.get(empresa)


        if dados_empresa:

            self.set_font("Verdana", "B", 8)
            self.set_fill_color(237, 237, 237)
            self.cell(self.largura, altura, "Empresa",1, True, "L", 1)
            self.set_font("Verdana", "", 8)

            razao_social = empresa
            cnpj = dados_empresa["cnpj"]
            endereco = f"{dados_empresa['rua']}, {dados_empresa['numero']} {dados_empresa['complemento']}".strip()
            bairro = dados_empresa["bairro"]
            cidade = dados_empresa["municipio"]
            uf = dados_empresa["uf"]
            cep = dados_empresa["cep"]
            telefone = dados_empresa["telefone"]
            email = dados_empresa["email"]


            empresa_info = (
                f'Razão Social: {razao_social}\n'
                f"CNPJ: {cnpj}\n"
                f"Endereço: {endereco}\n"
                f"Bairro: {bairro}\n"
                f"Cidade / UF: {cidade} / {uf}  CEP: {cep}\n"
                f"Telefone: {telefone}  Email: {email}"
            )

            self.multi_cell(self.largura, altura, empresa_info, 1, 'L')
        else:
            self.cell(0, 10, "Empresa não encontrada!", ln=True)
        self.ln(1) 

    def add_employee_section(self, funcionario):
        altura = 4.3
        self.set_font("Verdana", "B", 8)
        self.set_fill_color(237, 237, 237)
        self.cell(self.largura, altura, "Funcionário", 1, True, "L", 1)

        self.set_font("Verdana", "", 8)
        nome = funcionario.get("nome", "N/A")
        matricula = funcionario.get("matricula", "N/A")
        cpf = funcionario.get("cpf", "N/A")
        cpf_formatado = re.sub(r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\4', cpf)
        data_nascimento = (
            funcionario.get("data_nascimento", "N/A").strftime("%d/%m/%Y")
            if funcionario.get("data_nascimento")
            else "N/A"
        )
        cargo = funcionario.get("cargo", "N/A")

        funcionario_info = (
            f"Nome: {nome}\n"
            f"Código: {matricula}\n"
            f"CPF: {cpf_formatado}\n"
            f"Data de Nascimento: {data_nascimento}\n"
            f"Função: {cargo}"
        )

        self.multi_cell(self.largura, altura, funcionario_info, 1, 'L')
        self.ln(1) 

    def add_doctor_section(
        self,
    ):
        altura = 4.3
        self.set_font("Verdana", "B", 8)
        self.set_fill_color(237, 237, 237)
        self.cell(self.largura, altura, "Médico Responsável pelo PCMSO" ,1, True, "L", 1)

        medico_info = (
            f"Nome: IVAN LUCIO COSTA OLAIA\n"
            f"CRM: 3877PSP\n"
            f"Endereço: Praça 20 de Setembro, 122, Piso Superior\n"
            f"Bairro: Centro\n"
            f"Cidade/UF: Itapeva/SP\n"
            f"Telefone: (15) 3521-4169"

        )
        self.set_font("Verdana", "", 8)
        self.multi_cell(self.largura, altura, medico_info, 1, 'L')
        self.ln(1) 

    def add_risks_section(self, cargo):
        riscos_da_funcao = self.riscos.get(cargo)

        if riscos_da_funcao:
            altura = 5
            self.set_font("Verdana", "B", 8)
            self.set_fill_color(237, 237, 237)
            self.cell(self.largura, altura, "Perigos / Fatores de Risco", 1, True, "L", 1)
            self.set_font("Verdana", "", 8)

            riscos_fisicos = riscos_da_funcao["Risco Fisico"]
            riscos_quimicos = riscos_da_funcao["Risco Químico"]
            riscos_ergonomicos = riscos_da_funcao["Risco Ergonômico"]
            acidentes = riscos_da_funcao["Acidente"]

            riscos = (
                f"Físicos: {riscos_fisicos}\n"
                f"Químicos: {riscos_quimicos}\n"
                f"Ergonômicos: {riscos_ergonomicos}\n"
                f"Acidentes: {acidentes}"
            )

            self.set_font("Verdana", "", 8)
            self.multi_cell(self.largura, altura, riscos, 1, 'L')
        else:
            self.cell(0, 10, "Riscos não encontrados!", ln=True)
        self.ln(1) 

    def add_tipo_exame(self,):
        altura = 4.3
        self.set_font("Verdana", "B", 8)
        self.set_fill_color(237, 237, 237)
        self.multi_cell(self.largura, altura, "EM CUMPRIMENTO ÀS PORTARIAS NºS 3214/78, 3164/82, 12/83, 24/94 E 08/96 NR7 DO MINISTÉRIO DO TRABALHO E EMPREGO PARA FINS DE EXAME:", 1, "L", 1)
        self.set_font("Verdana", "", 8)

        self.cell(self.largura, altura, "Admissional", 1, True, "L")
        self.ln(1) 

    def add_exam_section(self, exames):
        altura = 5
        self.set_font("Verdana", "B", 8)
        self.set_fill_color(237, 237, 237)
        self.cell(self.largura, altura, "Avaliação Clínica e Exames Realizados", 1, True, "L", 1)
        self.set_font("Verdana", "", 8)

        exames_str = "\n".join(f"____/____/____ {exame}" for exame in exames)

        self.multi_cell(self.largura, altura, exames_str, 1, 'L')
        self.ln(1)

    def add_final_section(self, funcionario):
        altura = 4.3
        self.set_font("Verdana", "B", 8)
        self.set_fill_color(237, 237, 237)
        self.cell(self.largura, altura, "Parecer", 1, True, "L", 1)

        self.set_font("Verdana", "", 8)

        tamanho_quadrado = 3

        self.cell(self.largura / 4, 6, "Apto:", "LTB")
        y = self.get_y()
        self.rect(20,y+1,tamanho_quadrado,tamanho_quadrado)
        self.cell(self.largura - 47.5 , 6, "Inapto:", "RTB")
        y = self.get_y()
        x = 70
        self.rect(x,y+1,tamanho_quadrado,tamanho_quadrado)
        self.ln(20)

        y = self.get_y() + 3
        tamanho_linha = 50
        x = self.get_x()
        self.line(x, y, x + tamanho_linha, y)


        self.cell(0, 10, 'Médico / CRM', 0, 1, 'L')
        self.ln(15)

        y = self.get_y() + 3
        tamanho_linha = 50
        x = self.get_x()
        self.line(x, y, x + tamanho_linha, y)
        self.cell(0, 10, funcionario, 0, 1, 'L')


    def create_pdf(self, funcionario, exames):
        self.add_page()
        self.add_company_section(funcionario["empresa"])
        self.add_employee_section(funcionario)
        self.add_doctor_section()
        self.add_risks_section(funcionario['cargo'])
        self.add_tipo_exame()
        self.add_exam_section(exames)
        self.add_final_section(funcionario['nome'])
        self.output("aso.pdf")
