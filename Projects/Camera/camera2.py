import minescript as ms, time, math

# ===== SETTINGS =====
MIN_ROTATION_SPEED = 0.1
MAX_ROTATION_SPEED = 1.4
MIN_ANGLE_THRESHOLD = 10.0
MAX_ANGLE_THRESHOLD = 150.0
MAX_CURVE_INTENSITY = 1.5
PLAYER_EYE_HEIGHT = 1.62
# ====================

ease=lambda t:1-(1-t)**3
wrap=lambda a,b:(a-b+180)%360-180

def _rot(dy,dp,speed,curve,func=ease):
    a,b=ms.player_orientation();st=time.perf_counter()
    ang=math.sqrt(dy**2+dp**2);tn=0 if speed==0 else ang/(speed*180)
    t=0
    while t<1:
        t=(time.perf_counter()-st)/tn if tn>0 else 1
        if t>1:t=1
        e=func(t);yaw=a+dy*e;pit=b+dp*e
        ms.player_set_orientation(yaw,pit-curve*math.sin(math.pi*t))
    ms.player_set_orientation(a+dy,b+dp)

def _spd(ang):
    if ang<=MIN_ANGLE_THRESHOLD:return MIN_ROTATION_SPEED,0
    if ang>=MAX_ANGLE_THRESHOLD:return MAX_ROTATION_SPEED,MAX_CURVE_INTENSITY
    r=(ang-MIN_ANGLE_THRESHOLD)/(MAX_ANGLE_THRESHOLD-MIN_ANGLE_THRESHOLD)
    return MIN_ROTATION_SPEED+(MAX_ROTATION_SPEED-MIN_ROTATION_SPEED)*r,MAX_CURVE_INTENSITY*r

def look(yaw,pitch):
    a,b=ms.player_orientation();dy,dp=wrap(yaw,a),pitch-b
    ang=math.sqrt(dy**2+dp**2);s,c=_spd(ang);_rot(dy,dp,s,c)

def look_at(x,y,z):
    px,py,pz=ms.player_position()
    dx,dy,dz=x+0.5-px,y+0.5-(py+PLAYER_EYE_HEIGHT),z+0.5-pz
    ty,tp=-math.degrees(math.atan2(dx,dz)),-math.degrees(math.atan2(dy,math.sqrt(dx**2+dz**2)))
    a,b=ms.player_orientation();dy,dp=wrap(ty,a),tp-b
    ang=math.sqrt(dy**2+dp**2);s,c=_spd(ang);_rot(dy,dp,s,c)

# ===== EXAMPLES =====
look(90,0)
look_at(0,-60,0)
print("Done.")
