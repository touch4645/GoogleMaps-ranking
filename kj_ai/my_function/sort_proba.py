import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder


def func(proba, le):
    # classのMajor minorの表記を変更する
    class_names = []
    for c in le.classes_:
        if c.split('_')[-1] == 'Major':
            class_names.append(c.split('_')[0])
        else:
            class_names.append(c.split('_')[0] + 'm')

    # 確率とクラス名のdfを作って 確率の降順でソート 上位5つをreturn
    key_proba_df = pd.DataFrame({'proba': proba*100, 'key': class_names})
    key_proba_df = key_proba_df.sort_values('proba', ascending=False)[:5]

    return key_proba_df
