from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

connection = sqlite3.connect("data/minard.db")
quary_city = """
SELECT *
FROM cities;
"""
quary_temp = """
SELECT *
FROM temperatures;
"""
quary_troops = """
SELECT *
FROM troops;
"""
city_df = pd.read_sql(quary_city, con=connection)
temp_df = pd.read_sql(quary_temp, con=connection)
troops_df = pd.read_sql(quary_troops, con=connection)
# print(city_df, '\n',temp_df, '\n', troops_df)

loncs = city_df["lonc"].values
latcs = city_df["latc"].values
city_names = city_df["city"].values
rows = troops_df.shape[0]
lonps = troops_df["lonp"].values
latps = troops_df["latp"].values
survivals = troops_df["surviv"].values
directions = troops_df["direc"].values
fig, axes = plt.subplots(nrows=2, figsize=(25, 12), gridspec_kw={"height_ratios": [4, 1]})
m = Basemap(projection="lcc", resolution="i", width=1000000, height=400000,
            lon_0=31, lat_0=55, ax=axes[0])
m.drawcounties()
m.drawrivers()
m.drawparallels(range(54, 58), labels=[True, False, False, False])
m.drawmeridians(range(23, 56, 2), labels= [False, False, False, True])
x, y = m(loncs, latcs)
for xi, yi, city_name in zip(x, y, city_names):
    axes[0].annotate(text=city_name , xy=(xi, yi), fontsize=14, zorder=2)
x, y = m(lonps, latps)    
for i in range(rows - 1):
    if directions[i] == "A":
        line_color = "tan"
    else:
        line_color = "black"
    start_stop_lons = (x[i], x[i+1])
    start_stop_lats = (y[i], y[i+1])
    line_width = survivals[i]
    m.plot(start_stop_lons, start_stop_lats, linewidth=line_width/10000, color=line_color, zorder=1)

temp_celsius = (temp_df["temp"] * 5/4).astype(int)
lonts = temp_df["lont"].values
annotations = temp_celsius.astype(str).str.cat(temp_df["date"], sep="°C")
axes[1].plot(lonts, temp_celsius, linestyle='dashed',color='black')
for lont, temp_c, annotation in zip(lonts, temp_celsius, annotations):
    axes[1].annotate(annotation, xy=(lont - 0.3, temp_c - 10), fontsize=14)
axes[1].set_ylim(-50, 10)
axes[1].spines["top"].set_visible(False)
axes[1].spines["right"].set_visible(False)
axes[1].spines["bottom"].set_visible(False)
axes[1].spines["left"].set_visible(False)
axes[1].grid(True, which='major', axis='both')
axes[1].set_xticklabels([])
axes[1].set_yticklabels([])
axes[0].set_title("Napolean's disastrous Russian campaign of 1812", loc="left", fontsize=25)
plt.tight_layout()
fig.savefig("minard_clone.png")



## 地圖
# m = Basemap(projection="lcc", resolution="i", width=1000000, height=400000,
#             lon_0=31, lat_0=55, ax=ax)
# lons = [24.0, 37.6]
# lats = [55.0, 55.8]
# m.drawcounties()
# m.drawrivers()
# m.drawparallels(range(54, 58), labels=[True, False, False, False])
# m.drawmeridians(range(23, 56, 2), labels= [False, False, True, True])
# xi, yi = m(lons, lats)
# m.scatter(xi, yi)
# plt.show()

# 城市圖
# quary_city = """
# SELECT *
# FROM cities;
# """
# city_df = pd.read_sql(quary_city, con=connection)
# connection.close()
# # print(city_df)
# lons = city_df["lonc"].values
# lats = city_df["latc"].values
# city_names = city_df["city"].values
# fig, ax = plt.subplots()
# m = Basemap(projection="lcc", resolution="i", width=1000000, height=400000,
#             lon_0=31, lat_0=55, ax=ax)
# m.drawcounties()
# m.drawrivers()
# x, y = m(lons, lats)
# for xi, yi, city_name in zip(x, y, city_names):
#     ax.annotate(text=city_name, xy=(xi, yi), fontsize=6)
# plt.show()


# 氣溫圖
# quary_temp = """
# SELECT *
# FROM temperatures;
# """
# temp_df = pd.read_sql(quary_temp, con=connection)
# connection.close()
# print(temp_df)
# temp_celsius = (temp_df["temp"] * 5/4).values
# lons = temp_df["lont"].values
# fig, ax = plt.subplots()
# ax.plot(lons, temp_celsius)
# plt.show()

# 軍隊圖
# quary_troops = """
# SELECT *
# FROM troops;
# """
# troops_df = pd.read_sql(quary_troops, con=connection)
# connection.close()
# # print(troops_df)
# rows = troops_df.shape[0]
# lons = troops_df["lonp"].values
# lats = troops_df["latp"].values
# survivals = troops_df["surviv"].values
# directions = troops_df["direc"].values
# div = troops_df["division"].values

# fig, ax = plt.subplots()
# for i in range(rows - 1):
#     if directions[i] == "A":
#         line_color = "tan"
#     else:
#         line_color = "black"
#     start_stop_lons = (lons[i], lons[i+1])
#     start_stop_lats = (lats[i], lats[i+1])
#     line_width = survivals[i]
#     ax.plot(start_stop_lons, start_stop_lats, linewidth=line_width/10000, color=line_color)
# # ax.plot((30, 35), (50, 55))
# plt.show()



