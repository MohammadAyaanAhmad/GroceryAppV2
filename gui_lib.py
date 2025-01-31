import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
root = tk.Tk()
def createCanvas():
    global canvas
    canvas = tk.Canvas(root, width = 1280, height = 600, highlightthickness = 0)
    canvas.place(x = 0, y = 0)
    canvas.photos = []
 
def c(num):
    return num*(w/1920)
createCanvas()
#functions
    
def image(file,x,y,rw,rh,canvas=canvas):
    image = Image.open(file)
    resizeImage = image.resize((rw,rh))
    img = ImageTk.PhotoImage(resizeImage)
    canvas.photos.append(img)
    canvas.create_image(x,y, image= img)
    

def text(text, x, y, col = 'white', size = 15, font = 'Consolas', anchor = tk.CENTER,canvas=canvas):
    font =(font, int(size))
                     
    text_ = canvas.create_text(x, y, text = text, fill = col, font = font,   anchor = anchor)
    return text_
    
def dropDown(text, opt, x, y, col = 'white', bg_col = '#232328',canvas=canvas):
    menu = tk.StringVar()
    menu.set(text) 
    drop = tk.OptionMenu(canvas, menu,*opt)
    drop.config(bg = bg_col, fg=col, width = 30)
    drop['highlightthickness']=0  
    drop['menu'].config(bg = bg_col, fg=col,activebackground=bg_col)  
    drop.place(x=x,y=y)

def button(text, x, y,h,w,command, col = 'white', bg_col = '#232328',font='Consolas',canvas=canvas):
        pixel = tk.PhotoImage(width=1, height=1)
        canvas.photos.append(pixel)
        font =(font, int(15))
        h,w = h,w
        
        button = tk.Button(canvas, text = text,command = command,image=pixel,compound='c',relief='flat')
        button.config(background = bg_col, fg = col, font=font,height=h,width=w)
        buttonWindow = canvas.create_window(x, y,  window=button,anchor=tk.NW)
        return  button

def imgButton(buttonImage,x,y,command,canvas=canvas):
        button = tk.Button(canvas, image=buttonImage,command = command)
        button['background'] = '#0e1342'
        buttonWindow = canvas.create_window(x*(w/1920), y*(w/1920), anchor=tk.NW, window=button)
        
def inputBox(x, y, w,s,col = 'white', bg_col = '#232328', val='',font='Consolas', j = 'center',canvas=canvas):
    font = (font,int(s))
    entry = tk.Entry(canvas, borderwidth=2,bg = bg_col, fg = col, justify =j,width=int(w),font=font,relief='sunken')
    entry.insert(0,str(val))
    entryWindow = canvas.create_window(x, y,  window=entry,anchor=tk.NW)
    return entry

class numEntry(tk.Entry):
    def __init__(self, master=None, **kwargs):
        self.var = tk.StringVar()
        tk.Entry.__init__(self, master, textvariable=self.var, **kwargs)
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
            
def notif(text,canvas=canvas):
    nlabel = tk.Label(text=text)
    nlabel.configure(font=('Consolas', 18),bg='#000000',fg='white')
    notifWindow = canvas.create_window(cenx, 865, window= nlabel, anchor= tk.CENTER)
    root.after(3000, lambda: nlabel.destroy())

def scroll(span,canvas=canvas):
    bar=ttk.Scrollbar(root,command=canvas.yview, orient=tk.VERTICAL)
    bar.place(relx=0.99, height = span)
    canvas.configure(yscrollcommand=bar.set)
    canvas.configure(yscrollcommand=bar.set)
    canvas.configure(scrollregion=canvas.bbox("all"))

