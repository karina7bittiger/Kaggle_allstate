import pandas as pd
raw_data = pd.read_csv('./data/test_bokeh_interactive.csv')
raw_data = raw_data.iloc[:,1:]
temp = raw_data.iloc[:,:3]
col_name = list(temp.columns.values)
from bokeh.models import ColumnDataSource
s = ColumnDataSource(data=dict(x=[],y=[],z=[]))
from bokeh.plotting import figure
p = figure(title='numeric col',y_axis_label='col label')
p.circle(x='z',y='x',source=s, color='orchid')
p.circle(x='z',y='y',source=s, color='skyblue')
from bokeh.models.widgets import Slider, Select
col_base = Select(title='col base', options=col_name, value='cont1')
col_vs = Select(title='col vs', options=col_name, value='cont2')
row_limit_s = Slider(title='start number of rows', start=0, end=len(temp), step=1, value=10)
row_limit_e = Slider(title='end number of rows', start=0, end=len(temp), step=1, value=30)
controls = [col_base, col_vs, row_limit_s, row_limit_e]
def update_data(attrname, old, new):
    r1 = row_limit_s.value
    r2 = row_limit_e.value
    cb = col_base.value
    cv = col_vs.value
    
    x = temp.ix[r1:r2,cb]
    y = temp.ix[r1:r2,cv]
    z = range(abs(r2-r1))
	
    s.data = dict(x=x,y=y,z=z)
for i in controls:
    i.on_change('value', update_data)
from bokeh.layouts import row, widgetbox
inputs = widgetbox(*controls)
l = row(inputs, p)
from bokeh.io import curdoc
curdoc().add_root(l)
curdoc().title = "test"