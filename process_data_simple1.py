import torch
import pandas as pd
import numpy as np
from torch.utils.data import Dataset, random_split
import librosa
import librosa.display

class my_dataset(Dataset):

    classes = {'blues': 0,
               'classical': 1,
               'country': 2,
               'disco': 3,
               'hiphop': 4,
               'jazz': 5,
               'metal': 6,
               'pop': 7,
               'reggae': 8,
               'rock': 9}

    def __init__(self, root_path): #直接读取root_path下的csv文件，
        self.data = []
        self.targets = []

        df = pd.read_csv(root_path)
        for col in df.columns:
            if col != 'label' and col != 'filename' and col != 'length':
                df_min = df[col].min()
                df_max = df[col].max()
                df[col] = (df[col] - df_min) / (df_max - df_min)
        for row in range(len(df)):
            single_data = df.loc[row,'chroma_stft_mean' : 'mfcc20_var']
            single_label = df.loc[row, 'label']
            single_data = single_data.to_numpy()
            single_data = single_data.astype(np.float32)
            single_data = torch.from_numpy(single_data)
            single_data.to('cuda')
            self.data.append(single_data)
            self.targets.append(single_label)



    def __getitem__(self, index):
        x = self.data[index]
        #print(x.shape)
        y = self.classes[self.targets[index]]
        return x, y

    def __len__(self):
        return len(self.data)


class GTZANDataset:
    def __init__(self, rootDir=r"..\dataset\archive\Data\features_3_sec.csv"):
        self.rootDir = rootDir

        self.data = my_dataset(rootDir)

        self.trainDataset, self.testDataset = random_split(
            dataset=self.data,
            lengths=[int(len(self.data) * 0.7), len(self.data) - int(len(self.data) * 0.7)],
            generator=torch.Generator().manual_seed(0)
        )
        i = 0

    def __call__(self, train="False"):
        """
        :param train:
        :return: dataset (every picture is transformed into tensor whose size is [13, 432])
        """
        if train == "True":
            return self.trainDataset
        elif train == "False":
            return self.testDataset

if __name__ == "__main__":
    dataset = GTZANDataset(r"..\data\music\features_3_sec.csv")
    x = dataset(train="True")
    print(len(x))
    min_max = torch.load(r"..\models\min_max.pth")
    print(min_max)
    #print(x[1])
    '''data = pd.read_csv(r"..\data\music\features_3_sec.csv")
    for col in data.columns:
        print(col)
    single_data = data.loc[1]
    single_label = data.loc[0, 'chroma_stft_mean' : 'mfcc20_var']
    single_label = single_label.to_numpy()
    single_label = single_label.astype(np.float32)
    tensor = torch.from_numpy(single_label)
    print(tensor.size())
    tensor = torch.reshape(tensor,(1,1,57))
    print(tensor.size())
    zcr = librosa.feature.zero_crossing_rate'''
