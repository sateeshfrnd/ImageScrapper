from imagescrapper.ImageScrapper import ImageScrapper

class ImageScrapperService:

    def downloadImages( keyWord, header):
        imgScrapper = ImageScrapper
        url = imgScrapper.createURL(keyWord)
        rawHtml = imgScrapper.get_RawHtml(url, header)
        imageURLList = imgScrapper.getimageUrlList(rawHtml)
        masterListOfImages = imgScrapper.downloadImagesFromURL(imageURLList,keyWord, header)
        return masterListOfImages