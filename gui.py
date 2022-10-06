from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import movieProj, csv
from PIL import ImageTk, Image

#global reviewFile, listFile, posterFolder, graphicFolder
reviewFile = ""
listFile = ""
posterFolder = ""
graphicFolder = ""

def getReviews():
    global reviewFile
    reviewFile = filedialog.askopenfilename(#initialdir = "/",
                                          title = "Select Review File",
                                          filetypes = (("CSV files",
                                                        "*.csv*"),
                                                       ("all files",
                                                        "*.*")))
      
    # Change label contents
    #print(reviewFile)
    if (reviewFile != ""):
        label_reviews.configure(text="Review File: " + reviewFile.split("/")[-1])
    checkGenerate()

def getList():
    global listFile
    listFile = filedialog.askopenfilename(#initialdir = "/",
                                          title = "Select List File",
                                          filetypes = (("CSV files",
                                                        "*.csv*"),
                                                       ("all files",
                                                         "*.*")))
    if (listFile != ""):
        label_list.configure(text="List File: " + listFile.split("/")[-1])
    checkGenerate()

def getPosterFolder():
    global posterFolder
    posterFolder = filedialog.askdirectory()
      
    if (posterFolder != ""):
        label_posters.configure(text="Poster Folder: " + posterFolder.split("/")[-1])
    checkGenerate()

def getGraphicFolder():
    global graphicFolder
    graphicFolder = filedialog.askdirectory()
      
    if (graphicFolder != ""):
        label_graphics.configure(text="Graphics Folder: " + graphicFolder.split("/")[-1])
    checkGenerate()

def cbPosterClick():
    if cbPoster.get():
        cb_graphics.config(state = ACTIVE)
    else:
        cbGraphic.set(0)
        cb_graphics.config(state = DISABLED)

def cbOverrideClick():
    if cbOverride.get():
        entry_overrideValue.config(state = NORMAL)
    else:
        entOverrideValue.set("0")
        entry_overrideValue.config(state = DISABLED)

def checkGenerate():
    if (reviewFile != "" and listFile != "" and posterFolder != "" and graphicFolder != ""):
        button_generate.config(state = ACTIVE)
        button_preview.config(state = ACTIVE)
    else:
        button_generate.config(state = DISABLED)
        button_preview.config(state = DISABLED)

def generate():
    global generating, numGen

    if cbOverride.get():
        try:
            numGen = int(entry_overrideValue.get())
        except:
            top = Toplevel(root)
            top.geometry("200x50")
            top.title("Error!")
            Label(top, text = "Invalid number of entries!", anchor = "center").pack(expand = True)
            return
    else:
        numGen = 9999999
    
    generating = True
    
    if (not (reviewFile != "" and listFile != "" and posterFolder != "" and graphicFolder != "")):
        button_generate.config(state = DISABLED)
        return
    
    data = movieProj.loadData(listFile, reviewFile)

    if(sortStr.get() == "Sort by date"):
       data.sort(key=lambda x: x[5])
    elif(sortStr.get() == "Sort by score (asc)"):
       data.sort(key=lambda x: x[2])
    elif(sortStr.get() == "Sort by score (dec)"):
       data.sort(key=lambda x: x[2], reverse = True)
    elif(sortStr.get() == "Sort by Title"):
       data.sort(key=lambda x: x[0])
    elif(sortStr.get() == "Sort by list order"):
       pass

    #print(data[-5:-1])
    
    if(cbPoster.get()):
        i = 0
        for link in data:
            if(not cbOverride.get() or i < numGen):
                if (data[i][0] != ""):
                    print("Generating <" + str(data[i][0]) + ">" + " (" + str(i) + ")")
                    movieProj.downloadImg(link, i, posterFolder + "/") #Download images
                    if(cbGraphic.get()):
                        movieProj.generateGraphic(data, i, posterFolder + "/", graphicFolder + "/") #Generate Graphics
                    root.update()
                    if (not generating):
                        return
            i += 1

def preview():
    i = 0
    data = movieProj.loadData(listFile, reviewFile)
    movieProj.downloadImg(data[i], i, posterFolder + "/")
    movieProj.generateGraphic(data, i, posterFolder + "/", graphicFolder + "/")
    
    img = ImageTk.PhotoImage(Image.open(graphicFolder + "/" + str(i) + ".jpg"))
    
    top = Toplevel(root)
    #top.geometry("1000x1000")
    top.title("Image")
    l = Label(top, image = img)
    l.pack()

    top.mainloop()

def quitGui():
    global generating
    generating = False
    root.destroy()
    

