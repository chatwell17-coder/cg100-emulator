from casioplot import *
from random import randint
KU=14;KD=34;KL=23;KR=25;KO=24;KE=95;KH=16;KQ=12
W=H=192;S=8;GW=10;GH=20;X=12;Y=25;SX=100
BG=(235,242,252);P1=(210,224,243);P2=(154,178,210);EB=(247,250,255)
GD=(228,236,246);BD=(42,70,110);TX=(16,28,48);SB=(66,92,130);TT=(18,72,150)
C=[(0,210,220),(245,220,50),(170,70,230),(60,215,95),(235,70,70),(55,100,235),(245,150,45)]
M=[[0x0F0,0x2222,0x0F0,0x2222],[0x066]*4,[0x072,0x262,0x270,0x232],[0x036,0x231,0x036,0x231],[0x063,0x132,0x063,0x132],[0x071,0x226,0x470,0x322],[0x074,0x622,0x170,0x223]]
BEST=0;LK=None;POL=7;CHK=20;DAS=12;ARR=3;SM="small"
def pts(m):
 a=[];i=0
 while i<16:
  if(m>>i)&1:a.append((i&3,i>>2))
  i+=1
 return a
P=[[pts(M[p][r]) for r in range(4)] for p in range(7)]
HI=[tuple(min(255,v+60) for v in c) for c in C]
LO=[tuple(max(0,v-65) for v in c) for c in C]
def fr(x0,y0,x1,y1,c):
 if x0<0:x0=0
 if y0<0:y0=0
 if x1>W-1:x1=W-1
 if y1>H-1:y1=H-1
 if x0>x1 or y0>y1:return
 x=x0
 while x<=x1:
  y=y0
  while y<=y1:set_pixel(x,y,c);y+=1
  x+=1
def box(x,y,w,h,f):
 x1=x+w-1;y1=y+h-1
 fr(x,y,x1,y1,BD);fr(x+1,y+1,x1-1,y1-1,f)
def ec(x,y):
 px=X+x*S;py=Y+y*S
 fr(px,py,px+S-2,py+S-2,EB)
 fr(px+S-1,py,px+S-1,py+S-1,GD);fr(px,py+S-1,px+S-1,py+S-1,GD)
def fc(x,y,p):
 px=X+x*S;py=Y+y*S
 fr(px,py,px+S-2,py+S-2,C[p]);fr(px,py,px+S-2,py,HI[p]);fr(px,py,px,py+S-2,HI[p])
 fr(px+S-2,py+1,px+S-2,py+S-2,LO[p]);fr(px+1,py+S-2,px+S-2,py+S-2,LO[p])
 fr(px+S-1,py,px+S-1,py+S-1,GD);fr(px,py+S-1,px+S-1,py+S-1,GD)
def bc(b,x,y):
 if b[y][x]<0:ec(x,y)
 else:fc(x,y,b[y][x])
def board_bg():
 fr(X,Y,X+GW*S-1,Y+GH*S-1,EB)
 i=1
 while i<GW:fr(X+i*S-1,Y,X+i*S-1,Y+GH*S-1,GD);i+=1
 i=1
 while i<GH:fr(X,Y+i*S-1,X+GW*S-1,Y+i*S-1,GD);i+=1
def draw_board(b):
 y=0
 while y<GH:
  x=0
  while x<GW:bc(b,x,y);x+=1
  y+=1
def pset(p,r,x,y):return [(x+a,y+b) for a,b in P[p][r]]
def piece(p,r,x,y):
 for a,b in P[p][r]:fc(x+a,y+b,p)
def redraw(b,op,or_,ox,oy,p,r,x,y):
 u=[];a=pset(op,or_,ox,oy);n=pset(p,r,x,y)
 for v in a+n:
  if v not in u:u.append(v)
 i=0
 while i<len(u):
  gx,gy=u[i]
  if 0<=gx<GW and 0<=gy<GH:
   if (gx,gy) in n:fc(gx,gy,p)
   else:bc(b,gx,gy)
  i+=1
def ok(b,p,r,x,y):
 for a,b2 in P[p][r]:
  gx=x+a;gy=y+b2
  if gx<0 or gx>=GW or gy<0 or gy>=GH or b[gy][gx]!=-1:return 0
 return 1
def lock(b,p,r,x,y):
 for a,b2 in P[p][r]:b[y+b2][x+a]=p
