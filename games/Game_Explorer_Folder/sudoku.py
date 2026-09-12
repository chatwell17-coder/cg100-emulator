from casioplot import *
from random import randint
KU,KD,KL,KR=14,34,23,25
EXE,DEL,EXIT=95,64,12
DIG={81:1,82:2,83:3,71:4,72:5,73:6,61:7,62:8,63:9}
W,H=384,192
CS=20;X0,Y0=8,6;PX=202;HY=146
WHITE=(255,255,255);BLACK=(0,0,0);CUR=(230,230,230)
BAD=(220,0,0);FIX=(0,150,0);USR=(0,0,160)
B=[0]*81;S=[0]*81;F=[0]*81;bad=[];cur=0;sel=0

def fr(x,y,w,h,c):
 for yy in range(y,y+h):
  for xx in range(x,x+w):set_pixel(xx,yy,c)

def rr(x,y,w,h,c):
 x2=x+w-1;y2=y+h-1
 for xx in range(x,x+w):set_pixel(xx,y,c);set_pixel(xx,y2,c)
 for yy in range(y,y+h):set_pixel(x,yy,c);set_pixel(x2,yy,c)

def txt(x,y,s,c):draw_string(x,y,s,c)

def wait_release():
 while getkey()!=None:pass

def edge(last):
 k=getkey()
 if k!=None:
  if last!=0:return 0,last
  return k,k
 return 0,0

