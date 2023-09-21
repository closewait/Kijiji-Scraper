

class KijijiAd():

    def __init__(self, ad):
        self.title = ad.find('h3', {"data-testid": "listing-title"}).text.strip() \
            if ad.find('h3', {"data-testid": "listing-title"}) is not None else ""
        self.id = ad.find('a', {"data-testid": "listing-link"}).get("href").rsplit('/', 1)[-1] \
            if ad.find('h3', {"data-testid": "listing-title"}) is not None else ""
        self.ad = ad
        self.info = {}

        self.__locate_info()
        self.__parse_info()

    def __locate_info(self):
        # Locate ad information
        self.info["Title"] = self.ad.find('h3', {"data-testid": "listing-title"})
        self.info["Image"] = self.ad.find_all('img', {"data-testid": "listing-card-image"})[1] \
            if self.ad.find_all('img', {"data-testid": "listing-card-image"}) is not None else ""
        self.info["Url"] = self.ad.find('a', {"data-testid": "listing-link"}).get("href")
        self.info["Details"] = self.ad.find('div', {"data-testid": "listing-details"})
        self.info["Description"] = self.ad.find('p', {"data-testid": "listing-description"})
        # date is not populated in request
        self.info["Date"] = self.ad.find('div', {"data-testid": "listing-details"}).find('p', {"data-testid":"listing-date"})
        self.info["Location"] = self.ad.find('div', {"data-testid": "listing-details"}).find('p', {"data-testid":"listing-location"})
        self.info["Price"] = self.ad.find('p', {"data-testid": "listing-price"})
        self.info["DataSource"] = str(self.ad.find_all('img')[1].get('src')) \
            if str(self.ad.find_all('img')) is not None else ""

    def __parse_info(self):
        # Parse Details and Date information
        self.info["Details"] = self.info["Details"].text.strip() \
            if self.info["Details"] is not None else ""
        self.info["Date"] = self.info["Date"].text.strip() \
            if self.info["Date"] is not None else ""

        # Parse remaining ad information
        for key, value in self.info.items():
            if value:
                if key == "Url":
                    self.info[key] = 'http://www.kijiji.ca' + value

                elif key == "Description":
                    self.info[key] = value.text.strip() \
                        .replace(self.info["Details"], '')

                elif key == "Location":
                    self.info[key] = value.text.strip() \
                        .replace(self.info["Date"], '')
                    
                elif key == "Image":
                    self.info[key] = '<img src =\"' + (self.info["DataSource"]) + '\"/>'

                elif key not in ["DataSource", "Details", "Date"]:
                    self.info[key] = value.text.strip()
