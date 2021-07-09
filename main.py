import sys
import json
from lxml import etree
import xml.etree.ElementTree as ET

def main():#Main Function
    #Read command line and parse 
    input_file=sys.argv[1]
    output_file=sys.argv[2]
    option=sys.argv[3]

    #Control to command line. Split command line than control type of file
    input_control=input_file.split('.')
    output_control=output_file.split(".")

    #Options
    if option == "1":
        if(input_control[1] == "csv" and output_control[1]=="xml"): #Control type of file
            CsvToXml(input_file,output_file) # Convert xml from csv
        else:
            print("INVALID COMMOND LINE!")
    elif option== "2":
        if(input_control[1] == "xml" and output_control[1]=="csv"): #Control type of file
            XmlToCSV(input_file,output_file) #Convert csv from xml
        else:
            print("INVALID COMMOND LINE!")
    elif option== "3":
        if(input_control[1] == "xml" and output_control[1]=="json"): #Control type of file
            XmlToJson(input_file,output_file) #Convert json from xml
        else:
            print("INVALID COMMOND LINE!")
    elif option== "4":
        if(input_control[1] == "json" and output_control[1]=="xml"): #Control type of file
            JsonToXml(input_file,output_file) #Convert xml from json
        else:
            print("INVALID COMMOND LINE!")
    elif option=="5":
        if(input_control[1] == "csv" and output_control[1]=="json"): #Control type of file
            CsvToJson(input_file,output_file) #Convert json from csv
        else:
            print("INVALID COMMOND LINE!")
    elif option=="6":
        if(input_control[1] == "json" and output_control[1]=="csv"): #Control type of file
            JsonToCsv(input_file,output_file) #Convert csv from json
        else:
            print("INVALID COMMOND LINE!")
    elif option=="7":
        if(input_control[1] == "xml" and output_control[1]=="xsd"): #Control type of file
            XmlValidatesWithXsd(input_file,output_file) # Control xml file with xsd file
        else:
            print("INVALID COMMOND LINE!")
       
def CsvToXml(input_file,output_file):
    #Create a xml file
    mynewfile=open(output_file,"w")
    flag=True  # To avoid reading the first line of the csv file
    with open(input_file,"r") as file: # Open csv file to read
        for line in file: #Read line by line
            line=line.strip() #Clean /n 
            if flag==False: 
                olduniversity=word[1] # save old university's name to compare universities and create a new  unversity
            word=line.split(";") 
            newuniversity=word[1] 
            if flag:
                mynewfile.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n") 
                departments=ET.Element('departments') # when reading first line , creating root element
                flag=False # for don't create a new root
            else:
                if olduniversity!=newuniversity:
                    university=ET.SubElement(departments,"university") #create university sub element 
                    university.set("name",word[1])
                    university.set("uType", word[0])
            
                item=ET.SubElement(university,'item') #crate items
                item.set("id", word[3])
                item.set("faculty",word[2])
                name=ET.SubElement(item,"name") #create item's name

                if(word[5]!=""):
                    name.set("lang","en")
                else:
                    name.set("lang","tr")

                if(word[6]==""):
                    name.set("second","No")
                else:
                    name.set("second",word[6])

                name.text=word[4]  
                period=ET.SubElement(item,"period")  #create item's period
                period.text=word[8]
                quota=ET.SubElement(item,"quota") #create item's quota
                quota.set("spec",word[11])
                quota.text=word[10]
                field=ET.SubElement(item,"field") #create item's field
                field.text=word[9]
                last_min_score=ET.SubElement(item,"last_min_score") #create item's last_min_score
                if(word[12]!=""):
                    last_min_score.set("order",word[12])
                    last_min_score.text=word[13] #if item incule order, item incule last_min_score

                grant=ET.SubElement(item,"grant") #create item's grant

                if(word[7]!=""):
                    grant.text=word[7]

    #write in xml file
    data=ET.tostring(departments)       
    mynewfile.write(data.decode("UTF-8"))
    file.close()

