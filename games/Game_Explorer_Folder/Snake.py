from casioplot import *
from random import randint

K_UP=14;K_DOWN=34;K_LEFT=23;K_RIGHT=25;K_EXE=95;K_EXIT=12
W=192;H=192
BS=12
GW=16;GH=16
HUDPX=24;HUD=HUDPX//BS
SPEED=4

HUDBG=(245,245,245)
TXT=(0,0,0)
BORD=(0,0,0)
BG1=(246,248,244)
BG2=(232,238,230)
HEAD=(20,135,20)
HEAD2=(90,210,90)
BODY=(40,190,40)
BODY2=(120,230,120)
FOOD=(220,45,45)
FOOD2=(255,250,250)
STEM=(70,45,20)
LEAF=(30,150,60)

BEST=0
LK=None

INW=GW-2
INH=GH-HUD-2
MAXLEN=INW*INH


def fr(x0,y0,x1,y1,c):
 if x0<0:x0=0
 if y0<0:y0=0
 if x1>W-1:x1=W-1
 if y1>H-1:y1=H-1
 if x0>x1 or y0>y1:return
 x=x0
 while x<=x1:
  y=y0
  while y<=y1:
   set_pixel(x,y,c)
   y+=1
  x+=1


def cx(t,s):
 a=9 if s=="large" else 5 if s=="medium" else 4
 return 96-(len(t)*a//2)


def cell_bg(x,y):
 return BG1 if ((x+y)&1)==0 else BG2


def cell_rect(x,y):
 px=x*BS;py=y*BS
 return px,py,px+BS-1,py+BS-1


def draw_cell_bg(x,y):
 l,t,r,b=cell_rect(x,y)
 fr(l,t,r,b,cell_bg(x,y))


def draw_border():
 x=0
 while x<GW:
  l,t,r,b=cell_rect(x,HUD)
  fr(l,t,r,b,BORD)
  l,t,r,b=cell_rect(x,GH-1)
  fr(l,t,r,b,BORD)
  x+=1
 y=HUD
 while y<GH:
  l,t,r,b=cell_rect(0,y)
  fr(l,t,r,b,BORD)
  l,t,r,b=cell_rect(GW-1,y)
  fr(l,t,r,b,BORD)
  y+=1


def draw_playfield():
 y=HUD+1
 while y<GH-1:
  x=1
  while x<GW-1:
   draw_cell_bg(x,y)
   x+=1
  y+=1
 draw_border()


def draw_hud(score):
 fr(0,0,W-1,HUDPX-1,HUDBG)
 draw_string(4,2,"Score: "+str(score),TXT,"medium")
 draw_string(112,2,"Best: "+str(BEST),TXT,"medium")
 fr(0,HUDPX-1,W-1,HUDPX-1,BORD)


def draw_seg(x,y,head,dx,dy):
 draw_cell_bg(x,y)
 l,t,r,b=cell_rect(x,y)
 if head:
  fr(l+1,t+1,r-1,b-1,HEAD)
  fr(l+3,t+3,r-3,b-3,HEAD2)
  if dx==1:
   fr(r-4,t+3,r-3,t+4,TXT);fr(r-4,b-4,r-3,b-3,TXT)
   fr(r-2,(t+b)//2-1,r-1,(t+b)//2+1,TXT)
  elif dx==-1:
   fr(l+3,t+3,l+4,t+4,TXT);fr(l+3,b-4,l+4,b-3,TXT)
   fr(l,(t+b)//2-1,l+1,(t+b)//2+1,TXT)
  elif dy==-1:
   fr(l+3,t+3,l+4,t+4,TXT);fr(r-4,t+3,r-3,t+4,TXT)
   fr((l+r)//2-1,t,(l+r)//2+1,t+1,TXT)
  else:
   fr(l+3,b-4,l+4,b-3,TXT);fr(r-4,b-4,r-3,b-3,TXT)
   fr((l+r)//2-1,b-1,(l+r)//2+1,b,TXT)
 else:
  fr(l+2,t+2,r-2,b-2,BODY)
  fr(l+4,t+4,r-4,b-4,BODY2)
  if dx:
   fr(l+1,(t+b)//2-1,r-1,(t+b)//2+1,HEAD)
  else:
   fr((l+r)//2-1,t+1,(l+r)//2+1,b-1,HEAD)


def draw_food(x,y):
 draw_cell_bg(x,y)
 l,t,r,b=cell_rect(x,y)
 fr(l+3,t+4,r-3,b-2,FOOD)
 fr(l+5,t+6,r-5,b-4,FOOD2)
 fr((l+r)//2,t+2,(l+r)//2+1,t+4,STEM)
 fr((l+r)//2+1,t+2,(l+r)//2+3,t+3,LEAF)


def title_screen():
 global LK
 LK=None
 while getkey()!=None:pass
 tx=-30
 clear_screen()
 fr(0,0,W-1,H-1,HUDBG)
 draw_string(cx("SNAKE","large")+tx,42,"SNAKE",TXT,"large")
 draw_string(cx("CG100 EDITION","small")+tx,66,"CG100 EDITION",TXT,"small")
 draw_string(cx("EXE = START","medium")+tx,108,"EXE = START",TXT,"medium")
 draw_string(cx("AC = QUIT","medium")+tx,132,"AC = QUIT",TXT,"medium")
 draw_string(cx("BEST: "+str(BEST),"medium")+tx,160,"BEST: "+str(BEST),TXT,"medium")
 show_screen()
 while 1:
  k=getkey()
  if k==K_EXE:return 1
  if k==K_EXIT:return 0


def end_screen(score,win):
 global LK
 LK=None
 while getkey()!=None:pass
 clear_screen();fr(0,0,W-1,H-1,HUDBG)
 msg="YOU WIN" if win else "GAME OVER";tx=-30
 draw_string(cx(msg,"large")+tx,54,msg,TXT,"large")
 draw_string(cx("Score: "+str(score),"medium")+tx,96,"Score: "+str(score),TXT,"medium")
 draw_string(cx("Best: "+str(BEST),"medium")+tx,118,"Best: "+str(BEST),TXT,"medium")
 draw_string(cx("EXE = REPLAY","medium")+tx,146,"EXE = REPLAY",TXT,"medium")
 draw_string(cx("AC = QUIT","medium")+tx,168,"AC = QUIT",TXT,"medium")
 show_screen()
 while 1:
  k=key_edge_raw(getkey())
  if k==K_EXE:return 1
  if k==K_EXIT:return 0

def key_edge_raw(k):
 global LK
 if k==None:
  LK=None
  return None
 if LK==None:
  LK=k
  return k
 return None


def apply_turn(k,dx,dy,qdx,qdy):
 if k==K_UP:ndx,ndy=0,-1
 elif k==K_DOWN:ndx,ndy=0,1
 elif k==K_LEFT:ndx,ndy=-1,0
 elif k==K_RIGHT:ndx,ndy=1,0
 else:return qdx,qdy,1
 if ndx*dx+ndy*dy==0:return ndx,ndy,1
 return qdx,qdy,1


def tick_wait(dx,dy,qdx,qdy):
 polls=18
 chunk=120*SPEED
 playing=1
 i=0
 while i<polls:
  t=0
  while t<chunk:t+=1
  k=key_edge_raw(getkey())
  if k!=None:
   if k==K_EXIT:playing=0
   else:qdx,qdy,playing=apply_turn(k,dx,dy,qdx,qdy)
  i+=1
 return qdx,qdy,playing


def food_pos(snake):
 if len(snake)>=MAXLEN:return None
 while 1:
  x=randint(1,GW-2)
  y=randint(HUD+1,GH-2)
  ok=1
  i=0
  while i<len(snake):
   if snake[i]==(x,y):ok=0;break
   i+=1
  if ok:return x,y


def game():
 global LK,BEST
 LK=None
 clear_screen()
 draw_hud(0)
 draw_playfield()
 sx=GW//2+1;sy=(HUD+GH)//2
 snake=[(sx,sy),(sx-1,sy),(sx-2,sy)]
 food=food_pos(snake)
 dx=1;dy=0;qdx=1;qdy=0
 score=0
 i=len(snake)-1
 while i>=0:
  x,y=snake[i]
  draw_seg(x,y,i==0,dx,dy)
  i-=1
 draw_food(food[0],food[1])
 show_screen()
 while 1:
  qdx,qdy,playing=tick_wait(dx,dy,qdx,qdy)
  if not playing:return -1,0
  dx,dy=qdx,qdy
  hx,hy=snake[0]
  nx=hx+dx;ny=hy+dy
  if nx<=0 or nx>=GW-1 or ny<=HUD or ny>=GH-1:return score,0
  eat=(nx,ny)==food
  lim=len(snake) if eat else len(snake)-1
  i=0
  while i<lim:
   if snake[i]==(nx,ny):return score,0
   i+=1
  ox,oy=snake[0]
  snake.insert(0,(nx,ny))
  draw_seg(ox,oy,0,dx,dy)
  draw_seg(nx,ny,1,dx,dy)
  if eat:
   score+=1
   if score>BEST:BEST=score
   draw_hud(score)
   food=food_pos(snake)
   if food==None:
    show_screen()
    return score,1
   draw_food(food[0],food[1])
  else:
   tx,ty=snake.pop()
   draw_cell_bg(tx,ty)
  show_screen()


def main(show_title=1):
 global BEST
 if show_title and title_screen()==0:return
 while 1:
  score,win=game()
  if score<0:return
  if score>BEST:BEST=score
  if not end_screen(score,win):return

main()
