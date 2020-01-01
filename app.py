'''
Web scrapper to search Images based on the input
'''

# Importing the necessary Libraries
from flask_cors import CORS,cross_origin
from flask import Flask, render_template, request,jsonify
from imagescrapper.ImageScrapper import ImageScrapper
from imagescrapperservice.ImageScrapperService import ImageScrapperService

# initialising the flask app with the name 'app'
app = Flask(__name__)

isLocalMode = False

# route for redirecting to the home page
@app.route('/')
@cross_origin()
def home():
    return render_template('index.html')

# route to show the images on a webpage
@app.route('/showImages')
@cross_origin()
def show_images():
    # Instantiating the object of class ImageScrapper
    scraper_object=ImageScrapper()

    # obtaining the list of image files from the static folder
    list_of_jpg_files=scraper_object.list_only_jpg_files('static')
    print(list_of_jpg_files)

    # If images are present, show them
    try:
        if(len(list_of_jpg_files)>0): # if there are images present, show them on a wen UI
            return render_template('showImage.html',user_images = list_of_jpg_files)
        else:
            return "Please try with a different string" # show this error message if no images are present in the static folder
    except Exception as e:
        print('no Images found ', e)
        return "Please try with a different string"


# route to search for the images on submit button.
@app.route('/searchImages', methods=['GET','POST'])
def searchImages():
    if request.method == 'POST':
        print("entered post")
        keyWord = request.form['keyword'] # assigning the value of the input keyword to the variable keyword

    else:
        print("did not enter post")

    print('printing = ' + keyWord)

    scraper_object = ImageScrapper()
    # obtaining the list of image files from the static folder
    list_of_jpg_files = scraper_object.list_only_jpg_files('static')

    # deleting the old image files stored from the previous search
    scraper_object.delete_existing_image(list_of_jpg_files)

    # splitting and combining the keyword for a string containing multiple words
    image_name = keyWord.split()
    image_name = '+'.join(image_name)

    # adding the header metadata
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

    service = ImageScrapperService
    masterListOfImages = service.downloadImages(keyWord, header) # getting the master list from keyword

    imageList = masterListOfImages[0] # extracting the list of images from the master list
    imageTypeList = masterListOfImages[1] # extracting the list of type of images from the masterlist

    response = "We have downloaded ", len(imageList), "images of " + image_name + " for you"

    return show_images() # redirect the control to the show images method


if __name__ == "__main__":
    if isLocalMode:
        print("LocalMode")
        app.run(host='127.0.0.1', port=8000)
    else:
        print("Cloud")
        app.run(debug=True)