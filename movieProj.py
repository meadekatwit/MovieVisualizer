import requests, csv
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

def downloadImg(link, i):
    response = requests.get(link[4].split("\n")[0]).content
    imgLink = str(response).split('{"image":"')[1].split("?")[0]

    url = imgLink #Download Image
    r = requests.get(url)
    with open("IMAGES/" + str(i) + ".jpg", 'wb') as f:
        f.write(r.content)

def getTitle(response, i):
    title = str(response).split('<meta property="og:title" content="')[1].split('"')[0]
    return title.replace("&#039;", "'")
     
def loadData():
    # opening the CSV file
    with open('kyle-watches-a-movie-every-day-in-2022.csv', mode ='r', encoding="latin-1")as file:
       
      # reading the CSV file
      csvFile = csv.reader(file)
     
      i = 0
      yearList = [["", "", "", "", ""] for i in range(370)]
      for lines in csvFile:
          if (i > 4):
              yearList[i-5] = lines
          i+=1

    # opening the CSV file
    with open('reviews.csv', mode ='r', encoding='utf-8')as file2:
       
      # reading the CSV file
      csvFile2 = csv.reader(file2)
     
      i = 0
      reviews = [["","","","","",""] for i in range(370)]
      for lines in csvFile2:
          i+=1
          if (i > 1):
              reviews[i-2] = lines

    data = [["", "", "", "", "", ""] for i in range(370)]
    i = 0
    for movie in yearList:
        data[i][0] = movie[1] #Name
        data[i][1] = movie[2] #Year
        data[i][4] = movie[3] #Link
        #print(data[i])
        i+=1

    for movie in reviews:
        #print(movie[3])
        inList = False
        if(movie[1] != ""):
            for point in data:
                if(point[0] == movie[1] and point[1] == movie[2]):
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

    
    data.sort(key=lambda x: x[5]) #Sort data by when inputted
    return data

def generateGraphic(data, i):
    poster = Image.open("IMAGES/" + str(i) + ".jpg") #Put image on poster
    poster = poster.resize((690, 1035))
    canvas = Image.new('RGB', (1840, 1035))
    canvas.paste(poster, (0,0))

#------------------------    
    titleIMG = Image.new("RGBA",(1150,200),"yellow") #Generate Title
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
    scoreIMG = Image.new("RGBA",(1150,100),color = (50, 50, 50)) #Generate Score
    scoreFont = ImageFont.truetype("C:\Windows\Fonts\comicbd.ttf", 40)
    if(data[i][2] != ''):
        score = str(int(float(data[i][2])*2)) + " / 10"
    else:
        score = "N/A"
    draw2 = ImageDraw.Draw(scoreIMG)
    w, h = draw.textsize(score, font=scoreFont)
    draw2.text(((1150-w)/2,(100-h)/2), score, fill="white", font=scoreFont)
    canvas.paste(scoreIMG, (690,1035-250))
#------------------------
    reviewIMG = Image.new("RGBA",(1150,150),color = (20, 20, 20)) #Generate Review
    review = data[i][3]
    draw3 = ImageDraw.Draw(reviewIMG)
    
    size = 40
    w = 99999

    while(w > 1150):
        reviewFont = ImageFont.truetype("C:\Windows\Fonts\Arial.ttf", size)
        w, h = draw.textsize(review, font=reviewFont)
        size -= 1

    draw3.text(((1150-w)/2,(150-h)/2), review, fill="white", font=reviewFont)
    canvas.paste(reviewIMG, (690,1035-150))
    
    #canvas.show()
    canvas = canvas.save("GRAPHICS/" + str(i) + ".jpg") #Save to file

def main():
    data = loadData()
    
    i = 0
    
    for link in data:
        #link[3] = link[4].split("\n")[0]
        if (data[i][0] != ""):
            print("Generating <" + str(data[i][0]) + ">")
            #downloadImg(link, i) #Download images
            #generateGraphic(data, i) #Generate Graphics
        i += 1

    return data

data = main()
