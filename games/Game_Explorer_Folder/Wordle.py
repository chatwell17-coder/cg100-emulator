from casioplot import *
KU=14;KD=34;KL=23;KR=25;KOK=24;KEXE=95;KDEL=64;KEXIT=12
W=192;H=192
BG=(252,252,252);TXT=(15,15,15);BD=(70,70,70)
TL=(235,240,248);GY=(170,176,184);YL=(235,195,40);GR=(70,168,85)
CUR=(40,120,255);HD=(220,228,238)
T=16;G=2;COLS=5;ROWS=6;Y0=30;KH=16;KG=2;KW=16;SW=26
R1="QWERTYUIOP";R2="ASDFGHJKL";R3=["Z","X","C","V","B","N","M","DEL","ENT"]
X0=(W-(COLS*T+(COLS-1)*G))//2
TX=[X0+i*(T+G) for i in range(COLS)]
TY=[Y0+i*(T+G) for i in range(ROWS)]
keys=[];starts=[];lens=[];LK=None

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

def box(x,y,w,h,f,e):
 fr(x,y,x+w-1,y+h-1,f)
 fr(x,y,x+w-1,y,e);fr(x,y,x,y+h-1,e)
 fr(x+w-1,y,x+w-1,y+h-1,e);fr(x,y+h-1,x+w-1,y+h-1,e)

def tw(s,sz):return len(s)*(8 if sz=="medium" else 6)
def th(sz):return 10 if sz=="medium" else 8

def ct(x,y,w,h,s,c,sz,dx=0,b=0):
 px=x+(w-tw(s,sz))//2+dx;py=y+(h-th(sz))//2
 draw_string(px,py,s,c,sz)
 if b:draw_string(px+1,py,s,c,sz)

def ok_word(s):
 if len(s)!=5:return 0
 i=0
 while i<5:
  c=s[i]
  if not(("A"<=c<="Z")or("a"<=c<="z")):return 0
  i+=1
 return 1

def fb(w,g):
 w=w.upper();g=g.upper();r=["."]*5;cnt={};i=0
 while i<5:
  if g[i]==w[i]:r[i]="G"
  else:
   ch=w[i]
   if ch in cnt:cnt[ch]+=1
   else:cnt[ch]=1
  i+=1
 i=0
 while i<5:
  if r[i]==".":
   ch=g[i]
   if ch in cnt and cnt[ch]>0:r[i]="Y";cnt[ch]-=1
  i+=1
 return "".join(r)

def mcol(m):
 if m=="G":return GR
 if m=="Y":return YL
 return GY

def kcol(v):
 if v==3:return GR
 if v==2:return YL
 if v==1:return GY
 return BG

def li(ch):return ord(ch)-65

def upd_keys(ks,g,m):
 i=0
 while i<5:
  v=1
  if m[i]=="G":v=3
  elif m[i]=="Y":v=2
  j=li(g[i])
  if v>ks[j]:ks[j]=v
  i+=1

def tile(r,c,fill,ch):
 x=TX[c];y=TY[r]
 box(x,y,T,T,fill,BD)
 if ch:ct(x,y,T,T,ch,TXT,"small",-2,1)

def board():
 r=0
 while r<ROWS:
  c=0
  while c<COLS:tile(r,c,BG,"");c+=1
  r+=1

def header(a,b=""):
 box(8,1,176,22,TL,BD)
 fr(9,2,182,7,HD)
 if b:
  ct(8,1,176,10,a,TXT,"medium",-6)
  ct(8,10,176,9,b,TXT,"small",-6)
 else:ct(8,0,176,22,a,TXT,"medium",-6)

def prompt_box(label,val,hide=0):
 x0=50;y0=27;ts=16;gap=2
 if label:ct(8,27,27,20,label,TXT,"small")
 fr(36,26,156,48,BG)
 i=0
 while i<5:
  x=x0+i*(ts+gap)
  box(x,y0,ts,ts,BG,BD)
  if i<len(val):
   ch="*" if hide else val[i]
   px=x+(ts-tw(ch,"small"))//2-1;py=y0+(ts-th("small"))//2
   draw_string(px,py,ch,TXT,"small")
   draw_string(px+1,py,ch,TXT,"small")
  i+=1

def add_row(labels,y):
 starts.append(len(keys));lens.append(len(labels))
 n=len(labels);w=0;i=0
 while i<n:
  w+=(KW if len(labels[i])==1 else SW)
  if i<n-1:w+=KG
  i+=1
 x=(W-w)//2;i=0
 while i<n:
  lab=labels[i];ww=KW if len(lab)==1 else SW
  keys.append((x,y,ww,lab,1 if len(lab)==1 else 0,li(lab) if len(lab)==1 else -1))
  x+=ww+KG;i+=1

def key_at(kr,kc):
 i=starts[kr]+kc
 return i,keys[i]

