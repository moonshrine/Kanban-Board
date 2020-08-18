from tkinter import *
from tkinter import colorchooser
import mysql.connector
from datetime import datetime
from datetime import time
from datetime import date
import time
from functools import partial


####----------------------------------Code for tab/slot/To do-----------------------------------------
#start
def myfunction1(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=365,height=300)

def search_box1():
    global task_dict1,sch_dict1
    search_text = IPTEXT1.get()
    search_text = search_text.strip()
    temp_dict = {}
    if len(search_text) ==0:
        update_tab1(task_dict1)
    else:
        if search_text in sch_dict1:
            print("key is present in dictionary "+ search_text)
            temp_index = sch_dict1.get(search_text)
            temp_dict[temp_index] = task_dict1[temp_index]
            update_tab1(temp_dict)
            
        else:
            print("Key not present in dictionary "+ search_text)
        #print(task_dict1)
        '''
        for i in task_dict1:
            if task_dict1[i]['task_title'] == search_text :
                print("key is present in dictionary "+ str(search_text))
                break
        #print("Key not present in dictionary "+ search_text)
        '''
    
def create_tab1():
    global frame, myframe, canvas,row_no1,tab_task_index1,task_dict1
    global IPTEXT1, sch_dict1
    IPTEXT1 = StringVar()
    row_no1 =0
    tab_task_index1 =0
    sch_dict1 = {}
    task_dict1 = {}
    myframe = Frame(screen,relief = GROOVE, width= 100, height=100, bd=3, bg="blue")
    myframe.place(x=10, y=10)
       
    canvas = Canvas(myframe, bg="gray80")
    frame = Frame(canvas, bg ="gray80")
    
    myscrollbar = Scrollbar(myframe, orient = "vertical",command= canvas.yview)
    canvas.configure(yscrollcommand=myscrollbar.set)

    myscrollbar.pack(side="right",fill="y")
    canvas.pack(side = BOTTOM)

    canvas.create_window((0,0),window=frame,anchor='nw')
    frame.bind("<Configure>",myfunction1)

    tab_title = Label(myframe,text="Tab/To do").pack(fill=BOTH,expand =True)
    Entry(myframe, font= ("Caliber",15),textvariable = IPTEXT1).pack(side= LEFT, fill = BOTH, expand =True, padx = 2)  # Seach entry widget
    b1 = Button(myframe,text = "Search Task",background = "green",fg = "white", command = search_box1).pack( side = LEFT, fill =BOTH)
    b2 = Button(myframe,text = "Add Task",background = "yellow",fg = "black", command = add_task1).pack( side = LEFT)




def add_task_to_tab2_from_tab1(index):    #first copy/add directly to tab2 then remove that task from tab1
    global task_dict1
    temp_title = task_dict1[index]['task_title']
    temp_comment = task_dict1[index]['comment']
    temp_color = task_dict1[index]['color']

    add_task_to_tab2(temp_title, temp_comment, temp_color)

    remove_task_from_tab1(index)   # removing task from tab1/to do tab




def update_tab1(i_dict):
    global frame,canvas
    frame.destroy()

    frame = Frame(canvas, bg ="gray80")
    canvas.create_window((0,0),window=frame,anchor='nw')
    frame.bind("<Configure>",myfunction1)
    
    def add_task_from_dict1(index,t_title,comt,colr):
        global row_no1
        Label(frame, text = t_title, width = 35,background = colr,font = ("Caliber",10,'bold')).grid(row = row_no1, column =0)
        Button(frame, text = ">>", width = 5,background ='#ffff00', command = partial(add_task_to_tab2_from_tab1, index)).grid(row = row_no1, column =2)
        Button(frame, text = "|D|", width = 3, background ='#ea3015',command = partial(remove_task_from_tab1, index)).grid(row = row_no1, column =1)

        row_no1 +=1
        Label(frame, justify = LEFT, wraplength = 350, text = comt, width = 50).grid(row = row_no1, column =0,columnspan = 3)
        row_no1 +=1
        Label(frame, text = "*-*-*-*-*-*-*-*-*-*-*-*-*", background = "gray80").grid(row = row_no1, column =0,columnspan =2)    # Remove astrik later
        row_no1 +=1
    for i in i_dict:
        print(i_dict[i]['task_title'])
        print(i_dict[i]['comment'])
        print(i_dict[i]['color'])
        add_task_from_dict1(i, i_dict[i]['task_title'], i_dict[i]['comment'], i_dict[i]['color'])


def remove_task_from_tab1(t_index):
     global task_dict1,sch_dict1
     temp = task_dict1[t_index]['task_title']     # copy title of task to delete it from search dictionary
     del task_dict1[t_index]
     print("Deleted successfully from tab1")
     print(task_dict1)
    
     del sch_dict1[temp]        
     print(sch_dict1)
     update_tab1(task_dict1)   # updating tab1 after deleteing task
 
