from casioplot import *
from random import randint

U=14;D=34;L=23;R=25;EXE=95;BACK=22
W=192;H=192;HUD=10;S=6
BG=(255,255,255);TXT=(0,0,0);WALL=(25,55,210);DOT=(40,40,40)
PAC=(255,220,20);FR=(60,80,255)
GC=((240,55,55),(255,120,35),(245,100,180),(30,190,200))
DX=(0,1,0,-1);DY=(-1,0,1,0);REV=(2,3,0,1)
POLL=4;WAIT=320;FRAMES=38;BEST=0;LK=None

MAP=(
"############################",
"#............##............#",
"#.####.#####.##.#####.####.#",
"#o####.#####.##.#####.####o#",
"#.####.#####.##.#####.####.#",
"#..........................#",
"#.####.##.########.##.####.#",
"#......##....##....##......#",
"######.#####.##.#####.######",
"######.##..........##.######",
"######.##.###  ###.##.######",
"..........# GGGG #..........",
"######.##.########.##.######",
"######.##..........##.######",
"######.##.########.##.######",
"#............##............#",
"#.####.#####.##.#####.####.#",
"#o..##.......P........##..o#",
"###.##.##.########.##.##.###",
"#......##....##....##......#",
"#.##########.##.##########.#",
"#..........................#",
"############################")
GH=len(MAP);GW=len(MAP[0]);OX=(W-GW*S)//2;OY=HUD+(H-HUD-GH*S)//2

def fr(x,y,w,h,c):
 if x<0:w+=x;x=0
 if y<0:h+=y;y=0
 if x+w>W:w=W-x
 if y+h>H:h=H-y
 yy=y
 while yy<y+h:
  xx=x
  while xx<x+w:set_pixel(xx,yy,c);xx+=1
  yy+=1

def tx(x,y,s,c=TXT,sz="small"):draw_string(x,y,s,c,sz)

def edge():
 global LK
 k=getkey()
 if k==None:LK=None;return None
 if LK==None:LK=k;return k
 return None

def parse():
 g=[];px=1;py=1;gs=[];dots=0;y=0
 while y<GH:
  row=[];x=0
  while x<GW:
   c=MAP[y][x]
   if c=="#":v=9
   elif c==".":v=1;dots+=1
   elif c=="o":v=2;dots+=1
   else:v=0
   if c=="P":px=x;py=y
   elif c=="G":gs.append([x,y,1])
   row.append(v);x+=1
  g.append(row);y+=1
 return g,dots,px,py,gs

def tile(g,x,y):
 px=OX+x*S;py=OY+y*S;v=g[y][x]
 fr(px,py,S,S,BG)
 if v==9:
  fr(px,py,S,S,WALL)
  if x and MAP[y][x-1]=="#":fr(px,py,1,S,(15,40,170))
  if y and MAP[y-1][x]=="#":fr(px,py,S,1,(15,40,170))
 elif v==1:set_pixel(px+3,py+3,DOT)
 elif v==2:fr(px+2,py+2,3,3,DOT)

def pac(x,y,d):
 px=OX+x*S;py=OY+y*S
 fr(px+1,py+1,4,4,PAC)
 if d==0:fr(px+2,py+1,2,2,BG)
 elif d==1:fr(px+4,py+2,1,2,BG)
 elif d==2:fr(px+2,py+4,2,1,BG)
 else:fr(px+1,py+2,1,2,BG)

def ghost(x,y,c):
 px=OX+x*S;py=OY+y*S
 fr(px+1,py+1,4,4,c)
 set_pixel(px+2,py+2,BG);set_pixel(px+4,py+2,BG)

def hud(sc,life):
 fr(0,0,W,HUD,BG)
 tx(1,0,"S "+str(sc))
 tx(70,0,"L "+str(life))
 tx(125,0,"BEST "+str(BEST))

def full(g):
 clear_screen();y=0
 while y<GH:
  x=0
  while x<GW:tile(g,x,y);x+=1
  y+=1

def wrap(x):
 if x<0:return GW-1
 if x>=GW:return 0
 return x

def openat(g,x,y):
 return 0<=y<GH and g[y][wrap(x)]!=9

def choose(g,a,p,fright,who):
 x,y,d=a;opts=[];q=0
 while q<4:
  nx=wrap(x+DX[q]);ny=y+DY[q]
  if openat(g,nx,ny):opts.append(q)
  q+=1
 if len(opts)>1:
  rv=REV[d];q=0
  while q<len(opts):
   if opts[q]==rv:opts.pop(q);break
   q+=1
 if not opts:return REV[d]
 if fright or who==3 and randint(0,2)==0:return opts[randint(0,len(opts)-1)]
 px,py,pd=p
 if who==1:
  px=wrap(px+DX[pd]*3);py+=DY[pd]*3
 elif who==2:px=wrap(GW-1-px)
 best=opts[0];bd=99999;q=0
 while q<len(opts):
  d=opts[q];nx=wrap(x+DX[d]);ny=y+DY[d]
  dd=(nx-px)*(nx-px)+(ny-py)*(ny-py)
  if dd<bd:bd=dd;best=d
  q+=1
 return best

