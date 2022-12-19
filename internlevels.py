import requests
import gzip
import time

def findSalary(name):
	name = ''.join([c for c in name if c.isalnum() or c==' '])
	url  = "https://www.levels.fyi/companies/" + '-'.join((name).split()) + "/salaries/software-engineer"
	url = url.lower()
	page = requests.get(url)
	if page.status_code != 200:
		return("NULL")
	if "needed to unlock salaries at" in page.text:
		return("LOCK")
	beg = page.text.index("totals ") + len("totals ")
	end = page.text.index("K",beg+1)
	return page.text[beg:end+1]


f = open("rawInternshipBody.txt", "r")
internPage = f.read()
f.close()

def findInternSalary(name):
	url = "<h6 style=\"cursor: pointer;\" class=\"font-weight-bold mt-1 mb-2 mx-auto\">" + name + "\n"
	if url not in internPage:
		return None
	pos = internPage.index(url)
	url2 = "<h6 class=\"mt-1 mb-2  font-weight-bold\">$"
	pos = internPage.index(url2,pos+1)
	endPos = internPage.index("<",pos+len(url2))
	return float(internPage[pos+len(url2):endPos].strip())


rawUrl = "https://github.com/pittcsc/Summer2023-Internships/blob/dev/README.md"
page = requests.get(rawUrl)
stringPage = page.text
# f = open("newRawFile.txt", "w")
# f.write(page.text)
# f.close()


md = open("pittCSList.md", "w")
md.write("## The List\n")
md.write("| Index | Name | Median SWE Salary | Notes |\n")
md.write("| --- | --- | --- | --- |\n")

mdOrder = open("orderedList.md", "w")
mdOrder.write("## The List, Ordered\n")
mdOrder.write("| Index | Name | Median SWE Salary | Notes |\n")
mdOrder.write("| --- | --- | --- | --- |\n")

salaryList = open("salaryList.txt","w")

dic = {}

lst = []
pos = stringPage.index("<tbody>")
count = 1
while "<tr>" in stringPage[pos:]:
	pos = stringPage.index("<tr>",pos)
	pos = stringPage.index("<td>",pos)+len("<td>")
	newPos = stringPage.index("</td>",pos)
	name = stringPage[pos:newPos]
	pos = stringPage.index("<td>",pos)+len("<td>")
	pos = stringPage.index("<td>",pos)+len("<td>")
	newPos = stringPage.index("</td>",pos)	
	notes = stringPage[pos:newPos]
	tempName = name
	if "</a>" in tempName:
		tempName = name[name.index(">")+1:name.index("</a>")]
	# print(name, findSalary(name))
	salary = findSalary(tempName)
	if salary != "NULL" and salary != "LOCK":	
		internSalary = findInternSalary(tempName)
		if internSalary != None:
			dic[tempName] = {
							"name": tempName,
							"salary": float(salary[1:-1]),
							"internSalary": internSalary
						}
			phrase = (tempName + "," + salary[1:-1]) + "," + str(internSalary) + "\n"
			salaryList.write(phrase)
	lst.append((salary,name,notes))
	md.write("| " + str(count) + " | " + name + " | " + (str(dic[tempName]["internSalary"]) if tempName in dic and dic[tempName]["internSalary"]!=None else "none")  +  " | " + notes + " |\n")
	count += 1
lst.sort(key=lambda company: int(company[0][1:-1]) if company[0] not in {"NULL","LOCK"} else -1,reverse=True)
count = 1
for salary,name,notes in lst:
	mdOrder.write("| " + str(count) + " | " + name + " | " + salary +  " | " + notes + " |\n")
	count += 1


	 
md.close()
mdOrder.close()
salaryList.close()


