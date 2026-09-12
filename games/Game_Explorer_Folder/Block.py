from casioplot import *
from random import randint
K_UP=14;K_DOWN=34;K_LEFT=23;K_RIGHT=25;K_OK=24;K_EXE=95;K_EXIT=12;K1=81;K2=82;K3=83
W=192;H=192;HUD=24;S=18;BX=2;BY=HUD;BW=8*S-1;BH=8*S-1;TX=BX+8*S+4;TY=BY;SLOT=54;MINI=6
BG=(255,255,255);TXT=(0,0,0);GRID=(200,200,200);OKC=(0,120,255);BADC=(255,0,0);SEL=(0,0,0)
COL=[(40,160,255),(255,120,40),(120,220,80),(240,80,180),(255,220,60),(80,120,255),(255,80,80)]
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
def hud_clear():fr(0,0,W-1,HUD-1,BG)
def draw_hud(score,sel):
 hud_clear()
 draw_string(0,2,"Score: "+str(score),TXT,"medium")
 draw_string(0,14,"Sel: "+str(sel+1)+" (1-3)",TXT,"small")
 draw_string(92,14,"OK=Place",TXT,"small")
def cell_xy(x,y):return BX+x*S,BY+y*S
def draw_cell_fill(x,y,c):
 px,py=cell_xy(x,y);fr(px,py,px+S-2,py+S-2,c)
def draw_cell_grid(x,y):
 px,py=cell_xy(x,y)
 fr(px-1,py-1,px+S-1,py-1,GRID);fr(px-1,py-1,px-1,py+S-1,GRID)
 fr(px+S-1,py-1,px+S-1,py+S-1,GRID);fr(px-1,py+S-1,px+S-1,py+S-1,GRID)
def draw_grid_all():
 i=0
 while i<=8:
  x=BX+i*S-1;fr(x,BY,x,BY+BH,GRID);i+=1
 j=0
 while j<=8:
  y=BY+j*S-1;fr(BX,y,BX+BW,y,GRID);j+=1
SHP=[]
def add(sh):SHP.append(sh)
add([(0,0)])
n=2
while n<=5:
 add([(i,0) for i in range(n)]);add([(0,i) for i in range(n)]);n+=1
add([(x,y) for y in range(2) for x in range(2)])
add([(x,y) for y in range(3) for x in range(3)])
add([(x,y) for y in range(3) for x in range(2)])
add([(x,y) for y in range(2) for x in range(3)])
add([(0,0),(1,0),(2,0),(1,1)]);add([(1,0),(0,1),(1,1),(1,2)]);add([(1,0),(0,1),(1,1),(2,1)]);add([(0,0),(0,1),(1,1),(0,2)])
add([(1,0),(2,0),(0,1),(1,1)]);add([(0,0),(0,1),(1,1),(1,2)]);add([(0,0),(1,0),(1,1),(2,1)]);add([(1,0),(0,1),(1,1),(0,2)])
add([(0,0),(1,0),(0,1)]);add([(0,0),(1,0),(1,1)]);add([(0,0),(0,1),(1,1)]);add([(1,0),(0,1),(1,1)])
add([(0,0),(0,1),(0,2),(1,2),(2,2)]);add([(0,0),(1,0),(2,0),(0,1),(0,2)]);add([(0,0),(1,0),(2,0),(2,1),(2,2)]);add([(2,0),(2,1),(2,2),(0,0),(1,0)])
add([(0,0),(0,1),(0,2),(1,2),(2,2)]);add([(0,0),(1,0),(2,0),(0,1),(0,2)]);add([(2,0),(2,1),(2,2),(0,0),(1,0)]);add([(0,0),(1,0),(2,0),(2,1),(2,2)])
LK=None
def key_edge():
 global LK
 k=getkey()
 if k==None:LK=None;return None
 if LK==None:LK=k;return k
 return None
def can_place(b,sh,ax,ay):
 for dx,dy in sh:
  x=ax+dx;y=ay+dy
  if x<0 or x>7 or y<0 or y>7:return 0
  if b[y][x]!=-1:return 0
 return 1
def can_fit_any(b,sh):
 y=0
 while y<8:
  x=0
  while x<8:
   if can_place(b,sh,x,y):return 1
   x+=1
  y+=1
 return 0
def any_tray_fit(b,tr):
 i=0
 while i<3:
  if tr[i]!=None and can_fit_any(b,SHP[tr[i]]):return 1
  i+=1
 return 0
def gen_tray(b):
 fit=[];i=0
 while i<len(SHP):
  if can_fit_any(b,SHP[i]):fit.append(i)
  i+=1
 if len(fit)==0:return None
 a=fit[randint(0,len(fit)-1)];b1=randint(0,len(SHP)-1);c1=randint(0,len(SHP)-1)
 return [a,b1,c1]
def clear_lines(b):
 rf=[1]*8;cf=[1]*8;y=0
 while y<8:
  x=0
  while x<8:
   if b[y][x]==-1:rf[y]=0;cf[x]=0
   x+=1
  y+=1
 r=0;c=0;i=0
 while i<8:
  if rf[i]:r+=1
  if cf[i]:c+=1
  i+=1
 if r==0 and c==0:return 0,0
 y=0
 while y<8:
  x=0
  while x<8:
   if rf[y] or cf[x]:b[y][x]=-1
   x+=1
  y+=1
 return r,c
