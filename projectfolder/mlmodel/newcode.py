import textract
import PyPDF2
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter
import io
import os

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
  
def extract_text_from_word(filepath):
    txt = textract.process(filepath).decode('utf-8')
    return txt

def executetrige(filename,skills):
  t=skills
  t1=t.split(",")
  d1={}
  for u in t1:
    k,v=u.split("-")
    k = k.lower()
    d1[k]=v 

  lst1=list(d1.keys())
  exp=list(d1.values())
  lst2=[]
  for i in lst1:
      i=i.lower()
      lst2.append(i)
  fname = filename
  if fname.endswith(".docx"):
    text=extract_text_from_word(fname)
  else:
      resource_manager = PDFResourceManager()
      fake_file_handle = io.StringIO()
      converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
      page_interpreter = PDFPageInterpreter(resource_manager, converter)
      with open(fname, 'rb') as fh:

        for page in PDFPage.get_pages(fh,caching=True,
                                            check_extractable=True):
            page_interpreter.process_page(page)

            text = fake_file_handle.getvalue()

          # close open handles
        converter.close()
        fake_file_handle.close()
  text=text.lower()
  with open("op1.txt", 'w', encoding="utf-8") as rite:
            rite.write(text)
  exp_list=[]
  for txt in lst2:
      file_read = open("op1.txt", "r", encoding="utf-8")

      # reading file content line by line.
      lines = file_read.readlines()

      new_list = []
      idx = 0
      
      exp_small=[]

      # looping through each line in the file
      for line in lines:

          if txt in line:
              new_list.insert(idx, line)
              idx += 1


      if len(new_list)==0:
          # print("\n\"" +txt+ "\" is not found in file!")
          exp_small.append(0)

      else:
          lineLen = len(new_list)
          #print(lineLen)
          exp_small.append(lineLen)
          
          # print(lineLen,"times\n**** Lines containing \"" +txt+ "\" ****\n")
          # print("the number of times of repetition is", lineLen)

          for i in range(lineLen):
              res = [j for j in new_list[i].split() if (j.isdigit() or isfloat(j))]
              # print(res)
              if(len(res)>0):
                  if len(str(res[0]))>3 and len(res)>1:
                      if(res[1]==res[0]):
                          #print("no of years of experience is 1")
                          exp_small.append(1)
                          #exp_list.append(exp_small)
                      else:
                          #print("no of years of experience in",txt,"is",res[1]-res[0])
                          exp_small.append(res[1]-res[0])
                          #exp_list.append(exp_small)
                  elif(len(str(res[0]))>3):
                      # print("worked in the year",res[0])
                      exp_small.append(1)
                      #exp_list.append(exp_small)
                  else:
                      #print("no of years of experience in",txt,"is",res)
                      exp_small.append(res[0])
                      #exp_list.append(exp_small)
                      #print(exp_list)
          exp_list.append(exp_small) 
  
  exp_ex=[]
  for f in exp_list:
    if len(f)>1:
      exp_ex.append(f[1])
    else:
      exp_ex.append(0)
  exp_no=[]
  for f in exp_list:
    exp_no.append(f[0])

  short=[]
  for i in range(len(exp_ex)):
    if (float(exp_ex[i])>=(float(exp[i])-1)):
      short.insert(i,1)
    elif (int(exp_ex[i])==0):
      if (float(exp_no[i])>=(float(exp[i])-1)):
        short.insert(i,1)
      else:
        short.insert(i,1)
    else:
      short.insert(i,1)

  if 1 in short:
    return "Shortlisted"
  else:
    return "Not Shortlisted"

# print(executetrige('C:/Users/AVVB7D744/Downloads/Saumya_Singh_IBM.docx','Python-3'))