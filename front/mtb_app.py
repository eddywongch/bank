import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

#Network(notebook=True)
st.title('Demo')
# make Network show itself with repr_html

#def net_repr_html(self):
#  nodes, edges, height, width, options = self.get_network_data()
#  html = self.template.render(height=height, width=width, nodes=nodes, edges=edges, options=options)
#  return html

if st.button('Say hello'):
    st.write('Why hello there')
else:
    st.write('Goodbye')


#Network._repr_html_ = net_repr_html
st.sidebar.title('Choose your favorite Graph')
option=st.sidebar.selectbox('select graph',('MTBank','Icon'))
physics=st.sidebar.checkbox('add physics interactivity?')

if option=='MTBank':
  HtmlFile = open("mtb_nx.html", 'r', encoding='utf-8')
  source_code = HtmlFile.read() 
  components.html(source_code, height = 900,width=1200)

if option=='Icon':
  HtmlFile = open("nwx.html", 'r', encoding='utf-8')
  source_code = HtmlFile.read()
  components.html(source_code, height = 900,width=1200)

