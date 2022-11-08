import urllib.request
import urllib.error

def findSalary(name):
	name = ''.join([c for c in name if c.isalnum() or c==' '])
	url  = "https://www.levels.fyi/companies/" + '-'.join((name).split()) + "/salaries/software-engineer"
	url = url.lower()
	try: 
		page = urllib.request.urlopen(url)
	except urllib.error.URLError as e:
		return("NULL")
	stringPage = page.read().decode("utf-8")
	if "needed to unlock salaries at" in stringPage:
		return("LOCK")
	beg = stringPage.index("totals ") + len("totals ")
	end = stringPage.index("K",beg+1)
	return stringPage[beg:end+1]




rawUrl = "https://github.com/pittcsc/Summer2023-Internships/blob/dev/README.md"
page = urllib.request.urlopen(rawUrl)
stringPage = page.read().decode("utf-8")
# f = open("newRawFile.txt", "w")
# f.write(stringPage)
# f.close()

md = open("pittCSList.md", "w")
md.write("## The List\n")
md.write("| Index | Name | Salary |\n")
md.write("| --- | --- | --- |\n")
mdOrder = open("orderedList.md", "w")
mdOrder.write("## The List, Ordered\n")
mdOrder.write("| Index | Name | Salary |\n")
mdOrder.write("| --- | --- | --- |\n")



lst = []
pos = stringPage.index("<tbody>")
count = 1
while "<tr>" in stringPage[pos:]:
	pos = stringPage.index("<tr>",pos)
	pos = stringPage.index("<td>",pos)+len("<td>")
	newPos = stringPage.index("</td>",pos)
	name = stringPage[pos:newPos]
	if "</a>" in name:
		name = name[name.index(">")+1:name.index("</a>")]
	# print(name, findSalary(name))
	salary = findSalary(name)
	lst.append((salary,name))
	md.write("| " + str(count) + " | " + name + " | " + salary + " |\n")
	count += 1
lst.sort(key=lambda company: int(company[0][1:-1]) if company[0] not in {"NULL","LOCK"} else -1,reverse=True)
count = 1
for salary,name in lst:
	mdOrder.write("| " + str(count) + " | " + name + " | " + salary + " |\n")
	count += 1
md.close()
mdOrder.close()
