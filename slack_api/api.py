import requests
from typing import Dict, List
from .exception import SlackApiError


class SlackApi():

    def __init__(self, api_tokens: Dict[str, str]):
        """
        tokenとchannelのIDを受け取る

        Args:
            api_tokens: tokenとchannel_idを受け取る辞書
            channel_idは、省略可能
            {
                token:[your token],
                channel_id:[channel_id]
            }
        """
        self.token = api_tokens.get('token')
        self.channel_id = api_tokens.get('channel_id')

    def say(self, message: str, channel_id: str = ""):
        """
        slackへ発言を投稿する
        channel_idを省略した場合、__init__で渡した channel_idを利用する

        Args:
            message: 投稿するメッセージを入力する
            channel_id: 投稿するチャンネルを指定するばあいはここにchannel_idを渡す
        """
        url = 'https://slack.com/api/chat.postMessage'
        params = {'token': self.token,
                  'channel': channel_id if len(channel_id) > 0 else self.channel_id
                  }

        result = self._request_api(url, params, "POST")

        return result

    def delete(self, time_stamp: int, channel_id: str = ""):
        """
        特定のチャンネルの発言を削除する
        channel_idを省略した場合、__init__で渡した channel_idを利用する

        Args:
            time_stamp : 削除したいメッセージのタイムスタンプ(ex:1405894322.002768)
            channel_id : 削除する発言のあるチャンネルを指定するばあいはここにchannel_idを渡す
        """

        url = "https://slack.com/api/chat.delete"
        params = {'token': self.token,
                  'channel': channel_id if len(channel_id) > 0 else self.channel_id
                  }

        result = self._request_api(url, params, "POST")

        return result

    def history(self, limit: int = 1000, channel_id: str = "") -> List[Dict[str, str]]:
        """
        特定のチャンネルの発言を取得する

        Args:
            channel_id: 投稿するチャンネルを指定するばあいはここにchannel_idを渡す
            limit: 取得上限を設定する。
        """

        url = "https://slack.com/api/channels.history"
        params = {'token': self.token,
                  'channel': channel_id if len(channel_id) > 0 else self.channel_id,
                  'count': limit,
                  }
        self.history_data = self._request_api(url, params, "GET")

        return self.history_data['messages']

    def _request_api(self, url: str, data: Dict, method: str = "GET"):
        header = {'Content-Type', 'application/x-www-form-urlencoded'}

        if method.lower() == "get":
            res = requests.get(url, data=data)
        elif method.lower() == "post":
            res = requests.post(url, header=header, data=data)

        res.raise_for_status()
        res_json = res.json()

        # Slack APIの実行に失敗した時、例外を返す
        if not res_json.get('ok'):
            raise SlackApiError(res_json.get('error'))

        return res_json