def bi(i):return (i//27)*3+(i%9)//3

def cellxy(i):return X0+(i%9)*CS,Y0+(i//9)*CS

def pat(r,c):return (r*3+r//3+c)%9

def shuf(a):
 i=len(a)-1
 while i>0:
  j=randint(0,i)
  a[i],a[j]=a[j],a[i]
  i-=1
 return a

def perm9():
 a=[0,1,2];shuf(a);b=[0,1,2];shuf(b);o=[]
 for i in range(3):
  t=a[i]*3
  for j in range(3):o.append(t+b[j])
 return o

def build_full():
 rows=perm9();cols=perm9();nums=[1,2,3,4,5,6,7,8,9];shuf(nums)
 for r in range(9):
  pr=rows[r];t=r*9
  for c in range(9):
   v=nums[pat(pr,cols[c])]
   S[t+c]=v;B[t+c]=v

def make(diff):
 build_full()
 for i in range(81):F[i]=1
 target=(36,46,54)[diff]
 pos=[]
 for i in range(81):pos.append(i)
 shuf(pos)
 for n in range(target):
  q=pos[n]
  B[q]=0;F[q]=0

def calc_bad():
 z=[];i=0
 while i<81:
  v=B[i]
  if v:
   r=i//9;c=i%9;br=(r//3)*3;bc=(c//3)*3;j=0;bad1=0
   while j<9:
    if j!=c and B[r*9+j]==v:bad1=1;break
    if j!=r and B[j*9+c]==v:bad1=1;break
    j+=1
   y=br
   while not bad1 and y<br+3:
    x=bc
    while x<bc+3:
     q=y*9+x
     if q!=i and B[q]==v:bad1=1;break
     x+=1
    y+=1
   if bad1:z.append(i)
  i+=1
 return z

def setv(i,v):B[i]=v

def solved():
 if bad:return 0
 i=0
 while i<81:
  if B[i]==0:return 0
  i+=1
 return 1

def bg(i):
 if i==cur:return CUR
 return WHITE

def draw_num(i):
 v=B[i]
 if v:
  x,y=cellxy(i)
  txt(x+3,y+2,str(v),BLACK if F[i] else USR)

def draw_cell(i):
 x,y=cellxy(i)
 fr(x+1,y+1,CS-2,CS-2,bg(i))
 if F[i]:rr(x+1,y+1,CS-2,CS-2,FIX)
 elif i in bad:rr(x+2,y+2,CS-4,CS-4,BAD)
 draw_num(i)

def draw_grid():
 clear_screen();rr(0,0,W,H,BLACK)
 rr(PX,2,W-PX-2,138,BLACK)
 txt(PX+8,10,'SUDOKU',BLACK)
 txt(PX+8,28,'1-9 input',BLACK)
 txt(PX+8,44,'DEL clear',BLACK)
 txt(PX+8,60,'EXE new',BLACK)
 txt(PX+8,86,'green = clue',FIX)
 txt(PX+8,102,'red = wrong',BAD)
 txt(PX+8,118,'grey = cursor',BLACK)
 for i in range(10):
  x=X0+i*CS;y=Y0+i*CS;t=3 if i%3==0 else 1
  for a in range(t):
   xx=x+a;yy=y+a
   for k in range(9*CS+1):set_pixel(X0+k,yy,BLACK)
   for k in range(9*CS+1):set_pixel(xx,Y0+k,BLACK)
 for i in range(81):draw_cell(i)
 show_screen()

def hud(s):
 fr(PX+2,HY,W-PX-4,40,WHITE)
 rr(PX,HY-4,W-PX-2,46,BLACK)
 txt(PX+8,HY+8,s,BLACK)
 show_screen()

def menu():
 global sel
 wait_release();last=0
 clear_screen();rr(0,0,W,H,BLACK)
 names=('EASY','MED','HARD');bx=(44,146,248)
 while 1:
  txt(152,22,'SUDOKU',BLACK)
  txt(114,48,'PRESS 1 / 2 / 3 OR USE ARROWS',BLACK)
  for i in range(3):
   x=bx[i];y=84
   fr(x,y,92,32,CUR if i==sel else WHITE)
   rr(x,y,92,32,BLACK)
   txt(x+26,y+12,names[i],BLACK)
  txt(132,138,'1 EASY    2 MED    3 HARD',BLACK)
  txt(132,156,'EXE START   AC EXIT',BLACK)
  show_screen()
  k,last=edge(last)
  if k==81:return 0
  if k==82:return 1
  if k==83:return 2
  if k==KL and sel>0:sel-=1
  elif k==KR and sel<2:sel+=1
  elif k==EXE:return sel
  elif k==EXIT:return -1

def affect(i):
 r=i//9;c=i%9;g=bi(i);a=[]
 t=r*9
 for j in range(9):a.append(t+j)
 for j in range(9):
  q=j*9+c
  if q not in a:a.append(q)
 br=(r//3)*3;bc=(c//3)*3
 for y in range(3):
  for x in range(3):
   q=(br+y)*9+bc+x
   if q not in a:a.append(q)
 return a

def refresh(i):
 global bad
 ch=affect(i);old=bad[:]
 bad=calc_bad()
 for q in old:
  if q not in ch:ch.append(q)
 for q in bad:
  if q not in ch:ch.append(q)
 for q in ch:draw_cell(q)
 show_screen()
 if solved():hud('Solved! EXE = new game')
 else:hud('')

def new_game():
 global cur,bad
 d=menu()
 if d<0:return 0
 make(d);cur=0;bad=calc_bad();draw_grid();hud('');return 1

def main():
 global cur
 if not new_game():return
 last=0
 while 1:
  k,last=edge(last)
  if not k:continue
  i=cur;ni=i
  if k==EXIT:return
  if k==KU and i>8:ni=i-9
  elif k==KD and i<72:ni=i+9
  elif k==KL and i%9:ni=i-1
  elif k==KR and i%9<8:ni=i+1
  elif k==EXE:
   if not new_game():return
   last=0;continue
  elif k==DEL:
   if F[i]==0 and B[i]!=0:setv(i,0);refresh(i)
   continue
  elif k in DIG:
   if F[i]==0 and B[i]!=DIG[k]:setv(i,DIG[k]);refresh(i)
   continue
  else:continue
  if ni!=i:
   cur=ni;draw_cell(i);draw_cell(ni);show_screen()

main()
