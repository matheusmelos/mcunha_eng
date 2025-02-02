from models.pdf_manager import PDF
from models.dxf_manager import DXF
from models.dwg_manager import DWG
from models.erro_manager import registrar_erro

# Representam um conjunto de desenhos que formam uma peça. 
class Group:
    
    def __init__(self, pasta):
        self.pasta = pasta
        self.pdfs = []
        self.dxfs = []
        self.dwgs = []
        
        self.rows_to_add_first = []
        self.rows_to_add = []
        
    #Cria os objetos específicos para os arquivos .pdf, .dxf e .dwg e os adiciona ao grupo
    def adicionar_arquivo(self, arquivo_obj):

        if isinstance(arquivo_obj, PDF):
            self.pdfs.append(arquivo_obj)
        elif isinstance(arquivo_obj, DXF):
            self.dxfs.append(arquivo_obj)
        elif isinstance(arquivo_obj, DWG):
            self.dwgs.append(arquivo_obj)

    # Agrupa os arquivos .pdf e .dxf que formam uma peça
    def process_design(self):
        
        pdf_files_used = set()
        
    # Agrupa os arquivos .pdf e .dxf que formam uma peça
        for dxf in self.dxfs:
            for pdf in self.pdfs:
                if pdf.pdf_file in pdf_files_used:
                    continue
        
        # Cria uma linha com os dados do .pdf e .dxf correspondentes
                if pdf.name in dxf.dxf_name:
                    self.sheet_rows_complete(pdf, dxf)
                    pdf_files_used.add(pdf.pdf_file)
                    break
    
    # Adiciona os arquivos .pdf que não possuem .dxf correspondente, geralmente são desenhos de montagem (peça mãe)
        for pdf in self.pdfs:
            if pdf.pdf_file not in pdf_files_used:
            
            # Cria uma linha com os dados do .pdf correspondente
                self.sheet_rows(pdf)
                pdf_files_used.add(pdf.pdf_file)

        self.rows_to_add.append([])
    
    # Acrescenta um linha na planilha com seus respectivos dados (pdf e dxf)
    def sheet_rows_complete (self, pdf, dxf):
        
        self.rows_to_add.append([" ", " ", f'=HIPERLINK("C:\\Users\\" & T2 & "\\{pdf.pdf_local}", "Abrir PDF - {pdf.name}")', pdf.code_group, pdf.name, pdf.qtd, pdf.espessura, pdf.material,dxf.comprimento, 
                                 dxf.largura, dxf.area, pdf.area, dxf.cut_time, pdf.dobras, pdf.rebites, pdf.qtd_rebites, pdf.rosca, dxf.lote_min,
                                dxf.lote_max])
        
        
    
    # Acrescenta um linha na planilha com seus respectivos dados (pdf)
    def sheet_rows(self, pdf):
        
        self.rows_to_add_first.append([" ", " ", f'=HIPERLINK("C:\\Users\\" & T2 & "\\{pdf.pdf_local}", "Abrir PDF - {pdf.name}")', pdf.code_group, pdf.name, pdf.qtd, pdf.espessura, pdf.material," ", 
                                 " ", " ", pdf.area, " ", pdf.dobras, pdf.rebites, pdf.qtd_rebites, pdf.rosca, " ",
                                " "])
    
    
