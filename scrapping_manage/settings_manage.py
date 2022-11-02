import pandas as pd


class SettingsManage:
    """
    A class for getting and writing scrapper settings to a scrapping_settings.csv file

    Attributes
        df: pandas.Dataframe
            initializes a csv file with scraper settings as a dataframe

    Methods
        .. notes:: methods of this class work directly with a scrapping_settings.csv file
        without changing or setting attribute values inside the class
    """
    def __init__(self):
        self.df = pd.read_csv('data/scrapping_settings.csv')

    @property
    def delay(self) -> int:
        """Get or set a delay between each user's invitation"""
        return self.df['delay'][0]

    @delay.setter
    def delay(self, value: int) -> None:
        self.df.loc[0, 'delay'] = value
        self.df.to_csv('data/scrapping_settings.csv', index=False)

    @property
    def launch_time(self) -> str:
        """Get or set the time of the daily launch of user invitations to the channel"""
        return self.df['launch_time'][0]

    @launch_time.setter
    def launch_time(self, value: str) -> None:
        self.df.loc[0, 'launch_time'] = value
        self.df.to_csv('data/scrapping_settings.csv', index=False)

    @property
    def scrapping_status(self) -> bool:
        """Get or set the value of the scrapping status: if True, scraping is started, if False, it's stopped"""
        return self.df['scrapping_status'][0]

    @scrapping_status.setter
    def scrapping_status(self, value: bool) -> None:
        self.df.loc[0, 'scrapping_status'] = value
        self.df.to_csv('data/scrapping_settings.csv', index=False)

    @property
    def active_group(self) -> str:
        """Get or set the name of the group from which you want to collect participants"""
        return self.df['active_group'][0]

    @active_group.setter
    def active_group(self, value: str) -> None:
        self.df.loc[0, 'active_group'] = value
        self.df.to_csv('data/scrapping_settings.csv', index=False)

    @property
    def active_channel(self) -> str:
        """Get or set the name of the channel to invite users to"""
        return self.df['active_channel'][0]

    @active_channel.setter
    def active_channel(self, value: str) -> None:
        self.df.loc[0, 'active_channel'] = value
        self.df.to_csv('data/scrapping_settings.csv', index=False)

    @property
    def limit(self) -> int:
        """Get or set a maximum limit on the number of user invitations per day"""
        return self.df['limit'][0]

    @limit.setter
    def limit(self, value: int) -> None:
        self.df.loc[0, 'limit'] = value
        self.df.to_csv('data/scrapping_settings.csv', index=False)
