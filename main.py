from xml.dom.minidom import parseString
from dicttoxml import dicttoxml
import json
import os
import time


def tokenize(string):
    tokens = []
    
    # 0 - none, 2 - ", 3 - '
    quotation_mode = 0
    token_start = -1
    
    for i in range(len(string)):
        # include spaces inside quotes
        if (quotation_mode != 0) and string[i] == " ":
            continue

        # start a quote
        if (quotation_mode == 0) and token_start == -1 and (string[i] == '"' or string[i] == "'"):
            if string[i] == '"':
                quotation_mode = 2
            else:
                quotation_mode = 3
            token_start = i
            continue

        # end a quote
        if (quotation_mode != 0) and token_start != -1 and (string[i] == '"' or string[i] == "'"):
            if (string[i] == '"' and quotation_mode == 2) or (string[i] == "'" and quotation_mode == 3):
                tokens.append(string[token_start + 1:i:])
                token_start = -1
                quotation_mode = 0
                continue
            
        # start a word
        if token_start == -1 and string[i] != " ":
            token_start = i
            continue

        # end a word
        if token_start != -1 and (quotation_mode == 0) and string[i] == " ":
            tokens.append(string[token_start:i:])
            token_start = -1
            continue
  
    return tokens


def create_definition(tokens, name, index, isEnumeration):
    this_object = {}
    
    while(index < (len(tokens) - 1)):
        if tokens[index] == "}":
            return (index + 1, None, this_object)

        values = []
        if name == "Values" and isEnumeration: 
            while(tokens[index] != "}"):
                values.append(tokens[index])
                index += 1
            index += 1
            return (index, values, None) 

        defaults = []
        if tokens[index] == "Default" and tokens[index + 1] == "{":
            index = index + 2
            while(tokens[index] != "}"):
                defaults.append(tokens[index])
                index += 1

            this_object["Default"] = defaults
            index += 1
            continue

        long_help = ""
        if tokens[index] == "LongHelp" and tokens[index + 1] == "{":
            index = index + 2
            while(tokens[index] != "}"):
                long_help += tokens[index] + " "
                index += 1

            this_object["LongHelp"] = long_help
            index += 1
            continue
      
        short_help = ""
        if tokens[index] == "ShortHelp" and tokens[index + 1] == "{":
            index = index + 2
            while(tokens[index] != "}"):
                short_help += tokens[index] + " "
                index += 1

            this_object["ShortHelp"] = short_help
            index += 1
            continue

        example = ""
        if tokens[index] == "Example" and tokens[index + 1] == "{":
            index = index + 2
            while(tokens[index] != "}"):
                example += tokens[index] + " "
                index += 1

            this_object["Example"] = example
            index += 1
            continue
        
        if tokens[index + 1] == "{":
            new_index, values, new_object = create_definition(tokens, tokens[index], index + 2, isEnumeration)
            
            if values is not None:
                this_object["Values"] = values
            if new_object is not None:
                this_object[tokens[index]] = new_object
                
            index = new_index
            continue

        this_object[tokens[index]] = tokens[index + 1]
        if tokens[index] == "Type" and tokens[index + 1] == "Enumeration":
            isEnumeration = True
        index += 2

    return (index, None, this_object)


def make_table(object_name, object_value):
    global html
            
    for (key, value) in object_value.items():
        if isinstance(value, str):
            html += f"<tr><td id='key' colspan='2'>{key}</td><td>{value}</td></tr>"
        elif isinstance(value, list):
            html += f"<tr><td id='key' colspan='2'>{key}</td><td>"
            for i in range(0, len(value)):
                html += f"{value[i]}"
                if(i < len(value)-1):
                #   html+=", <br>" #for new line
                    html += ", "
            html += f"</td></tr>"
        else:
            html += f"<tr><td id='collapseButton' onclick='collapse(this)'>+</td><th>{key}</th><td id='hidden'><table id='new_table'>"
            make_table(key, value)

    html += f"</table></td></tr>"


file_list = []
path = "C:/xampp/htdocs/pydipl/cdl/"
for x in os.listdir(path): 
    if x.endswith(".cdl"): #hack
        file_list.append(x)

            
for file in file_list:

    start_time = time.time()

    file = open(path+file, 'r')
    contents = file.read()
    contents = contents.replace("\t", " ").replace("\n", " ").replace('=', ' ').replace(',', ' ').replace("}.", "}").replace("= {", "{").replace('}', " } ").replace('{', " { ")
    tokens = tokenize(contents)

    returnValue = create_definition(tokens, "start", 0, False)
    dictionary = returnValue[2]#print(json.dumps(dictionary, indent=4))
    name = list(dictionary.keys())[0]

##if Isa attribute exist ->
    if "Isa" in dictionary[name]:
        inherits = dictionary[name]["Isa"]
        html_inherits = f"<p>Inherits: {inherits}</p>"
    else:
        inherits = None
        html_inherits = ""

##    for specific information in cdl documents
##    name->Values->Values->Items
##    name->Values->Items
    try:
      dictionary = dictionary[name]["Values"]["Values"]["Items"]
    except:
      dictionary = dictionary[name]["Values"]["Items"]

    body_style = "body{margin: 60px 50px;}"
    name_style = "#name{text-transform: uppercase;background-color: white;}"
    header_style = ".header{position: sticky;top: 0px;padding:10px 0px}"
    key_style = "#key{background-color:#555151; color:white;}"
    table_style = "table,td,th{border: 1px solid;} table{width: 80%;border-collapse: collapse;} th{text-align: justify;background-color:black; color:white;}"
    table_style += "#new_table{width: 100%;border-collapse: collapse;}"
    hidden ="#hidden{display:none;}"
    collapseButton = "#collapseButton{height:auto; width:50px;background-color:black;color:white;text-align: center;}#collapseButton:hover {background-color: #7F8C8D;color:white;}"
    back_btn_style = "a:link,a:visited {background-color:white;color:black;border:2px solid black;padding:10px 20px;text-align:center;text-decoration:none;display:inline-block;}"
    back_btn_style += "a:hover, a:active {background-color: black;color: white;}"
    button_position = ".button_position{margin-left: 60%;}"
    style = f"<style>{body_style}{name_style}{header_style}{key_style}{table_style}{hidden}{collapseButton}{back_btn_style}{button_position}</style>"

    html_content = f"<html><head> {style}  </head> <body>"
    back_button = f"<a href='../index.php' class='button_position'> Configuration Reference </a>"
    html_content += f"<h3 id='name' class='header'> {name} {back_button}</h3> "
    html_content += html_inherits
    
    html = "<table>"
    make_table("", dictionary)
    html_content += html
    script = "function collapse(cell){var col = cell; var target_col = col.parentElement.children[col.cellIndex + 2];"
    script += "if (target_col.style.display == 'block') {cell.innerHTML = '+';target_col.style.display = 'none';}"
    script += " else {cell.innerHTML = '-';target_col.style.display = 'block';}}"
    html_content += f"</table><script>{script}</script></body></html>"
    
    with open("html/"+name+'.html', 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

    json_object = json.dumps(dictionary, indent = 4)
    with open("json/"+name+".json", 'w') as json_file:
        json_file.write(json_object)

    xml = dicttoxml(dictionary, attr_type = False)
    xml_string = parseString(xml).toprettyxml()
    with open("xml/"+name+".xml", 'w') as xml_file:
        xml_file.write(xml_string)

    end_time = time.time()

    print("File: ", name)
    print("Time of execution: ", end_time-start_time, "seconds")
    print()

    
 
    
   

        



    
