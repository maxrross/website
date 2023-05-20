"""
refresh_data.py
fetch data from mongodb every six hours on the background
* data will be saved as js data which can be read by javascript+html without safety issue
* background cron job can make frontend presenttion such as umap without delay
"""
import pymongo
from user import username, password
import umap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

# connection to mongodb
cluster = pymongo.MongoClient(
    f"mongodb+srv://{username}:{password}@cluster0.tk9aheu.mongodb.net/test"
)
db = cluster["Main"]
collections = [i for i in db.list_collection_names() if i != "molecules"]
# 'molecules' is a test collection

# fetch all the data that are not error
data_dump = []
for c in tqdm(range(len(collections)), desc="scanning collections"):
    for i in db[collections[c]].find():
        if i["status"] != "Error":
            dipole = (
                (i["dipole"][0]) ** 2 + (i["dipole"][1]) ** 2 + (i["dipole"][2]) ** 2
            ) ** 0.5
            data = [
                i["name"],
                i["opt_xyz"],
                i["HOMO"],
                i["LUMO"],
                i["GAP"],
                i["electronic_energy"],
                dipole,
            ]
            data_dump.append(data)

# normalize data
data_array = np.array(data_dump)
df = pd.DataFrame(data_array[:, 2:]).astype(float)
label_dump = data_array[:, 0]
xyz = data_array[:, 1]
for col in df.columns:
    df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

# add umap data
umap_embed = umap.UMAP().fit_transform(df)
df_umap = df.copy()
df_umap["umap_x"] = umap_embed[:, 0]
df_umap["umap_y"] = umap_embed[:, 1]

# convert and save to js
with open("/Users/jingzhang/Documents/Local/academia/Mingjie/atUF/Database/otherworld_dev/umap.js", "w") as f:
    f.write("const umap_label=\n[\n")
    for i in range(len(label_dump)):
        f.write(f'"{label_dump[i]}",\n')
    f.write("];\n")

    f.write("const carbon_num=\n[\n")
    for i in range(len(xyz)):
        count = 0
        for j in xyz[i]:
            if j["atom"] == "C":
                count += 1
        f.write(f"{count},\n")
    f.write("];\n")

    f.write("const umap_x=\n[\n")
    for i in range(len(df_umap)):
        f.write(f"{df_umap.iloc[i].umap_x},\n")
    f.write("];\n")

    f.write("const umap_y=\n[\n")
    for i in range(len(df_umap)):
        f.write(f"{df_umap.iloc[i].umap_y},\n")
    f.write("];")
