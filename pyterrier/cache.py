from .transformer import TransformerBase
import hashlib
from chest import Chest
from . import HOME_DIR 
import os
from os import path
CACHE_DIR = None
import pandas as pd
import pickle
from functools import partial


def init():
    global CACHE_DIR
    CACHE_DIR = path.join(HOME_DIR,"transformer_cache") 

class ChestCacheTransformer(TransformerBase):

    def __init__(self, inner, **kwargs):
        super().__init__(**kwargs)
        on="qid"
        self.inner = inner
        if CACHE_DIR is None:
            init()
        uid = hashlib.md5( bytes(str(self.inner.__repr__()), "utf-8") ).hexdigest()
        destdir = path.join(CACHE_DIR, uid)
        os.makedirs(destdir, exist_ok=True)
        self.chest = Chest(path=destdir, 
            dump=lambda data, filename: pd.DataFrame.to_pickle(data, filename) if isinstance(data, pd.DataFrame) else pickle.dump(data, filename, protocol=1),
            load=lambda filehandle: pickle.load(filehandle) if ".keys" in filehandle.name else pd.read_pickle(filehandle)
        )
        self.hits = 0
        self.requests = 0

    def stats(self):
        return self.hits / self.requests if self.requests > 0 else 0

    # dont double cache
    def __invert__(self):
        return self

    def __str__(self):
        return "Cache("+str(self.inner)+")"

    @property
    def NOCACHE(self):
        return self.inner

    def transform(self, input_res):
        return self._transform_qid(input_res)

    def _transform_qid(self, input_res):
        rtr = []
        todo=[]
        
        for index, row in input_res.iterrows():
            qid = row["qid"]
            self.requests += 1
            df = self.chest.get(qid, None)
            if df is None:
                todo.append(row.to_frame().T)
            else:
                self.hits += 1
                rtr.append(df)
        if len(todo) > 0:
            tood_df = pd.concat(todo)
            todo_res = self.inner.transform(tood_df)
            for indx, row in tood_df.iterrows():
                qid = row["qid"]
                this_query_res = todo_res[todo_res["qid"] == qid]
                self.chest[qid] = this_query_res
                rtr.append(this_query_res)
        self.chest.flush()
        return pd.concat(rtr)
