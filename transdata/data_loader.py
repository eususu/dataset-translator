from datasets import load_dataset,Dataset, DatasetDict
class DataLoader:
  _dataset:DatasetDict=None

  def __init__(self, path:str):
    _ds = load_dataset(path)
    if isinstance(_ds, Dataset):
      self._dataset = DatasetDict(dict(_=_ds))
    else:
      self._dataset = _ds
      
    print(f'loaded data: {self._dataset}')

    for data in self._dataset:
      print(f'DATA SPLIT({data}) = {len(self._dataset[data])}')

  def item(self, index:int=-1):
    for dt in self._dataset:
      return self._dataset[dt][0]