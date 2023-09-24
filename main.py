from tkinter import *
from tkinter.ttk import Combobox
from tkinter import font
import os
from tkinter import colorchooser
from tkinter import filedialog,messagebox

#functionality
def change_theme(bg_color , fg_color):
    textarea.config(bg = bg_color , fg= fg_color)

def toolbarFunc():
    if show_toolbar.get()==False:
        tool_bar.pack_forget()
    else:
        textarea.pack_forget()
        tool_bar.pack(fill=X)
        textarea.pack(fill=BOTH,expand = True)

def statusbarFunc():
    if show_statusbar.get()==False:
        statusBar.pack_forget()
    else:
        statusBar.pack()



fontSize =  11
fontStyle = 'arial'

def find():
    #functionality
    def find_words():
        textarea.tag_remove('match',1.0,END)
        start_pos = '1.0'
        word = findentryField.get()
        if word:
            while True:
                start_pos = textarea.search(word,start_pos,stopindex=END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(word)}c"
                textarea.tag_add('match',start_pos,end_pos)
                textarea.tag_config('match',foreground='red',background='yellow')
                start_pos = end_pos
        else:
            pass

    def replace_text():
        word = findentryField.get()
        replace =replaceentryField.get()
        content = textarea.get(1.0,END)
        new_content = content.replace(word,replace)
        textarea.delete(0.0,END)
        textarea.insert(1.0,new_content)



    #gui
    root1 = Toplevel()
    root1.title('Find')
    root1.geometry('450x250+500+200')
    root.resizable(0,0)
    labelFrame = LabelFrame(root1,text='Find and Replace')
    labelFrame.pack(pady=30)
    findLabel = Label(labelFrame, text='Find')
    findLabel.grid(row=0, column=0, padx=5, pady=5)

    findentryField = Entry(labelFrame)
    findentryField.grid(row = 0 , column = 1,padx=5,pady=5)

    replaceLabel = Label(labelFrame, text='replace')
    replaceLabel.grid(row=2, column=0, padx=5, pady=5)
    replaceentryField = Entry(labelFrame)
    replaceentryField.grid(row=2, column=1, padx=5, pady=5)


    findButton = Button(labelFrame , text='FIND',command=find_words)
    findButton.grid(row=3,column=0,padx=5,pady=5)

    replaceButton = Button(labelFrame , text='REPLACE',command=replace_text)
    replaceButton.grid(row=3,column=1,padx=5,pady=5)

    def doSomething():
        textarea.tag_remove('match',1.0,END)
        root1.destroy()

    root1.protocol('WM_DELETE_WINDOW',doSomething)
    root1.mainloop()


def font_style(event):
    global fontStyle
    fontStyle = font_family_variable.get()
    textarea.config(font = (fontStyle , fontSize))

def font_size(event):
    global fontSize
    fontSize = size_variable.get()
    textarea.config(font=(fontStyle  , fontSize))

def bold_text():
    text_property = font.Font(font=textarea['font']).actual()
    if text_property['weight'] == 'normal':
        textarea.config(font=(fontStyle , fontSize , 'bold'))
    if text_property['weight'] == 'bold':
        textarea.config(font=(fontStyle , fontSize , 'normal'))


def italic_text():
    text_property = font.Font(font=textarea['font']).actual()
    if text_property['slant'] == 'roman':
        textarea.config(font=(fontStyle , fontSize , 'italic'))
    if text_property['slant'] == 'italic':
        textarea.config(font=(fontStyle , fontSize , 'roman'))

    print(text_property)
def underline_text():
    text_property = font.Font(font=textarea['font']).actual()
    if text_property['underline'] == 0:
        textarea.config(font=(fontStyle , fontSize , 'underline'))
    if text_property['underline'] == 1:
        textarea.config(font=(fontStyle , fontSize , 'normal'))

def color_select():
    color = colorchooser.askcolor()
    textarea.config(fg = color[1])

def align_right():
    data = textarea.get(0.0,END)
    textarea.tag_config('right',justify=RIGHT)
    textarea.delete(0.0, END)
    textarea.insert(INSERT,data,'right')

def align_left():
    data = textarea.get(0.0,END)
    textarea.tag_config('left',justify=LEFT)
    textarea.delete(0.0, END)
    textarea.insert(INSERT,data,'left')

def align_center():
    data = textarea.get(0.0,END)
    textarea.tag_config('center',justify=CENTER)
    textarea.delete(0.0, END)
    textarea.insert(INSERT,data,'center')

