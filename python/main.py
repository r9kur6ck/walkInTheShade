import networkx as nx
import folium

# グラフデータとノード・エッジの定義
G = nx.Graph()
nodes = {
    'A': {'pos': (35.0, 135.0), 'shade_score': 5},
    'B': {'pos': (35.1, 135.1), 'shade_score': 2},
    'C': {'pos': (35.2, 135.2), 'shade_score': 7},
    'D': {'pos': (35.3, 135.3), 'shade_score': 3},
    'E': {'pos': (35.4, 135.4), 'shade_score': 6}
}
edges = [
    ('A', 'B', 2), ('B', 'C', 2), ('C', 'D', 2), ('D', 'E', 2), ('A', 'C', 3), ('B', 'D', 3)
]

# ノードとエッジの追加
for node, data in nodes.items():
    G.add_node(node, pos=data['pos'], shade_score=data['shade_score'])
for edge in edges:
    G.add_edge(edge[0], edge[1], weight=edge[2])

# 影の評価を考慮したコスト関数を作成
def shadow_path_cost(u, v, data):
    # 高い影の評価を持つ経路が低コストになるように調整
    max_shade = max([n['shade_score'] for n in nodes.values()])  # 最大の影評価値
    shade_adjustment = max_shade - ((G.nodes[u]['shade_score'] + G.nodes[v]['shade_score']) / 2)
    return data['weight'] + shade_adjustment

# 各エッジに影のコストを適用
for u, v, data in G.edges(data=True):
    data['weight'] = shadow_path_cost(u, v, data)

# ダイクストラ法で経路探索
start, goal = 'A', 'E'
path = nx.dijkstra_path(G, start, goal, weight='weight')

# マップの表示
map_center = nodes[start]['pos']
mymap = folium.Map(location=map_center, zoom_start=14)

# ノードとエッジをマップに描画
for node, data in nodes.items():
    folium.Marker(location=data['pos'], popup=f"{node} (Shade Score: {data['shade_score']})").add_to(mymap)

for u, v in G.edges:
    loc_u = nodes[u]['pos']
    loc_v = nodes[v]['pos']
    folium.PolyLine([loc_u, loc_v], color="blue").add_to(mymap)

# 経路を強調表示
route = [nodes[pt]['pos'] for pt in path]
folium.PolyLine(route, color="red", weight=5, opacity=0.8).add_to(mymap)

# 保存
mymap.save("shadow_path_map.html")
