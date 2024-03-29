import math
import pygame

class Buildenvironment:
    
    """_summary_ Build a environment for the simulation
    """
    
    def __init__(self, MapDimensions):
        pygame.init()
        
        self.map_path = "map.png"
        self.point_cloud = []
        self.external_map = pygame.image.load(self.map_path)
        
        self.maph, self.mapw = MapDimensions
        self.map_window_name = "RT path Planning"
        
        pygame.display.set_caption(self.map_window_name)
        self.map = pygame.display.set_mode((self.mapw, self.maph))
        self.map.blit(self.external_map, (0, 0))
        
        # colors
        self.black = (0, 0, 0)
        self.grey = (70, 70, 70)
        self.blue = (0, 0, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.white = (255, 255, 255)
        
    def ad2pos(self, distance, angle, robot_position):
        x = distance*math.cos(angle) + robot_position[0]
        y = -distance*math.sin(angle) + robot_position[1]
        return (int(x), int(y))
    
    def data_storage(self, data):
        
        print(len(self.point_cloud))
        print("data -->", data)
        
        for element in data:
            point = self.ad2pos(element[0], element[1], element[2])
            if point not in self.point_cloud:
                self.point_cloud.append(point)
    
    def show_sensor_data(self):
        print("self.point_cloud:", self.point_cloud)
        self.infomap = self.map.copy()
        for point in self.point_cloud:
            self.infomap.set_at((int(point[0]), int(point[1])), (255, 0, 0))
            
    #01Piano Cartesiano
    def draw_cartesian_plane(self):
        cartesian_plane = pygame.Surface((self.mapw, self.maph), pygame.SRCALPHA)
        line_color = (150, 150, 150)
        
        # Disegna le linee orizzontali
        for y in range(0, self.maph, 20):
            pygame.draw.line(cartesian_plane, line_color, (0, y), (self.mapw, y), 1)
        
        # Disegna le linee verticali
        for x in range(0, self.mapw, 20):
            pygame.draw.line(cartesian_plane, line_color, (x, 0), (x, self.maph), 1)

        self.map.blit(cartesian_plane, (0, 0))
                
        