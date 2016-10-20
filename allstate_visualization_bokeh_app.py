import pandas as pd
raw_data = pd.read_csv('./output/raw_train_num.csv')
raw_data = raw_data.iloc[:,1:]
#temp = raw_data.iloc[:,:3]
temp = raw_data
col_name = list(temp.columns.values)
from bokeh.models import ColumnDataSource
s = ColumnDataSource(data=dict(x=[],y=[],z=[]))
from bokeh.plotting import figure
p = figure(title='numeric col',y_axis_label='col label')
p.circle(x='z', y='x',source=s, color='orchid')
p.circle(x='z', y='y',source=s, color='skyblue')
from bokeh.models.widgets import Slider, Select, Button
col_base = Select(title='col base', options=col_name, value='cont1')
col_vs = Select(title='col vs', options=col_name, value='cont2')
about_range = Slider(title='rows range from', start=0, end=len(temp), step=5000, value=5000)
row_limit_s = Slider(title='the number of rows start in range', start=0, end=5000, step=10, value=1000)
row_limit_e = Slider(title='the number of rows end in range', start=0, end=5000, step=10, value=3000)
sort_data = Button(label='sort?')
controls = [col_base, col_vs, row_limit_s, row_limit_e, sort_data, about_range]
def update_data(attrname, old, new):
    r_s = row_limit_s.value
    r_e = row_limit_e.value
    cb = col_base.value
    cv = col_vs.value
    ar = about_range.value
    
    x = temp.ix[r_s+ar:r_e+ar,cb]
    y = temp.ix[r_s+ar:r_e+ar,cv]
    z = range(abs(r_e-r_s))

    s.data = dict(x=x,y=y,z=z)
for i in controls:
    i.on_change('value', update_data)

def update_data_sort():
    r_s = row_limit_s.value
    r_e = row_limit_e.value
    cb = col_base.value
    cv = col_vs.value
    ar = about_range.value
    
    z = range(abs(r_e-r_s))
    i = temp.ix[r_s+ar:r_e+ar,[cb,cv]]
    i = i.sort(columns=[cb,cv])
    
    s.data = dict(x=i[cb],y=i[cv],z=z)
sort_data.on_click(update_data_sort)

from bokeh.layouts import row, widgetbox
inputs = widgetbox(*controls)
l = row(inputs, p)
from bokeh.io import curdoc
curdoc().add_root(l)
curdoc().title = "numeric col visulization"
#run in command line
#bokeh serve --show allstate_visulization_bokeh_interactive.py