def add_task_to_tab1():
    global row_no1,tab_task_index1
    print(task_title.get())
    print(comment.get("1.0","end-1c"))

    Label(frame, text = task_title.get(), width = 35,background = taskcolor[1],font = ("Caliber",10,'bold')).grid(row = row_no1, column =0)
    Button(frame, text = ">>", width = 5,background ='#ffff00', command = partial(add_task_to_tab2_from_tab1, tab_task_index1)).grid(row = row_no1, column =2)
    Button(frame, text = "|D|", width = 3, background ='#ea3015',command = partial(remove_task_from_tab1, tab_task_index1)).grid(row = row_no1, column =1)
    
    row_no1 +=1
    Label(frame, justify = LEFT, wraplength = 350, text = comment.get("1.0","end-1c"), width = 50).grid(row = row_no1, column =0,columnspan = 3)
    row_no1 +=1
    
    Label(frame, text = "*-*-*-*-*-*-*-*-*-*-*-*-*", background = "gray80").grid(row = row_no1, column =0,columnspan =2)    # Remove astrik later
    row_no1 +=1
    def add_task_to_dict1():
        global tab_task_index1,task_dict1, taskcolor, sch_dict1
        task_dict1[tab_task_index1] = {}
        task_dict1[tab_task_index1]['task_title'] = task_title.get()
        task_dict1[tab_task_index1]['comment'] = comment.get("1.0","end-1c")
        task_dict1[tab_task_index1]['color'] = taskcolor[1]

        sch_dict1[task_title.get()] = tab_task_index1    # search box dictionary for 1st tab
        tab_task_index1 +=1
        print(sch_dict1)
    add_task_to_dict1()

    screen2.destroy()

def add_task1():
    global screen2,task_title, comment
    screen2 = Toplevel(screen)
    screen2.title("Add Task")
    screen2.geometry("350x200")

    task_title = StringVar()
    
    Label(screen2, text = "Title", ).grid(row = 0, column = 0, sticky = W)
    Entry(screen2, textvariable = task_title, width = 30,font = ("Caliber",12)).grid(row = 0, column = 1, sticky = W)

    Label(screen2, text = "Comment", font = ("Caliber",12)).grid(row = 1, column = 0, sticky = W)
    comment = Text(screen2,height=3,width=34)
    comment.grid(row = 1, column = 1, sticky = W)

    def ask_color():
        global taskcolor
        taskcolor = colorchooser.askcolor()
        Label(screen2,text = "Choosen color", background = taskcolor[1]).grid(row = 4, column = 0, sticky = W+E,columnspan =2)     
        print(taskcolor)
        
    Label(screen2, text = "Priority Color", font = ("Caliber",12)).grid(row = 2, column = 0, sticky = W+E,columnspan =2)
    Button(screen2,text = "Selected Color",fg = "black", command = ask_color).grid(row = 3, column = 0, sticky = W+E,columnspan =2)

    Label(screen2, text = "", font = ("Caliber",12)).grid(row = 5, column = 0, sticky = W+E,columnspan =2)
    Button(screen2,text = "Add Task",background = '#aaf49f',fg = "black", command = add_task_to_tab1).grid(row = 6, column = 0, sticky = W+E,columnspan =2)

#end of tab1 code---------------------

####--------------------------------------Code for Tab2/Doing -------------------------------
#start

def myfunction2(event):
    canvas2.configure(scrollregion=canvas2.bbox("all"),width=365,height=300)
    
def create_tab2():
    global frame2, canvas2,row_no2,tab_task_index2,task_dict2
    global IPTEXT2
    IPTEXT2 = StringVar()
    row_no2 =0
    tab_task_index2 =0
    task_dict2 = {}
    myframe2 = Frame(screen,relief = GROOVE, width= 100, height=100, bd=3, bg="green")
    myframe2.place(x=445, y=10)
       
    canvas2 = Canvas(myframe2, bg="gray80")
    frame2 = Frame(canvas2, bg ="gray80")
    
    myscrollbar2 = Scrollbar(myframe2, orient = "vertical",command= canvas2.yview)
    canvas2.configure(yscrollcommand=myscrollbar2.set)

    myscrollbar2.pack(side="right",fill="y")
    canvas2.pack(side = BOTTOM)

    canvas2.create_window((0,0),window=frame2,anchor='nw')
    frame2.bind("<Configure>",myfunction2)

    Label(myframe2,text="Tab2/Doing").pack(fill=BOTH,expand =True)
    Entry(myframe2, font= ("Caliber",15),textvariable = IPTEXT2).pack(side= LEFT, fill = BOTH, expand =True, padx = 2)  # Seach entry widget
    b1 = Button(myframe2,text = "Search Task",background = "green",fg = "white").pack( side = LEFT, fill =BOTH)
