# Content of file /Users/user/PycharmProjects/users_scrapper_telegram_bot/scrapper/scrapp.py
from typing import Union, List, Dict

import pandas as pd
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import Dialog, InputChannel, InputPeerEmpty

from conf.config import ALL_IMPORTED_USERS_FNAME, SAVE_HIST_DATA, TG_MSGS
from ..utils.db import Database
from ..utils.loggy import log, LOG, logger

DB = Database()


class UsersScrapper:
    """
    A class for searching for client groups in a telegram
    searching for and adding members of these groups to the client channel in a telegram.

    Attributes
        client: telethon.sync.TelegramClient
            Initializes the client using the bot

    Methods
        get_groups() -> Dict[str, Dialog]
            Gets the groups that the client is a member of

        get_chat_participants(target_group: Dialog) -> List[str]
            Gets the members of the group that the client has selected

        invite_users(channel: Union[str, int, InputChannel], usernames: list) -> List[str]
            Invites users to the channel selected by the client

        save_new_users_to_csv(new_users: list) -> None
            staticmethod for recording newly received group members in a users.csv file

        update_users_status(invited_users: list) -> None
            staticmethod that changes the status of the user "invited" in the users.csv from 0 to 1 if he was invited

        clear_users_data() -> None
            Clears all data about previously added users in a users.csv file

        get_users_to_invite() -> List[str]
            Gets a list of users from a users.csv file who have not yet been invited to the channel
    """

    @log
    def __init__(self, client: TelegramClient):
        """
        Constructor that initializes the client using the bot

        :param client: a client who uses a bot
        :type client: telethon.sync.TelegramClient
        """
        self.client = client
        self._load_users = DB.load_users
        self.get_users_db_fname = DB.get_users_db_fname
        # self._save_users = DB.save_users

    @log
    async def get_chat_participants(self, target_group: Dialog,
                                    *, save_hist_data=SAVE_HIST_DATA
                                    ## ) -> Dict[str, Dict[str, Union[str, int]]]:
                                    ) -> list:
        """
        #ChatGPT created with changes
        Gets the members of the group that the client has selected and returns a dictionary with usernames as keys and a dictionary containing the import timestamp and source chat id as values.

        :param target_group: group chosen by the client for scrapping participants
        :type target_group: telethon.tl.types.Dialog

        :rtype: dict
        :return: a dictionary where keys are the usernames of the group members and values are a dictionary with import timestamp and source chat id
        """
        from datetime import datetime
        import_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_users = []
        new_users_dict = {}
        participants = await self.client.get_participants(target_group, limit=200)
        df = self._load_users()
        for user in participants:
            if user.username and f'@{user.username}' not in list(df['username']):
                new_users.append(f'@{user.username}')
                new_users_dict[f'@{user.username}'] = dict(
                    user_id=user.userid,
                    # todo: убрать, если невозможно его достать (хорошо бы сохранять, тк юзернейм может меняться, но не критично)
                    import_timestamp=import_timestamp,
                    source_chat_id=target_group.id,  # todo: аналогично user_id (см выше)
                    source_chat_name=target_group.name
                    # fixme: тут надо как-то вытянуть id и name чата (или link для непубличных - такие тоже нужны уже).. \
                    # .. GhatGPT и я не осилили 🥲
                )
        if save_hist_data: self._save_chat_participants(new_users_dict)
        return new_users

    @log
    @staticmethod
    def _save_chat_participants(self, users: pd.DataFrame or dict, csv_fname=ALL_IMPORTED_USERS_FNAME) -> None:
        """ Save all received group members in a ALL_IMPORTED_USERS_FNAME-csv file
        :param users: users with attrs as pandas-DF or dict for saving into csv
        :param csv_fname: csv file name (ALL_IMPORTED_USERS_FNAME by default)
        """
        log(f"Save all importing users data to <{csv_fname}> ({len(users)} rows):..")
        DB.save_users(users, csv_fname=csv_fname, index=False, header=False, mode='a')

    @log
    async def get_groups(self) -> Dict[str, Dialog]:
        """
        Gets the groups that the client is a member of

        :rtype: dict
        :return: dict where key is the name of the group and value is an object of the telethon.tl.types.Dialog
        """
        groups = {}
        all_dialogs = await self.client(GetDialogsRequest(
            offset_date=None,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=200,
            hash=0
        ))
        for user_chat in all_dialogs.chats:
            try:
                if user_chat.megagroup:
                    groups[user_chat.title] = user_chat
            except AttributeError as e:
                LOG.error(e, f"user_chat=<{user_chat}>")
                continue
        return groups

    @log
    async def invite_users(self, channel: Union[str, int, InputChannel], usernames: list) -> List[str]:
        """
        Invites users to the channel selected by the client

        :param channel: telegram channel to invite users to
        :type channel:  str | int | telethon.tl.types.InputChannel

        :param usernames: the list of usernames of users who need to be invited to the channel
        :type usernames: list

        :rtype: list
        :return: list of invited users
        """
        invited_users = []
        try:
            await self.client(InviteToChannelRequest(channel, usernames))
            invited_users.extend(usernames)
        except Exception as e:
            if str(e) in TG_MSGS.USER_NOT_ALLOWED_TO_ADD:
                invited_users.extend(usernames)
            else:
                ##?ready LOG.exception(f"Some exception in {utils.current_function()}")
                logger.exception()
        return invited_users

    @staticmethod
    def save_new_users_to_csv(new_users: list) -> None:
        """
        staticmethod for recording newly received group members in a users.csv file

        :param new_users: list of usernames of group members who have not yet been invited
        :type new_users: list
        """
        data_dict = {'username': new_users, 'invited': 0}
        log(f"Savind users attrs <{data_dict.keys()}> to `db` (total {len(data_dict)} rows):..")
        DB.save_users(data_dict, index=False, header=False, mode='a')

    @log
    @staticmethod
    def update_users_status(invited_users: list) -> None:
        """
        staticmethod that changes the status of the user "invited" in the users.csv file from 0 to 1 if he was invited

        :param invited_users: list of usernames of users who have been invited
        :type invited_users: list
        """
        df = DB.load_users(index_col='username')
        for user in invited_users:
            df.loc[user, 'invited'] = 1
        DB.save_users(df)

    @log
    @staticmethod
    def get_users_to_invite() -> List[str]:
        """
        Gets a list of users from a users.csv file who have not yet been invited to the channel

        :rtype: list
        :return: list of usernames of users from the users.csv file whose invited status is 0
        """
        df = DB.load_users(index_col='invited')
        to_invite = list(df.loc[0]['username'])
        return to_invite

    @log
    @staticmethod
    def clear_users_data() -> None:
        """Clears all data about previously added users in a users.csv file"""
        data_dict = {'username': list(), 'invited': list()}
        DB.save_users(data_dict, index=False)
