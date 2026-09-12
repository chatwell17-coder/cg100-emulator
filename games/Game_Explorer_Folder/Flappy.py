from casioplot import *
from random import randint

UP=14;EXE=95;BACK=22
W=192;H=192;HUD=18
BG=(255,255,255);TXT=(20,24,30);MUT=(105,110,120)
PIPE=(80,175,65);CAP=(55,140,45)
BIRD=(250,215,35);WING=(225,175,25);BEAK=(250,125,20)
BLUE=(35,115,220);RED=(210,50,45)

PW=14;GAP=48;SPACE=94;SPD=3
BX=44;BW=7;BH=7
Q=4;GRAV=2;FLAP=-14;MAXV=13
POLLS=4;WORK1=85;WORK2=12
BEST=0;LK=None

def fr(x0,y0,x1,y1,c):
 if x0<0:x0=0
 if y0<0:y0=0
 if x1>=W:x1=W-1
 if y1>=H:y1=H-1
 if x0>x1 or y0>y1:return
 x=x0
 while x<=x1:
  y=y0
  while y<=y1:set_pixel(x,y,c);y+=1
  x+=1

def hl(x,y,n,c):fr(x,y,x+n-1,y,c)

def text(x,y,s,c=TXT,z="small"):draw_string(x,y,s,c,z)

def edge_raw(k):
 global LK
 if k==None:LK=None;return None
 if LK==None:LK=k;return k
 return None

def tick(two):
 flap=0;p=0;w=WORK2 if two else WORK1
 while p<POLLS:
  t=0
  while t<w:t+=1
  k=edge_raw(getkey())
  if k==UP or k==EXE:flap=1
  elif k==BACK:return flap,0
  p+=1
 return flap,1

def wait_key():
 global LK
 LK=None
 while 1:
  k=edge_raw(getkey())
  if k!=None:return k

def gap_edges(g):
 return g-GAP//2,g+GAP//2

def new_gap(old):
 g=old+randint(-30,30)
 lo=HUD+GAP//2+7;hi=H-GAP//2-8
 if g<lo:g=lo
 if g>hi:g=hi
 return g

def pipe_full(x,g):
 a,b=gap_edges(g)
 # stem is deliberately 1 px left of cap centre
 fr(x-1,HUD,x+PW-2,a-1,PIPE)
 fr(x-1,b+1,x+PW-2,H-1,PIPE)
 fr(x-2,a-4,x+PW+1,a-1,CAP)
 fr(x-2,b+1,x+PW+1,b+4,CAP)

def pipe_clear(x,g):
 a,b=gap_edges(g)
 fr(x-2,HUD,x+PW+1,a-1,BG)
 fr(x-2,b+1,x+PW+1,H-1,BG)

def pipe_move(ox,nx,g):
 d=ox-nx
 if d<=0:return
 a,b=gap_edges(g)

 # trailing pixels: erase only what actually left the pipe
 br=ox+PW-2
 cr=ox+PW+1
 fr(br-d+1,HUD,br,a-1,BG)
 fr(br-d+1,b+1,br,H-1,BG)
 fr(cr-d+1,a-4,cr,a-1,BG)
 fr(cr-d+1,b+1,cr,b+4,BG)

 # leading pixels: draw only the newly exposed strips
 bl=nx-1
 cl=nx-2
 fr(bl,HUD,bl+d-1,a-1,PIPE)
 fr(bl,b+1,bl+d-1,H-1,PIPE)
 fr(cl,a-4,cl+d-1,a-1,CAP)
 fr(cl,b+1,cl+d-1,b+4,CAP)

def visible(x):
 return x+PW+1>=0 and x-2<W

def bird_box(y):
 h=BH//2
 return BX-BW//2,y-h,BX+BW//2,y+h

def bird_clear(y):
 l,t,r,b=bird_box(y)
 fr(l-1,t-1,r+3,b+1,BG)