#    b2 = Button(myframe2,text = "Add Task",background = "yellow",fg = "black", command = add_task1).pack( side = LEFT)



def add_task_to_tab3_from_tab2(index):    #first copy/add directly to tab3 then remove that task from tab2
    global task_dict2
    temp_title = task_dict2[index]['task_title']
    temp_comment = task_dict2[index]['comment']
    temp_color = task_dict2[index]['color']

    add_task_to_tab3(temp_title, temp_comment, temp_color)

    remove_task_from_tab2(index)   # removing task from tab2/Doing tab

def update_tab2():
    global frame2,canvas2,task_dict2
    frame2.destroy()

    frame2 = Frame(canvas2, bg ="gray80")
    canvas2.create_window((0,0),window=frame2,anchor='nw')
    frame2.bind("<Configure>",myfunction2)
    
    def add_task_from_dict2(index,t_title,comt,colr):
        global row_no2
        Label(frame2, text = t_title, width = 35,background = colr,font = ("Caliber",10,'bold')).grid(row = row_no2, column =0)
        Button(frame2, text = ">>", width = 5,background ='#ffff00', command = partial(add_task_to_tab3_from_tab2, index)).grid(row = row_no2, column =2)
        Button(frame2, text = "|D|", width = 4, background ='#ea3015',command = partial(remove_task_from_tab2, index)).grid(row = row_no2, column =1)

        row_no2 +=1
        Label(frame2, justify = LEFT, wraplength = 350, text = comt, width = 50).grid(row = row_no2, column =0,columnspan = 3)
        row_no2 +=1
        Label(frame2, text = "*-*-*-*-*-*-*-*-*-*-*-*-*", background = "gray80").grid(row = row_no2, column =0,columnspan =2)    # Remove astrik later
        row_no2 +=1
    for i in task_dict2:
        print(task_dict2[i]['task_title'])
        print(task_dict2[i]['comment'])
        print(task_dict2[i]['color'])
        add_task_from_dict2(i, task_dict2[i]['task_title'], task_dict2[i]['comment'], task_dict2[i]['color'])



def remove_task_from_tab2(t_index):
     global task_dict2
     del task_dict2[t_index]
     print("Deleted successfully")
     print(task_dict2)
     
     update_tab2()   # updating tab1 after deleteing task
 
def add_task_to_tab2(title, comment,color):
    global row_no2, tab_task_index2
    #print(task_title.get())
    #print(comment.get("1.0","end-1c"))

    Label(frame2, text = title, width = 35,background = color,font = ("Caliber",10,'bold')).grid(row = row_no2, column =0)
    Button(frame2, text = ">>", width = 5,background ='#ffff00', command = partial(add_task_to_tab3_from_tab2, tab_task_index2)).grid(row = row_no2, column =2)
    Button(frame2, text = "|D|", width = 4, background ='#ea3015',command = partial(remove_task_from_tab2, tab_task_index2)).grid(row = row_no2, column =1)
    
    row_no2 +=1
    Label(frame2, justify = LEFT, wraplength = 350, text = comment, width = 50).grid(row = row_no2, column =0,columnspan = 3)
    row_no2 +=1
    Label(frame2, text = "*-*-*-*-*-*-*-*-*-*-*-*-*", background = "gray80").grid(row = row_no2, column =0,columnspan =3)    # Remove astrik later
    row_no2 +=1
    def add_task_to_dict2():
        global tab_task_index2,task_dict2
        task_dict2[tab_task_index2] = {}
        task_dict2[tab_task_index2]['task_title'] = title
        task_dict2[tab_task_index2]['comment'] = comment
        task_dict2[tab_task_index2]['color'] = color
        tab_task_index2 +=1
        #print(task_dict)
    add_task_to_dict2()


#end of tab2 code-----------------


####--------------------------------------Code for Tab3/Done -------------------------------
#start

def myfunction3(event):
    canvas3.configure(scrollregion=canvas3.bbox("all"),width=365,height=300)
    
