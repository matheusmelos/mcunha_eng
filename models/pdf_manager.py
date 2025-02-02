import fitz
import re
import pandas as pd

class PDF: 
    def __init__(self, pdf_file, pdf_name):
    
        self.pdf_file = pdf_file
        self.pdf_name = pdf_name
        
        self.name = PDF.filter_name(pdf_name)
        self.size = PDF.type_page(self)
        self.pdf_local = str(self.pdf_file.replace("/", "\\"))
        self.code_group = self.extract_code_group(self.pdf_local)

        self.revisao = PDF.search_revision_number(self)
        self.title = PDF.search_title(self)
        self.material, self.espessura = PDF.search_material_espessura(self)
        self.dobras = PDF.count_folds(self)
        self.protheus = PDF.protheus_code(self)
        self.rebites =  ' '
        self.qtd = ' '
        self.qtd_rebites = '0'
        self.rosca = '0'
        self.aviso = ' '
        self.area = '0'
        self.code = ' '
        self.data  = PDF.data_material(self)
        self.found_area()
        self.found_rebites()
        self.found_roscas()
    
    def extract_code_group(self, pdf_local):
        
        # Expressão para capturar um trecho no formato "XX.XX.XXXXX"
        padrao = r"\b\d{2}\.\d{2}\.\d{5}\b"

        code_group = re.search(padrao, pdf_local)

        if code_group:
            return (code_group.group()) 
        else:
            code_group = 'Código não encontrado'
            
            return code_group
        
    def filter_name(pdf_name):
        return pdf_name[:-4]
     
    def type_page(self):
        
        doc = fitz.open(self.pdf_file)
        page = doc.load_page(0)
        text = page.get_text('text')
        large = page.rect.width
        
        if 'S   E   C   U   R   I   T   Y' in text:   
         
            if(large > 2000):
                size = 'A1_SECURITY'
            
            elif(1300 < large < 2000): 
                rect = fitz.Rect(1160, 995, 1660, 1030)
                texto = page.get_text("text", clip=rect)
                if "Material" in texto:
                    size = "A2_MATERIAL"
                elif "MATERIAL" in texto:
                    size = "A2.2"
                else:
                    size = 'A2_SECURITY'
            elif(870 <large < 1200):
                rect = fitz.Rect(680, 645, 1150, 680)   
                texto = page.get_text("text", clip=rect)
                rectfrase = fitz.Rect(840,680, 1120, 705) 
                frase = page.get_text("text", clip=rectfrase) 
                
                if "MATERIAL" in texto:  
                    size = 'A3.2_SECURITY'
                elif "Material" in texto:
                    if "Este Documento é de Propriedade da VMIS" in frase:
                         size = "A3_DESCRICAO"
                    else:
                            size = "A3_MATERIAL"
                else:
                    size = 'A3_SECURITY'
            
            elif(large < 840): 
                rect = fitz.Rect(65, 640, 500, 680)   
                texto = page.get_text("text", clip=rect)
                rectfrase = fitz.Rect(243, 690, 420, 708)
                frase = page.get_text("text", clip=rectfrase) 
            
               
                if "Material" in texto:
                    if "Este Documento é de Propriedade da VMIS" in frase:
                        
                        size = "A4_MATERIAL"
                    else:
                        size = 'A4'
                else:
                    size = "A4_RETRATO"
            
            else:
                size = 'A4_SECURITY'
        
        elif 'SISTEMAS DE SEGURANÇA' in text:
            
            if(large > 2000):
                size = 'A1_SISTEMAS'
            
            elif(1300 < large < 2000): 
                size = 'A2_SISTEMAS'
            
            elif(870 < large < 1200):
               size = 'A3_SISTEMAS'
            
            elif(845 < large < 1000):
                size = "A4_SISTEMAS"
            
            elif(large < 850):
                size = "A4.1_SISTEMAS"
        else:
            if(870 < large < 1200):
                rect = fitz.Rect(700, 645, 1050, 680)   
                texto = page.get_text("text", clip=rect)
               
                if "Material" in texto: 
                        size = 'A3_MATERIAL'
                else:
                        size = 'A3'
            else: 
                size = 'A4'
                
                
        doc.close()
        return size
    
    def search_revision_number(self):
        
        doc = fitz.open(self.pdf_file)
        page = doc.load_page(0)
        rect = None
        
        if self.size == 'A1_SECURITY':
            rect = fitz.Rect(2193, 1607, 2230, 1621)  # Revisão
        elif self.size == 'A2_SECURITY':
            rect = fitz.Rect(1500, 1123, 1540, 1140)  # Revisão
        elif self.size == 'A3_SECURITY':
            rect = fitz.Rect(1005, 774, 1048, 792)  # Revisão
        elif self.size == 'A3.2_SECURITY':
            rect = fitz.Rect(1008.4999389648438, 804, 1045, 820)  # Revisão
        elif self.size == 'A4_SECURITY':
            rect = fitz.Rect(760, 560, 795, 570)  # Revisão
        elif self.size == 'A4_SISTEMAS':
            rect = fitz.Rect(812, 548, 840, 555)  # Revisão
        elif self.size == 'A4.1_SISTEMAS':
            rect = fitz.Rect(778.1859130859375, 515, 805, 525)  # Revisão
        elif self.size == 'A3_MATERIAL':
            rect = fitz.Rect(1008.5, 775, 1045, 790) # Revisão
        elif self.size == 'A3':
            rect = fitz.Rect(1005, 774, 1048,  792)  # Revisão
        elif self.size == 'A4':
            rect = fitz.Rect(412, 775, 445, 789.1289672851562)
        elif self.size == "A4_RETRATO":
            rect =fitz.Rect(413, 775, 450, 790)
        elif self.size == "A4_MATERIAL":
            rect = fitz.Rect(413, 805, 450, 822)
        elif self.size == "A2_MATERIAL":
            rect = fitz.Rect(1500, 1123, 1540, 1140) #REVISAO
        elif self.size == "A2.2":
            rect = fitz.Rect(1500, 1155, 1540, 1170) 
        elif self.size =="A3_DESCRICAO":
            rect = fitz.Rect(1008.5, 805, 1045,820)
        text = page.get_text("text", clip=rect)
        revision_number = str(text.replace("\n", "").strip())
        
        doc.close()
        return revision_number

    def search_title(self):
        doc = fitz.open(self.pdf_file)
        page = doc.load_page(0)
        rect = None
        if self.size == 'A1_SECURITY':
            rect = fitz.Rect(2027.2437744140625, 1523, 2179, 1540)  # Denominação
        elif self.size == 'A2_SECURITY':
            rect = fitz.Rect(1334, 1038, 1530, 1055)  # Denominação
        elif self.size == 'A3_SECURITY':
            rect = fitz.Rect(841, 690, 1045, 708)  # Denominação
        elif self.size == 'A3.2_SECURITY':
            rect = fitz.Rect(825.3499755859375, 718, 1130, 735)  # Denominação
        elif self.size == 'A4_SECURITY':
            rect = fitz.Rect(471, 540, 615, 550)  # Denominação
        elif self.size == 'A4_SISTEMAS':
            rect = fitz.Rect(541, 585, 720, 595)  # Denominação
        elif self.size == 'A4.1_SISTEMAS':
            rect = fitz.Rect(528.177490234375, 550, 700, 560)  # Denominação
        elif self.size == "A3_MATERIAL":
           rect = fitz.Rect(840, 690, 1045, 705)
        elif self.size == "A3":
            rect = fitz.Rect(841, 690, 1045, 708)
        elif self.size == "A4":
            rect = fitz.Rect(243, 690, 420, 708)
        elif self.size == "A4_RETRATO":
            rect =fitz.Rect(247, 690, 440, 708)
        elif self.size == "A4_MATERIAL":
            rect = fitz.Rect(230, 720, 430, 735)
        elif self.size == "A2_MATERIAL":
            rect = fitz.Rect(1334, 1038, 1530, 1055) #DENOMINACAO
        elif self.size == "A2.2":
            rect = fitz.Rect(1320, 1067, 1530, 1083) 
        elif self.size =="A3_DESCRICAO":
            rect = fitz.Rect(825, 720, 1100, 735)
                      
                        
        text = page.get_text("text", clip=rect)
        title = str(text.replace("\n", " ").strip())
        
        doc.close()
        return title

    def found_espessura(self, base):
        
        if any(char.isalpha() for char in base) or base == '':
            return base
        else: 
            
            espessura = float(((((base.upper()).replace("MM", ""))).replace(",", ".")).strip())
            
            if espessura < 0.9:
                espessura = 0.45
            elif 0.5 < espessura < 1:
                espessura = 0.9
            elif 1 < espessura < 1.5:
                espessura = 1.2
            elif 1.2 < espessura < 1.8:
                espessura = 1.5
            elif 1.5 < espessura <= 2:
                espessura = 1.9
            elif 2 < espessura < 3:
                espessura = 2.65
            elif 2.7 < espessura < 4:
                espessura = 3
            elif 3 < espessura < 5:
                espessura = 4.75
            elif 5 < espessura < 7:
                espessura = 6.35
            elif 7 < espessura < 9:
                espessura = 8
            elif 8 < espessura < 10:
                espessura = 9.5
            elif 10 < espessura < 13:
                espessura = 12.7
            elif 13 < espessura < 19:
                espessura = 16
            else:
                espessura = 19
            
            return espessura     
    
    def type_material (self, material):
       
        base = str(((material.upper()).replace("Ç", "C")).strip())
        type_material = ' '
        
    
        if 'GALV' in base:
            type_material = 'ACO GALVANIZADO'
        elif 'ACO CARB' or 'SAE' in base:
            type_material =  'ACO CARBONO'
        elif 'ACO INOX' or 'AISI' in base:
            type_material = 'ACO INOX'
        elif 'ALUM' in base:
            type_material = 'ALUMINIO'

        return type_material
    
    def search_material_espessura(self):
        doc = fitz.open(self.pdf_file)
        page = doc.load_page(0)
        
        rect_material = None
        rect_espessura = None
        espessura = None
        
        if self.size == 'A1_SECURITY':
            rect_material = fitz.Rect(2026.67724609375, 1639, 2160, 1652)  # Material
            rect_espessura = fitz.Rect(2198, 1638, 2228, 1655)  # Espessura
        elif self.size == 'A2_SECURITY':
            rect_material = fitz.Rect(1335, 1154, 1470, 1170)  # Material
            rect_espessura = fitz.Rect(1500, 1155, 1540, 1170)  # Espessura
        elif self.size == 'A3_SECURITY':
            rect_material = fitz.Rect(840, 805, 1000, 820)  # Material
            rect_espessura = fitz.Rect(1005, 805, 1048, 820)  # Espessura
        elif self.size == 'A3.2_SECURITY':
            rect_material = fitz.Rect(949, 645, 1063, 660)  # Material
        elif self.size == 'A4_SECURITY':
            rect_material = fitz.Rect(620, 540, 720, 550)  # Material
            rect_espessura = fitz.Rect(725, 540, 760, 550)  # Espessura
        elif self.size == 'A4_SISTEMAS':
            rect_material = fitz.Rect(542.8748168945312, 564, 613, 574)  # Material
        elif self.size == 'A4.1_SISTEMAS':
            rect_material = fitz.Rect(528, 530, 600, 540)  # Material
        elif self.size == "A3_MATERIAL":
            rect_material = fitz.Rect(790, 645, 880, 660)  # Material
            rect_espessura = fitz.Rect(723, 645, 790, 660)  # Espessura
        elif self.size == 'A3':
            rect_material = fitz.Rect(840, 805, 1000, 820)  # Material
            rect_espessura = fitz.Rect(1005, 805, 1048, 820)  # Espessura
        elif self.size == 'A4':    
            rect_material = fitz.Rect(195, 645, 290, 665)  # Material
            rect_espessura = fitz.Rect(130.0518798828125, 645.3804321289062, 191.1731414794922, 664)  # Espessura
        elif self.size == "A4_RETRATO":
            rect_material = fitz.Rect(246.5, 805, 400, 820) 
            rect_espessura = fitz.Rect(413.3974914550781, 805, 450, 820)
        elif self.size == "A4_MATERIAL":
            rect_material = fitz.Rect(370, 647, 460, 663)
        elif self.size == "A2_MATERIAL":
            rect_material = fitz.Rect(1280, 995, 1380, 1010) 
            rect_espessura = fitz.Rect(1230, 995,1270, 1010) 
        elif self.size == "A2.2":
            rect_material = fitz.Rect(1430, 995, 1580, 1010)
        elif self.size =="A3_DESCRICAO":
            rect_material = fitz.Rect(930, 645, 1045, 660)
                        
        text_material = page.get_text("text", clip=rect_material)
        material = str((((text_material.strip()).replace("/", "-"))).replace("\n", ""))
        type = ' '
        
        if  'VER TABELA' == material.upper() :
            type = material
            
        else:
            type = self.type_material(material)
        try:
            if rect_espessura:
                text = page.get_text("text", clip=rect_espessura)
                text_espessura = ((((text.upper()).replace("MM", ""))).replace(",", ".")).strip()
                espessura = self.found_espessura(text_espessura)
            else:
                if "mm" in material:
                    espessura = float((((material[-6:].replace("mm","")).replace(",", "."))).replace("#", ""))
                elif "MM" in material:
                    espessura = float((((material[-6:].replace("MM","")).replace(",", "."))).replace("#", ""))
                else:
                    espessura = 0
        except Exception:
            espessura = 0
        
        
        doc.close()
        
        return type, espessura 
         
    def found_area(self):
  
        documento = fitz.open(self.pdf_file)
        termo =  'Área'
       
        for numero_pagina in range(documento.page_count):
            pagina = documento.load_page(numero_pagina)  
            
            # Procurar pelo termo na página
            resultados_pagina = pagina.search_for(termo)  # Retorna as coordenadas de onde o termo é encontrado
            
            # Se o termo for encontrado, desenhar um retângulo e salvar a imagem
            for area in resultados_pagina:
                x0, y0, x1, y1 = area
                
                # Ajustar as coordenadas para pegar o texto logo abaixo, como exemplo
                offset = 10  
                nova_area = fitz.Rect(x0, y1, x1, y1 + offset)  # Área logo abaixo

                # Extrair o texto da nova área
                self.area = pagina.get_text("text", clip=nova_area)  # Pega o texto da área destacada
                self.area = self.area.replace("\n", "").strip()
                
    def count_folds(self):
        
        doc = fitz.open(self.pdf_file)
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            text = page.get_text("text") 
            dobras_total = 0
            dobras_up = text.count("UP")
            dobras_down = text.count("DOWN")
            dobras_baixo = text.count("PARA BAIXO")
            dobras_cima = text.count("PARA CIMA")
               
            dobras_total += (dobras_baixo + dobras_cima + dobras_up + dobras_down)
            
        doc.close()
 
        return dobras_total

    def protheus_code(self):
        protheus_code = str(self.name + "-" + self.revisao + "-" + self.title)
        return protheus_code

    def data_material(self):
        
        # dataframes of materials
        data_aco_galvanizado = {
            "Codigo": ["0000000000", "0000000174", "0000000098", "0000000099", "0000000100", "0000000117", "0000000000"],
            "Espessura (mm)": [0.45, 0.9, 1.2, 1.5, 1.9, 2.65, 3],
            "Descricao": [
                "CHAPA DE ACO GALVANIZADO  #26 0.45X1200X3000",
                "CHAPA DE ACO GALVANIZADO #20 0.9X1200X3000",
                "CHAPA DE ACO GALVANIZADO #18 1.25X1200X3000",
                "CHAPA DE ACO GALVANIZADO #16 1.55X1200X3000",
                "CHAPA DE ACO GALVANIZADO #14 1.95X1200X3000",
                "CHAPA DE ACO GALVANIZADO #12 2.65X1200X3000",
                "CHAPA DE ACO GALVANIZADO #11 3.05X1200X3000"
            ],
        }

        data_aco_carbono = {
            "Codigo": [
                "0000000000", "0000000084", "0000000090", "0000000085", "0000000192", "0000000119", 
                "0000000087", "0000000088", "0000000089", "0000000095", "0000000096", 
                "0000000120", "0000000000", "0000000000"
            ],
            "Espessura (mm)": [
                0.45, 0.9, 1.2, 1.5, 1.9, 2.65, 3, 4.75, 6.35, 8, 9.5, 12.7, 16, 19
            ],
            "Descricao": [
                "CHAPA ACO CARBONO #26 0.45X1200X3000",
                "CHAPA ACO CARBONO #20 0.90X1200X3000",
                "CHAPA ACO CARBONO #18 1.20X1200X3000",
                "CHAPA ACO CARBONO #16 1.50X1200X3000",
                "CHAPA ACO CARBONO #14 1,9MMX1200X3000",
                "CHAPA ACO CARBONO #12 2.65X1200X3000",
                "CHAPA ACO CARBONO #1-8 3.0X1200X3000",
                "CHAPA ACO CARBONO #3-16 4.75X1200X3000",
                "CHAPA ACO CARBONO #1-4 6,35X1200X3000",
                "CHAPA ACO CARBONO #5-16 8MMX1200X3000",
                "CHAPA ACO CARBONO #3-8 9,5X1200X3000",
                "CHAPA ACO CARBONO #1-2 12,7X1200X3000",
                "CHAPA ACO CARBONO #1020 GR 5-8 16MMX1000X1500",
		        "CHAPA ACO CARBONO #1020 GR 3-4 19MMX1000X2000"
            ]
        }
        
        data_aco_inox = {
            "Codigo": ["0000000000","0000000153", "0000000121", "0000000106", "0000000254", "0000000000"],
            "Espessura (mm)": [0.9, 1.2, 1.5, 1.9, 2.65, 3],
            "Descricao": [
                "CHAPA INOX AISI 304 #20 0,9X1200X3000MM"
                "CHAPA INOX AISI 304  #18 1,2X1200X3000MM",
                "CHAPA INOX #16 1,5X1200X3000MM",
                "CHAPA INOX #14 2,0X1200X3000MM",
                "CHAPA INOX AISI 304 2,50X1200X3000MM",
                "CHAPA INOX AISI 304 1-8 3X1200X3000MM"
            ]
        }

        data_aluminio = {
            "Codigo": ["0000000000","0000000159","0000000000", "0000000111", "0000000110", "0000000220"],
            "Espessura (mm)": [0.9, 1.2, 1.5, 1.9, 3.0, 6.35],
            "Descricao": [
                "CHAPA LISA ALUMINIO LIGA 1200H14 2000X1000X0,9 MM",
                "CHAPA LISA ALUMINIO LIGA 1200H14 3000X1200X1,2",
                "CHAPA LISA ALUMINIO LIGA 1200H14  2000X1000X1,5 MM",
                "CHAPA LISA ALUMINIO LIGA 1200H14 2000X1250X2,00",
                "CHAPA LISA  ALUMINIO 3000X1200X3,0",
                "CHAPA LISA ALUMINIO LIGA 1200 1-4 2000X1000",
            ]
        }

        busca = None
        
        if  "ACO GALVANIZADO" in self.material.upper() :
        
            aco_galvanizado = pd.DataFrame(data_aco_galvanizado)
            espessura_consulta = (self.espessura)
           

            busca = aco_galvanizado.loc[
                (aco_galvanizado["Espessura (mm)"] == espessura_consulta),
                ["Codigo", "Descricao"]  # Selecionar múltiplas colunas
            ]
            
        elif "ACO INOX" in self.material.upper() :
            aco_inox = pd.DataFrame(data_aco_inox)
            espessura_consulta = (self.espessura)

            busca = aco_inox.loc[
                (aco_inox["Espessura (mm)"] == espessura_consulta),
                ["Codigo", "Descricao"]  # Selecionar múltiplas colunas
            ]

        elif  "ACO CARB" in self.material.upper():
            aco = pd.DataFrame(data_aco_carbono)
            espessura_consulta = (self.espessura)

            busca = aco.loc[
                (aco["Espessura (mm)"] == espessura_consulta),
                ["Codigo", "Descricao"]  # Selecionar múltiplas colunas
            ]
        
        elif "ALUMINIO" in self.material.upper() :
            aluminio = pd.DataFrame(data_aluminio)
            espessura_consulta = float(self.espessura)

            busca = aluminio.loc[
                (aluminio["Espessura (mm)"] == espessura_consulta),
                ["Codigo", "Descricao"]  # Selecionar múltiplas colunas
            ]
        
        if busca is not None and not busca.empty:
            self.code, self.material = busca.iloc[0]
        else:
            self.code = 'Não encontrado'

    def found_rebites(self):
        
        doc = fitz.open(self.pdf_file)
        
        for page in doc:
            text = page.get_text("text")
            
            if "Rebite " in text:
                self.rebites = "Rebite"
                break 

        doc.close()

        self.qtd_rebites = ' '
        
        """# Abrir o arquivo PDF
        documento = fitz.open(self.pdf_file)
        termo = "Rebite"
        # Percorrer todas as páginas
        for numero_pagina in range(documento.page_count):
            pagina = documento.load_page(numero_pagina)  # Carrega a página
            # Procurar pelo termo na página
            resultados_pagina = pagina.search_for(termo)  # Retorna as coordenadas de onde o termo é encontrado
            
            # Se o termo for encontrado, desenhar um retângulo e salvar a imagem
            for area in resultados_pagina:
                x0, y0, x1, y1 = area
                
                # Desenhar um retângulo na área onde o termo foi encontrado
                rect = fitz.Rect(x0, y0, x1, y1)  # Cria o retângulo com as coordenadas encontradas
                pagina.draw_rect(rect, color=(1, 0, 0), width=2)  # Desenha o retângulo (vermelho)

                # Ajustar as coordenadas para pegar o texto logo abaixo, como exemplo
                offset = 15 # Ajuste conforme necessário
                nova_area = fitz.Rect(x0, y0, x1 + 130, y1 + offset)  # Área logo abaixo
                qtd_rebite = fitz.Rect(x0 - 30, y0, x0, y1 + offset)
                
                pagina.draw_rect(qtd_rebite, color=(0,1,0))
                # Desenhar um retângulo na nova área
                pagina.draw_rect(nova_area, color=(0, 0, 1), width=2)  # Desenha o retângulo abaixo (azul)
                
                # Extrair o texto da nova área
                self.qtd_rebites = pagina.get_text("text", clip = qtd_rebite)
                
                self.rebites = pagina.get_text("text", clip=nova_area)  # Pega o texto da área destacada
"""


    def found_roscas(self):
        # Abrir o arquivo PDF
        documento = fitz.open(self.pdf_file)
        termos = ["M4", "M5", "M6", "M7", "M8"]
        
        # Percorrer todas as páginas
        for numero_pagina in range(documento.page_count):
            pagina = documento.load_page(numero_pagina)  # Carrega a página
            text = pagina.get_text("text")
            if "Rebite" in text:
                self.aviso = "EXISTEM REBITES E ROSCAS"
            # Procurar pelo termo na página
            for termo in termos:
                resultados_pagina = pagina.search_for(termo)  # Retorna as coordenadas de onde o termo é encontrado
            
            # Se o termo for encontrado, desenhar um retângulo e salvar a imagem
            for area in resultados_pagina:
                x0, y0, x1, y1 = area
                # Ajustar as coordenadas para pegar o texto logo abaixo, como exemplo
                offset = 15 
                nova_area = fitz.Rect(x0-20, y0-30, x1 + 130, y1 + offset)  # Área logo abaixo

                # Extrair o texto da nova área
                self.roscas = pagina.get_text("text", clip=nova_area)  # Pega o texto da área destacada