url = ''
def new_file():
    global url
    url = ''
    root.title('New File')
    textarea.delete(0.0,END)



def open_file():
    global url
    url = filedialog.askopenfilename(initialdir=os.getcwd , title='Select File' , filetypes=(('Text File' , 'txt'), ('All Files' , '*.*')))
    if url != '':
        f = open(url, "r")
        textarea.insert(0.0,f.read())
    root.title(os.path.basename(url))
    # url = ''

def save_file():

    if url == '':
        save_url = filedialog.asksaveasfile(mode= 'w' , defaultextension='.txt' , filetypes=(('Text File' , 'txt'), ('All Files' , '*.*')))
        content = textarea.get(0.0,END)
        save_url.write(content)
        save_url.close()
    else:
        content = textarea.get(0.0,END)
        f = open(url , 'w')
        f.write(content)
        # url = ''
def saveas_file():

    save_url = filedialog.asksaveasfile(mode='w', defaultextension='.txt',filetypes=(('Text File', 'txt'), ('All Files', '*.*')))
    content = textarea.get(0.0, END)
    save_url.write(content)
    save_url.close()
    if url != '':
        os.remove(url)
def iexit():
    if textarea.edit_modified():
        result = messagebox.askyesnocancel('Warning' , 'Do you want to save the file?')
        if result is True:
            if url != '':
                content = textarea(0.0 , END)
                f = open(url , 'w')
                f.write(content)
                f.close()
                root.destroy()
            else:
                content = textarea(0.0, END)
                save_url = filedialog.asksaveasfile(mode= 'w' , defaultextension='.txt' , filetypes=(('Text File' , 'txt'), ('All Files' , '*.*')))
                save_url.write(content)
                save_url.close()
                root.destroy()
        elif result is False:
            root.destroy()
        else:
            pass
    else:
        root.destroy()

def statusBarFunction(event):
    if textarea.edit_modified():
        words = len(textarea.get(0.0,END).split())
        characters = len(textarea.get(0.0,END).replace(' ',''))
        statusBar.config(text = f'Character : {characters} Words : {words}')
    textarea.edit_modified(False)

root = Tk()
root.title("Text Editor")
root.geometry("1500x700+0+0")
root.resizable(False, False)

menubar = Menu()
root.config(menu=menubar)

fileMenu = Menu(menubar, tearoff=False)
menubar.add_cascade(label="File", menu=fileMenu)

newImage = PhotoImage(file="images/new.png")
openImage = PhotoImage(file="images/open.png")
saveImage = PhotoImage(file="images/save.png")
save_asImage = PhotoImage(file="images/save_as.png")
exitImage = PhotoImage(file="images/exit.png")
fileMenu.add_command(label="New", accelerator='Ctrl+N', image=newImage, compound=LEFT , command = new_file)
fileMenu.add_command(label="Open", accelerator='Ctrl+O', image=openImage, compound=LEFT,command=open_file)
fileMenu.add_command(label="Save", accelerator='Ctrl+S', image=saveImage, compound=LEFT,command=save_file)
fileMenu.add_command(label="Save as", accelerator='Ctrl+Alt+S', image=save_asImage, compound= LEFT,command=saveas_file)
fileMenu.add_separator()
fileMenu.add_command(label="Quit", accelerator='Ctrl+Q', image=exitImage, compound=LEFT,  command=iexit)


# for item in fileMenu.winfo_children():
#     item.config(width=33)


editMenu = Menu(menubar, tearoff=False)
menubar.add_cascade(label="Edit", menu=editMenu)

cutImage = PhotoImage(file="images/cut.png")
copyImage = PhotoImage(file="images/copy.png")
pasteImage = PhotoImage(file="images/paste.png")
findImage = PhotoImage(file="images/find.png")
clear_allImage = PhotoImage(file="images/clear_all.png")


