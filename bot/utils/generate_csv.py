import os
import pandas as pd


class MongoDataProcessor:
    def __init__(self, data) -> None:
        self.data = data
        self.df = pd.DataFrame(data)
        self.filename = None

    def count_items(self) -> pd.DataFrame:
        self.item_count = self.df.shape[0]
        self.df["item_count"] = self.item_count
        return self.df

    def export_to_csv(self, filename="report.csv") -> None:
        file_path = os.path.join("./bot/files", filename)
        self.df.to_csv(file_path, index=False)
        self.filename = filename

    def get_dataframe(self) -> pd.DataFrame:
        return self.df

    @property
    def file_path(self) -> str:
        return os.path.join("./bot/files", self.filename)
