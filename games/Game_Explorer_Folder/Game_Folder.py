from casioplot import *
U=14;D=34;OK=24;EXE=95;AC=12
TXT=(20,24,30);MUT=(105,110,120);SEL=(35,115,220);ERR=(210,55,55);BG=(255,255,255)

ACTION=(("BLOCK","Block"),("FLAPPY","Flappy"),("PAC-MAN","Pacman"),("SNAKE","Snake"))
PUZZLE=(("MINESWEEPER","Mine"),("STARFALL QUEST","Starfall"),("SUDOKU","sudoku"),("TETRIS","Tetris2"))
TWO=(("CHESS","Chess"),("CONNECT 4","Connect4"),("TIC-TAC-TOE","TicTac"),("WORDLE","Wordle"))
UTIL=(("TRIANGLE SOLVER","Triangle"),("KEY TEST","KeyTest"))
P=((("GAMES",1),("UTILITIES",5)),(("ACTION",2),("PUZZLE / QUEST",3),("2 PLAYER",4)),ACTION,PUZZLE,TWO,UTIL)
T=("GAME EXPLORER","GAMES","ACTION GAMES","PUZZLE / QUEST","2 PLAYER GAMES","UTILITIES")
BACK=(0,0,1,1,1,0);LK=None;LOAD={}

def load(n):
 if n=="Block":import Block;return Block
 if n=="Flappy":import Flappy;return Flappy
 if n=="Mine":import Mine;return Mine
 if n=="Pacman":import Pacman;return Pacman
 if n=="Snake":import Snake;return Snake
 if n=="Starfall":import Starfall;return Starfall
 if n=="sudoku":import sudoku;return sudoku
 if n=="Tetris2":import Tetris2;return Tetris2
 if n=="Chess":import Chess;return Chess
 if n=="Connect4":import Connect4;return Connect4
 if n=="TicTac":import TicTac;return TicTac
 if n=="Wordle":import Wordle;return Wordle
 if n=="Triangle":import Triangle;return Triangle
 if n=="KeyTest":import KeyTest;return KeyTest
 raise ImportError(n)

def edge():
 global LK
 k=getkey()
 if k==None:LK=None;return None
 if LK==None:LK=k;return k
 return None

def cursor(i,c):
 x=14;y=43+i*19;n=0
 while n<5:
  set_pixel(x+n,y+n,c);set_pixel(x+n,y+8-n,c);n+=1

def page(p,s):
 clear_screen()
 draw_string(18,7,T[p],TXT,"medium")
 if p==0:draw_string(278,9,"GAMES + TOOLS",MUT,"small")
 elif p>=2 and p<=4:draw_string(334,9,str(len(P[p])),MUT,"small")
 i=0
 while i<len(P[p]):
  a=P[p][i];y=41+i*19
  draw_string(30,y,a[0],TXT,"small")
  if p<2:draw_string(354,y,">",MUT,"small")
  i+=1
 draw_string(18,181,"OK/EXE OPEN",MUT,"small")
 draw_string(305,181,"AC "+("EXIT" if p==0 else "BACK"),MUT,"small")
 cursor(s,SEL);show_screen()

def err(s):
 clear_screen()
 draw_string(18,54,"COULD NOT OPEN",ERR,"medium")
 draw_string(18,82,s[:52],TXT,"small")
 draw_string(18,116,"PRESS ANY KEY",MUT,"small")
 show_screen()
 while getkey()!=None:pass
 while getkey()==None:pass
 while getkey()!=None:pass

def run(a):
 global LK
 while getkey()!=None:pass
 n=a[1]
 try:
  if n in LOAD:LOAD[n].main()
  else:LOAD[n]=load(n)
 except Exception as e:err(str(e))
 while getkey()!=None:pass
 LK=None

def main():
 p=0;s=0;page(p,s)
 while 1:
  k=edge()
  if k==None:continue
  old=s
  if k==U and s:s-=1
  elif k==D and s+1<len(P[p]):s+=1
  elif k==AC:
   if p==0:return
   p=BACK[p];s=0;page(p,s);continue
  elif k==OK or k==EXE:
   if p<2:
    p=P[p][s][1];s=0;page(p,s);continue
   run(P[p][s]);page(p,s);continue
  if s!=old:
   cursor(old,BG);cursor(s,SEL);show_screen()
main()