def create_tab3():
    global frame3, canvas3,row_no3,tab_task_index3,task_dict3
    global IPTEXT3
    IPTEXT3 = StringVar()
    row_no3 =0
    tab_task_index3 =0
    task_dict3 = {}
    myframe3 = Frame(screen,relief = GROOVE, width= 100, height=100, bd=3, bg="yellow")
    myframe3.place(x=875, y=10)
       
    canvas3 = Canvas(myframe3, bg="gray80")
    frame3 = Frame(canvas3, bg ="gray80")
    
    myscrollbar3 = Scrollbar(myframe3, orient = "vertical",command= canvas3.yview)
    canvas3.configure(yscrollcommand=myscrollbar3.set)

    myscrollbar3.pack(side="right",fill="y")
    canvas3.pack(side = BOTTOM)

    canvas3.create_window((0,0),window=frame3,anchor='nw')
    frame3.bind("<Configure>",myfunction3)

    Label(myframe3,text="Tab2/Doing").pack(fill=BOTH,expand =True)
    Entry(myframe3, font= ("Caliber",15),textvariable = IPTEXT3).pack(side= LEFT, fill = BOTH, expand =True, padx = 2)  # Seach entry widget
    b1 = Button(myframe3,text = "Search Task",background = "green",fg = "white").pack( side = LEFT, fill =BOTH)
#    b2 = Button(myframe2,text = "Add Task",background = "yellow",fg = "black", command = add_task1).pack( side = LEFT)




def add_task_to_tab2_from_tab3(index):    #first copy/add directly to tab2 then remove that task from tab3
    global task_dict3
    temp_title = task_dict3[index]['task_title']
    temp_comment = task_dict3[index]['comment']
    temp_color = task_dict3[index]['color']

    add_task_to_tab2(temp_title, temp_comment, temp_color)

    remove_task_from_tab3(index)   # removing task from tab3/Done tab



def update_tab3():
    global frame3,canvas3,task_dict3
    frame3.destroy()

    frame3 = Frame(canvas3, bg ="gray80")
    canvas3.create_window((0,0),window=frame3,anchor='nw')
    frame3.bind("<Configure>",myfunction3)
    
    def add_task_from_dict3(index,t_title,comt,colr):
        global row_no3
        Label(frame3, text = t_title, width = 38,background = colr,font = ("Caliber",10,'bold')).grid(row = row_no3, column =0)
        Button(frame3, text = "<<", width = 5,background ="yellow", command = partial(add_task_to_tab2_from_tab3,index)).grid(row = row_no3, column =1)
        row_no3 +=1
        Label(frame3, justify = LEFT, wraplength = 350, text = comt, width = 50).grid(row = row_no3, column =0,columnspan = 2)
        #row_no3 +=1
        #Button(frame3, text = "Delete Task", width = 50, background ='#ea3015',command = partial(remove_task_from_tab3, index)).grid(row = row_no3, column =0,columnspan = 2)
        row_no3 +=1
        Label(frame3, text = "*-*-*-*-*-*-*-*-*-*-*-*-*", background = "gray80").grid(row = row_no3, column =0,columnspan =2)    # Remove astrik later
        row_no3 +=1
    for i in task_dict3:
        print(task_dict3[i]['task_title'])
        print(task_dict3[i]['comment'])
        print(task_dict3[i]['color'])
        add_task_from_dict3(i, task_dict3[i]['task_title'], task_dict3[i]['comment'], task_dict3[i]['color'])



def remove_task_from_tab3(t_index):
     global task_dict3
     del task_dict3[t_index]
     print("Deleted successfully")
     print(task_dict3)
     
     update_tab3()   # updating tab3 after deleteing task
 
def add_task_to_tab3(title, comment,color):
    global row_no3, tab_task_index3
    
    Label(frame3, text = title, width = 38,background = color,font = ("Caliber",10,'bold')).grid(row = row_no3, column =0)
    Button(frame3, text = "<<", width = 5,background ='#ffff00', command = partial(add_task_to_tab2_from_tab3,tab_task_index3)).grid(row = row_no3, column =1)
    row_no3 +=1
    Label(frame3, justify = LEFT, wraplength = 350, text = comment, width = 50).grid(row = row_no3, column =0,columnspan = 2)
    row_no3 +=1
    #Button(frame3, text = "Delete Task", width = 50, background ='#ea3015',command = partial(remove_task_from_tab3, tab_task_index3)).grid(row = row_no3, column =0,columnspan = 2)
    #row_no3 +=1
    Label(frame3, text = "*-*-*-*-*-*-*-*-*-*-*-*-*", background = "gray80").grid(row = row_no3, column =0,columnspan =2)    # Remove astrik later
    row_no3 +=1
    def add_task_to_dict3():
        global tab_task_index3,task_dict3
        task_dict3[tab_task_index3] = {}
        task_dict3[tab_task_index3]['task_title'] = title
        task_dict3[tab_task_index3]['comment'] = comment
        task_dict3[tab_task_index3]['color'] = color
        tab_task_index3 +=1
        #print(task_dict)
    add_task_to_dict3()


#end of tab3 code-----------------


def create_window():
    global screen
    
    screen = Tk()
    screen.title("Task Manager")
    screen.geometry("1320x400")
    create_tab1()
    create_tab2()
    create_tab3()

    screen.mainloop()
create_window()