def clear_lines(b):
 c=0;y=GH-1
 while y>=0:
  x=0
  while x<GW and b[y][x]!=-1:x+=1
  if x==GW:
   c+=1;i=y
   while i>0:b[i]=b[i-1][:];i-=1
   b[0]=[-1]*GW
  else:y-=1
 return c
def pbox(px,py,p):
 for a,b in P[p][0]:
  x=px+a*8;y=py+b*8
  fr(x,y,x+6,y+6,C[p]);fr(x,y,x+6,y,HI[p]);fr(x,y,x,y+6,HI[p])
def st(y,v):
 fr(SX+42,y,SX+80,y+8,P1);draw_string(SX+42,y,str(v),TX,SM)
def stats(sc,ln,lv,nx,hp):
 global BEST
 if sc>BEST:BEST=sc
 st(35,sc);st(49,ln);st(63,lv);st(77,BEST)
 fr(SX+2,108,SX+81,134,P1);pbox(SX+4,110,nx)
 if hp+1:pbox(SX+45,110,hp)
def frame():
 clear_screen();fr(0,0,W-1,H-1,BG);fr(0,0,W-1,22,TT);fr(0,22,W-1,23,(255,255,255))
 draw_string(8,7,"TETRIS",(255,255,255),SM)
 box(X-6,Y-6,GW*S+12,GH*S+12,(226,236,248));board_bg()
 box(SX,28,84,60,P1);box(SX,96,84,42,P1);box(SX,140,84,48,P1)
 draw_string(SX+4,100,"NEXT",SB,SM);draw_string(SX+45,100,"HOLD",SB,SM)
 fr(SX+6,44,SX+77,44,P2);fr(SX+6,58,SX+77,58,P2);fr(SX+6,72,SX+77,72,P2)
 draw_string(SX+8,35,"Score:",SB,SM);draw_string(SX+8,49,"Lines:",SB,SM)
 draw_string(SX+8,63,"Level:",SB,SM);draw_string(SX+8,77,"Best:",SB,SM)
 draw_string(SX+4,147,"L/R mv",SB,SM);draw_string(SX+44,147,"UP rot",SB,SM)
 draw_string(SX+4,159,"DN soft",SB,SM);draw_string(SX+44,159,"OK drop",SB,SM)
 draw_string(SX+4,171,"PGUP hold",SB,SM);draw_string(SX+48,171,"EXE ps",SB,SM)
def bag7():
 b=[0,1,2,3,4,5,6];i=6
 while i>0:
  j=randint(0,i);b[i],b[j]=b[j],b[i];i-=1
 return b
def rel():
 global LK
 while getkey():pass
 LK=None
def scr(t):
 clear_screen();fr(0,0,W-1,H-1,BG);box(20,16,152,160,(246,250,255))
 fr(28,24,163,42,TT);draw_string(36,29,t,(255,255,255),SM)