def draw_tray(tr,sel):
 fr(TX,TY,W-1,TY+3*SLOT-2,BG);i=0
 while i<3:
  y0=TY+i*SLOT
  fr(TX,y0,W-2,y0+SLOT-2,BG);fr(TX,y0,W-2,y0,GRID);fr(TX,y0,TX,y0+SLOT-2,GRID)
  fr(W-2,y0,W-2,y0+SLOT-2,GRID);fr(TX,y0+SLOT-2,W-2,y0+SLOT-2,GRID)
  if i==sel:fr(TX+1,y0+1,W-3,y0+SLOT-3,SEL);fr(TX+2,y0+2,W-4,y0+SLOT-4,BG)
  if tr[i]==None:
   draw_string(TX+6,y0+18,"(used)",TXT,"small")
  else:
   sid=tr[i];sh=SHP[sid];ox=TX+10;oy=y0+12
   for dx,dy in sh:
    px=ox+dx*MINI;py=oy+dy*MINI
    fr(px,py,px+MINI-2,py+MINI-2,COL[sid%len(COL)])
   draw_string(TX+6,y0+2,str(i+1),TXT,"small")
  i+=1
def erase_cursor(b,ax,ay,sh):
 for dx,dy in sh:
  x=ax+dx;y=ay+dy
  if 0<=x<=7 and 0<=y<=7:
   v=b[y][x];draw_cell_fill(x,y,BG if v==-1 else COL[v]);draw_cell_grid(x,y)
def draw_cursor(ax,ay,sh,c):
 for dx,dy in sh:
  x=ax+dx;y=ay+dy
  if 0<=x<=7 and 0<=y<=7:
   px,py=cell_xy(x,y)
   fr(px,py,px+S-2,py,c);fr(px,py,px,py+S-2,c);fr(px+S-2,py,px+S-2,py+S-2,c);fr(px,py+S-2,px+S-2,py+S-2,c)
def redraw_full_board(b):
 fr(BX,BY,BX+BW,BY+BH,BG);y=0
 while y<8:
  x=0
  while x<8:
   v=b[y][x]
   if v!=-1:draw_cell_fill(x,y,COL[v])
   x+=1
  y+=1
 draw_grid_all()
def end_screen(score):
 global LK
 LK=None
 clear_screen();draw_string(45,70,"GAME OVER",TXT,"large")
 draw_string(35,110,"Score: "+str(score),TXT,"medium")
 draw_string(10,150,"EXE=Restart  AC=Quit",TXT,"small");show_screen()
 while 1:
  k=key_edge()
  if k==K_EXE:return 1
  if k==K_EXIT:return 0

def game():
 global LK
 LK=None
 b=[[-1]*8 for _ in range(8)]
 score=0;tr=gen_tray(b)
 if tr==None:return score
 sel=0;ax=0;ay=0
 clear_screen();draw_hud(score,sel);redraw_full_board(b);draw_tray(tr,sel)
 prev_ax=ax;prev_ay=ay;prev_sh=SHP[tr[sel]] if tr[sel]!=None else None
 if prev_sh!=None:draw_cursor(ax,ay,prev_sh,OKC)
 show_screen()
 while 1:
  k=key_edge()
  if k==None:continue
  if k==K_EXIT:return -1
  moved=0;traychg=0;hudchg=0;boardchg=0
  if k==K1:sel=0;traychg=1
  elif k==K2:sel=1;traychg=1
  elif k==K3:sel=2;traychg=1
  elif k==K_LEFT and ax>0:ax-=1;moved=1
  elif k==K_RIGHT and ax<7:ax+=1;moved=1
  elif k==K_UP and ay>0:ay-=1;moved=1
  elif k==K_DOWN and ay<7:ay+=1;moved=1
  elif k==K_OK and tr[sel]!=None:
   sh=SHP[tr[sel]]
   if can_place(b,sh,ax,ay):
    cid=randint(0,len(COL)-1)
    for dx,dy in sh:b[ay+dy][ax+dx]=cid
    score+=len(sh);hudchg=1
    r,c=clear_lines(b)
    if r or c:score+=8*r+8*c;hudchg=1
    tr[sel]=None;traychg=1;boardchg=1
    if tr[0]==None and tr[1]==None and tr[2]==None:
     tr=gen_tray(b)
     if tr==None:break
     sel=0;traychg=1
    if not any_tray_fit(b,tr):break
  if prev_sh!=None:erase_cursor(b,prev_ax,prev_ay,prev_sh)
  if hudchg or traychg or moved:draw_hud(score,sel)
  if boardchg:redraw_full_board(b)
  if traychg:draw_tray(tr,sel)
  sh2=SHP[tr[sel]] if tr[sel]!=None else None
  if sh2!=None:draw_cursor(ax,ay,sh2,OKC if can_place(b,sh2,ax,ay) else BADC)
  prev_ax=ax;prev_ay=ay;prev_sh=sh2
  show_screen()
 return score
def main():
 while 1:
  sc=game()
  if sc<0:return
  if not end_screen(sc):return
main()
