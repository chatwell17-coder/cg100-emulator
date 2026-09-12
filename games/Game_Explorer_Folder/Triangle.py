from math import *
from casioplot import *
KU=14;KD=34;KL=23;KR=25;KOK=24;KEXE=95;KFORMAT=94;KDEL=64
K7=61;K8=62;K9=63;K4=71;K5=72;K6=73;K1=81;K2=82;K3=83;K0=91;KDOT=92;KMIN=93;KEXIT=12
W=384;H=192;LK=None;EPS=1e-3
BG=(248,249,252);TXT=(18,22,28);BD=(72,82,96);TL=(236,241,248)
B1=(242,245,250);ACC=(238,198,48);ED=(94,173,106);SEL=(255,245,210);CUR=(230,170,40)
D={"a":"","b":"","c":"","A":"","B":"","C":""};SOL=[];SV=0
IT=[];VALS='abcABC';NUM={K0:'0',K1:'1',K2:'2',K3:'3',K4:'4',K5:'5',K6:'6',K7:'7',K8:'8',K9:'9'}
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
def ln(x0,y0,x1,y1,c):
 dx=abs(x1-x0);sx=1 if x0<x1 else -1;dy=-abs(y1-y0);sy=1 if y0<y1 else -1;er=dx+dy
 while 1:
  set_pixel(x0,y0,c)
  if x0==x1 and y0==y1:return
  e2=er+er
  if e2>=dy:er+=dy;x0+=sx
  if e2<=dx:er+=dx;y0+=sy
def box(x,y,w,h,f,e):
 fr(x,y,x+w-1,y+h-1,f);fr(x,y,x+w-1,y,e);fr(x,y,x,y+h-1,e)
 fr(x+w-1,y,x+w-1,y+h-1,e);fr(x,y+h-1,x+w-1,y+h-1,e)
