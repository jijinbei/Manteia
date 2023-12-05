# ファイル名の変更(1,Ⅰ,一などをⅠに統一)
def cource_rename(name):
    list1 = ["1","i","Ⅰ"]
    for i in list1:
        name = name.replace(i, "I")
    
    list2 = ["2","ii","Ⅱ"]
    for i in list2:
        name = name.replace(i, "II")
    
    list3 = ["3","iii","Ⅲ"]
    for i in list3:
        name = name.replace(i, "III")
    
    list4 = ["4","iv","Ⅳ"]
    for i in list4:
        name = name.replace(i, "IV")
    return name