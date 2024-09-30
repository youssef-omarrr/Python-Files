from tkinter import *
###############################  FUNCTIONS  ####################################
def write(num):
    global ans1, ans2, op, txt, flag, cur1

    if num == 'ac': #clears all data
        clear()

    #taking the first input before the opetator 
    elif (ans2.get() == 'y') and (op.get() == 'y') and (num not in operations):
        ans1.set(num) 
        cur1 = ans1.get()
        cur2 = txt.cget('text')
        txt.config(text = cur2 + cur1) #cascades old and new data so the screen diplays all the data 
        ans1.set(cur2 + cur1) #changes the first input each time to have multi digit variables
                              #by cascading the old digit with the new 

    elif op.get() == 'y': #getting the operator
        op.set(num)
        txt.config(text = ans1.get() + op.get())

    #taking the second input untill the input is '='
    elif ((ans2.get() == 'y') or (op.get() != 'y')) and (num != '='):
        if flag == 0: #here I used a flag to check for the first digit 
            ans2.set(num)
            cur1 = ans2.get()
            cur2 = txt.cget('text')
            txt.config(text = cur2 + cur1)
            flag = 1
        else:
            ans2.set(cur1 + num) #because we cant cascade the second input without the first
            cur1 = ans2.get()
            cur2 = txt.cget('text')
            txt.config(text = cur2 + num)

    if num == '=' : #checks for wich operation is used
        flag = 0
        if op.get() == '+':
            add()
        elif op.get() == '-':
            sub()
        elif op.get() == 'x':
            mul()
        elif op.get() == '/':
            div()
        elif op.get() == '^':
            power()

        op.set('y') #resets the operator and second input because the first input will be
        ans2.set('y') #the result of whatever operation was used
    return

def add ():
    global ans1, ans2,txt
    res = float(ans1.get()) + float (ans2.get())
    ans1.set(str(res)) 
    txt.config(text = str(res))
    return

def sub():
    global ans1, ans2,txt
    res = float(ans1.get()) - float (ans2.get())
    ans1.set(str(res))
    txt.config(text = str(res))
    return

def mul():
    global ans1, ans2,txt
    res = float(ans1.get()) * float (ans2.get())
    ans1.set(str(res))
    txt.config(text = str(res))
    return

def div():
    global ans1, ans2,txt
    res = float(ans1.get()) / float (ans2.get())
    ans1.set(str(res))
    txt.config(text = str(res))
    return

def power():
    global ans1, ans2,txt
    res = pow (float(ans1.get()), float (ans2.get()))
    ans1.set(str(res))
    txt.config(text = str(res))
    return

def clear(): #clears all data by reseting them to their intial values and makes the display empty
    ans1.set('y')
    op.set('y')
    ans2.set('y')
    txt.config(text = '')
    return

################################  MAIN  ###################################
wind = Tk()
wind.title("Dumb calculator")
wind.geometry('365x570') #display ratio
wind.configure(bg = '#EEEEEE'.lower())

txt = Label(wind, text = '', height= 2,font = ("bold",50), bg = '#EEEEEE'.lower(), fg = 'black') #our screen that will display the output
txt.grid(row = 0,rowspan=2, columnspan= 7) 

ans1 = StringVar(wind, 'y') #random initial values just to know if it they changed or not
ans2 = StringVar(wind, 'y')
op = StringVar(wind, 'y')
operations = ['+', '-', 'x', '/', '=', 'ac', '^'] #to make sure durin taking the input that it is not an operation
flag = 0 
cur1 = ''

###################  intializing the buttons  ###################################
b1 =     Button(wind, text = '1', height= 5, width = 7, command= lambda:write('1'))
b2 =     Button(wind, text = '2', height= 5, width = 7, command= lambda:write('2'))
b3 =     Button(wind, text = '3', height= 5, width = 7, command= lambda:write('3'))
b4 =     Button(wind, text = '4', height= 5, width = 7, command= lambda:write('4'))
b5 =     Button(wind, text = '5', height= 5, width = 7, command= lambda:write('5'))
b6 =     Button(wind, text = '6', height= 5, width = 7, command= lambda:write('6'))
b7 =     Button(wind, text = '7', height= 5, width = 7, command= lambda:write('7'))
b8 =     Button(wind, text = '8', height= 5, width = 7, command= lambda:write('8'))
b9 =     Button(wind, text = '9', height= 5, width = 7, command= lambda:write('9'))
b0 =     Button(wind, text = '0', height= 5, width = 7, command= lambda:write('0'))
bdot =   Button(wind, text = '•', height= 5, width = 7, command= lambda:write('.'))

