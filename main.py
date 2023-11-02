
import env
import sensors
import Features
import random 
import pygame

pygame.init()

def random_color():
    levels = range(32,256,32)
    return tuple(random.choice(levels) for _ in range(3))


if __name__ == "__main__":
    FeatureMAP= Features.featuresDetection()
    environment= env.Buildenvironment((600, 1200))
    originalMap = environment.map.copy()
    laser=sensors.LaserSensor(200,originalMap,uncertainty=(0.5,0.01))

    #Mappa Bianca 
    environment.map.fill((255,255,255))

    #Coloro la mappa infomap di binaco
    environment.infomap = environment.map.copy()

    #Coloro la OriginalMap di bianco
    #originalMap=environment.map.copy()

    running = True
    FEATURE_DETECTION= True
    BREAK_POINT_IND=0

    while running:
        #la nostra mappa sarà la mappa bianca
        environment.infomap=originalMap.copy()
        #abilitato su true l' abilitazione al rilevamento dei punti 
        FEATURE_DETECTION = True
        #indice punto di interruzzione è 0
        BREAK_POINT_IND = 0
        #tutti gli ed point inzialmente somno 0
        ENDPOINT =[0,0] 
        #sensore spento
        sensorON=False
        #punti previsti sono vuoti
        PREDICTED_POINTS_TODRAW= [] 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
        if pygame.mouse.get_focused():
            sensorON=True
        elif not pygame.mouse.get_focused():
            sensorON=False
        
        if sensorON:
            position=pygame.mouse.get_pos() 
            laser.position=position
            sensor_data = laser.sense_obstacles()
            FeatureMAP.laser_points_set(sensor_data)

        
            print("ok")
            while BREAK_POINT_IND <(FeatureMAP.NP - FeatureMAP.PMIN):
                print("FEATURE_DETECTION: ", FEATURE_DETECTION)
                seedSeg=FeatureMAP.seed_segment_detection(laser.position, BREAK_POINT_IND)
                if seedSeg == False:
                    break
                else:
                    seedSegment=seedSeg[0]
                    PREDICTED_POINTS_TODRAW=seedSeg[1]
                    INDICES=seedSeg[2]
                    results=FeatureMAP.seed_segment_growing(INDICES, BREAK_POINT_IND)
                    if results == False:
                        BREAK_POINT_IND=INDICES[1]
                        continue 
                    else:

                        line_eq=results[1]
                        m,c=results[5]
                        line_seg=results[0]
                        OUTERMOST=results[2]
                        BREAK_POINT_IND = results[3]
                        
                        #modifica
                        ENDPOINT[0]=FeatureMAP.projection_point2line(OUTERMOST[0], m, c)
                        ENDPOINT[1]=FeatureMAP.projection_point2line(OUTERMOST[1], m, c)
                        

                        COLOR = random_color()
                        for point in line_seg:
                            environment.infomap.set_at((int(point[0][0]), int(point[0][1])),(0, 255, 0)) 
                            pygame.draw.circle(environment.infomap,COLOR,(int(point[0][0]), int(point[0][1])),2,0)
                        
                        pygame.draw.line(environment.infomap, (255, 0, 0), ENDPOINT[0], ENDPOINT[1], 2)
                        
                        #modifica
                        environment.data_storage(sensor_data)
        #02
        else:
            continue
        environment.map.blit(environment.infomap, (0, 0)) 
        #01Piano Cartesiano
        #environment.draw_cartesian_plane()
        pygame.display.update()
        #pygame.display.flip()
    



                