def bird(y,wing):
 l,t,r,b=bird_box(y)
 fr(l,t+1,r-1,b-1,BIRD)
 fr(l+1,t,r-1,b,BIRD)
 fr(r,t+2,r,b-2,BIRD)
 if wing:fr(l-1,y,l+2,y+2,WING)
 else:fr(l-1,y-2,l+2,y,WING)
 set_pixel(r-1,y-1,TXT)
 set_pixel(r+1,y,BEAK);set_pixel(r+2,y,BEAK)

def hit(y,x,g):
 l,t,r,b=bird_box(y);a,z=gap_edges(g)
 if r<x-2 or l>x+PW+1:return 0
 # pipe body
 if r>=x-1 and l<=x+PW-2 and (t<a or b>z):return 1
 # caps extend two pixels sideways
 if b>=a-4 and t<=a-1:return 1
 if b>=z+1 and t<=z+4:return 1
 return 0

def hud(sc):
 fr(0,0,W-1,HUD-1,BG)
 text(4,2,"SCORE "+str(sc),TXT)
 text(83,2,"BEST "+str(BEST),TXT)
 text(153,2,"BACK",MUT)
 hl(0,HUD-1,W,(185,190,198))

def panel(title,sc=-1):
 clear_screen()
 text(45,34,title,TXT,"large")
 if sc>=0:
  text(55,72,"SCORE "+str(sc),TXT,"medium")
  text(55,94,"BEST  "+str(BEST),TXT,"medium")
  text(35,132,"EXE REPLAY",BLUE,"medium")
 else:
  text(46,78,"UP / EXE = FLAP",MUT)
  text(48,108,"EXE = START",BLUE,"medium")
 text(48,158,"BACK = EXIT",MUT)
 show_screen()

def title():
 panel("FLAPPY BIRD")
 while 1:
  k=wait_key()
  if k==EXE or k==UP:return 1
  if k==BACK:return 0

def over(sc):
 global BEST
 if sc>BEST:BEST=sc
 panel("GAME OVER",sc)
 while 1:
  k=wait_key()
  if k==EXE:return 1
  if k==BACK:return 0

def game():
 global BEST,LK
 LK=None
 yq=96*Q;vy=0;sc=0;wing=0
 x1=W+14;g1=96;p1=0
 x2=x1+SPACE;g2=new_gap(g1);p2=0
 clear_screen();hud(0)
 pipe_full(x1,g1);pipe_full(x2,g2);bird(yq//Q,wing);show_screen()
 while 1:
  flap,go=tick(visible(x1) and visible(x2))
  if not go:return -1
  oy=yq//Q;ox1=x1;ox2=x2
  if flap:vy=FLAP
  vy+=GRAV
  if vy>MAXV:vy=MAXV
  yq+=vy
  y=yq//Q
  x1-=SPD;x2-=SPD

  if y-BH//2<=HUD or y+BH//2>=H-1:return sc
  if hit(y,x1,g1) or hit(y,x2,g2):return sc

  if not p1 and x1+PW+1<BX:
   sc+=1;p1=1
   if sc>BEST:BEST=sc
   hud(sc)
  if not p2 and x2+PW+1<BX:
   sc+=1;p2=1
   if sc>BEST:BEST=sc
   hud(sc)

  bird_clear(oy)
  pipe_move(ox1,x1,g1);pipe_move(ox2,x2,g2)

  if x1+PW+1<0:
   pipe_clear(x1,g1)
   x1=x2+SPACE;g1=new_gap(g2);p1=0
   pipe_full(x1,g1)
  if x2+PW+1<0:
   pipe_clear(x2,g2)
   x2=x1+SPACE;g2=new_gap(g1);p2=0
   pipe_full(x2,g2)

  wing=0 if wing else 1
  bird(y,wing)
  show_screen()

def main():
 while 1:
  if not title():return
  s=game()
  if s<0:return
  if not over(s):return

main()
