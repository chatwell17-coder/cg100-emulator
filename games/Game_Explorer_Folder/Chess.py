from casioplot import *
KU=14;KD=34;KL=23;KR=25;KOK=24;KEXE=95;KEXIT=12
W=192;H=192;HUD=20;S=20;OX=16;OY=HUD
L=(235,236,208);D=(115,149,82);BG=(255,255,255)
CUR=(0,120,255);SEL=(255,0,0);MOV=(255,200,0);TXT=(0,0,0)
WF=(250,250,250);BF=(20,20,20)

b=list("rnbqkbnr"+"pppppppp"+"........"+"........"+"........"+"........"+"PPPPPPPP"+"RNBQKBNR")
wt=1;LK=None

def sq(i):return i&7,i>>3
def ix(x,y):return (y<<3)+x
def inb(x,y):return 0<=x<8 and 0<=y<8
def isw(p):return "A"<=p<="Z"
def isb(p):return "a"<=p<="z"

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

def dsq(x,y,c):
 px=OX+x*S;py=OY+y*S
 fr(px,py,px+S-2,py+S-2,c)

def ol(x,y,c):
 px=OX+x*S;py=OY+y*S
 fr(px,py,px+S-2,py,c);fr(px,py,px,py+S-2,c)
 fr(px+S-2,py,px+S-2,py+S-2,c);fr(px,py+S-2,px+S-2,py+S-2,c)

GN="KQRBNP"
G=[["00100","01110","11111","10101","01110","11111","11111"],
   ["01010","10101","11111","01110","00100","01110","11111"],
   ["10101","11111","01110","01110","01110","11111","11111"],
   ["00100","01110","01010","00100","01110","11111","11111"],
   ["00100","01110","11111","00111","00110","01110","11111"],
   ["00000","00100","01110","00100","00100","01110","11111"]]

def pg(px,py,gi,sc,c):
 y=0
 while y<7:
  row=G[gi][y];x=0
  while x<5:
   if row[x]=="1":fr(px+x*sc,py+y*sc,px+x*sc+sc-1,py+y*sc+sc-1,c)
   x+=1
  y+=1

def dp(x,y,p):
 if p==".":return
 u=p.upper();gi=0
 while gi<6 and GN[gi]!=u:gi+=1
 px=OX+x*S+4;py=OY+y*S+3;sc=2
 if p==u:oc=(0,0,0);fc=WF
 else:oc=(255,255,255);fc=BF
 pg(px-1,py-1,gi,sc,oc);pg(px,py-1,gi,sc,oc);pg(px-1,py,gi,sc,oc);pg(px,py,gi,sc,oc);pg(px,py,gi,sc,fc)

def draw_base(i):
 x,y=sq(i)
 dsq(x,y,L if ((x+y)&1)==0 else D)
 dp(x,y,b[i])

def head():
 fr(0,0,W-1,HUD-1,BG)
 draw_string(0,2,("White" if wt else "Black")+" to move",TXT,"medium")

def kfind(ch):
 i=0
 while i<64:
  if b[i]==ch:return i
  i+=1
 return -1

kw=kfind("K");kb=kfind("k")

def atk(byw,sq0):
 x,y=sq(sq0)
 if byw:
  yy=y+1
  if yy<8:
   if x and b[ix(x-1,yy)]=="P":return 1
   if x<7 and b[ix(x+1,yy)]=="P":return 1
 else:
  yy=y-1
  if yy>=0:
   if x and b[ix(x-1,yy)]=="p":return 1
   if x<7 and b[ix(x+1,yy)]=="p":return 1
 for dx,dy in ((1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)):
  xx=x+dx;yy=y+dy
  if inb(xx,yy):
   p=b[ix(xx,yy)]
   if byw and p=="N":return 1
   if (not byw) and p=="n":return 1
 for dx,dy in ((1,1),(1,-1),(-1,1),(-1,-1)):
  xx=x+dx;yy=y+dy
  while inb(xx,yy):
   p=b[ix(xx,yy)]
   if p!=".":
    if byw and (p=="B" or p=="Q"):return 1
    if (not byw) and (p=="b" or p=="q"):return 1
    break
   xx+=dx;yy+=dy
 for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
  xx=x+dx;yy=y+dy
  while inb(xx,yy):
   p=b[ix(xx,yy)]
   if p!=".":
    if byw and (p=="R" or p=="Q"):return 1
    if (not byw) and (p=="r" or p=="q"):return 1
    break
   xx+=dx;yy+=dy
 for dx in (-1,0,1):
  for dy in (-1,0,1):
   if dx or dy:
    xx=x+dx;yy=y+dy
    if inb(xx,yy):
     p=b[ix(xx,yy)]
     if byw and p=="K":return 1
     if (not byw) and p=="k":return 1
 return 0

def incheck(white):
 return atk(0 if white else 1,kw if white else kb)

def mv_do(frm,to):
 global kw,kb
 p=b[frm];cap=b[to];okw=kw;okb=kb
 b[to]=p;b[frm]="."
 ty=to>>3
 if p=="P" and ty==0:b[to]="Q"
 elif p=="p" and ty==7:b[to]="q"
 if p=="K":kw=to
 elif p=="k":kb=to
 return (frm,to,cap,okw,okb,p)

def mv_un(s):
 global kw,kb
 frm,to,cap,okw,okb,p=s
 kw=okw;kb=okb
 b[frm]=p
 b[to]=cap