def draw_key(i,fill,edge,inv=0):
 x,y,w,lab,islet,idx=keys[i]
 t=TXT
 if inv:t,fill=fill,t
 box(x,y,w,KH,fill,edge)
 dx=-2 if lab=="DEL" or lab=="ENT" else -1
 draw_string(x+(w-tw(lab,"small"))//2+dx,y+(KH-th("small"))//2,lab,t,"small")

def draw_all_keys(ks,cur=-1):
 i=0
 while i<len(keys):
  x,y,w,lab,islet,idx=keys[i]
  f=kcol(ks[idx]) if islet else BG
  draw_key(i,f,CUR if i==cur else BD,i==cur);i+=1

def move_to_row(kr,cx):
 best=0;bd=999;i=0
 while i<lens[kr]:
  idx,(x,y,w,lab,islet,ii)=key_at(kr,i)
  d=x+w//2-cx
  if d<0:d=-d
  if d<bd:bd=d;best=i
  i+=1
 return kr,best

def edge():
 global LK
 k=getkey()
 if k==None:LK=None;return None
 if LK==None:LK=k;return k
 return None

def erase_letter(r,s):
 if len(s):
  s=s[:-1]
  tile(r,len(s),BG,"")
  show_screen()
 return s

def recolour_used(ks,sel):
 seen=[0]*26;i=0
 while i<len(keys):
  x,y,w,lab,islet,idx=keys[i]
  if islet and seen[idx]==0:
   seen[idx]=1;draw_key(i,kcol(ks[idx]),CUR if i==sel else BD,i==sel)
  i+=1

def submit_row(r,s,w,ks,sel):
 m=fb(w,s);i=0
 while i<5:tile(r,i,mcol(m[i]),s[i]);i+=1
 upd_keys(ks,s,m);recolour_used(ks,sel);show_screen()
 if s==w:return -1
 return r+1

def end_screen(msg,word):
 box(18,62,156,62,TL,BD)
 ct(15,64,156,12,msg,TXT,"medium")
 ct(15,84,156,10,"Word: "+word,TXT,"small")
 ct(18,102,156,10,"EXE restart  AC quit",TXT,"small")
 show_screen()
 while 1:
  k=getkey()
  if k==KEXE:return 1
  if k==KEXIT:return 0

def kb_pick(kr,kc,ks,sel):
 old=sel;k=edge()
 if k==None:return kr,kc,sel,None
 if k==KEXE:return kr,kc,sel,"ENT"
 if k==KDEL:return kr,kc,sel,"DEL"
 if k==KEXIT:return kr,kc,sel,"EXIT"
 moved=0
 if k==KL:
  kc=lens[kr]-1 if kc==0 else kc-1;moved=1
 elif k==KR:
  kc=0 if kc==lens[kr]-1 else kc+1;moved=1
 elif k==KU:
  i,(x,y,w,lab,islet,ii)=key_at(kr,kc)
  kr,kc=move_to_row(2 if kr==0 else kr-1,x+w//2);moved=1
 elif k==KD:
  i,(x,y,w,lab,islet,ii)=key_at(kr,kc)
  kr,kc=move_to_row(0 if kr==2 else kr+1,x+w//2);moved=1
 if moved:
  sel=starts[kr]+kc
  if sel!=old:
   x,y,w,lab,islet,ii=keys[old]
   draw_key(old,kcol(ks[ii]) if islet else BG,BD)
   x,y,w,lab,islet,ii=keys[sel]
   draw_key(sel,kcol(ks[ii]) if islet else BG,CUR,1)
   show_screen()
  return kr,kc,sel,None
 if k!=KOK:return kr,kc,sel,None
 i,(x,y,w,lab,islet,ii)=key_at(kr,kc)
 return kr,kc,sel,lab

def enter_word(title,label,hide=1):
 ks=[0]*26;kr=1;kc=0;sel=starts[kr]+kc;s=""
 clear_screen();header(title);prompt_box(label,s,hide)
 draw_all_keys(ks,sel);show_screen()
 while 1:
  kr,kc,sel,act=kb_pick(kr,kc,ks,sel)
  if act==None:continue
  if act=="EXIT":return ""
  if act=="DEL":
   if len(s):s=s[:-1];prompt_box(label,s,hide);show_screen()
   continue
  if act=="ENT":
   if len(s)==5:return s
   continue
  if len(act)==1 and len(s)<5:
   s+=act;prompt_box(label,s,hide);show_screen()

def init_ui(ks,sel):
 clear_screen();header("WORDLE");board();draw_all_keys(ks,sel);show_screen()

def play_one():
 w=enter_word("SET WORD","",0)
 if not w:return 0
 ks=[0]*26;gr=0;curg="";kr=1;kc=0;sel=starts[kr]+kc
 init_ui(ks,sel)
 while 1:
  kr,kc,sel,act=kb_pick(kr,kc,ks,sel)
  if act==None:continue
  if act=="EXIT":return 0
  if act=="DEL":curg=erase_letter(gr,curg);continue
  if act=="ENT":
   if len(curg)==5:
    ng=submit_row(gr,curg,w,ks,sel)
    if ng==-1:return end_screen("Correct",w)
    gr=ng;curg=""
    if gr>=6:return end_screen("Game Over",w)
   continue
  if len(act)==1 and len(curg)<5:
   curg+=act;tile(gr,len(curg)-1,BG,act);show_screen()

def main():
 if not keys:
  add_row(list(R1),138);add_row(list(R2),156);add_row(R3,174)
 while 1:
  if play_one()==0:break

main()
