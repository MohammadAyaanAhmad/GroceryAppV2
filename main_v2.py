#importing libraries
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import pickle
import mysql.connector as sql_con
con = sql_con.connect(host="localhost", username="root", passwd="AsteroidImpact000",database="Bill")
cur=con.cursor()
SQL = "TRUNCATE TABLE BillInfo;"
cur.execute(SQL)
con.commit()
#creating window

root = tk.Tk()
h = root.winfo_screenheight()
w = root.winfo_screenwidth()

root.geometry(str(w)+'x'+str(h))
root.title('')
root.grid_anchor('center')
root.resizable(False,False)
cenx=w/2
ceny=h/2
style = ttk.Style()
style.theme_use('default')
style.configure('TButton', background='#db500b')
money=0
bh,bw=33,33
print(root.winfo_screenwidth())

#canvas
def createCanvas():
    global canvas
    canvas = tk.Canvas(root, width = w, height = h, highlightthickness = 0)
    canvas.place(x = 0, y = 0)
    canvas['background']= '#f0e3c0'
    canvas.create_rectangle(0,0,1920,220, fill='#0e1342')
    canvas.photos = []
    
createCanvas()

def c(num):
    return num*(w/1920)

#functions
    
def image(file,x,y,rw,rh):
    image = Image.open(file)
    resizeImage = image.resize((rw,rh))
    img = ImageTk.PhotoImage(resizeImage)
    canvas.photos.append(img)
    canvas.create_image(x,y, image= img)
    

def text(text, x, y, col = 'white', size = 15, font = 'Consolas', anchor = tk.CENTER):
    font =(font, int(size))
                     
    text_ = canvas.create_text(x, y, text = text, fill = col, font = font,   anchor = anchor)
    return text_
    
def dropDown(text, opt, x, y, col = 'white', bg_col = '#232328'):
    menu = tk.StringVar()
    menu.set(text) 
    drop = tk.OptionMenu(canvas, menu,*opt)
    drop.config(bg = bg_col, fg=col, width = 30)
    drop['highlightthickness']=0  
    drop['menu'].config(bg = bg_col, fg=col,activebackground=bg_col)  
    drop.place(x=x,y=y)

def button(text, x, y,h,w,command, col = 'white', bg_col = '#232328',font='Consolas'):
        pixel = tk.PhotoImage(width=1, height=1)
        canvas.photos.append(pixel)
        font =(font, int(15))
        h,w = h,w
        
        button = tk.Button(canvas, text = text,command = command,image=pixel,compound='c', relief ='ridge')
        button.config(background = bg_col, fg = col, font=font,height=h,width=w)
        buttonWindow = canvas.create_window(x, y,  window=button,anchor=tk.NW)
        

def imgButton(buttonImage,x,y,command):
        button = tk.Button(canvas, image=buttonImage,command = command, relief = 'flat')
        button['background'] = '#0e1342'
        buttonWindow = canvas.create_window(x*(w/1920), y*(w/1920), anchor=tk.NW, window=button)
        
def inputBox(x, y, w,s,col = 'white', bg_col = '#232328', val='',font='Consolas', j = 'center'):
    font = (font,int(s))
    entry = tk.Entry( borderwidth=2,bg = bg_col, fg = col, justify =j,width=int(w),font=font,relief='flat')
    entry.insert(0,str(val))
    entryWindow = canvas.create_window(x, y,  window=entry,anchor=tk.NW)
    return entry

class numEntry(tk.Entry):
    def __init__(self, master=None, **kwargs):
        self.var = tk.StringVar()
        tk.Entry.__init__(self, master, textvariable=self.var,relief='flat', **kwargs)
        self.old_value = ''
        self.var.trace('w', self.check)
        self.get, self.set = self.var.get, self.var.set

    def check(self, *args):
        if self.get().isdigit(): 
            # the current value is only digits; allow this
            self.old_value = self.get()
        else:
            # there's non-digit characters in the input; reject this 
            self.set(self.old_value)
            
def notif(text):
    nlabel = tk.Label(text=text)
    nlabel.configure(font=('Consolas', 18),bg='#000000',fg='white')
    notifWindow = canvas.create_window(cenx, 865, window= nlabel, anchor= tk.CENTER)
    root.after(3000, lambda: nlabel.destroy())

def scroll():
    bar=ttk.Scrollbar(root,command=canvas.yview, orient=tk.VERTICAL)
    bar.place(relx=0.99, height = 1080)
    canvas.configure(yscrollcommand=bar.set)
    canvas.configure(yscrollcommand=bar.set)
    canvas.configure(scrollregion=canvas.bbox("all"))
#logic
f = open('details.txt','rb')
info = pickle.load(f)

