import requests

import csv


menURL = "https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=A1400060322AE5F1E7B9A90E5536DC4C&country=us&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(US)%26filter%3Dlanguage(en)%26filter%3DemployeePrice(true)%26filter%3DattributeIds(16633190-45e5-4830-a068-232ac7aea82c%2C0f64ecc7-d624-4e91-b171-b83a03dd8550)%26anchor%3D00%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D48"
womenURL = "https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=A1400060322AE5F1E7B9A90E5536DC4C&country=us&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(US)%26filter%3Dlanguage(en)%26filter%3DemployeePrice(true)%26filter%3DattributeIds(7baf216c-acc6-4452-9e07-39c2ca77ba32%2C16633190-45e5-4830-a068-232ac7aea82c)%26anchor%3D00%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D48"

visitedShoes = []
csvRows = []


def gatherRowData(jsonData):
    for each in jsonData:
        shoeName = each.get("title")

        if "Nike" in shoeName:
            shoeName = shoeName.replace("Nike", "").strip()

        gender = each.get("subtitle").split("'", 1)[0]
        category = each.get("subtitle")
        if "Nike" in category:
            category = category.replace("Nike", "").strip()
        if "Women's" in category:
            category = category.replace("Women's", "").strip()
        if "Men's" in category:
            category = category.replace("Men's", "").strip()


        for colors in each.get("colorways"):

            pid = colors.get("pid")
            # print(pid)

            if pid in visitedShoes:
                break

            visitedShoes.append(pid)

            numColors = len(colors.get("colorDescription").split("/"))
            color1 = "NaN"
            color2 = "NaN"
            color3 = "NaN"
            color4 = "NaN"

            if numColors == 1:
                color1 = colors.get("colorDescription").split("/")
            if numColors == 2:
                color1, color2 = colors.get("colorDescription").split("/")
            if numColors == 3:
                color1, color2, color3 = colors.get(
                    "colorDescription").split("/")
            if numColors == 4:
                color1, color2, color3, color4 = colors.get(
                    "colorDescription").split("/")

            price = colors.get("price").get("fullPrice")

            expensive = False

            if price > 120:
                expensive = True

            isNew = colors.get("isNew")
            isBestSeller = colors.get("isBestSeller")
            isMemberExclusive = colors.get("isMemberExclusive")
            inStock = colors.get("inStock")
            isSustainable = colors.get("isSustainable") or False

            csvRows.append([shoeName, isNew, gender, category, isBestSeller, isMemberExclusive, isSustainable, inStock, numColors,
                            color1, color2, color3, color4, price, expensive])


# Now start collecting data
def collectData(url):
    req = requests.get(url, headers="")
    data = req.json().get("data").get("products").get("products")
    count = 00
    while (data != None):
        gatherRowData(jsonData=data)

        # gross way to get change "pages" but it works
        count += 24
        url = url.replace("anchor%3D{}".format(
            count-24), "anchor%3D{}".format(count))
        req = requests.get(url, headers="")
        data = req.json().get("data").get("products").get("products")


collectData(womenURL)
collectData(menURL)

with open('shoes.csv', 'w', newline='') as csvfile:
    fieldNames = ["Shoe name", "isNew", "Gender", "category",  "isBestSeller", "isMemberExclusive", "isSustainable", "inStock", "numColors",
                  "Color 1", "Color 2", "Color 3", "Color 4", "Price", "Expensive"]
    shoeWriter = csv.writer(csvfile)
    shoeWriter.writerow(fieldNames)
    shoeWriter.writerows(csvRows)

# print(visitedShoes)