def tw(s,m):return len(s)*(8 if m else 6)
def th(m):return 10 if m else 8
def ct(x,y,w,h,s,c,m=0,dx=0):draw_string(x+(w-tw(s,m))//2+dx,y+(h-th(m))//2,s,c,'medium' if m else 'small')
def edge():
 global LK
 k=getkey()
 if k==None:LK=None;return None
 if LK==None:LK=k;return k
 return None

def d2r(x):return x*pi/180
def r2d(x):return x*180/pi
def clamp(x):return -1 if x<-1 else 1 if x>1 else x
def fmt(v):
 if v=='':return ''
 try:v=float(v)
 except:return str(v)
 if abs(v-round(v))<0.005:return str(int(round(v)))
 s='%.2f'%v
 return s.rstrip('0').rstrip('.')

def tri_ok(a,b,c):return a>0 and b>0 and c>0 and a+b>c and a+c>b and b+c>a
def sss(a,b,c):
 if not tri_ok(a,b,c):return []
 A=r2d(acos(clamp((b*b+c*c-a*a)/(2*b*c))));B=r2d(acos(clamp((a*a+c*c-b*b)/(2*a*c))))
 return [{'a':a,'b':b,'c':c,'A':A,'B':B,'C':180-A-B}]
def solve3(V):
 s=[x for x in V if x in 'abc'];g=[x for x in V if x in 'ABC'];o=[]
 if not s:return None,'1 side needed'
 if len(s)==3:o=sss(V['a'],V['b'],V['c'])
 elif len(g)==2 and len(s)==1:
  A=V.get('A',0);B=V.get('B',0);C=V.get('C',0)
  if A+B+C>=180:return None,'Angles too big'
  if 'A' not in V:A=180-B-C
  elif 'B' not in V:B=180-A-C
  else:C=180-A-B
  ang={'A':A,'B':B,'C':C};r=s[0];rv=V[r];ra=ang[r.upper()]
  if ra<=0:return None,'Bad triangle'
  z={'A':A,'B':B,'C':C}
  for n in 'abc':z[n]=rv*sin(d2r(ang[n.upper()]))/sin(d2r(ra))
  o=[z]
 elif len(s)==2 and len(g)==1:
  G=g[0];ga=G.lower();pair=''.join(sorted(s));inc={'bc':'A','ac':'B','ab':'C'}[pair]
  if G==inc:
   x=V[s[0]];y=V[s[1]];z=sqrt(x*x+y*y-2*x*y*cos(d2r(V[G])));vv={s[0]:x,s[1]:y,ga:z}
   if z<=0:return None,'Bad triangle'
   o=sss(vv['a'],vv['b'],vv['c'])
  elif ga in s:
   other=s[0] if s[1]==ga else s[1];oa=other.upper();rem=[x for x in 'ABC' if x not in (G,oa)][0]
   q=V[other]*sin(d2r(V[G]))/V[ga]
   if q>1.000001 or q<-1.000001:return [],'No fit'
   a2=r2d(asin(clamp(q)))
   for ang2 in (a2,180-a2):
    ang3=180-V[G]-ang2
    if 0<ang2<180 and 0<ang3<180:
     z={G:V[G],oa:ang2,rem:ang3,ga:V[ga],other:V[other]};rs=[x for x in 'abc' if x not in (ga,other)][0]
     z[rs]=V[ga]*sin(d2r(ang3))/sin(d2r(V[G]))
     if not o or abs(o[0][oa]-z[oa])>1e-4:o.append(z)
  else:return None,'No solve'
 else:return None,'Not enough info'
 return o,''
def fits(sol,V):
 for k in V:
  if abs(sol[k]-V[k])>EPS:return 0
 return 1
def addsol(out,sol):
 i=0
 while i<len(out):
  for k in VALS:
   if abs(out[i][k]-sol[k])>EPS:break
  else:return
  i+=1
 out.append(sol)
def solve_data(src):
 k=[];V={}
 for n in VALS:
  if src[n]!='':k.append(n)
 if len(k)<3:return None,'Need 3+'
 for n in k:
  try:V[n]=float(src[n])
  except:return None,'Bad value'
  if n in 'abc' and V[n]<=0:return None,'Side > 0'
  if n in 'ABC' and not(0<V[n]<180):return None,'Ang 0-180'
 if len([x for x in k if x in 'abc'])==0:return None,'1 side needed'
 if 'A' in V and 'B' in V and 'C' in V and abs(V['A']+V['B']+V['C']-180)>1e-2:return None,'A sum 180'
 if 'a' in V and 'b' in V and 'c' in V and not tri_ok(V['a'],V['b'],V['c']):return None,'Bad sides'
 out=[];seen=0;last='No solve';i=0
 while i<len(k)-2:
  j=i+1
  while j<len(k)-1:
   m=j+1
   while m<len(k):
    r,msg=solve3({k[i]:V[k[i]],k[j]:V[k[j]],k[m]:V[k[m]]})
    if r==None:last=msg
    else:
     seen=1
     for s in r:
      if fits(s,V):addsol(out,s)
    m+=1
   j+=1
  i+=1
 if out:return out,''
 if seen:return [],'Conflict'
 return None,last

def arc(cx,cy,rx,ry,a0,a1):
 t=a0
 while t<=a1:
  x=int(cx+cos(d2r(t))*rx);y=int(cy-sin(d2r(t))*ry);fr(x,y,x+1,y+1,TXT);t+=3

def draw_tri():
 ln(124,150,192,50,TXT);ln(192,50,260,150,TXT);ln(124,150,260,150,TXT)
 arc(192,74,14,10,210,330);arc(146,138,12,12,0,88);arc(238,138,12,12,92,180)
 draw_string(186,76,'A',TXT,'small');draw_string(154,136,'B',TXT,'small');draw_string(224,136,'C',TXT,'small')
def field(i,sel=0,vals=None):
 if vals==None:vals=D
 x,y,w,h,k=IT[i]
 e=BD;f=SEL if sel else B1;t=TXT
 box(x,y,w,h,f,e)
 if sel:
  fr(x+2,y+2,x+w-3,y+3,CUR);fr(x+2,y+h-4,x+w-3,y+h-3,CUR);fr(x+2,y+2,x+3,y+h-3,CUR);fr(x+w-4,y+2,x+w-3,y+h-3,CUR)
 ct(x,y,w,10,k,t,0,-1)
 ct(x,y+11,w,h-12,fmt(vals[k]) or '_',t,1,-6)
def draw_all(sel=0,vals=None):
 clear_screen();draw_tri();i=0
 while i<len(IT):field(i,i==sel,vals);i+=1
 show_screen()
def redraw_pair(a,b,vals=None):field(a,0,vals);field(b,1,vals);show_screen()
def redraw_one(a,sel,vals=None):field(a,sel,vals);show_screen()
def redraw_sol(sel):
 i=0
 while i<len(IT):field(i,i==sel,SOL[SV]);i+=1
 show_screen()
NEI={
 0:{KR:2,KU:1,KD:4},
 1:{KL:0,KR:2,KU:3,KD:3},
 2:{KL:0,KU:1,KD:5},
 3:{KL:4,KR:5,KU:1,KD:1},
 4:{KR:3,KU:0},
 5:{KL:3,KU:2}
}
def move_sel(s,k):
 return NEI[s][k] if s in NEI and k in NEI[s] else s
def apply_key(ch,cur):
 if ch==KDEL:return cur[:-1]
 if ch==KMIN:return cur[1:] if cur[:1]=='-' else '-'+cur
 if ch==KDOT:return (cur if cur else '0')+'.' if '.' not in cur else cur
 if ch in NUM:
  d=NUM[ch]
  return d if cur=='0' else '-'+d if cur=='-0' else cur+d
 return cur
def clear_press(sel):
 global SOL,SV
 for k in VALS:D[k]=''
 SOL=[];SV=0;draw_all(sel)
def solve_press(sel):
 global SOL,SV
 r,msg=solve_data(D)
 if r==None or len(r)==0:return
 SOL=r;SV=0;draw_all(sel,SOL[0])
def use_key_on_field(sel,k):
 global SOL,SV
 key=IT[sel][4]
 n=apply_key(k,D[key])
 if n==D[key]:return 0
 if SOL:SOL=[];SV=0;field(sel,1)
 D[key]=n;redraw_one(sel,1);return 1
def main():
 global IT,SV,SOL,LK
 for q in VALS:D[q]=''
 SOL=[];SV=0;LK=None
 IT=[(28,66,88,38,'c'),(146,8,92,36,'A'),(268,66,88,38,'b'),(146,152,92,36,'a'),(36,148,80,34,'B'),(268,148,80,34,'C')]
 s=0;draw_all(s)
 while 1:
  k=edge()
  if k==None:continue
  if k==KEXIT:return
  if k in (KL,KR,KU,KD):
   if SOL and k==KL and SV>0:SV-=1;draw_all(s,SOL[SV])
   elif SOL and k==KR and SV<len(SOL)-1:SV+=1;draw_all(s,SOL[SV])
   else:
    n=move_sel(s,k)
    if n!=s:
     redraw_pair(s,n,SOL[SV] if SOL else None);s=n
  elif k in (KOK,KEXE):solve_press(s)
  elif k==KFORMAT:clear_press(s)
  elif k in NUM or k in (KDOT,KMIN,KDEL):use_key_on_field(s,k)
main()
