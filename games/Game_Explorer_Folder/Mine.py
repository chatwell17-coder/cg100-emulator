from casioplot import *
from random import randint

U=14;D=34;L=23;R=25;OK=24;DEL=64;EXE=95;BACK=22
W=384;H=192;TOP=28
BG=(255,255,255);TXT=(20,24,30);MUT=(105,110,120)
FACE=(176,180,186);HI=(245,245,245);LO=(78,82,88)
OPEN=(222,224,228);GRID=(145,148,154);CUR=(20,115,235)
RED=(220,40,40);MINE=(25,25,25)
NC=((0,0,0),(20,70,210),(20,135,55),(205,40,40),(80,45,160),(150,45,35),(20,135,140),(20,20,20),(90,90,90))
MODES=(("SMALL",9,9,10,18),("LARGE",12,12,25,13),("WIDE",24,12,55,13))

bw=9;bh=9;mines=10;cs=18;ox=0;oy=0;n=81
board=[];state=[];near=[];left=0;flags=0;first=1
cx=0;cy=0;lk=None;hold=0;mode=0

def fill(x,y,w,h,c):
 if x<0:w+=x;x=0
 if y<0:h+=y;y=0
 if x+w>W:w=W-x
 if y+h>H:h=H-y
 yy=y
 while yy<y+h:
  xx=x
  while xx<x+w:
   set_pixel(xx,yy,c);xx+=1
  yy+=1

def hline(x,y,w,c):
 i=0
 while i<w:set_pixel(x+i,y,c);i+=1

def vline(x,y,h,c):
 i=0
 while i<h:set_pixel(x,y+i,c);i+=1

def rect(x,y,w,h,c):
 hline(x,y,w,c);hline(x,y+h-1,w,c)
 vline(x,y,h,c);vline(x+w-1,y,h,c)

def text(x,y,s,c=TXT,sz="small"):draw_string(x,y,s,c,sz)

def idx(x,y):return y*bw+x

def make_near():
 global near
 near=[];i=0
 while i<n:
  x=i%bw;y=i//bw;a=[];yy=y-1
  while yy<=y+1:
   xx=x-1
   while xx<=x+1:
    if 0<=xx<bw and 0<=yy<bh and (xx!=x or yy!=y):a.append(idx(xx,yy))
    xx+=1
   yy+=1
  near.append(a);i+=1

def setup(m):
 global bw,bh,mines,cs,ox,oy,n,board,state,left,flags,first,cx,cy,lk,hold,mode
 mode=m;z=MODES[m];bw=z[1];bh=z[2];mines=z[3];cs=z[4];n=bw*bh
 ox=(W-bw*cs)//2;oy=TOP+(H-TOP-bh*cs)//2
 board=[0]*n;state=[0]*n;left=n-mines;flags=0;first=1
 cx=bw//2;cy=bh//2;lk=None;hold=0;make_near()

def generate(safe):
 banned=[safe];j=0
 while j<len(near[safe]):banned.append(near[safe][j]);j+=1
 made=0
 while made<mines:
  q=randint(0,n-1)
  if board[q]!=9 and q not in banned:
   board[q]=9;made+=1;j=0
   while j<len(near[q]):
    t=near[q][j]
    if board[t]!=9:board[t]+=1
    j+=1

