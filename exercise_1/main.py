import math

#== Constances:

TIME_FRAME = 0.01 # second
Cx = 25.031617
Cy = 121.535829
R  = 0.5
C1 = 0.1
ALTITUDE_LIMITATION = 60000
LOGGING_PERIOD = 1 # second, must be integer


#== Classes:

class Balloon:
    def __init__(self, x, y, r, m):
        self.x = x
        self.y = y
        self.z = 0
        self.vx = 0
        self.vy = 0
        self.vz = 0
        self.r = r
        self.m = m
        self.release_time = 0
        self.bursted = False
        self.buoyancy = 150
        self.log = []
    def get_ax(self):
        wind_vx = self.get_wind_vx()
        return (wind_vx-self.vx)*math.pi*self.r**2*C1/self.m
    def get_ay(self):
        wind_vy = self.get_wind_vy()
        return (wind_vy-self.vy)*math.pi*self.r**2*C1/self.m
    def get_az(self):
        wind_vy = self.get_wind_vy()
        force = -self.vz*math.pi*self.r**2*C1 - 9.8*self.m + self.buoyancy
        return force/self.m
    def get_wind_vx(self):
        return 5.14*math.sin( math.sqrt( (self.x-Cx)**2 + (self.y-Cy)**2 ) )
    def get_wind_vy(self):
        return 5.14*math.cos( math.sqrt( (self.x-Cx)**2 + (self.y-Cy)**2 ) )

    def release(self):
        while (self.z>=0):

            # update time
            self.release_time += TIME_FRAME

            # update v:
            self.vx += self.get_ax()*TIME_FRAME
            self.vy += self.get_ay()*TIME_FRAME
            self.vz += self.get_az()*TIME_FRAME
            # update position:
            self.x += self.vx*TIME_FRAME/2/111.111*math.cos(self.y*math.pi/180)
            self.y += self.vy*TIME_FRAME/2/111.111
            self.z += self.vz*TIME_FRAME/2
            
            # burst
            if(self.z>=ALTITUDE_LIMITATION and self.bursted==False):
                self.bursted = True
                self.buoyancy = 0

            if int(self.release_time*100) % (LOGGING_PERIOD*100) == 0 :
                self.log.append( [self.x,self.y] )

        text_file = open("path_log.txt", "w")
        for cor in self.log:
            text_file.write(str(cor[0])+","+str(cor[1])+"\n")
        text_file.close()

        text_file = open("google_map.txt", "w")
        for cor in self.log:
            text_file.write("{lat:"+str(cor[0])+", lng:"+str(cor[1])+"},\n")
        text_file.close()

        print("Costed "+ str(self.release_time)+" seconds...")
        print("Fall at "+str(self.x)+","+str(self.y))


#== Main codes:

balloon = Balloon(Cx, Cy, 0.5, 10)
balloon.release()

