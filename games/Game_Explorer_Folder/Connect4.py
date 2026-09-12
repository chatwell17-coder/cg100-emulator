from casioplot import *

KU=14;KD=34;KL=23;KR=25;KOK=24;KEXE=95;KEXIT=12
W=192;H=192;HUD=22
CW=7;CH=6
S=24
OX=12;OY=HUD+10
BG=(255,255,255);TXT=(0,0,0)
BD=(40,70,200)
P1=(255,0,0);P2=(255,220,0)
SEL=(0,120,255)

b=[[0]*CW for _ in range(CH)]
sel=3
pl=1

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
   set_pixel(x,y,c);y+=1
  x+=1

def mk(r):
 pts=[]
 y=-r
 while y<=r:
  x=-r
  yy=y*y
  while x<=r:
   if x*x+yy<=r*r:pts.append((x,y))
   x+=1
  y+=1
 return pts

RH=S//2-3
RD=S//2-5
PH=mk(RH)
PD=mk(RD)

def circ(cx,cy,pts,c):
 i=0
 while i<len(pts):
  dx,dy=pts[i]
  set_pixel(cx+dx,cy+dy,c)
  i+=1

def head(p):
 fr(0,0,W-1,HUD-1,BG)
 draw_string(0,2,"Connect 4",TXT,"medium")
 fr(110,0,W-1,HUD-1,BG)
 draw_string(110,2,("P1" if p==1 else "P2")+" to move",TXT,"small")

def draw_bg():
 fr(0,HUD,W-1,H-1,BG)
 fr(OX-2,OY-2,OX+CW*S+2,OY+CH*S+2,BD)
 r=0
 while r<CH:
  c=0
  while c<CW:
   cx=OX+c*S+S//2
   cy=OY+r*S+S//2
   circ(cx,cy,PH,BG)
   c+=1
  r+=1

def draw_disc(r,c,p):
 cx=OX+c*S+S//2
 cy=OY+r*S+S//2
 circ(cx,cy,PD,P1 if p==1 else P2)

def sel_box(col,cc):
 x=OX+cc*S
 fr(x,OY-10,x+S-2,OY-4,col)

def drop(cc,p):
 r=CH-1
 while r>=0:
  if b[r][cc]==0:
   b[r][cc]=p
   draw_disc(r,cc,p)
   return r
  r-=1
 return -1

def win_at(r,c,p):
 for dr,dc in ((0,1),(1,0),(1,1),(1,-1)):
  cnt=1
  rr=r+dr;cc=c+dc
  while 0<=rr<CH and 0<=cc<CW and b[rr][cc]==p:
   cnt+=1;rr+=dr;cc+=dc
  rr=r-dr;cc=c-dc
  while 0<=rr<CH and 0<=cc<CW and b[rr][cc]==p:
   cnt+=1;rr-=dr;cc-=dc
  if cnt>=4:return 1
 return 0

def full_board():
 c=0
 while c<CW:
  if b[0][c]==0:return 0
  c+=1
 return 1

def end_screen(msg):
 global LK
 LK=None
 clear_screen()
 draw_string(40,70,msg,TXT,"large")
 draw_string(20,120,"EXE=Restart",TXT,"medium")
 draw_string(25,145,"AC=Quit",TXT,"medium")
 show_screen()
 while 1:
  k=key_edge()
  if k==KEXE:return 1
  if k==KEXIT:return 0

def main():
 global b,sel,pl,LK
 while 1:
  b=[[0]*CW for _ in range(CH)];sel=3;pl=1;LK=None
  clear_screen();head(pl);draw_bg();sel_box(SEL,sel);show_screen()
  restart=0
  while 1:
   k=key_edge()
   if k==None:continue
   if k==KEXIT:return
   if k==KEXE:restart=1;break
   if k==KL and sel>0:
    sel_box(BG,sel);sel-=1;sel_box(SEL,sel);show_screen()
   elif k==KR and sel<CW-1:
    sel_box(BG,sel);sel+=1;sel_box(SEL,sel);show_screen()
   elif k==KOK:
    r=drop(sel,pl)
    if r<0:continue
    if win_at(r,sel,pl):
     show_screen()
     if end_screen("P"+str(pl)+" wins"):restart=1
     else:return
     break
    if full_board():
     show_screen()
     if end_screen("Draw"):restart=1
     else:return
     break
    pl=2 if pl==1 else 1;head(pl);show_screen()
  if not restart:return

main()
