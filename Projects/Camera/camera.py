import minescript as ms, time, math

# ===== SETTINGS =====
ease_in=True; ease_out=True
steps=180
delay=0.001
PLAYER_EYE_HEIGHT=1.62
SMOOTH_TIME=0.01
THRESHOLD=1
# ====================

s=lambda t,c:(t-c+180)%360-180

def look(y,p): a,b=ms.player_orientation();dy=s(y,a);dp=p-b; [ms.player_set_orientation(a+dy*(0.5-0.5*math.cos(i/steps*math.pi) if ease_in and ease_out else i/steps), b+dp*(0.5-0.5*math.cos(i/steps*math.pi) if ease_in and ease_out else i/steps)) or time.sleep(delay) for i in range(steps+1)]

def look_at(x,y,z): px,py,pz=ms.player_position();a,b=ms.player_orientation();dx,dy,dz=x+0.5-px,y+0.5-(py+PLAYER_EYE_HEIGHT),z+0.5-pz;tx,tp=math.degrees(math.atan2(-dx,dz)),math.degrees(-math.atan2(dy,math.sqrt(dx**2+dz**2)));dyaw,dpitch=s(tx,a),tp-b; [ms.player_set_orientation(a+dyaw*(0.5-0.5*math.cos(i/steps*math.pi) if ease_in and ease_out else i/steps), b+dpitch*(0.5-0.5*math.cos(i/steps*math.pi) if ease_in and ease_out else i/steps)) or time.sleep(delay) for i in range(steps+1)]

def look_at_dynamic(x,y,z):
    tx,ty,tz=x+0.5,y+0.5,z+0.5
    while True:
        px,py,pz=ms.player_position()
        a,b=ms.player_orientation()
        dx,dy,dz=tx-px,ty-(py+PLAYER_EYE_HEIGHT),tz-pz
        tyaw,tpitch=math.degrees(math.atan2(-dx,dz)),math.degrees(-math.atan2(dy,math.sqrt(dx**2+dz**2)))
        dyaw,dpitch=s(tyaw,a),tpitch-b
        if abs(dyaw)<THRESHOLD and abs(dpitch)<THRESHOLD: break
        f=1-math.exp(-delay/SMOOTH_TIME)
        ms.player_set_orientation(a+dyaw*f,b+dpitch*f)
        time.sleep(delay)

#Examples
look(90, 0)
look_at(100, 0, 100)
look_at_dynamic(0, 0, 0) #work while player is moving 10% of the time
