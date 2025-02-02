import ezdxf
import math

class DXF:
    def __init__(self, dxf_file, dxf_name):
        self.dxf_file = dxf_file
        self.dxf_name = dxf_name
        self.material = ' '
        self.largura = 0
        self.comprimento = 0
        self.area = 0
        self.cut_speed = 167
        self.lote_min = 0
        self.lote_max = 0
        self.perimeter = DXF.calculate_perimeter_total(self)
        self.cut_time = DXF.calculate_cut_time(self)
        self.compare_coordinates()
        self.calculate_quantity()
        
    def calculate_perimeter_total(self):
        doc = ezdxf.readfile(self.dxf_file)
        modelspace = doc.modelspace()

        lines = modelspace.query('LINE')
        arcs = modelspace.query('ARC')
        circles = modelspace.query('CIRCLE')
        lwpolylines = modelspace.query('LWPOLYLINE')
        ellipses = modelspace.query('ELLIPSE')
        polylines = modelspace.query('POLYLINE')

        perimeter_total = (
            DXF.calculate_perimeter_of_lines(lines) +
            DXF.calculate_perimeter_of_arcs(arcs) +
            DXF.calculate_perimeter_of_circles(circles) +
            DXF.calculate_perimeter_of_lwpolylines(lwpolylines) +
            DXF.calculate_perimeter_of_ellipses(ellipses) +
            DXF.calculate_perimeter_of_lwpolylines(polylines)
        )

        return perimeter_total

    def calculate_cut_time(self):
        cut_time = self.perimeter / self.cut_speed
        return f"{cut_time:.3f}"

    def calculate_distance(point1, point2):
        return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

    def calculate_perimeter_of_lines(lines):
        perimeter = 0.0
        for line in lines:
            start_point = (line.dxf.start.x, line.dxf.start.y)
            end_point = (line.dxf.end.x, line.dxf.end.y)
            perimeter += DXF.calculate_distance(start_point, end_point)
        return perimeter

    def calculate_perimeter_of_arcs(arcs):
        perimeter = 0.0
        for arc in arcs:
            start_angle = arc.dxf.start_angle
            end_angle = arc.dxf.end_angle
            radius = arc.dxf.radius
            angle_diff = abs(end_angle - start_angle)
            angle_diff = math.radians(angle_diff)
            perimeter += radius * angle_diff
        return perimeter

    def calculate_perimeter_of_circles(circles):
        perimeter = 0.0
        for circle in circles:
            radius = circle.dxf.radius
            perimeter += 2 * math.pi * radius
        return perimeter

    def calculate_perimeter_of_lwpolylines(lwpolylines):
        perimeter = 0.0
        for polyline in lwpolylines:
            vertices = list(polyline.vertices())
            for i in range(len(vertices) - 1):
                perimeter += DXF.calculate_distance(vertices[i], vertices[i + 1])
            if polyline.closed:
                perimeter += DXF.calculate_distance(vertices[-1], vertices[0])
        return perimeter

    def calculate_perimeter_of_ellipses(ellipses):
        perimeter = 0.0
        for ellipse in ellipses:
            a = ellipse.dxf.major_axis.magnitude / 2
            b = ellipse.dxf.minor_axis.magnitude / 2
            perimeter += math.pi * (3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b)))
        return perimeter

    def print_coordinates(self):
        doc = ezdxf.readfile(self.dxf_file)
        modelspace = doc.modelspace()

        entities = modelspace.query('*')
        for entity in entities:
            if hasattr(entity.dxf, 'start') and hasattr(entity.dxf, 'end'):
                print(f"Entity: LINE, Start: {entity.dxf.start}, End: {entity.dxf.end}")
            elif hasattr(entity.dxf, 'center'):
                print(f"Entity: {entity.dxftype()}, Center: {entity.dxf.center}")

    def compare_coordinates(self):
        doc = ezdxf.readfile(self.dxf_file)
        modelspace = doc.modelspace()

        x_coords = []
        y_coords = []

        entities = modelspace.query('*')
        for entity in entities:
            if hasattr(entity.dxf, 'start') and hasattr(entity.dxf, 'end'):
                x_coords.extend([entity.dxf.start.x, entity.dxf.end.x])
                y_coords.extend([entity.dxf.start.y, entity.dxf.end.y])
            elif hasattr(entity.dxf, 'center'):
                x_coords.append(entity.dxf.center.x)
                y_coords.append(entity.dxf.center.y)

        max_x = max(x_coords)
        min_x = min(x_coords)
        max_y = max(y_coords)
        min_y = min(y_coords)
        
        self.comprimento = max_x - min_x
        self.largura = max_y - min_y
        self.area = (self.comprimento*self.largura)/1000000
        
    def calculate_quantity(self):
            
        chapa_largura = 1200 - 50
        chapa_comprimento_30 = 1000 - 50
        chapa_comprimento_100 = 3000 - 50
        
        resultados = []
        if self.comprimento and self.largura !=0:
            #Calculo 30% de chapa                     
            largura_X = chapa_largura/self.comprimento
                                
            largura_Y = chapa_largura/self.largura
                                                    
            comprimento_X = chapa_comprimento_30/self.comprimento
                                                
            comprimento_Y = chapa_comprimento_30/self.largura
            
            resultado_1 =  largura_X*comprimento_Y
           
            
            #Calculo 100% de chapa
            largura_X_100 = chapa_largura/self.comprimento
                                
            largura_Y_100 = chapa_largura/self.largura
                                                    
            comprimento_X_100 = chapa_comprimento_100 /self.comprimento
                                                
            comprimento_Y_100 = chapa_comprimento_100 /self.largura
            
            resultado_2 = largura_Y_100*comprimento_X_100
            
            perda_5 = 0.95
            perda_retalhos = 0.9
            self.lote_min = ((resultado_1)*perda_5)*perda_retalhos
            self.lote_max = ((resultado_2)*perda_5)*perda_retalhos
            