root = Tk()
root.title("Kyle's Movie Visualizer")
root.geometry("500x300+400+300")
root.resizable(False, False)
topFrame = Frame(root)
topFrame.pack(side = TOP)

cbFrame = Frame(root)
cbFrame.pack(padx = (10, 10), side = RIGHT)

loadFrame = Frame(root)
loadFrame.pack(padx = (10, 10))

bottomFrame = Frame(root)
bottomFrame.pack(side = BOTTOM, pady = (10, 10))

cbPoster = IntVar(master=root, value=0)
cbGraphic = IntVar(master=root, value=0)
cbOverride = IntVar(master=root, value=0)
entOverrideValue = StringVar(master = root, value="0")

sortOptions = ["Sort by list order", "Sort by Title", "Sort by score (asc)", "Sort by score (dec)", "Sort by date"]
sortStr = StringVar()
sortStr.set(sortOptions[0])

label_title =     Label(
                            topFrame,
                            text = "Kyle's Movie Visualizer",
                            width = 30,
                            height = 3,
                            borderwidth=1,
                            font = ("Arial", 15),
                            fg = "black")

label_reviews =     Label(
                            loadFrame,
                            text = "<Select a File>",
                            width = 100,
                            height = 2,
                            borderwidth=1,
                            fg = "blue",
                            anchor="w")

label_list =        Label(
                            loadFrame,
                            text = "<Select a File>",
                            width = 100,
                            height = 2,
                            borderwidth=1,
                            fg = "blue",
                            anchor="w")

label_posters =        Label(
                            loadFrame,
                            text = "<Select a Folder>",
                            width = 100,
                            height = 2,
                            borderwidth=1,
                            fg = "blue",
                            anchor="w")

label_graphics =        Label(
                            loadFrame,
                            text = "<Select a Folder>",
                            width = 100,
                            height = 2,
                            borderwidth=1,
                            fg = "blue",
                            anchor="w")

button_reviews =        Button(
                            loadFrame,
                            text = "Select Reviews File",
                            command = getReviews,
                            width = 15)

button_list =           Button(
                            loadFrame,
                            text = "Select List File",
                            command = getList,
                            width = 15)

button_poster =         Button(
                            loadFrame,
                            text = "Select Poster Folder",
                            command = getPosterFolder,
                            width = 15)

button_graphic =        Button(
                            loadFrame,
                            text = "Select Graphic Folder",
                            command = getGraphicFolder,
                            width = 15)

button_exit =           Button(
                            bottomFrame,
                            text="Quit",
                            command=quitGui)

button_generate =       Button(
                            bottomFrame,
                            text="Generate",
                            state = DISABLED,
                            command = generate)

button_preview =        Button(
                            bottomFrame,
                            text="Preview",
                            state = DISABLED,
                            command = preview)

cb_posters =            Checkbutton(
                            cbFrame,
                            text='Download Posters',
                            variable = cbPoster,
                            command = cbPosterClick,
                            width = 15,
                            anchor="w")

cb_graphics =           Checkbutton(
                            cbFrame,
                            text='Generate Graphics',
                            state = DISABLED,
                            variable = cbGraphic,
                            width = 15,
                            anchor="w")

cb_override =           Checkbutton(
                            cbFrame,
                            text='Override Count',
                            variable = cbOverride,
                            command = cbOverrideClick,
                            width = 15,
                            anchor = "w")

drop_option =           OptionMenu(cbFrame,
                                   sortStr,
                                   *sortOptions)

entry_overrideValue =   Entry(cbFrame,
                              state = DISABLED,
                              textvariable = entOverrideValue)

label_title.grid(column = 0, row = 0)

button_reviews.grid(column = 0, row = 0)
button_list.grid(column = 0, row = 1)
button_poster.grid(column = 0, row = 2)
button_graphic.grid(column = 0, row = 3)


button_preview.grid(column = 0, row = 1)
button_generate.grid(column = 1, row = 1)
button_exit.grid(column = 2, row = 1)

label_reviews.grid(column = 1, row = 0)
label_list.grid(column = 1, row = 1)
label_posters.grid(column = 1, row = 2)
label_graphics.grid(column = 1, row = 3)

cb_posters.grid(column = 0, row = 0)
cb_graphics.grid(column = 0, row = 1)
cb_override.grid(column = 0, row = 2)
entry_overrideValue.grid(column = 0, row = 3)

drop_option.grid(column = 0, row = 4)

#Kyle Default
reviewFile = "reviews.csv"
listFile = "kyle-watches-a-movie-every-day-in-2022.csv"
posterFolder = "IMAGES"
graphicFolder = "GRAPHICS"
checkGenerate() #Kyle Default

root.mainloop()
