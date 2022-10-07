from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import movieProj, csv
from PIL import ImageTk, Image
from tkinter.colorchooser import askcolor

reviewFile = ""
listFile = ""
posterFolder = ""
graphicFolder = ""
colorList = ["blue", "grey", "yellow"]

def getReviews(): #Get CSV file for the list of 
    global reviewFile
    reviewFile = filedialog.askopenfilename(#initialdir = "/",
                                          title = "Select Review File",
                                          filetypes = (("CSV files",
                                                        "*.csv*"),
                                                       ("all files",
                                                        "*.*")))
      
    # Change label contents
    if (reviewFile != ""):
        label_reviews.configure(text="Review File: " + reviewFile.split("/")[-1])
    checkGenerate()

def getList():  #Get CSV file for the list of movies to be included
    global listFile
    listFile = filedialog.askopenfilename(#initialdir = "/",
                                          title = "Select List File",
                                          filetypes = (("CSV files",
                                                        "*.csv*"),
                                                       ("all files",
                                                         "*.*")))
    #Change label contents
    if (listFile != ""):
        label_list.configure(text="List File: " + listFile.split("/")[-1])
    checkGenerate()

def getPosterFolder(): #Get folder to output files
    global posterFolder
    posterFolder = filedialog.askdirectory()

    #Change Label Contents
    if (posterFolder != ""):
        label_posters.configure(text="Poster Folder: " + posterFolder.split("/")[-1])
    checkGenerate()

def getGraphicFolder():
    global graphicFolder, posterFolder
    graphicFolder = filedialog.askdirectory()
    if (graphicFolder != ""):
        if (not cbPosterFolder.get()):
            posterFolder = graphicFolder
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
        entry_overrideValue.grid(column = 0, row = 4)
        entry_overrideValue.config(state = NORMAL)
    else:
        entry_overrideValue.grid_remove()
        entOverrideValue.set("0")
        entry_overrideValue.config(state = DISABLED)

def cbPosterFolderClick():
    global graphicFolder, posterFolder
    if cbPosterFolder.get():
        posterFolder = ""
        button_poster.grid(column = 0, row = 3)
        button_poster.config(state = ACTIVE)
        label_posters.config(text = "<Select Poster Folder>")
    else:
        posterFolder = graphicFolder
        button_poster.grid_remove()
        button_poster.config(state = DISABLED)
        label_posters.config(text = "")
        

def checkGenerate():
    if (reviewFile != "" and listFile != "" and posterFolder != "" and graphicFolder != ""):
        button_generate.config(state = ACTIVE)
        button_preview.config(state = ACTIVE)
    else:
        button_generate.config(state = DISABLED)
        button_preview.config(state = DISABLED)

def getTopColor():
    global colorList
    colorList[0] = askcolor(title = "Choose Title Backround Color")[0]

def getScoreColor():
    global colorList
    colorList[1] = askcolor(title = "Choose Score Backround Color")[0]

def getReviewColor():
    global colorList
    colorList[2] = askcolor(title = "Choose Review Backround Color")[0]
    
def generate():
    global generating, numGen, colorList
    generating = False #End other proccess while new data loads
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
        numGen = -1
    
    if (not (reviewFile != "" and listFile != "" and posterFolder != "" and graphicFolder != "")):
        button_generate.config(state = DISABLED)
        return
    
    data = movieProj.loadData(listFile, reviewFile)
    if (numGen == -1):
        numGen = len(data)

    if(sortStr.get() == "Sort by date"): #Sort data based off dropdown (drop_option)
       data.sort(key=lambda x: x[5])
    elif(sortStr.get() == "Sort by score (asc)"):
       data.sort(key=lambda x: x[2])
    elif(sortStr.get() == "Sort by score (dec)"):
       data.sort(key=lambda x: x[2], reverse = True)
    elif(sortStr.get() == "Sort by Title"):
       data.sort(key=lambda x: x[0])
    elif(sortStr.get() == "Sort by list order"):
       pass

    generating = True
    progress['value'] = 0
    progress.grid(column = 0, row = 0)
    button_terminate.grid(column = 1, row = 0, padx = (10, 10))
    
    if(cbPoster.get()): #Proccess Loop
        i = 0
        for link in data:
            try:
                progress['value'] = i / numGen * 100
            except:
                pass
            root.update()
            root.update_idletasks()
            if (not generating):
                        try:
                            button_terminate.grid_remove()
                            progress.grid_remove()
                        except:
                            pass
                        return
            if(not cbOverride.get() or i < numGen):
                if (data[i][0] != ""):
                    print("Generating <" + str(data[i][0]) + ">" + " (" + str(i) + ")")
                    movieProj.downloadImg(link, i, posterFolder + "/") #Download images
                    if(cbGraphic.get()):
                        movieProj.generateGraphic(data, i, posterFolder + "/", graphicFolder + "/", colors = colorList) #Generate Graphics

            i += 1
            
    button_terminate.grid_remove()
    progress.grid_remove()

def preview():
    i = 0
    data = movieProj.loadData(listFile, reviewFile, singular = 0)
    movieProj.downloadImg(data[i], i, posterFolder + "/")
    movieProj.generateGraphic(data, i, posterFolder + "/", graphicFolder + "/", colors = colorList)

    jpgImage = Image.open(graphicFolder + "/" + str(i) + ".jpg")
    jpgImage.thumbnail((200,200))
    
    img = ImageTk.PhotoImage(jpgImage)
    top = Toplevel(root)
    top.resizable(False, False)
    top.title("Image")
    l = Label(top, image = img)
    l.pack()

    top.mainloop()

