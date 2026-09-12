from casioplot import *
KEXIT=12
def main():
 clear_screen();show_screen();last=None
 while 1:
  k=getkey()
  if k==KEXIT:return
  if k!=None and k!=last:
   clear_screen();draw_string(10,10,str(k),(0,0,0));show_screen()
  last=k
main()
