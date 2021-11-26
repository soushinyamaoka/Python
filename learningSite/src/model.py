import pandas as pd
import setting
import os

def getModel(nameList):
    if setting.LOCAL＿MODE:
        imageFilePath = os.getcwd() + "src/static/" + setting.LOCAL_DMM_IMAGE_FILE_PATH
        # 対象の入ったcsv
        df1 = pd.read_csv(setting.LOCAL_CSV_FILE_PATH)
    else:
        imageFilePath = setting.STATIC_PATH  + "/" +  setting.DMM_IMAGE_FILE_PATH
        # 対象の入ったcsv
        df1 = pd.read_csv(setting.CSV_FILE_PATH)
    modelList = []
    for i, rows in enumerate(df1.iterrows()):
        for name in nameList:
            # CSVの女優名とDMMの女優名が一致した場合
            if name == rows[1]["name"]:
                modelInfo = {}
                imageDir = imageFilePath + "/" + str(rows[1]["id"]) + "/"
                fileName = ""
                if os.path.exists(imageDir):
                    fileName = os.listdir(imageDir)[0]
                modelInfo["image"] = setting.DMM_IMAGE_FILE_PATH + "/" + str(rows[1]["id"]) + "/" + fileName
                modelInfo["name"] = rows[1]["name"]
                modelInfo["birthday"] = rows[1]["birthday"]
                modelInfo["height"] = rows[1]["height"]
                modelInfo["listURL"] = rows[1]["listURL"]
                modelInfo["id"] = rows[1]["id"]
                modelInfo["B"] = rows[1]["B"]
                modelInfo["C"] = rows[1]["C"]
                modelInfo["W"] = rows[1]["W"]
                modelInfo["H"] = rows[1]["H"]
                modelList.append(modelInfo)

    return modelList
    