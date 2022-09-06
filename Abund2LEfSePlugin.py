# Objective:
#   Transform QIIME2 abundance file to format suitable for LefSe analysis

# 1 - Non-User
# 2 - User

import pandas as pd

import PyPluMA

class Abund2LEfSePlugin:
    def input(self, infile):
        inputfile = open(infile, 'r')
        self.parameters = dict()
        for line in inputfile:
            contents = line.strip().split('\t')
            self.parameters[contents[0]] = contents[1]

    def run(self):
        pass

    def output(self, outfile):
       abundance_file = PyPluMA.prefix()+"/"+self.parameters["abundance"]
       metadata_file = PyPluMA.prefix()+"/"+self.parameters["metadata"]

       out = outfile

       metadata_df = pd.read_csv(metadata_file, sep="\t")
       #metadata_df["group"] = metadata_df["COCAINE USE"].apply(lambda x: 1 if x=="Non-User" else 2)
       metadata_df["group"] = metadata_df[self.parameters["variable"]]

       metadata_df["ClientID"] = metadata_df[self.parameters["ClientID"]]
       metadata_df = metadata_df[["group", "ClientID"]]

       df = pd.read_csv(abundance_file, index_col=0)
       #df = df.set_index(["Unnamed: 0"])

       # Normalize
       print(df)
       df = df.div(df.sum(axis=1), axis=0)

       df["ClientID"] = df.index
       # transform sample to match metadata
       df["ClientID"] = df["ClientID"].apply(lambda x: x.split("_")[0].replace(".", "/"))

       df = df.merge(metadata_df, how="left", on="ClientID")
       df.index = df["ClientID"]

       df_transposed = df.T

       df_transposed["bacteria"] = df_transposed.index

       df_transposed.to_csv(out, sep="\t")