user_selections = {}
def addCart(item, quantity):
    if quantity.isdigit() and int(quantity) > 0:
        if int(quantity)<= info[item][0]:
             
            user_selections[item] = int(quantity)
            notif(str(quantity) + ' kg of ' + str(item)+' added to the cart.')
        else:
            notif("Sorry, the requested amount exceeds the stock, the available stock is " + str(menu[item][0])+" kg.")
        
    else:
        notif("Please enter a valid quantity!")


def removeCart(item):
    user_selections.pop(item)
    notif(item+ 'removed from cart.')
    cartScreen()
def calc():
    total_price = 0
    for item,quantity in user_selections.items():

                price = info[item][1] * quantity
                total_price += price
    notif('The total price is: ₹'+str(total_price))
    return (str(total_price))
def add(entryWidget):
    n = entryWidget.get()
    entryWidget.delete(0,len(n))
    entryWidget.insert(0,str(int(n)+1))
def sub(entryWidget):
    n = entryWidget.get()
    entryWidget.delete(0,len(n))
    entryWidget.insert(0,str(int(n)-1))
#components
def itemBox(boxText,x,y):
    canvas.create_rectangle(x,y,x+315,y+385,outline='#a1a1a1',width='3')
    text(boxText,x+157.5,y+288.75,size=30,col ="#1e1433")
    text('₹'+str(int(info[boxText][1]))+' per kg',x+157.5,y+315,size=10,col ="#1e1433")
    text('Available stock: '+str(int(info[boxText][0]))+' kg',x+157.5,y+330,size=10,col ="#1e1433")
    fileName = 'Assets\\'+boxText+'.jpg'
    image(fileName,x+157.5,y+136.5,306,262)
    canvas.create_rectangle(x+5.25,y+264.25,x+313.25,y+267.5,outline='#4a4a4a',fill='#4a4a4a')
    boxQuantity = inputBox(x+52.5,y+341.25,2,24,val=0)
    button('+',x+14,y+341.25,bh,bw,lambda: add(boxQuantity), font='Consolas 16 bold',bg_col="#019404")
    button('-',x+91,y+341.25,bh,bw,lambda: sub(boxQuantity), font='Consolas 16 bold',bg_col="#db000b")
    button('Add to Cart',x+185,y+341,bh,115,lambda: addCart(boxText,boxQuantity.get()),bg_col="#3d1ab0",font = 'Consolas 11 bold')

def cartBox(item,y):
    fileName = 'Assets\\'+item+'.jpg'
    price = int(info[item][1]* user_selections[item])
    image(fileName,c(100)+96.5,y+85.5,193,169)   
    canvas.create_rectangle(c(100),y,w-c(100),y+172.5,outline='#a1a1a1',width='4')
    text(item, 310, y+5, size=30, anchor=tk.NW,col='black')
    text('Quantity:', 310,y+80,size=14,anchor=tk.NW,col='black')
    price = text('₹'+str(price),1800,y+20,size=25,anchor=tk.NE,col='black')
    boxQuantity = inputBox(359,y+115,2,24,val=user_selections[item])
    def addr():
        global money, total_price
        add(boxQuantity)       
        if boxQuantity.get().isdigit() and int(boxQuantity.get()) > 0:
            user_selections[item] = int(boxQuantity.get())
            notif('1 more kg of ' + str(item)+' added to the cart.')
        else:
            notif("Please enter a valid quantity!")
        canvas.itemconfig(price, text = '₹'+str(int(info[item][1]* user_selections[item])))
        canvas.itemconfig(money, text='Total price: ₹'+calc())
        cartScreen()
    def subr():
        sub(boxQuantity)
        if boxQuantity.get()=="0":
            removeCart(item)
            return
        elif boxQuantity.get().isdigit() and int(boxQuantity.get()) > 0:
            user_selections[item] = int(boxQuantity.get())
            notif('1 kg of ' + str(item)+' removed from the cart.')
        else:
            notif("Please enter a valid quantity!")
            
        canvas.itemconfig(price, text = '₹'+str(int(info[item][1]* user_selections[item])))
        canvas.itemconfig(money, text='Total price: ₹'+calc())
        cartScreen()
    button('+',316,y+115,35,35,addr,bg_col='#0e1342', font='Consolas 16 bold')
    button('-',400,y+115,35,35,subr,bg_col='#0e1342', font='Consolas 16 bold')
    button('Remove', 1650,y+115,35,130, lambda: removeCart(item),bg_col='red', font='Consolas 7 bold',col='white')

#pages

def homeScreen():
    createCanvas()
    text("Groceries", cenx, 55, '#dbbe7b', 75, font='Lucida Handwriting')
    text("Fresh fruits and veggies at your doorstep!", cenx, 140, size = 25,font='Lucida Sans')
    cartImage = Image.open('Assets\Cart.png')
    resizeCartImage = cartImage.resize((100,100))
    img = ImageTk.PhotoImage(resizeCartImage)
    canvas.photos.append(img)
    imgButton(img,1750,50,cartScreen)
    #boxes per row
    bpr = root.winfo_screenwidth()//315
    boxx= -10+(w - 315*bpr)/2
    boxy=230
    count = 0
    boxes = len(info)

    #for key,values in info.items():
    for key in info:
        itemBox(key,boxx,boxy)
        boxx+= 315
        count+=1
        boxes -= 1
        if count==bpr:
            if boxes < bpr :
                bpr = boxes
            boxx= -10+(w - 315*bpr)/2
            boxy+=420
            count = 0

    
    text('',6,boxy+50)
    scroll()
