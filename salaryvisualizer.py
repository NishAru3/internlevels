from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show, output_file
from bokeh.io import export_png
names = []
x = []
y = []


data = open("salaryList.txt", "r")
for line in data:
    line = line.split(',')
    names.append(line[0])
    x.append(float(line[1]))
    y.append(float(line[2]))

data.close()

TOOLTIPS = [
    ("Company", "@name"),
    ("Intern Hourly", "@y"),
    ("Median SWE Salary", "@x")
]

source = ColumnDataSource(data=dict(x=x,y=y,name=names))

p = figure(title="Intern Hourly vs Median SWE Salary", x_axis_label='Median SWE Salary ($1000)', y_axis_label='Intern Hourly ($/hr)', tooltips=TOOLTIPS)
# p.x_range = range(0,int(max(x))+10**len(str(int(max(x)))))
# p.y_range = range(0,int(max[y])+10**len(str(int(max(y)))))
p.width = 1400
p.height = 800
p.circle(source=source, size=15, color="navy", alpha=0.5)
# p.line(x, y, legend_label="Temp.", line_width=2)
output_file("salaryvisualizer.html")
export_png(p, filename="salaryvisualizer.png")
# show(p)