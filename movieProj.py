import requests, csv
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

def downloadImg(link, i, imageLoc):
    response = requests.get(link[4].split("\n")[0]).content
    imgLink = str(response).split('{"image":"')[1].split("?")[0]

    url = imgLink #Download Image
    r = requests.get(url)
    with open(imageLoc + "poster_" + str(i) + ".jpg", 'wb') as f:
        f.write(r.content)

def getTitle(response, i):
    title = str(response).split('<meta property="og:title" content="')[1].split('"')[0]
    return title.replace("&#039;", "'")
     
def loadData(listFile, reviewFile, singular = -1):
    #data[0] = Movie Title
    #data[1] = Movie Year
    #data[2] = Score
    #data[3] = Review
    #data[4] = Link
    #data[5] = Date
    
    # opening the CSV file

    with open(reviewFile, mode ='r', encoding='utf-8')as lenFile:
        csvFile = csv.reader(lenFile)
        csvLen = 0
        for lines in csvFile:
            csvLen += 1
        #print(csvLen)
    
    with open(listFile, mode ='r', encoding="latin-1")as file:
       
      # reading the CSV file
      csvFile = csv.reader(file)
     
      i = 0
      movieList = [["", "", "", "", ""] for i in range(csvLen)]
      for lines in csvFile:
          if (i > 4):
              movieList[i-5] = lines
          i+=1

    # opening the CSV file
    with open(reviewFile, mode ='r', encoding='utf-8')as file2:
       
      # reading the CSV file
      csvFile2 = csv.reader(file2)
     
      i = 0
      reviews = [["","","","","",""] for i in range(csvLen)]
      for lines in csvFile2:
          i+=1
          if (i > 1):
              reviews[i-2] = lines

    data = [["", "", "", "", "", ""] for i in range(csvLen)]
    i = 0

    if (singular != -1):
        movieList = [movieList[singular]]
    
    for movie in movieList:
        data[i][0] = movie[1] #Name
        data[i][1] = movie[2] #Year
        data[i][4] = movie[3] #Link
        #print(data[i])
        i+=1

    for movie in reviews:
        inList = False
        if(movie[1] != ""):
            for point in data:
                if(point[0] == movie[1] and point[1] == movie[2]):
                    #print(point[0])
                    inList = True
                    point[2] = movie[4] #Score
                    point[3] = movie[6].replace("<i>","").replace("</i>","") #Review
                    if(movie[8] != ""):
                        try:
                            point[5] = datetime.strptime(movie[8], "%Y-%m-%d")
                        except:
                            point[5] = datetime.strptime(movie[8], "%m/%d/%Y")
                    else:
                        point[5] = datetime.strptime("9999-01-01", "%Y-%m-%d")
                        #print(movie[1] + ("."*(50-len(movie[1])) + movie[8]))

            if (not inList):
                #print(movie[1] + ("."*(50-len(movie[1])) + movie[8]))
                pass
                

    for point in data:
        if (point[5] == ""): #Add dummy datetime to null point
            point[5] = datetime.strptime("9999-01-01", "%Y-%m-%d")
            #print(point[0] + " has no date")

    trimmedData = []
    for point in data:
        if (point[0] != ""):
            trimmedData.append(point)
    
    
    return trimmedData

def generateGraphic(data, i, imageLoc, graphicLoc, colors = ["yellow", "yellow", "yellow"]):
    poster = Image.open(imageLoc + "poster_" + str(i) + ".jpg") #Put image on poster
    poster = poster.resize((690, 1035))
    canvas = Image.new('RGB', (1840, 1035))
    canvas.paste(poster, (0,0))

#------------------------    
    titleIMG = Image.new("RGBA",(1150,200),colors[0]) #Generate Title
    title = data[i][0] + " (" + data[i][1] + ")"
    draw = ImageDraw.Draw(titleIMG)
    
    size = 60
    w = 99999

    while(w > 1150):
        titleFont = ImageFont.truetype("C:\Windows\Fonts\Arial.ttf", size)
        w, h = draw.textsize(title, font=titleFont)
        size -= 1

    draw.text(((1150-w)/2,(200-h)/2), title, fill="black", font=titleFont)
    canvas.paste(titleIMG, (690,0))
#------------------------
    scoreIMG = Image.new("RGBA",(1150,100),color = colors[1]) #Generate Score
    scoreFont = ImageFont.truetype("C:\Windows\Fonts\comicbd.ttf", 40)
    if(data[i][2] != ''):
        score = str(int(float(data[i][2])*2)) + " / 10"
    else:
        score = "N/A"
    draw2 = ImageDraw.Draw(scoreIMG)
    w, h = draw.textsize(score, font=scoreFont)
    draw2.text(((1150-w)/2,(100-h)/2), score, fill="black", font=scoreFont)
    canvas.paste(scoreIMG, (690,1035-250))
#------------------------
    reviewIMG = Image.new("RGBA",(1150,150),color = colors[2]) #Generate Review
    review = data[i][3]
    draw3 = ImageDraw.Draw(reviewIMG)
    
    size = 40
    w = 99999

    while(w > 1150):
        reviewFont = ImageFont.truetype("C:\Windows\Fonts\Arial.ttf", size)
        w, h = draw.textsize(review, font=reviewFont)
        size -= 1

    draw3.text(((1150-w)/2,(150-h)/2), review, fill="black", font=reviewFont)
    canvas.paste(reviewIMG, (690,1035-150))
    
    #canvas.show()
    canvas = canvas.save(graphicLoc + str(i) + ".jpg") #Save to file

def preview(data, i, imageLoc, graphicLoc):
    downloadImg(data[i], i, imageLoc)
    generateGraphic(data, i, imageLoc, graphicLoc)
    im = Image.open(graphicLoc + str(i) + ".jpg")
    im.show()
    

def main():
    data = loadData('kyle-watches-a-movie-every-day-in-2022.csv', 'reviews.csv', singular = 2)
    
    i = 0

    imageLoc = "IMAGES/"
    graphicLoc = "GRAPHICS/"

    return data

#data = main()