# for item in editMenu.winfo_children():
#     item.config(width=33)
show_toolbar = BooleanVar()
show_statusbar = BooleanVar()
statusImage = PhotoImage(file="images/status_bar.png")
toolImage = PhotoImage(file="images/tool_bar.png")
viewMenu = Menu(menubar , tearoff=False)
menubar.add_cascade(label="View" , menu=viewMenu)
viewMenu.add_checkbutton(label='Tool Bar', variable=show_toolbar, onvalue=True, offvalue=False, image=toolImage, compound=LEFT,command=toolbarFunc)
show_toolbar.set(True)
viewMenu.add_checkbutton(label='Status Bar', variable=show_statusbar, onvalue=True, offvalue=False, image=statusImage , compound=LEFT,command=statusbarFunc)
show_statusbar.set(True)
themesMenu = Menu(menubar , tearoff=False)
menubar.add_cascade(label='Themes', menu=themesMenu)
theme_choice = ""
light = PhotoImage(file='images/light_default.png')
dark = PhotoImage(file='images/dark.png')
pink = PhotoImage(file='images/red.png')
monokai = PhotoImage(file='images/monokai.png')
themesMenu.add_radiobutton(label='Light Default',image=light , variable=theme_choice, compound=LEFT,command=lambda: change_theme('white','black') )
themesMenu.add_radiobutton(label='Dark',image=dark , variable=theme_choice, compound=LEFT ,command=lambda: change_theme('gray20','white'))
themesMenu.add_radiobutton(label='Pink',image=pink , variable=theme_choice, compound=LEFT,command=lambda: change_theme('pink','blue') )
themesMenu.add_radiobutton(label='Monokai',image=monokai , variable=theme_choice, compound=LEFT ,command=lambda: change_theme('orange','white'))


#tool_bar section
tool_bar = Label(root)
tool_bar.pack(side=TOP, fill=X)

font_families = font.families()

font_family_variable = StringVar()
fontfamily_Combobox = Combobox(tool_bar, width=30, values=font_families,state='readonly',textvariable=font_family_variable)
fontfamily_Combobox.current(font_families.index('Arial'))
fontfamily_Combobox.grid(row=0, column=0 , padx = 5)
fontfamily_Combobox.bind('<<ComboboxSelected>>' , font_style)


size_variable = IntVar()

font_size_combobox = Combobox(tool_bar,width=14,textvariable=size_variable,state="readonly",values=tuple(range(8,81)) )
font_size_combobox.current(3)
font_size_combobox.bind('<<ComboboxSelected>>' , font_size)

font_size_combobox.grid(row= 0 , column = 1 , padx = 5)


# button section

boldImage = PhotoImage(file="images/bold.png")
boldButton = Button(tool_bar,image=boldImage,command=bold_text)
boldButton.grid(row = 0 , column = 2 , padx= 20)

italicImage = PhotoImage(file="images/italic.png")
italicButton = Button(tool_bar,image=italicImage,command=italic_text)
italicButton.grid(row = 0 , column = 3 , padx= 20)

underlineImage = PhotoImage(file="images/underline.png")
underlineButton = Button(tool_bar,image=underlineImage,command=underline_text)
underlineButton.grid(row = 0 , column = 4 , padx= 20)

font_colorImage = PhotoImage(file="images/font_color.png")
font_colorButton = Button(tool_bar,image=font_colorImage,command=color_select)
font_colorButton.grid(row = 0 , column = 5 , padx= 20)

leftImage = PhotoImage(file="images/left.png")
leftButton = Button(tool_bar,image=leftImage,command=align_left)
leftButton.grid(row = 0 , column = 6 , padx= 20)


centerImage = PhotoImage(file="images/center.png")
centerButton = Button(tool_bar,image=centerImage,command=align_center)
centerButton.grid(row = 0 , column = 7 , padx= 20)

rightImage = PhotoImage(file="images/right.png")
rightButton = Button(tool_bar,image=rightImage,command=align_right)
rightButton.grid(row = 0 , column = 8 , padx= 20)

scrollbar = Scrollbar(root)
scrollbar.pack(side = RIGHT , fill = Y)
textarea = Text(root , yscrollcommand=scrollbar.set , font=('arial',11 ))
textarea.pack(fill=BOTH , expand = True)



scrollbar.config(command=textarea.yview)




statusBar = Label(root , text='Status Bar')
statusBar.pack(side = BOTTOM)

textarea.bind('<<Modified>>' , statusBarFunction)


editMenu.add_cascade(label="Cut", accelerator="Ctrl+X", image=cutImage ,compound=LEFT,command=lambda : textarea.event_generate('<Control x>'))
editMenu.add_cascade(label="Copy", accelerator="Ctrl+C", image=copyImage ,compound=LEFT,command=lambda : textarea.event_generate('<Control c>'))
editMenu.add_cascade(label="Paste", accelerator="Ctrl+P", image=pasteImage ,compound=LEFT,command=lambda : textarea.event_generate('<Control v>'))
editMenu.add_cascade(label="Find", accelerator="Ctrl+H", image=findImage ,compound=LEFT , command=find)
editMenu.add_cascade(label="Clear", accelerator="Ctrl+Alt+H", image=clear_allImage ,compound=LEFT,command=lambda : textarea.delete(0.0,END))


root.mainloop()
