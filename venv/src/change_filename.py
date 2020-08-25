import os
location = "./report_output/"
with os.scandir(location) as dirs:
    for entry in dirs:
        new_name = entry.name.split("-")
        print(new_name[1])

        if (new_name[1][0:10] == "MarketData"):
            #print(new_name[1][10:len(new_name[1])-4] + "MarketData2020-08-11_20.55.41" + ".csv")
            os.rename(location + entry.name, location + new_name[1][10:len(new_name[1])-4] + "MarketData2020-08-11_20.55.41" + ".csv")

        if (new_name[1][0:9] == "Estimates"):
            #print(new_name[1][9:len(new_name[1])-4] + "Estimates2020-08-11_20.55.41" + ".csv")
            os.rename(location + entry.name, location + new_name[1][9:len(new_name[1])-4] + "Estimates2020-08-11_20.55.41" + ".csv")

        if (new_name[1][0:12] == "QtrYoYGrowth"):
            #print(new_name[1][9:len(new_name[1])-4] + "Estimates2020-08-11_20.55.41" + ".csv")
            os.rename(location + entry.name, location + new_name[1][12:len(new_name[1])-4] + "QtrYoYGrowth2020-08-11_20.55.41" + ".csv")