def tile_xy(i):return ox+(i%bw)*cs,oy+(i//bw)*cs

def closed(x,y):
 fill(x,y,cs,cs,FACE)
 hline(x,y,cs,HI);vline(x,y,cs,HI)
 hline(x,y+cs-1,cs,LO);vline(x+cs-1,y,cs,LO)
 if cs>10:
  hline(x+1,y+1,cs-2,(225,225,225))
  vline(x+1,y+1,cs-2,(225,225,225))

def flag_icon(x,y):
 if cs<15:
  vline(x+cs//2,y+3,cs-6,MINE)
  hline(x+3,y+cs-4,cs-6,MINE)
  fill(x+cs//2,y+3,4,3,RED)
 else:
  vline(x+cs//2,y+4,cs-8,MINE)
  hline(x+4,y+cs-5,cs-8,MINE)
  fill(x+cs//2,y+4,5,4,RED)

def mine_icon(x,y):
 c=cs//2
 fill(x+c-2,y+c-2,5,5,MINE)
 hline(x+c-4,y+c,9,MINE);vline(x+c,y+c-4,9,MINE)

def draw_tile(i,cur=0):
 x,y=tile_xy(i);s=state[i];v=board[i]
 if s==0:
  closed(x,y)
 elif s==2:
  closed(x,y);flag_icon(x,y)
 else:
  fill(x,y,cs,cs,OPEN);rect(x,y,cs,cs,GRID)
  if v==9:mine_icon(x,y)
  elif v:
   dx=4 if cs>=16 else 2
   dy=2 if cs>=16 else 0
   text(x+dx,y+dy,str(v),NC[v])
 if cur:
  rect(x+1,y+1,cs-2,cs-2,CUR)
  if cs>=16:rect(x+2,y+2,cs-4,cs-4,CUR)

def hud():
 fill(0,0,W,TOP,BG)
 text(8,4,"MINESWEEPER",TXT,"medium")
 text(154,5,"MINES "+str(mines),MUT)
 text(231,5,"FLAGS "+str(flags),MUT)
 text(305,5,"SAFE "+str(left),MUT)
 hline(0,TOP-1,W,(190,194,200))

def draw_board():
 clear_screen();hud();i=0
 while i<n:
  draw_tile(i,i==idx(cx,cy));i+=1
 show_screen()

def cursor_move(old,new):
 draw_tile(old,0);draw_tile(new,1);show_screen()

def update_cells(a):
 i=0
 while i<len(a):draw_tile(a[i],0);i+=1
 draw_tile(idx(cx,cy),1);hud();show_screen()

def reveal(i):
 global first,left
 if state[i]!=0:return 0,[]
 if first:generate(i);first=0
 if board[i]==9:
  state[i]=1;return -1,[i]
 q=[i];ch=[]
 while q:
  a=q.pop()
  if state[a]!=0:continue
  state[a]=1;left-=1;ch.append(a)
  if board[a]==0:
   j=0
   while j<len(near[a]):
    t=near[a][j]
    if state[t]==0 and board[t]!=9:q.append(t)
    j+=1
 return 1 if left==0 else 0,ch

def chord(i):
 if state[i]!=1 or board[i]<=0:return 0,[]
 f=0;j=0
 while j<len(near[i]):
  if state[near[i][j]]==2:f+=1
  j+=1
 if f!=board[i]:return 0,[]
 allc=[];j=0
 while j<len(near[i]):
  t=near[i][j]
  if state[t]==0:
   r,c=reveal(t);allc+=c
   if r==-1:return -1,allc
  j+=1
 return 1 if left==0 else 0,allc

def toggle(i):
 global flags
 if state[i]==0:
  state[i]=2;flags+=1;return 1
 if state[i]==2:
  state[i]=0;flags-=1;return 1
 return 0

def show_mines(hit):
 i=0
 while i<n:
  if board[i]==9:
   state[i]=1;draw_tile(i,i==hit)
  elif state[i]==2:
   x,y=tile_xy(i);closed(x,y);text(x+2,y+1,"X",RED)
  i+=1
 hud();show_screen()

def end_screen(win):
 global lk
 fill(70,62,244,70,BG);rect(70,62,244,70,LO)
 text(126,74,"YOU WIN" if win else "GAME OVER",TXT,"medium")
 text(97,101,"EXE NEW    BACK EXIT",MUT)
 show_screen();lk=None
 while 1:
  k=getkey()
  if k==None:lk=None
  elif lk==None:
   lk=k
   if k==EXE:return 1
   if k==BACK:return 0

def menu():
 global mode,lk
 lk=None
 while 1:
  clear_screen()
  text(18,12,"MINESWEEPER",TXT,"medium")
  text(18,34,"SELECT BOARD",MUT)
  i=0
  while i<3:
   x=28+i*116;y=70
   fill(x,y,100,54,(228,238,252) if i==mode else (242,244,247))
   rect(x,y,100,54,CUR if i==mode else GRID)
   z=MODES[i]
   text(x+12,y+10,z[0],TXT)
   text(x+12,y+29,str(z[1])+"x"+str(z[2])+"  "+str(z[3])+"M",MUT)
   i+=1
  text(18,160,"LEFT/RIGHT   OK START   BACK EXIT",MUT)
  show_screen()
  while 1:
   k=getkey()
   if k==None:lk=None;continue
   if lk!=None:continue
   lk=k
   if k==L:mode=(mode-1)%3;break
   if k==R:mode=(mode+1)%3;break
   if k==OK or k==EXE:return 1
   if k==BACK:return 0

def key():
 global lk,hold
 k=getkey()
 if k==None:lk=None;hold=0;return None
 if k in (U,D,L,R):
  if lk!=k:lk=k;hold=0;return k
  hold+=1
  if hold>500 and hold%180==0:return k
  return None
 if lk==None:lk=k;return k
 return None

def game():
 global cx,cy
 setup(mode);draw_board()
 while 1:
  k=key()
  if k==None:continue
  old=idx(cx,cy)
  if k==BACK:return -1
  if k==EXE:return 2
  if k==L:cx=(cx-1)%bw
  elif k==R:cx=(cx+1)%bw
  elif k==U:cy=(cy-1)%bh
  elif k==D:cy=(cy+1)%bh
  elif k==DEL:
   if toggle(old):update_cells([old])
   continue
  elif k==OK:
   if state[old]==1:r,ch=chord(old)
   else:r,ch=reveal(old)
   if r==-1:
    show_mines(old);return 0
   update_cells(ch)
   if r==1:return 1
   continue
  new=idx(cx,cy)
  if new!=old:cursor_move(old,new)

def main():
 while 1:
  if not menu():return
  while 1:
   r=game()
   if r==-1:return
   if r==2:continue
   if r==0 or r==1:
    if not end_screen(r==1):return
    break

main()
