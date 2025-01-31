import gui_lib as G
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageTk, Image
import pickle
import os
import shutil

h = G.root.winfo_screenheight()
w = G.root.winfo_screenwidth()


G.root.geometry("1280x600")
G.root.title('Edit Window')
G.root.grid_anchor('center')
G.root.resizable(False,False)
G.canvas['background']= 'white'
cenx=w/2
ceny=h/2

f = open("details.txt","rb")
info = pickle.load(f)
n = len(info)
f.close()

def test():
    print(0)
def add():
    add_win = tk.Toplevel()
    add_win.geometry("500x250")
    add_win.title('Add')
    add_win.grid_anchor('center')
    add_win.resizable(False,False)
    add_canvas = tk.Canvas(add_win, width = 500, height = 250, highlightthickness = 0, bg='#c7c7c7')
    add_canvas.place(x = 0, y = 0)
    add_canvas.photos = []
    G.text('Name:',200,10,canvas=add_canvas,col='black',anchor=tk.W)
    new_name = G.inputBox(200,25,30,12,bg_col='white',col='black',j='left',canvas=add_canvas)
    G.text('Stock: ',200,70,canvas=add_canvas,col='black',anchor=tk.W)
    new_stock = G.inputBox(200,85,20,12,bg_col='white',col='black',j='left',canvas=add_canvas)
    G.text('kg',390,100,canvas=add_canvas,col='black',anchor=tk.W,size=12)
    G.text('Cost: ',200,130,canvas=add_canvas,col='black',anchor=tk.W)
    new_cost = G.inputBox(200,145,20,12,bg_col='white',col='black',j='left',canvas=add_canvas)
    G.text('Rs per kg',390,160,canvas=add_canvas,col='black',anchor=tk.W,size=12)
    global new_path
    new_path = None
    def add_item(img):
        global n
        f = open("details.txt","rb")        
        info = pickle.load(f)
        f.close()

        Name = new_name.get()
        Price = int(new_cost.get())
        Stock = int(new_stock.get())
        if Stock < 20 :
             Status = 'Low Stock, Resupply'
        else :
             Status = 'Sufficient Stock'

        info[Name] = [Stock, Price, Status]
        f = open("details.txt","wb")   
        pickle.dump(info,f)
        f.close()
        ext =  os.path.splitext(img)[1]
        filename = os.path.basename(img)
        shutil.copy(img,"Assets")
        assets = "Assets\\"
        os.rename(assets+filename,assets+Name+'.jpg')
        search()
        n+=1
    def addPhoto():
        fileName = filedialog.askopenfilename(parent=add_win)
        G.image(fileName,97,84,194,168,canvas=add_canvas)
        global new_path, photo_button
        new_path =  fileName
        photo_button.destroy()
    global photo_button
    photo_button = G.button('Add \nphoto',30,80,60,160,canvas=add_canvas,col='blue',bg_col='#c7c7c7',command=addPhoto,font='Consolas 40 bold')
    G.button('OK',430,210,20,40,col='black',bg_col='white', command = lambda: add_item(new_path), canvas = add_canvas)
