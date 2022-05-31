from pyresparser import ResumeParser
import json 
def executeTriage(path,skills):
    data = ResumeParser(path, skills_file='C:/Users/AVVB7D744/IBM SREENIVAS K/PROJECT/Newtry/skills.csv').get_extracted_data()
    json_object = json.dumps(data, indent = 4) 
    print(json_object)

    match1 = data['skills']
    skill_required = skills
    count = 0
    for k in skill_required:
        if(k in match1):
            count+=1
    print("\n\nPercentage Match with the Resume: "+str((count/len(skill_required))*100) +"%")
    result = str((count/len(skill_required))*100) +"%"
    return result