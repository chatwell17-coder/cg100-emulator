from casioplot import *

KU=14;KD=34;KL=23;KR=25;KOK=24;KEXE=95;KEXIT=12
W=192;H=192

BG=(255,255,255)
TXT=(0,0,0)
GRID=(0,0,0)
CUR=(0,120,255)

# Layout
S=48
OX=24
OY=30

b=[0]*9  # 0 empty, 1 X, 2 O
cur=4
pl=1
LK=None

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

def line(x0,y0,x1,y1,c):
 dx=1 if x1>=x0 else -1
 dy=1 if y1>=y0 else -1
 x=x0;y=y0
 fr(x,y,x,y,c)
 while x!=x1 or y!=y1:
  if x!=x1:x+=dx
  if y!=y1:y+=dy
  fr(x,y,x,y,c)

def key_edge():
 global LK
 k=getkey()
 if k==None:
  LK=None;return None
 if LK==None:
  LK=k;return k
 return None

def cell_xy(i):
 return OX+(i%3)*S, OY+(i//3)*S

def draw_grid():
 fr(0,0,W-1,H-1,BG)
 draw_string(0,0,"Tic Tac Toe",TXT,"medium")
 # vertical lines
 x=OX+S;fr(x,OY,x,OY+3*S-1,GRID)
 x=OX+2*S;fr(x,OY,x,OY+3*S-1,GRID)
 # horizontal lines
 y=OY+S;fr(OX,y,OX+3*S-1,y,GRID)
 y=OY+2*S;fr(OX,y,OX+3*S-1,y,GRID)

def draw_x(px,py):
 m=10
 line(px+m,py+m,px+S-m,py+S-m,GRID)
 line(px+S-m,py+m,px+m,py+S-m,GRID)

def draw_o(px,py):
 cx=px+S//2;cy=py+S//2
 r=S//2-10
 rr=r*r
 y=-r
 while y<=r:
  x=-r
  while x<=r:
   d=x*x+y*y
   if rr-2*r<=d<=rr:
    set_pixel(cx+x,cy+y,GRID)
   x+=1
  y+=1

def highlight(i,on):
 px,py=cell_xy(i)
 c=CUR if on else BG
 fr(px+1,py+1,px+S-2,py+2,c)
 fr(px+1,py+1,px+2,py+S-2,c)
 fr(px+S-3,py+1,px+S-2,py+S-2,c)
 fr(px+1,py+S-3,px+S-2,py+S-2,c)

def draw_piece(i):
 px,py=cell_xy(i)
 # clear interior (keep grid lines)
 fr(px+2,py+2,px+S-3,py+S-3,BG)
 if b[i]==1:draw_x(px,py)
 elif b[i]==2:draw_o(px,py)

def win(p):
 # rows
 if b[0]==p and b[1]==p and b[2]==p:return 1
 if b[3]==p and b[4]==p and b[5]==p:return 1
 if b[6]==p and b[7]==p and b[8]==p:return 1
 # cols
 if b[0]==p and b[3]==p and b[6]==p:return 1
 if b[1]==p and b[4]==p and b[7]==p:return 1
 if b[2]==p and b[5]==p and b[8]==p:return 1
 # diags
 if b[0]==p and b[4]==p and b[8]==p:return 1
 if b[2]==p and b[4]==p and b[6]==p:return 1
 return 0

def full():
 i=0
 while i<9:
  if b[i]==0:return 0
  i+=1
 return 1

def end_screen(msg):
 global LK
 LK=None
 fr(0,0,W-1,H-1,BG)
 draw_string(35,70,msg,TXT,"large")
 draw_string(20,120,"EXE=Restart",TXT,"medium")
 draw_string(25,145,"AC=Quit",TXT,"medium")
 show_screen()
 while 1:
  k=key_edge()
  if k==KEXE:return 1
  if k==KEXIT:return 0

def main():
 global b,cur,pl,LK
 while 1:
  b=[0]*9;cur=4;pl=1;LK=None
  draw_grid();i=0
  while i<9:draw_piece(i);i+=1
  highlight(cur,1);show_screen();restart=0
  while 1:
   k=key_edge()
   if k==None:continue
   if k==KEXIT:return
   if k==KEXE:restart=1;break
   old=cur
   if k==KU and cur>=3:cur-=3
   elif k==KD and cur<=5:cur+=3
   elif k==KL and cur%3:cur-=1
   elif k==KR and cur%3!=2:cur+=1
   elif k==KOK:
    if b[cur]:continue
    b[cur]=pl;draw_piece(cur);highlight(cur,1);show_screen()
    if win(pl):
     if end_screen("P"+str(pl)+" wins"):restart=1
     else:return
     break
    if full():
     if end_screen("Draw"):restart=1
     else:return
     break
    pl=2 if pl==1 else 1
   if cur!=old:
    highlight(old,0);highlight(cur,1);show_screen()
  if not restart:return

main()