def edit(item,data):
    edit_win = tk.Toplevel()
    edit_win.geometry("500x250")
    edit_win.title('Edit')
    edit_win.grid_anchor('center')
    edit_win.resizable(False,False)
    edit_canvas = tk.Canvas(edit_win, width = 500, height = 250, highlightthickness = 0, bg='#c7c7c7')
    edit_canvas.place(x = 0, y = 0)
    edit_canvas.photos = []
    G.text('Name:',200,10,canvas=edit_canvas,col='black',anchor=tk.W)
    new_name = G.inputBox(200,25,30,12,bg_col='white',col='black',j='left',canvas=edit_canvas,val=item)
    G.text('Stock: ',200,70,canvas=edit_canvas,col='black',anchor=tk.W)
    new_stock = G.inputBox(200,85,20,12,bg_col='white',col='black',j='left',canvas=edit_canvas,val=data[0])
    G.text('kg',390,100,canvas=edit_canvas,col='black',anchor=tk.W,size=12)
    G.text('Cost: ',200,130,canvas=edit_canvas,col='black',anchor=tk.W)
    new_cost = G.inputBox(200,145,20,12,bg_col='white',col='black',j='left',canvas=edit_canvas,val=data[1])
    G.text('Rs per kg',390,160,canvas=edit_canvas,col='black',anchor=tk.W,size=12)
    
    fileName = 'Assets\\'+item+'.jpg'
    G.image(fileName,97,84,194,168,canvas=edit_canvas)
    global new_path
    new_path = None
    def updatePhoto():
        global new_path
        fileName = filedialog.askopenfilename(parent=edit_win)
        G.image(fileName,97,84,194,168,canvas=edit_canvas)
        new_path = shutil.copy(fileName,"Assets")
        return new_path
    
    G.button('Change photo',0,140,20,186,col='blue',bg_col='white',command=updatePhoto, canvas = edit_canvas)
    
    def update_inv(): #attach toedit button next to each item
         f = open("details.txt","rb")        
         info = pickle.load(f)
         f.close()
         
         global  new_path
         Name = new_name.get()
         Stock = int(new_stock.get())
         Price = int(new_cost.get())
         
         
         if Stock < 20 :
            Status = 'Low Stock, Resupply'
         else :
            Status = 'Sufficient Stock'
         if new_path != None:
             print(new_path)
             assets = "Assets\\"
             ext =  os.path.splitext(new_path)[1]
             new_path_rename = assets+Name+'.jpg'
             if os.path.isfile(new_path_rename):
                 os.remove(new_path_rename)
                 print('clone file detectde')
             if os.path.isfile(new_path):
                 os.rename(new_path,new_path_rename)
         else:
             ext =  os.path.splitext(fileName)[1]
             print(fileName)
             assets = "Assets\\"
             if os.path.isfile(fileName):
                 os.rename(fileName,assets+Name+'.jpg')
         if item in info:
             del info[item]

         info[Name] = [Stock, Price, Status]
         f = open("details.txt","wb")
         pickle.dump(info,f)
         f.close()
         edit_win.destroy()
         search()
    G.button('OK',430,210,20,40,col='black',bg_col='white', command = update_inv, canvas = edit_canvas)

def delete_item(name):
    global n
    f = open("details.txt","rb")        
    info = pickle.load(f)
    f.close()
    del info[name]
    os.remove('Assets//'+name+'.jpg')
    f = open("details.txt","wb")   
    pickle.dump(info,f)
    f.close()
    search()
    n-=1
def tabulate(name,data,y, bgcol):
    r = G.canvas.create_rectangle(0,y-20,1920,y+30, fill=bgcol,outline=bgcol)
    t1 = G.text(name, 200, y,col='black')
    t2 = G.text(str(data[0])+' kg',400,y,col='black')
    t3 = G.text('₹'+str(data[1])+' per kg',600,y,col='black')
    t4 = G.text(data[2],900,y,col='black')
    b1 = G.button('Edit', 1100,y-10,25,100 ,col='blue',bg_col=bgcol,command=lambda: edit(name, data))
    b2 = G.button('🗑',1200,y-10,25,25,col='red', bg_col= bgcol, command=lambda: delete_item(name ))
    G.scroll(600)

    return (b1, b2)

def view_inv(): #default canvas

    print(f"{'Sno' : <5}{'Item_Name' : ^15}{'Stock' : ^10}{'Price' : ^10}{'Status' : ^25}")
    searchbox = G.inputBox(110,5,72,20,bg_col='white',col='black',j='left')
    button_list= []
    global search

    def search():
        f = open("details.txt","rb")        
        info = pickle.load(f)
        search_input = searchbox.get().lower()
        y = 120
        
        
        #print(n)
        for i in button_list:
            for j in i:
                j.destroy()
        global n       
        G.canvas.create_rectangle(0,y-20,1280,y+50*n,fill='white',outline='white')
        
        
        col = '#c7c7c7'
        for k,v in info.items():
            
            if search_input in k.lower() or search_input=='':
                buttons = tabulate(k,v,y,col)
                button_list.append(buttons)
                
                if col == '#c7c7c7':

                    col = 'white'
                else:
                    col='#c7c7c7'
                y+=50
                print(search_input)
        print(info)
        f.close()
    G.button('⟳',5,5,30,30,command=lambda: edit('Apple',data))
    G.button('Add+',45,5,30,50,command=add)
    G.button('🔍',1200,5,30,30,command=search)
    G.canvas.create_rectangle(0,45,1280,120, fill='black')
    G.text(f"{'Product' : ^12}{'Stock' : ^24}{'Price' : ^12}{'Status' : ^45}",140,75,anchor=tk.W)
    search()

        #print(f'{list(info).index(k)+1: <5}{k : ^15}{info[k][0] : ^10}{info[k][1] : ^10}{info[k][2] : ^25}')


view_inv()
G.root.mainloop()
