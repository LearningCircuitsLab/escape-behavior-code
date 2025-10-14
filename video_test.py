# #%%
# mainpath = "/home/pi/Desktop/"
# import pandas as pd
# import matplotlib.pylab as plt
# import numpy as np

# # list all the csv files in the path
# import os
# paths = [os.path.join(mainpath, f) for f in os.listdir(mainpath) if f.endswith('.csv')]

# dfslist = []

# for path in paths:
#     df = pd.read_csv(path, sep=";")

#     nframes = len(df)

#     df["difs"] = df.camera_timestamp.diff() * 1000

#     print(df.loc[(df.difs == np.max(df.difs))])

#     percentiles = np.percentile(df["difs"].dropna(), [1, 25, 50, 75, 99])

#     mean = df["difs"].mean()
#     std = df["difs"].std()

#     filename = path.split("/")[-1].split("_")
#     fps = int(filename[0][:-3])
#     res = filename[1]
#     mode = filename[2][:-4]

#     expected_frames = 160 * fps

#     captured_frames = nframes / expected_frames * 100

#     datadict = {
#         "filename": path.split("/")[-1],
#         "fps": fps,
#         "res": res,
#         "mode": mode,
#         "nframes": nframes,
#         "expected_frames": expected_frames,
#         "percentage_of_frames": captured_frames,
#         "mean": mean,
#         "std": std,
#         "p1": percentiles[0],
#         "p25": percentiles[1],
#         "p50": percentiles[2],
#         "p75": percentiles[3],
#         "p99": percentiles[4],
#     }

#     dfslist.append(pd.DataFrame(datadict, index=[0]))
# final_df = pd.concat(dfslist, ignore_index=True)
# final_df
# #plt.xlim(0.01, 0.05)
# # %%
# print(final_df)
