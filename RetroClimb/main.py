import pygame
import random

try:
    import android
except ImportError:
    android = None

FPS = 20



def main():
    
    try:
        with open('records.txt'):pass
    except IOError:
        with open('records.txt','w') as records:
            records.write('0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n')
    total=-1
    level=-1
    bottom=-1
    christina=-1
    
    records_=[]
    with open('records.txt') as records:
        for line in records:
            if level==-1:
                level=int(line.rstrip())
            elif total==-1:
                total=int(line.rstrip())
            elif bottom==-1:
                bottom=int(line.rstrip())
            elif christina==-1:
                christina=int(line.rstrip())
            else:
                records_.append(int(line.rstrip()))
        
    records=records_
    #print records
    
    pygame.init()
    
    if android:
        android.init()
        android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
        #android.map_key(176, pygame.K_s)
        info=pygame.display.Info()
        sx=info.current_w
        sy=info.current_h
        dpi=android.get_dpi()
        
    else:
        sx=640
        sy=360
        dpi=120
        
    screen = pygame.display.set_mode((sx,sy))
    clock=pygame.time.Clock()
    
    su=sx/128
    
    font=pygame.font.Font('DroidSansMono.ttf',4*su)
    
    x1=4*su
    x2=132*su
    
    DOCK=(0,0,0)
    LINES=(31,31,31)#(63,63,63)
    GROUND=(63,63,63)#(63,31,0)
    GRASS=(255,255,255)#(0,127,0)
    ENEMY=(255,0,0)#(255,0,0)
    INNERENEMY=(255,127,127)#(0,0,0)
    GHOST=(0,0,0)
    INNERGHOST=(0,0,0)
    BAT=(0,0,0)
    INNERBAT=(255,0,0)
    PLAYER=(255,255,255)
    SHOT=(255,0,0)
    SKY=(127,127,255)
    TEXT=(255,255,255)
    
    if level==1:
        SKY=(31,31,31)
    elif level==2:
        SKY=(0,0,0)
        GROUND=(0,0,0)
        GRASS=(31,31,31)
        PLAYER=(31,31,31)
    
    
    
    while True:
        savehighscore=0
        menu=True
        pygame.event.clear()
        while menu:
            
            if android and android.check_pause():
                '''with open('records.txt','w') as records_:
                    records_.write(str(total)+'\n')
                    for record in records:
                        records_.write(str(record)+'\n')'''
                android.wait_for_resume()
            
            events = pygame.event.get()
            
            #manage events
            for event in events:
                #get touches
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y=event.pos
                    if x!=0:
                        if y<32*su:
                            menu=False
                            howtoplay=False
                            running=True
                            showrecords=False
                            settings=False
                        elif y<64*su:
                            menu=False
                            howtoplay=False
                            running=False
                            showrecords=True
                            settings=False
                        elif x<sx/2:
                            menu=False
                            howtoplay=True
                            running=False
                            showrecords=False
                            settings=False
                        else:
                            menu=False
                            howtoplay=False
                            running=False
                            showrecords=False
                            settings=True
                    
                            
            x1-=su*0.25
            x2-=su*0.25
            if x1<-128*su:x1=128*su
            if x2<-128*su:x2=128*su
            screen.fill(SKY)
            screen.fill(GROUND,((x1,36*su),(124*su,28*su)))
            screen.fill(GRASS,((x1,36*su),(124*su,su)))
            screen.fill(GROUND,((x2,32*su),(124*su,32*su)))
            screen.fill(GRASS,((x2,32*su),(124*su,su)))
            screen.fill(DOCK,((0,64*su),(sx,sy-64*su)))
            screen.fill(DOCK,((128*su,0),(sx,sy)))
            screen.blit(font.render(('Play'),True,TEXT),(su,su))
            screen.blit(font.render(('Highscores'),True,TEXT),(su,57*su))
            screen.blit(font.render(('Controls'),True,TEXT),(su,65*su))
            screen.blit(font.render(('Settings'),True,TEXT),(sx-font.size('Settings')[0]-su,65*su))
            clock.tick(FPS)
            pygame.display.flip()
        
        while settings:
            
            if android and android.check_pause():
                '''with open('records.txt','w') as records_:
                    records_.write(str(total)+'\n')
                    for record in records:
                        records_.write(str(record)+'\n')'''
                android.wait_for_resume()
            
            events = pygame.event.get()
            
            #manage events
            for event in events:
                #get touches
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y=event.pos
                    if x!=0:
                        if y<32*su:
                            if christina:
                                christina=0
                            else:
                                christina=1
                        elif y<64*su:
                            level=0
                            botton=0
                        else:
                            total=0
                            records=[0,0,0,0,0,0,0,0,0,0]
                elif event.type == pygame.KEYDOWN and (event.key==pygame.K_s or event.key==pygame.K_ESCAPE):
                    menu=True
                    howtoplay=False
                    running=False
                    showrecords=False
                    settings=False
                        
            x1-=su*0.25
            x2-=su*0.25
            if x1<-128*su:x1=128*su
            if x2<-128*su:x2=128*su
            screen.fill(SKY)
            screen.fill(GROUND,((x1,36*su),(124*su,28*su)))
            screen.fill(GRASS,((x1,36*su),(124*su,su)))
            screen.fill(GROUND,((x2,32*su),(124*su,32*su)))
            screen.fill(GRASS,((x2,32*su),(124*su,su)))
            screen.fill(DOCK,((0,64*su),(sx,sy-64*su)))
            screen.fill(DOCK,((128*su,0),(sx,sy)))
            if christina:
                screen.blit(font.render(('Christina Mode (On)'),True,TEXT),(su,su))
            else:
                screen.blit(font.render(('Christina Mode (Off)'),True,TEXT),(su,su))
            if level==0:
                screen.blit(font.render(('Reset Layer (Done)'),True,TEXT),(su,57*su))
            else:
                screen.blit(font.render(('Reset Layer'),True,TEXT),(su,57*su))
            if total==0:
                screen.blit(font.render(('Reset Highscores (Done)'),True,TEXT),(su,65*su))
            else:
                screen.blit(font.render(('Reset Highscores'),True,TEXT),(su,65*su))
            clock.tick(FPS)
            pygame.display.flip()
        
        if christina:
            level=0
            bottom=0
        
        with open('records.txt','w') as records_:
            records_.write(str(level)+'\n')
            records_.write(str(total)+'\n')
            records_.write(str(bottom)+'\n')
            records_.write(str(christina)+'\n')
            for record in records:
                records_.write(str(record)+'\n')
        
        pygame.event.clear()
        if howtoplay:
            screen.fill((0,0,63),((0,0),(0.75*dpi,sy)))
            screen.blit(pygame.transform.rotate(font.render(('Left'),True,TEXT),-90),(su,su))
            screen.fill((0,0,127),((0.75*dpi,0),(0.5*dpi,sy)))
            screen.blit(pygame.transform.rotate(font.render(('Stop'),True,TEXT),-90),(0.75*dpi+su,su))
            screen.fill((0,0,191),((1.25*dpi,0),(0.75*dpi,sy)))
            screen.blit(pygame.transform.rotate(font.render(('Right'),True,TEXT),-90),(1.25*dpi+su,su))
            screen.fill((0,0,63),((2*dpi,0),(sx-2*dpi,sy-dpi)))
            screen.blit(font.render(('Double Jump'),True,TEXT),(2*dpi+su,su))
            screen.blit(font.render((' (Lose Health)'),True,TEXT),(2*dpi+su,8*su))
            #screen.blit(font.render(('  Gain 50pts'),True,TEXT),(2*dpi+su,13*su))
            screen.fill((0,0,127),((2*dpi,sy-dpi),(sx-2*dpi,dpi)))
            screen.blit(font.render(('Jump'),True,TEXT),(2*dpi+su,sy-dpi+su))
            
            pygame.display.flip()
            event=pygame.event.poll()
            while not (event.type==pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                if android and android.check_pause():
                    '''with open('records.txt','w') as records_:
                        records_.write(str(total)+'\n')
                        for record in records:
                            records_.write(str(record)+'\n')'''
                    android.wait_for_resume()
                clock.tick(FPS)
                event=pygame.event.poll()
            event=pygame.event.clear()
            howtoplay=False
            menu=True
            
        hole=None
        
        land=[hole,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,hole,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,hole,9]
        #land=[hole,5,5,5,5,hole,7,7,7,7,hole,8,8,8,8,hole,6,6,6,6,hole,9,9,9,9,hole,10,10,10,10,hole,12,12,12,12,hole,11,11,11,11,hole]
        
        offset=[0,0]
        shift=[0,0]
        ghostpos=(0,0)
        batpos=(0,0)
        batshift=(0,0)
        
        fall=0.25
        
        mouseclick=left=right=jump=hard=killed=bat=ghost=ghostfade=boss=False
        fullhealth=True
        jumppos=sy
        enemies=[]
        shots=[]
        body=0
        shotclock=0
        score=0
        highscore=0
        
        pygame.event.clear()
        
        #run game
        while running:
            #pause if closed
            if android and android.check_pause():
                '''with open('records.txt','w') as records_:
                    records_.write(str(total)+'\n')
                    for record in records:
                        records_.write(str(record)+'\n')'''
                android.wait_for_resume()
            
            #get events
            events = pygame.event.get()
            
            #manage events
            for event in events:
                #get touches
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                    x,y=event.pos
                    if x!=0:
                        if x<dpi*2:
                            mousepos=x
                            mouseclick=True
                        else:
                            jumppos=y
                            jump=True
                
                #end touch
                elif event.type == pygame.MOUSEBUTTONUP:
                    x,ignore=event.pos
                    if x!=0:
                        if x<dpi*2:
                            mouseclick=False
                        else:
                            jump=False
                
                #simulate touch
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running=False
                    elif event.key == pygame.K_LEFT:
                        mousepos=0.5*dpi
                        mouseclick=True
                    elif event.key == pygame.K_RIGHT:
                        mousepos=1.5*dpi
                        mouseclick=True
                    elif event.key == pygame.K_UP:
                        jump=True
                    elif event.key == pygame.K_SPACE:
                        jumppos=1
                
                #turn off touch simulation
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        mouseclick=False
                    elif event.key == pygame.K_UP:
                        jump=False
                        jumppos=sy-1
            
            #jump
            if jump:
                offset[1]+=4.125
            
            if jumppos<sy-dpi and fullhealth and fall>4:
                fall=-0.75
                fullhealth=False
            
            #gravity
            if fall!=-1 and ((land[8]<7 or(land[8]==7 and offset[1]!=0)or land[8]==hole) and (offset[0]==0 or (offset[0]!=0 and (land[9]<7 or(land[9]==7 and offset[1]!=0)or land[9]==hole)))):
                offset[1]-=fall
                fall+=0.5
            else:
                offset[1]=0
                fall=0.25
            
            #check for vertical shifting
            shift[1]=0
            while offset[1]>3:
                offset[1]-=4
                shift[1]-=1
            while offset[1]<0:
                offset[1]+=4
                shift[1]+=1
            if land[8] !=hole and land[8]+shift[1]>7:
                shift[1]=7-land[8]
                offset[1]==0
                fall=-1
            
            if offset[0]!=0 and land[9] !=hole and land[9]+shift[1]>7:
                shift[1]=7-land[9]
                offset[1]==0
                fall=-1
            
            land_=[]
            for height in land:
                if height!=hole:
                    land_.append(height+shift[1])
                else:
                    land_.append(hole)
                land=land_
            
            #touch button locations
            if mouseclick:
                if mousepos<0.75*dpi:
                    left=True
                elif mousepos>1.25*dpi:
                    right=True
                else:
                    left=right=False
            else:
                left=right=False
            
            if left and (land[7]<=7 or land[7]==hole or offset[0]!=0):
                offset[0]-=1
            elif right and (land[9]<=7 or land[9]==hole):
                offset[0]+=1
                
            if offset[0]>3:
                offset[0]-=4
                shift[0]=1
                score+=1
            elif offset[0]<0:
                offset[0]+=4
                shift[0]=-1
                score-=1
            else:
                shift[0]=0
            
            #right shift
            if shift[0]==1:
                land_=[]
                for height in land[1:]:
                    land_.append(height)
                
                rand=random.randint(-5,5)
                
                if rand<-2 and not hard:
                    rand=random.randint(1,2)
                   
                if land[-3:]==[hole,hole,hole] or max(land[-6+rand:])==hole:
                    height=land[-4]
                elif rand==5:
                    height=hole
                elif rand<-2 and hard:
                    height=hole
                else:
                    height=max(land[-6+rand:])+rand-random.randint(0,1)
                    
                if random.randint(0,99)==0:
                    hard=not hard
                    #print hard
                
                land_.append(height)
                land=land_
                
                enemies_=[]
                for enemy in enemies:
                    if enemy>1:
                        enemies_.append(enemy-1)
                    enemies=enemies_
                
                if land[-1]>land[-2] and random.randint(0,4)==0 and not christina:
                    enemies.append(len(land)-1)
                
                #print enemies
                
            #left shift
            elif shift[0]==-1:
                land_=[hole]
                for height in land[:-1]:
                    land_.append(height)
                land=land_
                
                enemies_=[]
                for enemy in enemies:
                    if enemy<len(land)-1:
                        enemies_.append(enemy+1)
                    enemies=enemies_
                #print enemies
            
            if land[8]==hole and shift[1]>=10:
                if highscore>=500+savehighscore and level!=2 and not christina:# and random.randint(0,1)==0:
                    fall=4.25
                    offset[0]=3
                    shift[1]=0
                    hard=True
                    shotclock=0
                    savehighscore=highscore
                    level+=1    
                    fullhealth=False
                    if level==1:
                        enemies=[0,]
                        bat=5
                        batpos=(130,68)
                        boss=True
                    else:
                        enemies=[0,14]
                        ghost=True
                        ghosthealth=5
                        GHOST=(-1,-1,-1)
                        ghostpos=(random.randint(7,9),random.randint(7,12))
                        ghostfade=False
                        boss=True
                    land=[-8,hole,hole,hole,hole,-6,hole,-10,-10,-10,-10,-10,-10,hole,0,-19,-19,-19,-19,-19,-19,-19,-19,-19,-19,-19,-19,-19,-19,-19,-19,-19,-19,-19,-19,-19,-19,-19,-19,-19,]
                else:
                    running=False
            elif highscore>=1000+savehighscore and level!=0:
                level-=1
                savehighscore=highscore
            elif highscore>=1000+savehighscore and bottom and not boss:
                boss=True
                level=-1
                land=[land[0],land[1],land[2],hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole,hole]
            
            if boss and level==2:
                bat=False
                ghost=True
            
            if level==0:
                SKY=(SKY[0]+(SKY[0]<127),SKY[1]+(SKY[1]<127),SKY[2]+(SKY[2]<255))
            elif level==1:
                SKY=(SKY[0]+(SKY[0]<31)-(SKY[0]>31),SKY[1]+(SKY[1]<31)-(SKY[1]>31),SKY[2]+(SKY[2]<31)-(SKY[2]>31))
                GROUND=(GROUND[0]+(GROUND[0]<63),GROUND[1]+(GROUND[1]<63),GROUND[2]+(GROUND[2]<63))
                GRASS=(GRASS[0]+(GRASS[0]<255),GRASS[1]+(GRASS[1]<255),GRASS[2]+(GRASS[2]<255))
                PLAYER=(PLAYER[0]+(PLAYER[0]<255),PLAYER[1]+(PLAYER[1]<255),PLAYER[2]+(PLAYER[2]<255))
            else:
                SKY=(SKY[0]-(SKY[0]>0),SKY[1]-(SKY[1]>0),SKY[2]-(SKY[2]>0))
                GROUND=(GROUND[0]-(GROUND[0]>0),GROUND[1]-(GROUND[1]>0),GROUND[2]-(GROUND[2]>0))
                GRASS=(GRASS[0]-(GRASS[0]>31),GRASS[1]-(GRASS[1]>31),GRASS[2]-(GRASS[2]>31))
                PLAYER=(PLAYER[0]-(PLAYER[0]>31),PLAYER[1]-(PLAYER[1]>31),PLAYER[2]-(PLAYER[2]>31))
            
            if level>=1 and random.randint(0,799)==0 and not bat:
                bat=random.randint(1,3)
                batpos=(130,68)
            
            if level==2 and random.randint(0,799)==0 and not ghost:
                ghost=True
                ghosthealth=3
                GHOST=(-1,-1,-1)
                ghostpos=(random.randint(7,9),random.randint(7,12))
                ghostfade=False
            
                
            screen.fill(SKY)
            
            heightcount=0
            for height in land:
                if height!=hole:
                    p1=(4*su*heightcount-offset[0]*su,64*su-4*su*height+offset[1]*su)
                    p2=(4*su, 4*su*height+offset[1]*su)
                    screen.fill(GROUND,(p1,p2))
                    screen.fill(GRASS,(p1,(4*su,su)))
                heightcount+=1
            
            shots_=[]
            for shot in shots:
                shot_=(shot[0]-4*su*shift[0]-2*su,shot[1]-4*su*shift[1])
                if shot[0]>0 and not (land[(shot_[0]-shot_[0]%(4*su))/(4*su)] !=hole and 64*su-land[(shot_[0]-shot_[0]%(4*su))/(4*su)]*4*su<shot_[1] and shot[0]%(4*su)==3*su):
                    shots_.append(shot_)
            shots=shots_
            
            shotclock+=1
            if shotclock==1*FPS:
                shotclock=0
                for enemy in enemies:
                    if enemy<=28:
                        shots.append(((4*enemy+1)*su,(64-4*land[enemy]+1)*su))
            
            
            
            enemies_=[]
            for enemy in enemies:
                enemyx=4*su*enemy-offset[0]*su
                enemyy=64*su-4*su*land[enemy]+offset[1]*su
                screen.fill(ENEMY,((enemyx,enemyy),(4*su,4*su)))
                screen.fill(INNERENEMY,((enemyx+su,enemyy+su),(2*su,2*su)))
                screen.fill(INNERENEMY,((enemyx+su,enemyy-su),(2*su,1*su)))
                screen.fill(ENEMY,((enemyx,enemyy-2*su+(shotclock<=1 and enemy<=28)*su),(4*su,1*su)))
                if ((land[8]==7 and enemy==8) or (land[9]==7 and offset[0]!=0 and enemy==9)) and offset[1]==0:
                    if random.randint(0,9)==0:
                        screen.fill(INNERENEMY,((enemyx-2*su,enemyy-2*su),(8*su,8*su)))
                        screen.fill(ENEMY,((enemyx,enemyy),(4*su,4*su)))
                        if fullhealth:
                            offset[1]=2
                            score+=100
                            highscore+=100
                            if random.randint(0,9)==0:
                                score+=200
                                highscore+=200
                                screen.fill(INNERENEMY,((enemyx-3*su,enemyy-3*su),(10*su,10*su)))
                                screen.fill(ENEMY,((enemyx-su,enemyy-su),(6*su,6*su)))
                                fullhealth=False
                                offset[1]=3
                        else:
                            fullhealth=True
                        #print 'good'
                    else:
                        screen.fill(INNERENEMY,((enemyx-su,enemyy-su),(6*su,6*su)))
                        screen.fill(ENEMY,((enemyx,enemyy),(4*su,4*su)))
                        score+=10
                        highscore+=10
                else:
                    enemies_.append(enemy)
                enemies=enemies_
            
            if bat:
                if random.randint(0,2)!=0:
                    if batpos[0]>=32 and batpos[1]>=32:
                        batshift=(-2,-2)
                    elif batpos[0]<32 and batpos[1]>=32:
                        batshift=(2,-2)
                    elif batpos[0]<32 and batpos[1]<32:
                        batshift=(2,2)
                    else:# batpos[0]<=16 and batpos[1]<=16:
                        batshift=(-2,2)
                else:
                    rand=random.randint(0,3)
                    if rand==0:
                        batshift=(-1,1)
                    elif rand==1:
                        batshift=(-1,-1)
                    elif rand==2:
                        batshift=(1,-1)
                    else:# rand==3:
                        batshift=(1,1)
                
                #print batpos
                batpos=(batpos[0]+batshift[0],batpos[1]+batshift[1])
                batpos=(batpos[0]-4*shift[0],batpos[1]+4*shift[1])
                
                screen.fill(BAT,((su*batpos[0]-su*offset[0]+su,64*su-su*batpos[1]+su*offset[1]+su),(7*su,su)))
                screen.fill(BAT,((su*batpos[0]-su*offset[0]+3*su,64*su-su*batpos[1]+su*offset[1]),(su,su)))
                screen.fill(BAT,((su*batpos[0]-su*offset[0]+5*su,64*su-su*batpos[1]+su*offset[1]),(su,su)))
                screen.fill(BAT,((su*batpos[0]-su*offset[0]+3*su,64*su-su*batpos[1]+su*offset[1]+2*su),(3*su,su)))
                screen.fill(BAT,((su*batpos[0]-su*offset[0],64*su-su*batpos[1]+su*offset[1]+su*(shotclock%4>1)),(2*su,su)))
                screen.fill(BAT,((su*batpos[0]-su*offset[0]+su*7,64*su-su*batpos[1]+su*offset[1]+su*(shotclock%4>1)),(2*su,su)))
                screen.fill(INNERBAT,((su*batpos[0]-su*offset[0]+3*su,64*su-su*batpos[1]+su*offset[1]+su),(su,su)))
                screen.fill(INNERBAT,((su*batpos[0]-su*offset[0]+5*su,64*su-su*batpos[1]+su*offset[1]+su),(su,su)))
                
                if batpos[0]-offset[0]>25 and batpos[0]-offset[0]<36 and batpos[1]+offset[1]>32 and batpos[1]+offset[1]<40:
                    #if batpos[1]+offset[1]<31 and batpos[1]+offset[1]+fall>28 and fall>0.5:
                    if fall-4.125*jump>0.25:
                        bat-=1
                        batpos=(130,68)
                        screen.fill(BAT,((31*su,33*su),(6*su,6*su)))
                        if not fullhealth and (not bat or not boss):
                            fullhealth=True
                        else:
                            highscore+=25
                            score+=25
                    #elif batpos[1]>23 and batpos[1]<36:
                    else:
                        if fullhealth:
                            fullhealth=False
                        else:
                            killed=True
                        batpos=(130,68)
            if boss and level==1 and not bat:
                boss=False
                        
            if ghost:
                GHOST=(GHOST[0]+8-16*ghostfade,GHOST[1]+8-16*ghostfade,GHOST[2]+8-16*ghostfade)
                if GHOST[0]>255:
                    GHOST=(255,255,255)
                    ghostfade=True
                elif GHOST[0]<0:
                    GHOST=(0,0,0)
                    ghostfade=False
                    ghostpos=(random.randint(7,9),random.randint(7,12))
                ghostpos=(ghostpos[0]-shift[0],ghostpos[1]+shift[1])
                screen.fill(GHOST,((4*su*ghostpos[0]-su*offset[0],64*su-4*su*ghostpos[1]+su*offset[1]),(8*su,8*su)))
                screen.fill(INNERGHOST,((4*su*ghostpos[0]-su*offset[0]+su,64*su-4*su*ghostpos[1]+su*offset[1]+su),(2*su,2*su)))
                screen.fill(INNERGHOST,((4*su*ghostpos[0]-su*offset[0]+5*su,64*su-4*su*ghostpos[1]+su*offset[1]+su),(2*su,2*su)))
                screen.fill(INNERGHOST,((4*su*ghostpos[0]-su*offset[0]+3*su,64*su-4*su*ghostpos[1]+su*offset[1]+4*su),(2*su,3*su)))
                
                if GHOST[0]>=191 and 4*su*ghostpos[0]-su*offset[0]>24*su and 4*su*ghostpos[0]-su*offset[0]<36*su and 64*su-4*su*ghostpos[1]+su*offset[1]<36*su and 64*su-4*su*ghostpos[1]+su*offset[1]>24*su-4*su*fullhealth:
                    if fullhealth:
                        fullhealth=not fullhealth
                    else:
                        killed=True
                    ghost=False
            
            
            if fullhealth and body<8:
                body+=1
            elif not fullhealth and body>4:
                body-=1
            
            screen.fill(PLAYER,((32*su,(36-body)*su),(4*su,body*su)))
            
            shots_=[]
            for shot in shots:
                screen.fill(SHOT, ((shot[0]-su*offset[0],shot[1]+su*offset[1]),(2*su,2*su)))
                
                #(shot[0]-su*offset[0],shot[1]+su*offset[1])
                
                if shot[0]-su*offset[0]>30*su and shot[0]-su*offset[0]<36*su:
                    if fullhealth and shot[1]+su*offset[1]>26*su and shot[1]+su*offset[1]<36*su:
                        fullhealth=False
                        #print 'hurt'
                    elif not fullhealth and shot[1]+su*offset[1]>30*su and shot[1]+su*offset[1]<36*su:
                        #print 'dead'
                        killed=True
                    else:
                        shots_.append(shot)
                elif ghost and shot[0]-su*offset[0]>=4*su*ghostpos[0]-su*offset[0] and shot[0]-su*offset[0]<4*su*ghostpos[0]-su*offset[0]+su*8 and shot[1]+su*offset[1]>=64*su-4*su*ghostpos[1]+su*offset[1] and shot[1]+su*offset[1]<64*su-4*su*ghostpos[1]+su*offset[1]+8*su:
                    ghosthealth-=1
                    if ghosthealth==0:
                        ghost=False
                        if not fullhealth:
                            fullhealth=True
                        else:
                            score+=100
                            highscore+=100
                        if boss:
                            boss=False
                            enemies=[]
                            bottom=1
                    GHOST=(-1,-1,-1)
                    ghostpos=(random.randint(7,9),random.randint(7,12))
                    ghostfade=False
                else:
                    shots_.append(shot)
            shots=shots_
            
            if score>highscore:
                highscore=score
                #print highscore
            
            screen.fill(DOCK,((0,64*su),(sx,sy-64*su)))
            pygame.draw.line(screen, LINES, (0.75*dpi,64*su),(0.75*dpi,sy),su)
            pygame.draw.line(screen, LINES, (1.25*dpi,64*su),(1.25*dpi,sy),su)
            pygame.draw.line(screen, LINES, (2*dpi,64*su),(2*dpi,sy),su)
            pygame.draw.line(screen, LINES, (122*su,sy-dpi),(sx,sy-dpi),su)
            screen.fill(DOCK,((128*su,0),(sx,sy)))
            screen.blit(font.render(str(highscore),True,TEXT),(2*dpi+3*su,66*su))
            
            pygame.display.flip()
            if killed:
                clock.tick(0.5)
                running=False
                
            clock.tick(FPS)
            
        score=highscore
        total+=highscore
        records_=[]
        for record in records:
            if record>=highscore:
                records_.append(record)
            else:
                records_.append(highscore)
                highscore=-1
                records_.append(record)
                showrecords=True
        records=records_[:10]
        
        if boss:
            if level!=-1:
                level-=1
            else:
                level=0
                
        with open('records.txt','w') as records_:
            records_.write(str(level)+'\n')
            records_.write(str(total)+'\n')
            records_.write(str(bottom)+'\n')
            records_.write(str(christina)+'\n')
            for record in records:
                records_.write(str(record)+'\n')
                
        
        
        pygame.event.clear()
        while showrecords:
            if android and android.check_pause():
                '''with open('records.txt','w') as records_:
                    records_.write(str(total)+'\n')
                    for record in records:
                        records_.write(str(record)+'\n')'''
                android.wait_for_resume()
            
            events = pygame.event.get()
            
            #manage events
            for event in events:
                #get touches
                if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    showrecords=False
                    menu=True
                            
            x1-=su*0.25
            x2-=su*0.25
            if x1<-128*su:x1=128*su
            if x2<-128*su:x2=128*su
            screen.fill(SKY)
            screen.fill(GROUND,((x1,36*su),(124*su,28*su)))
            screen.fill(GRASS,((x1,36*su),(124*su,su)))
            screen.fill(GROUND,((x2,32*su),(124*su,32*su)))
            screen.fill(GRASS,((x2,32*su),(124*su,su)))
            screen.fill(DOCK,((0,64*su),(sx,sy-64*su)))
            screen.fill(DOCK,((128*su,0),(sx,sy)))
            
            screen.blit(font.render((str(records[0])),True,TEXT),(su,su))
            screen.blit(font.render((str(records[1])),True,TEXT),(su,13*su))
            screen.blit(font.render((str(records[2])),True,TEXT),(su,2*13*su))
            screen.blit(font.render((str(records[3])),True,TEXT),(su,3*13*su))
            screen.blit(font.render((str(records[4])),True,TEXT),(su,4*13*su))
            
            screen.blit(font.render((str(records[5])),True,TEXT),(sx/2,su))
            screen.blit(font.render((str(records[6])),True,TEXT),(sx/2,13*su))
            screen.blit(font.render((str(records[7])),True,TEXT),(sx/2,2*13*su))
            screen.blit(font.render((str(records[8])),True,TEXT),(sx/2,3*13*su))
            screen.blit(font.render((str(records[9])),True,TEXT),(sx/2,4*13*su))
            
            if score>0:
                banner=('Total '+str(total)+'    New Ranked Score '+str(score))
            else:
                banner=('Total '+str(total))
            screen.blit(font.render(banner,True,TEXT),(su,65*su))
            
            
            clock.tick(FPS)
            pygame.display.flip()
            

if __name__ == "__main__":
    main()
