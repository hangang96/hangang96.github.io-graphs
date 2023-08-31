import folium
import pandas as pd
from pyvis.network import Network
import networkx as nx
from geopy.geocoders import Nominatim

# 创建地理编码器
geolocator = Nominatim(user_agent="my_app")

# 定义获取经纬度的函数
def get_latitude_longitude(place):
    location = geolocator.geocode(place)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# 读取CSV文件，获取人名、地区和经纬度信息
data = pd.read_csv('1.csv', encoding='GBK')

# 创建世界地图
world_map = folium.Map(location=[0, 0], zoom_start=2)

# 添加搜索栏
search = folium.Search().add_to(world_map)

# 循环处理每个地区
for place in data['place'].unique():
    # 过滤出属于当前地区的人名
    sub_data = data[data['place'] == place]
    
    # 创建NetworkX图
    G = nx.Graph()
    for _, row in sub_data.iterrows():
        G.add_node(row['name'])
    
    # 将其他节点与中心节点（地区）连接
    for _, row in sub_data.iterrows():
        G.add_edge(place, row['name'])
    
    # 创建PyVis网络
    nt = Network(width="800px", height="800px", notebook=True, bgcolor="Black", font_color="White")

    # 设置节点的颜色
    nt.add_node(place, color="SeaGreen")

    # 添加节点和边
    for node in G.nodes():
        nt.add_node(node)
    for edge in G.edges():
        nt.add_edge(edge[0], edge[1], color="SteelBlue")
    
    # 将PyVis网络保存为HTML文件
    subgraph_html = f"{place}_subgraph.html"
    nt.show(subgraph_html)
    
    # 获取当前地区的经纬度信息
    latitude, longitude = get_latitude_longitude(place)  # 根据地区名获取经纬度，需要自行实现
    
    # 如果经纬度有效，则创建标记和弹出框
    if latitude is not None and longitude is not None:
        html = f'<iframe src="{subgraph_html}" width="800px" height="800px"></iframe>'
        popup = folium.Popup(html, max_width=800)
        
        # 在世界地图上添加标记
        folium.Marker([latitude, longitude], popup=popup).add_to(world_map)

# 保存世界地图为HTML文件
world_map.save('world_map_with_subgraphs.html')