def tw(s):return len(s)*4
def btn(x,y,w,s,d=0):
 box(x,y,w,14,EB);draw_string(x+(w-tw(s))//2+d,y+4,s,SB,SM)
def bw(a):
 w=0;i=0
 while i<len(a):
  t=tw(a[i])+26
  if t>w:w=t
  i+=1
 return w
def row(y,a,w,d=None):
 n=len(a);g=12;x=(W-(n*w+(n-1)*g))//2;i=0
 while i<n:
  btn(x+i*(w+g),y,w,a[i],0 if d==None else d[i]);i+=1
def title():
 rel();scr("START")
 draw_string(44,50,"TETRIS",TT,"medium");fr(42,72,149,73,P2)
 a=("L/R move","UP rotate","DN soft","OK drop","PGUP hold","EXE pause");w=bw(a)
 row(86,a[:2],w,(1,0));row(106,a[2:4],w,(2,2));row(126,a[4:],w,(0,2))
 btn((W-(tw("OK start")+26))//2,150,tw("OK start")+26,"OK start")
 show_screen()
 while 1:
  k=getkey()
  if k==KO:rel();return 1
  if k==KQ:rel();return 0
def over(sc,ln,lv):
 global BEST
 if sc>BEST:BEST=sc
 rel();scr("RESULT")
 draw_string(30,46,"GAME OVER",TT,"medium")
 box(38,82,116,16,P1);box(38,104,116,16,P1);box(38,126,116,16,P1)
 draw_string(48,87,"Score",SB,SM);draw_string(108,87,str(sc),TX,SM)
 draw_string(48,109,"Lines",SB,SM);draw_string(108,109,str(ln),TX,SM)
 draw_string(48,131,"Level",SB,SM);draw_string(108,131,str(lv),TX,SM)
 btn((W-(tw("OK replay")+26))//2,152,tw("OK replay")+26,"OK replay")
 draw_string(72,171,"AC quit",SB,SM)
 show_screen()
 while 1:
  k=getkey()
  if k==KO:rel();return 1
  if k==KQ:rel();return 0
def pause(b,p,r,x,y,sc,ln,lv,nx,hp):
 rel();scr("PAUSE")
 draw_string(52,58,"PAUSED",TT,"medium");fr(48,80,143,81,P2)
 draw_string(50,92,"Game frozen",SB,SM)
 btn((W-(tw("EXE resume")+26))//2,126,tw("EXE resume")+26,"EXE resume")
 draw_string(72,145,"AC quit",SB,SM)
 show_screen()
 while 1:
  k=getkey()
  if k==KE:
   rel();frame();stats(sc,ln,lv,nx,hp);draw_board(b);piece(p,r,x,y);show_screen();return 1
  if k==KQ:rel();return 0
def rep(h,c,k):
 if h==k:
  c+=1
  if c==1 or c>DAS and (c-DAS)%ARR==0:return c,1
  return c,0
 return 0,0
def tick():
 global LK
 h=None;e=None;i=0
 while i<POL:
  t=0
  while t<CHK:t+=1
  k=getkey()
  if k:h=k
  if not k:LK=None
  elif LK==None:LK=k;e=k
  i+=1
 return h,e
def game():
 b=[[-1]*GW for _ in range(GH)]
 bg=bag7();i=0;sc=0;ln=0;lv=0;hp=-1;can=1
 p=bg[i];i+=1
 if i>6:bg=bag7();i=0
 nx=bg[i];i+=1
 r=0;x=3;y=0
 frame();stats(sc,ln,lv,nx,hp);piece(p,r,x,y);show_screen()
 fall=0;rl=0;rr=0
 while 1:
  h,e=tick()
  if KQ in(h,e):return -2,0,0
  if e==KE:
   if not pause(b,p,r,x,y,sc,ln,lv,nx,hp):return -2,0,0
   continue
  ox=x;oy=y;or_=r;op=p;chg=0
  if e==KH and can:
   q=hp;hp=p
   if q<0:
    p=nx
    if i>6:bg=bag7();i=0
    nx=bg[i];i+=1
   else:p=q
   r=0;x=3;y=0;fall=0;can=0;stats(sc,ln,lv,nx,hp)
   if not ok(b,p,r,x,y):show_screen();break
   redraw(b,op,or_,ox,oy,p,r,x,y);show_screen();continue
  rl,m=rep(h,rl,KL)
  if m and ok(b,p,r,x-1,y):x-=1;chg=1
  rr,m=rep(h,rr,KR)
  if m and ok(b,p,r,x+1,y):x+=1;chg=1
  if h!=KL:rl=0
  if h!=KR:rr=0
  if e==KU:
   nr=(r+1)&3
   if ok(b,p,nr,x,y):r=nr;chg=1
   elif ok(b,p,nr,x-1,y):x-=1;r=nr;chg=1
   elif ok(b,p,nr,x+1,y):x+=1;r=nr;chg=1
  if e==KO:
   while ok(b,p,r,x,y+1):y+=1
   fall=99;chg=1
  fall+=2 if h==KD else 1
  need=12-lv
  if need<4:need=4
  if fall>=need:
   fall=0
   if ok(b,p,r,x,y+1):y+=1;chg=1
   else:
    lock(b,p,r,x,y);c=clear_lines(b)
    if c:
     ln+=c
     if c==1:sc+=100*(lv+1)
     elif c==2:sc+=300*(lv+1)
     elif c==3:sc+=500*(lv+1)
     else:sc+=800*(lv+1)
     nlv=ln//10
     if nlv>lv:lv=nlv
    p=nx
    if i>6:bg=bag7();i=0
    nx=bg[i];i+=1
    r=0;x=3;y=0;can=1;stats(sc,ln,lv,nx,hp)
    if c:draw_board(b)
    if not ok(b,p,r,x,y):show_screen();break
    if c:piece(p,r,x,y)
    else:redraw(b,op,or_,ox,oy,p,r,x,y)
    show_screen();continue
  if chg or y!=oy:redraw(b,op,or_,ox,oy,p,r,x,y);show_screen()
 return sc,ln,lv
def main():
 show=1
 while 1:
  if show and not title():return
  show=1
  r=game()
  if r[0]==-2:return
  if over(r[0],r[1],r[2]):show=0
  else:return
main()
