import pandas as pd

list = ["orange", "sun", "train", "sea"]
price = [100, 200, 300, 400]

df = pd.DataFrame({"list":list,
                   "price":price},index=False)