def XmlToCSV(input_file,output_file):
    mynewfile=open(output_file,"w") #create a csv file to write
    mynewfile.write("ÜNİVERSİTE_TÜRÜ;ÜNİVERSİTE;FAKÜLTE;PROGRAM_KODU;PROGRAM;DİL;ÖĞRENİM_TÜRÜ;BURS;ÖĞRENİM_SÜRESİ;PUAN_TÜRÜ;KONTENJAN;OKUL_BİRİNCİSİ_KONTENJANI;GEÇEN_YIL_MİN_SIRALAMA;GEÇEN_YIL_MİN_PUAN\n")
    tree=ET.parse(input_file) #parse xml file
    root=tree.getroot()
    for x in range(len(root)): # for travel universities
        elem=root[x]
        for y in range(len(root[x])):  #for travel items
            sub_elem=elem[y]
            mynewfile.write(elem.get("uType")+";")
            mynewfile.write(elem.get("name")+";")
            mynewfile.write(sub_elem.get("faculty")+";")
            mynewfile.write(sub_elem.get("id")+";")
            mynewfile.write(sub_elem.find("name").text+";")

            if sub_elem.find("name").get("lang") == "en":
                mynewfile.write("İngilizce;")
            else:
                mynewfile.write(";")

            if sub_elem.find("name").get("second") == "No":
                mynewfile.write(";")
            else:
                mynewfile.write(sub_elem.find("name").get("second")+";")

            if sub_elem.find("grant").text==None:
                mynewfile.write(";")
            else:
                mynewfile.write(sub_elem.find("grant").text+";")

            mynewfile.write(sub_elem.find("period").text+";")
            mynewfile.write(sub_elem.find("field").text+";")
            mynewfile.write(sub_elem.find("quota").text+";")

            if sub_elem.find("quota").get("spec")==None:
                mynewfile.write(";")
            else:
                mynewfile.write(sub_elem.find("quota").get("spec")+";")

            if sub_elem.find("last_min_score").get("order")==None:
                mynewfile.write(";")
            else:
                mynewfile.write(sub_elem.find("last_min_score").get("order")+";")

            if sub_elem.find("last_min_score").text==None:
                mynewfile.write("\n")
            else:
                mynewfile.write(sub_elem.find("last_min_score").text+"\n")

def CsvToJson(input_file,output_file):

    flag=True # to don't read csv file's first line
    flag2=True # Don't compore csv'first line and second line
    with open(output_file, 'w', encoding='UTF-8') as json_file: #create a json file to write
        with open(input_file,"r") as file:#open csv file to read
            for line in file: #Read csv file line by line
                line=line.strip() #Clean /n

                if flag==False: 
                    olduniversity=newuniversity #save old university's name before split to compare universities and create a new university element
                    oldfaculty=newfaculty  #save old faculty's name before split to compare faculties and create a new faculty element
                word=line.split(";")
                newuniversity=word[1] 
                newfaculty=word[2] 
                    
                if flag: # when reading first line , creating lists
                    list_quality=[]
                    list_item=[]
                    list_csv=[]
                    flag=False
                else:
                    if oldfaculty!=newfaculty or olduniversity!=newuniversity : # Maybe different universities has got same faculty name but we still have to we create a new university 
                        if flag2==False: # the faculty in csv file's fist line not equal faculty in second line  and we shouldn't create a new faculty
                            dict_department={"department": list_quality} #facultY's department has got a few quality like id,name etc.
                            dict_faculty.update(dict_department) #update department's information
                            list_item.append(dict_faculty)#for save all items 
                            list_quality=[]#when we create a new faculty's department, we have to clear all qualities 
                        dict_faculty={"faculty" : word[2],"department":{}} #faculties has got a few departmens. At the same time, if we create a new faculty we have to describe a new dictionary

                    if olduniversity!=newuniversity : #for create a new university
                        if flag2==False: # the university in csv file's fist line not equal university in second line  and we shouldn't create a new university
                            dict_items={"items": list_item} # To save all items 
                            dict_university.update(dict_items) #update items's information
                            list_csv.append(dict_university) # To save all universities
                            list_item=[] # when we create a new university, we have to clear all items
                        dict_university={"university name": word[1],"uType":word[0],"items":{}} #universities has got a few items. At the same time, if we create a new university we have to describe a new dictionary

                    if(word[5]=="İngilizce"):
                        lan="en"
                    else:
                        lan="tr"

                    if(word[6]!="İkinci Öğretim"):
                        second="No"
                    else:
                        second=word[6]

                    if(word[11]==""):
                        spec=None
                    else:
                        spec=word[11]

                    period=word[8]
                    quota=word[10]
                    field=word[9]

                    if(word[13]=="" or word[13]=="-"):
                        last_min_score=None
                    else:
                        last_min_score=word[13]

                    if(word[12]==""):
                        last_min_order=None
                    else:
                        last_min_order=word[12]
                    
                    if word[7]=="":
                        grant=None
                    else:
                        grant=word[7]

                    #Crate a new dictionary to qualities and we have to add this dictionary in a list, beacuse a department has got a few quality
                    dict_quality={"id" : word[3], "name": word[4], "lang" : lan, "second": second,"period": period, "spec": spec, "quota": quota,"field": field, "last_min_score": last_min_score, "last_min_order": last_min_order, "grant": grant}
                    list_quality.append(dict_quality)

                    flag2=False

        # The algorithm create olduniversity after find a new university and the algorithm can't a new university in last line. So, we have to do all steps again for last universiy.
        dict_department={"department": list_quality} 
        dict_faculty.update(dict_department)
        list_item.append(dict_faculty)
        dict_items={"items": list_item}
        dict_university.update(dict_items)
        list_csv.append(dict_university)

        json.dump(list_csv,json_file,ensure_ascii=False, indent=4) # write properly in json 
        file.close()
            