def delivScreen():
    createCanvas()
    x_ = 480*(w/1920)
    x__ = x_ + 600*(w/1920)
    #modifying details.txt, creating table

    text("Delivery", cenx, 100, '#dbbe7b', 75, font='Lucida Handwriting')
    m=calc()
    text("First Name: ",x_,330 , 'black',anchor=tk.W)
    firstname = inputBox(x_, 350,25,20, col ="Black", bg_col= 'White', j='left')
    text("Last Name: ",x_,430 , 'black',anchor=tk.W)
    lastname = inputBox(x_, 450,25,20, col ="Black", bg_col= 'White', j='left')
    text("Phone: ",x_,530,'black',anchor=tk.W)
    phone = numEntry( borderwidth=2,bg = 'white', fg = 'black',width=25,font='Consolas 20')
    phoneWindow = canvas.create_window(x_,550,  window=phone,anchor=tk.NW)
    text("Email: ",x_,630,'black',anchor=tk.W)
    email = inputBox(x_, 650,25,20, col ="Black", bg_col= 'White', j='left')

    text('Home Address:', x__, 330, col = "Black",anchor=tk.W)
    address  = inputBox(x__, 350,25,20, col ="Black", bg_col= 'White', j='left')
    text('City:', x__, 430, col = "Black",anchor=tk.W)
    address  = inputBox(x__, 450,25,20, col ="Black", bg_col= 'White', j='left')
    text('State/UT:', x__, 530, col = "Black",anchor=tk.W)
    states =["Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu","Lakshadweep","National Capital Territory of Delhi","Puducherry"]
    dropDown('State/UT', states, x__,550, col="Black", bg_col="White")
    text("ZIP Code: ",x__,630,'black',anchor=tk.W)
    zip_ = numEntry( borderwidth=2,bg = 'white', fg = 'black',width=25,font='Consolas 20')
    zipWindow = canvas.create_window(x__,650,  window=zip_,anchor=tk.NW)
    def generateBill():
        f = open('details.txt','rb')
        info = pickle.load(f)
        f.close()
        srn = 1
        for name, qty in user_selections.items():
            price = info[name][1]
            t_price = price*qty
            SQL = "INSERT INTO BillInfo VALUES( {} , '{}' , {} , {} , {} );".format( str(srn), name, str(qty), str(price), str(t_price) )
            cur.execute(SQL)
            con.commit()
            srn += 1
            info[name][0] = info[name][0] - qty
            if info[name][0]<20:
                info[name][2] = 'Low Stock, Resupply'
            else:
                info[name][2] = 'Sufficient Stock'
            f = open('details.txt','wb')
            pickle.dump(info,f)
            f.close()
            billScreen()
    confirmPurchase = button("Confirm Purchase", (w/1920)*840, 750, 30, 300, generateBill,col ="Black", bg_col= 'White')
def cartScreen():
    
    createCanvas()
    
    text("Your Cart", cenx, 55, '#dbbe7b', 75, font='Lucida Handwriting')
    boxy=230
    count = 0

    
    
    for key in user_selections:
        cartBox(key,boxy)
        boxy+=230
      
    text('Total:'+calc(),100,boxy+50,col='black')
    button('Proceed',100,boxy+120,bg_col='cyan',col='white',h=40,w=130,command=delivScreen)
    button('Back',c(100),50,bg_col='red',col='white',h=40,w=130,command=homeScreen)
    text('',6,boxy+200)
    scroll()
    print(user_selections)

def billScreen():
    createCanvas()
    text("Bill", cenx, 55, '#dbbe7b', 75, font='Lucida Handwriting')
    y = 500
    SQL = "SELECT * FROM BillInfo"
    cur.execute (SQL)
    table = cur.fetchall()

    text(f"{'Sno' : <5}{'Item_Name' : ^15}{'Quantity' : ^10}{'Price' : ^10}{'Total Price' : ^15}",cenx, 400,size=18,col='Black',font='Monospace')
    for sno,name,qty,price,t_price in table :  #yaha par apne hisaab se print krwa lena
        text(f"{sno : <5}{name : ^15}{qty : ^10}{price : ^10}{t_price : ^15}",cenx, y,col='Black',font='Monospace',size=18)
        y+=50
    canvas.create_rectangle(cenx-400,350,cenx+400,y)
    text('',6,y+200)
    scroll()
homeScreen()
root.mainloop()