def terminate():
    global generating
    generating = False

def quitGui():
    global generating
    generating = False
    root.destroy()
    
#Generate Root
root = Tk()
root.title("Kyle's Movie Visualizer")
root.geometry("500x300+400+300")
root.resizable(False, False)

#Generate Frames
topFrame = Frame(root) #Top frame (title)
topFrame.pack(side = TOP)

bottomFrame = Frame(root) #Bottom frame (buttons)
bottomFrame.pack(side = BOTTOM, pady = (10, 10))

progressFrame = Frame(root) #Second to bottom frame (progress bar)
progressFrame.pack(side = BOTTOM, pady = (10, 10))

cbFrame = Frame(root) #Right frame (options)
cbFrame.pack(padx = (10, 10), side = RIGHT)

loadFrame = Frame(root, width = 5) #Left frame (data)
loadFrame.pack(padx = (10, 10), side = LEFT)

cbPoster = IntVar(master=root, value=0)
cbGraphic = IntVar(master=root, value=0)
cbOverride = IntVar(master=root, value=0)
cbPosterFolder = IntVar(master=root, value=0)
entOverrideValue = StringVar(master = root, value="0")

sortOptions = ["Sort by list order", "Sort by Title", "Sort by score (asc)", "Sort by score (dec)", "Sort by date"]
sortStr = StringVar()
sortStr.set(sortOptions[0])

#Generate Elements
label_title =           Label(
                            topFrame,
                            text = "Kyle's Movie Visualizer",
                            width = 30,
                            height = 3,
                            borderwidth=1,
                            font = ("Arial", 15),
                            fg = "black")

label_reviews =         Label(
                            loadFrame,
                            text = "<Select a File>",
                            width = 30,
                            height = 2,
                            borderwidth=1,
                            fg = "blue",
                            anchor="w")

label_list =            Label(
                            loadFrame,
                            text = "<Select a File>",
                            width = 30,
                            height = 2,
                            borderwidth=1,
                            fg = "blue",
                            anchor="w")

label_posters =         Label(
                            loadFrame,
                            width = 30,
                            height = 2,
                            borderwidth=1,
                            fg = "blue",
                            anchor="w")

label_graphics =        Label(
                            loadFrame,
                            text = "<Select a Folder>",
                            width = 30,
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
                            state = DISABLED,
                            width = 15)

button_graphic =        Button(
                            loadFrame,
                            text = "Select Graphic Folder",
                            command = getGraphicFolder,
                            width = 15)

button_topColor =       Button(
                            loadFrame,
                            text="Select Header Color",
                            command = getTopColor,
                            width = 15)

button_scoreColor =     Button(
                            loadFrame,
                            text="Select Score Color",
                            command = getScoreColor,
                            width = 15)

button_reviewColor =       Button(
                            loadFrame,
                            text="Select Review Color",
                            command = getReviewColor,
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

button_terminate =      Button(
                            progressFrame,
                            text="Terminate Proccess",
                            command = terminate)

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

cb_posterFolder =       Checkbutton(
                            cbFrame,
                            text='Seperate Posters',
                            variable = cbPosterFolder,
                            command = cbPosterFolderClick,
                            width = 15,
                            anchor = "w")

drop_option =           OptionMenu(cbFrame,
                                   sortStr,
                                   *sortOptions)

entry_overrideValue =   Entry(
                            cbFrame,
                            state = DISABLED,
                            textvariable = entOverrideValue)

progress =              ttk.Progressbar(
                            progressFrame,
                            orient = HORIZONTAL,
                            length = 100,
                            mode = 'determinate')

#Place Elements
label_title.grid(column = 0, row = 0)

button_reviews.grid(column = 0, row = 0)
button_list.grid(column = 0, row = 1)
#button_poster.grid(column = 0, row = 3)
button_graphic.grid(column = 0, row = 2)

button_topColor.place(x=210,y=5)
button_scoreColor.place(x=210,y=35)
button_reviewColor.place(x=210,y=70)

#button_terminate.grid(column = 0, row = 1)
#progress.grid(column = 0, row = 0)

button_preview.grid(column = 0, row = 1)
button_generate.grid(column = 1, row = 1)
button_exit.grid(column = 2, row = 1)

label_reviews.grid(column = 1, row = 0)
label_list.grid(column = 1, row = 1)
label_posters.grid(column = 1, row = 3)
label_graphics.grid(column = 1, row = 2)

cb_posters.grid(column = 0, row = 0)
cb_graphics.grid(column = 0, row = 1)
cb_posterFolder.grid(column = 0, row = 2)
cb_override.grid(column = 0, row = 3)
#entry_overrideValue.grid(column = 0, row = 4)

drop_option.grid(column = 0, row = 5)

#Kyle Default
reviewFile = "reviews.csv"
listFile = "kyle-watches-a-movie-every-day-in-2022.csv"
#posterFolder = "IMAGES"
graphicFolder = "GRAPHICS"
posterFolder = graphicFolder
checkGenerate()

root.mainloop()