def JsonToCsv(input_file,output_file):
    mynewfile=open(output_file,"w") # Create a new csv file to write
    mynewfile.write("ÜNİVERSİTE_TÜRÜ;ÜNİVERSİTE;FAKÜLTE;PROGRAM_KODU;PROGRAM;DİL;ÖĞRENİM_TÜRÜ;BURS;ÖĞRENİM_SÜRESİ;PUAN_TÜRÜ;KONTENJAN;OKUL_BİRİNCİSİ_KONTENJANI;GEÇEN_YIL_MİN_SIRALAMA;GEÇEN_YIL_MİN_PUAN\n")
    with open(input_file) as file: #Open json file to read
        data = json.load(file)
        for i in range(len(data)): # Travel to universities
            for j in range(len(data[i]["items"])):# Travel to items
                for x in range(len(data[i]["items"][j]["department"])):# Travel to faculty's departments
                    mynewfile.write(data[i]["uType"]+";")
                    mynewfile.write(data[i]["university name"]+";")
                    mynewfile.write(data[i]["items"][j]["faculty"]+";")
                    mynewfile.write((data[i]["items"][j]["department"][x]["id"])+";")
                    mynewfile.write((data[i]["items"][j]["department"][x]["name"])+";")
                    if(data[i]["items"][j]["department"][x]["lang"]!=None):
                        mynewfile.write("İngilizce;")
                    else:
                        mynewfile.write(";")

                    if(data[i]["items"][j]["department"][x]["second"]!="No"):
                        mynewfile.write((data[i]["items"][j]["department"][x]["second"])+";")
                    else:
                        mynewfile.write(";")
                    
                    if(data[i]["items"][j]["department"][x]["grant"]!=None):
                        mynewfile.write((data[i]["items"][j]["department"][x]["grant"])+";")
                    else:
                        mynewfile.write(";")

                    mynewfile.write((data[i]["items"][j]["department"][x]["period"])+";")
                    mynewfile.write((data[i]["items"][j]["department"][x]["field"])+";")
                    mynewfile.write((data[i]["items"][j]["department"][x]["quota"])+";")

                    if(data[i]["items"][j]["department"][x]["spec"]!=None):
                        mynewfile.write((data[i]["items"][j]["department"][x]["spec"])+";")
                    else:
                        mynewfile.write(";")

                    if(data[i]["items"][j]["department"][x]["last_min_order"]!=None):
                        mynewfile.write((data[i]["items"][j]["department"][x]["last_min_order"])+";")
                        mynewfile.write((data[i]["items"][j]["department"][x]["last_min_score"])) #if a faculty's department hasn't got a last_min order, this faculty hasn't got a last_min_score too.
                    else:
                        mynewfile.write(";")

                    mynewfile.write("\n") # To end of the line

    file.close()
           