def dirty(g,cells):
 done=[];i=0
 while i<len(cells):
  x,y=cells[i];k=y*GW+x
  if k not in done:done.append(k);tile(g,x,y)
  i+=1

def tick(want):
 p=0
 while p<POLL:
  t=0
  while t<WAIT:t+=1
  k=getkey()
  if k==BACK:return want,-1
  if k==EXE:return want,0
  if k==U:want=0
  elif k==R:want=1
  elif k==D:want=2
  elif k==L:want=3
  p+=1
 return want,1

def pause():
 global LK
 LK=None
 fr(34,66,124,58,BG);tx(69,76,"PAUSED",TXT,"medium")
 tx(48,102,"EXE RESUME   BACK EXIT")
 show_screen()
 while 1:
  k=edge()
  if k==EXE:return 1
  if k==BACK:return 0

def end(sc,win):
 global BEST,LK
 if sc>BEST:BEST=sc
 LK=None;clear_screen()
 tx(54,56,"YOU WIN" if win else "GAME OVER",TXT,"large")
 tx(53,91,"SCORE "+str(sc),TXT,"medium")
 tx(41,122,"EXE REPLAY  BACK EXIT")
 show_screen()
 while 1:
  k=edge()
  if k==EXE:return 1
  if k==BACK:return 0

def title():
 global LK
 LK=None;clear_screen()
 tx(59,48,"PAC-MAN",TXT,"large")
 tx(48,91,"EXE START",TXT,"medium")
 tx(48,116,"BACK EXIT",TXT,"medium")
 tx(55,148,"BEST "+str(BEST),TXT,"medium")
 show_screen()
 while 1:
  k=edge()
  if k==EXE:return 1
  if k==BACK:return 0

def game():
 global BEST
 g,dots,px,py,gs=parse();spx=px;spy=py
 home=[];i=0
 while i<len(gs):home.append((gs[i][0],gs[i][1],gs[i][2]));i+=1
 life=3;sc=0;pd=1;want=1;fright=0
 full(g);hud(sc,life);pac(px,py,pd)
 i=0
 while i<len(gs):ghost(gs[i][0],gs[i][1],GC[i&3]);i+=1
 show_screen()
 while life:
  want,go=tick(want)
  if go<0:return -1,0
  if go==0:
   while getkey()!=None:pass
   if not pause():return -1,0
   while getkey()!=None:pass
   full(g);hud(sc,life);pac(px,py,pd);i=0
   while i<len(gs):
    ghost(gs[i][0],gs[i][1],FR if fright else GC[i&3]);i+=1
   show_screen();continue
  opx=px;opy=py;old=[(px,py)];i=0
  while i<len(gs):old.append((gs[i][0],gs[i][1]));i+=1
  nx=wrap(px+DX[want]);ny=py+DY[want]
  if openat(g,nx,ny):pd=want
  nx=wrap(px+DX[pd]);ny=py+DY[pd]
  if openat(g,nx,ny):px=nx;py=ny
  v=g[py][px]
  if v:
   g[py][px]=0;dots-=1
   if v==1:sc+=10
   else:sc+=50;fright=FRAMES
   if sc>BEST:BEST=sc
  dead=0;i=0
  while i<len(gs):
   a=gs[i];gx=a[0];gy=a[1];gd=a[2]
   nd=choose(g,a,(px,py,pd),fright>0,i)
   ngx=wrap(gx+DX[nd]);ngy=gy+DY[nd]
   if openat(g,ngx,ngy):gx=ngx;gy=ngy;gd=nd
   a[0]=gx;a[1]=gy;a[2]=gd
   hit=(gx==px and gy==py) or (gx==opx and gy==opy and old[i+1][0]==px and old[i+1][1]==py)
   if hit:
    if fright:
     sc+=200;a[0],a[1],a[2]=home[i]
    else:dead=1
   i+=1
  now=[(px,py)];i=0
  while i<len(gs):now.append((gs[i][0],gs[i][1]));i+=1
  dirty(g,old+now);hud(sc,life);pac(px,py,pd)
  i=0
  while i<len(gs):
   ghost(gs[i][0],gs[i][1],FR if fright else GC[i&3]);i+=1
  if fright:fright-=1
  show_screen()
  if dots==0:return sc,1
  if dead:
   life-=1;hud(sc,life);show_screen()
   if not life:break
   dirty(g,now);px=spx;py=spy;pd=1;want=1;fright=0
   i=0
   while i<len(gs):gs[i][0],gs[i][1],gs[i][2]=home[i];i+=1
   pac(px,py,pd);i=0
   while i<len(gs):ghost(gs[i][0],gs[i][1],GC[i&3]);i+=1
   show_screen()
 return sc,0

def main():
 show=1
 while 1:
  if show and not title():return
  r=game()
  if r[0]<0:return
  if end(r[0],r[1]):show=0
  else:return
main()