plus =   Button(wind, text = '+', height= 5, width = 7, command= lambda:write('+'), font = ("bold"))
minus =  Button(wind, text = '-', height= 5, width = 7, command= lambda:write('-'), font = ("bold"))
times =  Button(wind, text = 'x', height= 5, width = 7, command= lambda:write('x'), font = ("bold"))
divide = Button(wind, text = '/', height= 5, width = 7, command= lambda:write('/'), font = ("bold"))

equal =  Button(wind, text = '=', height= 5, width = 14, command= lambda:write('='), font = ("bold"))
ac =     Button(wind, text = 'AC', height= 5, width = 7, command= lambda:write('ac'), font = ("bold"))
poww =   Button(wind, text = '^', height= 5, width = 7, command= lambda:write('^'), font = ("bold"))


####################  putting the buttons in their grid  ###################################
b1.grid     (row = 4, column = 0, sticky = 'nsew')
b2.grid     (row = 4, column = 1, sticky = 'nsew')
b3.grid     (row = 4, column = 2, sticky = 'nsew')
b4.grid     (row = 3, column = 0, sticky = 'nsew')
b5.grid     (row = 3, column = 1, sticky = 'nsew')
b6.grid     (row = 3, column = 2, sticky = 'nsew')
b7.grid     (row = 2, column = 0, sticky = 'nsew')
b8.grid     (row = 2, column = 1, sticky = 'nsew')
b9.grid     (row = 2, column = 2, sticky = 'nsew')
b0.grid     (row = 5, column = 0, sticky = 'nsew')
bdot.grid   (row = 5, column = 1, sticky = 'nsew')
 
plus.grid   (row = 4, column = 3, sticky = 'nsew')
minus.grid  (row = 4, column = 4, sticky = 'nsew')
times.grid  (row = 3, column = 3, sticky = 'nsew')
divide.grid (row = 3, column = 4, sticky = 'nsew')
 
equal.grid  (row = 5, column = 2,columnspan=3, sticky = 'nsew')
ac.grid     (row = 2, column = 4, sticky = 'nsew')
poww.grid   (row = 2, column = 3, sticky = 'nsew')

##################  changing the color of the buttons  ###################################
b1.configure     (bg = '#508C9B'.lower(),font = ("bold"))
b2.configure     (bg = '#508C9B'.lower(),font = ("bold"))
b3.configure     (bg = '#508C9B'.lower(),font = ("bold"))
b4.configure     (bg = '#508C9B'.lower(),font = ("bold"))
b5.configure     (bg = '#508C9B'.lower(),font = ("bold"))
b6.configure     (bg = '#508C9B'.lower(),font = ("bold"))
b7.configure     (bg = '#508C9B'.lower(),font = ("bold"))
b8.configure     (bg = '#508C9B'.lower(),font = ("bold"))
b9.configure     (bg = '#508C9B'.lower(),font = ("bold"))
b0.configure     (bg = '#508C9B'.lower(),font = ("bold"))
bdot.configure   (bg = '#508C9B'.lower(),font = ("bold"))

plus.configure   (bg = '#134B70'.lower(), fg='white')
minus.configure  (bg = '#134B70'.lower(), fg='white')
times.configure  (bg = '#134B70'.lower(), fg='white')
divide.configure (bg = '#134B70'.lower(), fg='white')

equal.configure  (bg = '#E2E2B6'.lower())
ac.configure     (bg = '#201E43', fg='white')
poww.configure   (bg = '#134B70'.lower(), fg='white')

#we could have made the grid and changed the color in the same line we intialized the butons at
#but this is more organized if we wanted to add any extra buttons
#note: when writing color codes they must be lower cases so use '.lower()'


wind.mainloop()