def XmlToJson(input_file,output_file):
    tree=ET.parse(input_file) # Parse xml file
    root=tree.getroot()
    with open(output_file, 'w', encoding='UTF-8') as json_file: # Create a json file to write
        dict_item={} # Create a new dictionary to items
        list_csv=[] #Cretae a new list to universities
        list_item=[]# Save items 
        for x in range(len(root)): # Travel to universities
            elem=root[x]
            list_quality=[]
            for y in range(len(root[x])):  # Travel to items

                sub_elem=elem[y]
                
                dict_item.update({"id":sub_elem.get("id")})
                dict_item.update({"name":sub_elem.find("name").text})
                dict_item.update({"lang":sub_elem.find("name").get("lang")})
                dict_item.update({"second":sub_elem.find("name").get("second")})
                dict_item.update({"period":sub_elem.find("period").text})
                dict_item.update({"spec":sub_elem.find("quota").get("spec")})
                dict_item.update({"quota":sub_elem.find("quota").text})
                dict_item.update({"field":sub_elem.find("field").text})
                dict_item.update({"last_min_score":sub_elem.find("last_min_score").text})
                dict_item.update({"last_min_order":sub_elem.find("last_min_score").get("order")})
                dict_item.update({"grant":sub_elem.find("grant").text})
                
                #THIS PROJECT DON'T INCLUDE THİS PART, JUST I TRY
                #This if statement for as a new faculty's department
                #if(y!=0 and x>0 and root[x].find("name")!=root[x-1].find("name")): # if universities are different, we have to create a new faculty even faculties are same.
                    #if(elem[y].find("faculty")!=elem[y-1].find("faculty")): #if faculties are diffent, we have to create a new faculty
                        #dict_faculty={"faculty":sub_elem.get("faculty"),"department":{}}
                        #dict_faculty.update({"department":list_quality})
                        #list_item.append(dict_faculty)
                        #list_quality=[]
                        #list_item=[]

                list_quality.append(dict_item) # To save all items
                dict_item={}

            dict_faculty={"faculty":sub_elem.get("faculty"),"department":{}} # Faculties has got departments
            dict_faculty.update({"department":list_quality})  # Departments has got a few quality and this step add departmen's qualities
            list_item.append(dict_faculty) # We have to all items to can add all faculties
            dict_university={"university name": elem.get("name"),"uType":elem.get("uType"),"items":{}} # Cratea a new university and each university has got items
            dict_university.update({"items":list_item}) # Adding university's items
            list_item=[] # After add a university items, have to clean this item list.
            list_csv.append(dict_university) # To save all universities
            
       
        json.dump(list_csv,json_file,ensure_ascii=False, indent=4) # write properly in json 

def JsonToXml(input_file,output_file):  
    mynewfile=open(output_file,"w") # Open a new xml file to write
    mynewfile.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
    departments=ET.Element('departments') # Create root element
    with open(input_file) as file: #Open json file to read
        data = json.load(file) #To read  json file
        for i in range(len(data)): #To travel universities
            university=ET.SubElement(departments,"university") # Create a new university element
            university.set("name",data[i]["university name"])
            university.set("uType", data[i]["uType"])
            for j in range(len(data[i]["items"])): # To travel items
                for x in range(len(data[i]["items"][j]["department"])): #To travel faculty's departments
                    item=ET.SubElement(university,'item') # Create a new item
                    item.set("faculty",data[i]["items"][j]["faculty"])
                    item.set("id", data[i]["items"][j]["department"][x]["id"])

                    name=ET.SubElement(item,"name") # Create name element
                    name.set("lang",data[i]["items"][j]["department"][x]["lang"])
                    name.set("second",data[i]["items"][j]["department"][x]["second"])
                    name.text=data[i]["items"][j]["department"][x]["name"]

                    period=ET.SubElement(item,"period")#Crate period element
                    period.text=data[i]["items"][j]["department"][x]["period"]

                    quota=ET.SubElement(item,"quota")#Create quota element
                    if(data[i]["items"][j]["department"][x]["spec"]!=None):
                        quota.set("spec",data[i]["items"][j]["department"][x]["spec"])
                    else:
                        quota.set("spec","")
                    quota.text=data[i]["items"][j]["department"][x]["quota"]

                    field=ET.SubElement(item,"field") #Create field element
                    field.text=data[i]["items"][j]["department"][x]["field"]

                    last_min_score=ET.SubElement(item,"last_min_score")#Create last_min_score element
                    if(data[i]["items"][j]["department"][x]["last_min_order"]!=None):
                        last_min_score.set("order",data[i]["items"][j]["department"][x]["last_min_order"])
                    last_min_score.text=data[i]["items"][j]["department"][x]["last_min_score"]

                    grant=ET.SubElement(item,"grant")#Create grant element
                    grant.text=data[i]["items"][j]["department"][x]["grant"]
                
    # Write in xml file
    data=ET.tostring(departments)       
    mynewfile.write(data.decode("UTF-8"))
    file.close()
                    
def XmlValidatesWithXsd(input_file,output_file):

    xml = etree.parse(input_file)
    xsd_doc = etree.parse(output_file)
    xsd = etree.XMLSchema(xsd_doc)
    validation_result = xsd.validate(xml)
    print("VALIDATION RESULT: ")
    print(validation_result)
    xsd.assert_(xml)

    #Note1: in xsd file, spec is string because I have to control empty value
    #Note2: in xsd file, last_min_score is string because this element is written string type by elementTree
    #I control according to string 
               
main()                   