def gen(frm):
 p=b[frm]
 if p==".":return []
 w=isw(p)
 if w!=wt:return []
 x,y=sq(frm);cand=[]
 def add(t):
  pp=b[t]
  if pp=="." or (w and isb(pp)) or ((not w) and isw(pp)):cand.append(t)
 if p=="P":
  if y and b[ix(x,y-1)]==".":cand.append(ix(x,y-1))
  if y==6 and b[ix(x,5)]=="." and b[ix(x,4)]==".":cand.append(ix(x,4))
  if y and x and isb(b[ix(x-1,y-1)]):cand.append(ix(x-1,y-1))
  if y and x<7 and isb(b[ix(x+1,y-1)]):cand.append(ix(x+1,y-1))
 elif p=="p":
  if y<7 and b[ix(x,y+1)]==".":cand.append(ix(x,y+1))
  if y==1 and b[ix(x,2)]=="." and b[ix(x,3)]==".":cand.append(ix(x,3))
  if y<7 and x and isw(b[ix(x-1,y+1)]):cand.append(ix(x-1,y+1))
  if y<7 and x<7 and isw(b[ix(x+1,y+1)]):cand.append(ix(x+1,y+1))
 elif p=="N" or p=="n":
  for dx,dy in ((1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)):
   xx=x+dx;yy=y+dy
   if inb(xx,yy):add(ix(xx,yy))
 elif p=="B" or p=="b" or p=="Q" or p=="q":
  for dx,dy in ((1,1),(1,-1),(-1,1),(-1,-1)):
   xx=x+dx;yy=y+dy
   while inb(xx,yy):
    t=ix(xx,yy);pp=b[t]
    if pp==".":cand.append(t)
    else:
     if w and isb(pp):cand.append(t)
     if (not w) and isw(pp):cand.append(t)
     break
    xx+=dx;yy+=dy
 if p=="R" or p=="r" or p=="Q" or p=="q":
  for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
   xx=x+dx;yy=y+dy
   while inb(xx,yy):
    t=ix(xx,yy);pp=b[t]
    if pp==".":cand.append(t)
    else:
     if w and isb(pp):cand.append(t)
     if (not w) and isw(pp):cand.append(t)
     break
    xx+=dx;yy+=dy
 if p=="K" or p=="k":
  for dx in (-1,0,1):
   for dy in (-1,0,1):
    if dx or dy:
     xx=x+dx;yy=y+dy
     if inb(xx,yy):add(ix(xx,yy))
 out=[];i=0
 while i<len(cand):
  t=cand[i]
  st=mv_do(frm,t)
  ok=not incheck(wt)
  mv_un(st)
  if ok:out.append(t)
  i+=1
 return out

def ke():
 global LK
 k=getkey()
 if k==None:LK=None;return None
 if LK==None:LK=k;return k
 return None

def mark_add(mark,arr,v):
 if 0<=v<64 and mark[v]==0:
  mark[v]=1;arr.append(v)

def apply_overlays(cur,sel,hl):
 i=0
 while i<len(hl):
  x,y=sq(hl[i]);ol(x,y,MOV);i+=1
 if sel!=-1:
  sx,sy=sq(sel);ol(sx,sy,SEL)
 cx,cy=sq(cur);ol(cx,cy,CUR)

def init_screen(cur,sel,hl):
 clear_screen();head()
 i=0
 while i<64:
  draw_base(i);i+=1
 apply_overlays(cur,sel,hl)
 show_screen()

def update_screen(cur,sel,hl,dirty):
 head()
 i=0
 while i<len(dirty):
  draw_base(dirty[i]);i+=1
 apply_overlays(cur,sel,hl)
 show_screen()

def main():
 global b,wt,kw,kb,LK
 b=list("rnbqkbnr"+"pppppppp"+"........"+"........"+"........"+"........"+"PPPPPPPP"+"RNBQKBNR")
 wt=1;kw=60;kb=4;LK=None
 cur=ix(4,6);sel=-1;hl=[]
 init_screen(cur,sel,hl)
 while 1:
  k=ke()
  if k==None:continue
  if k==KEXIT:break
  ncur=cur;nsel=sel;nhl=hl
  moved_fr=-1;moved_to=-1;wt_changed=0
  if k==KU and (cur>>3):ncur=cur-8
  elif k==KD and (cur>>3)<7:ncur=cur+8
  elif k==KL and (cur&7):ncur=cur-1
  elif k==KR and (cur&7)<7:ncur=cur+1
  elif k==KEXE:nsel=-1;nhl=[]
  elif k==KOK:
   if sel==-1:
    p=b[cur]
    if p!="." and ((wt and isw(p)) or ((not wt) and isb(p))):
     nsel=cur;nhl=gen(nsel)
   else:
    ok=0;i=0
    while i<len(hl):
     if hl[i]==cur:ok=1;break
     i+=1
    if ok:
     mv_do(sel,cur);moved_fr=sel;moved_to=cur;wt=0 if wt else 1;wt_changed=1
    nsel=-1;nhl=[]
  if ncur==cur and nsel==sel and nhl==hl and moved_fr==-1 and moved_to==-1 and wt_changed==0:continue
  mark=[0]*64;dirty=[]
  mark_add(mark,dirty,cur);mark_add(mark,dirty,ncur)
  mark_add(mark,dirty,sel);mark_add(mark,dirty,nsel)
  if nhl!=hl:
   i=0
   while i<len(hl):mark_add(mark,dirty,hl[i]);i+=1
   i=0
   while i<len(nhl):mark_add(mark,dirty,nhl[i]);i+=1
  if moved_fr!=-1:mark_add(mark,dirty,moved_fr)
  if moved_to!=-1:mark_add(mark,dirty,moved_to)
  cur=ncur;sel=nsel;hl=nhl
  update_screen(cur,sel,hl,dirty)

main()
