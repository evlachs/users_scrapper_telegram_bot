import pandas as pd

from utils.loggy import log, LOG
from utils import shortext
from types import NoneType

USERS_CSV_FNAME = 'data/users.csv'
saveDbRes = NoneType


class Database:
    @log
    def __init__(self, users_csv_fname=USERS_CSV_FNAME):
        self._users_csv_fname = users_csv_fname
        log(f"`db` as <{users_csv_fname}>'s been initialized.")

    @log
    def load_users(self, **kw) -> pd.DataFrame: return pd.read_csv(self._users_csv_fname, **kw)

    def _save_users_df(self, df: pd.DataFrame, *, csv_fname=None, **kw) -> saveDbRes:
        csv_fname = csv_fname or self._users_csv_fname
        df_rows = len(df)
        if not df_rows: LOG.warning(f"Users dataframe consists {df_rows} rows!")
        LOG.debug(f"save {shortext(df), f'rows: {df_rows}'} to <{csv_fname}>:..")
        df.to_csv(csv_fname, **kw)
        return NoneType()

    def _save_users_dict(self, d: dict, **kw) -> saveDbRes:
        return self._save_users_df(pd.DataFrame(d), **kw)

    @log
    def save_users(self, d: dict or pd.DataFrame, **kw) -> saveDbRes: return (
        ({
            dict: self._save_users_dict,
            pd.DataFrame: self._save_users_df
        }[type(d)])
        (d, **kw)
    )
