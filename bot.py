import os
from time import sleep
import logging
from datetime import datetime, timedelta
import random

import json

from dotenv import load_dotenv
from mastodon import (
    Mastodon,
    MastodonAPIError,
    MastodonNetworkError,
    MastodonRatelimitError,
)
import pytz
import toaster

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

MIN_TIME_BETWEEN_ANNOUNCEMENTS_MINUTES = int(
    os.environ.get("MIN_TIME_BETWEEN_ANNOUNCEMENTS_MINUTES", 15)
)
UPDATE_INTERVAL_SECONDS = int(os.environ.get("UPDATE_INTERVAL_SECONDS", 10))


def generate_random_interval():
    return MIN_TIME_BETWEEN_ANNOUNCEMENTS_MINUTES + (random.random() * 60 * 24)


class TalkieToasterBotException(Exception):
    pass


class TalkieToasterBot:
    STATE_FILENAME = os.environ.get("STATE_FILE", "state.json")

    def __init__(self, mastodon):
        self.current_followers = set()
        self.mastodon = mastodon
        self.replied_toots = set()
        self.me = mastodon.me()
        self.last_notification_seen_id = 0
        self.init_datetime = datetime.now(tz=pytz.UTC)

    def get_initial_state(self):
        self.current_followers = self._get_my_followers()
        self.load_state()

    def load_state(self):
        if os.path.exists(self.STATE_FILENAME):
            with open(self.STATE_FILENAME, "r") as f:
                state = json.load(f)
                self.last_notification_seen_id = state["last_notification_seen_id"]

    def save_state(self):
        with open(self.STATE_FILENAME, "w") as f:
            state = dict(last_notification_seen_id=self.last_notification_seen_id)
            state = json.dump(state, f)

    def _call_mastodon(self, action, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except MastodonAPIError as e:
            raise TalkieToasterBotException(f"Couldn't {action} due to a API error {e}")
        except MastodonNetworkError as e:
            raise TalkieToasterBotException(
                f"{action} failed due to a network error: {e}"
            )
        except MastodonRatelimitError as e:
            logger.error(f"{action} got ratelimited! Back off!")
            sleep(30)
            raise TalkieToasterBotException("Rate limited")

    def _get_my_followers(self):
        followers = self.mastodon.account_followers(self.me)
        if followers != None:
            return set([follower["acct"] for follower in followers])
        else:
            raise TalkieToasterBotException("Couldn't get list of followers")

    def _get_new_followers(self):
        refreshed = self._get_my_followers()
        new_followers = refreshed - self.current_followers
        self.current_followers = refreshed
        return new_followers

    def process_notifications(self):
        notifications = self._call_mastodon(
            "get_my_notifications",
            self.mastodon.notifications,
            types=["mention", "follow"],
            min_id=self.last_notification_seen_id,
        )
        if len(notifications):
            logger.info(f"Retrieved {len(notifications)} notifications")
        highest_id = 0
        for notification in notifications:
            if notification["created_at"] < (self.init_datetime - timedelta(hours=1)):
                logger.debug(
                    f"Skipped notification {notification['id']} as it was created over an hour before we started {notification['created_at']}"
                )
                highest_id = max(highest_id, notification["id"])
                continue
            if (
                notification["type"] == "mention"
                and len(notification["status"]["mentions"]) == 1
            ):
                logger.info(f"Replying to {notification['account']['acct']}")
                self._call_mastodon(
                    "reply_to_mention",
                    self.mastodon.status_reply,
                    notification["status"],
                    f"{toaster.retort_offer_of_toast()}",
                    untag=True,
                )
                self.replied_toots.add(notification["status"]["id"])
            elif notification["type"] == "follow":
                logger.info(f"Greeting {notification['account']['acct']}")
                self._call_mastodon(
                    "greet_follower",
                    self.mastodon.toot,
                    f"@{notification['account']['acct']} {toaster.greet()} {toaster.directed_offer_of_toast()}?",
                )
            highest_id = max(highest_id, notification["id"])
        self.last_notification_seen_id = max(self.last_notification_seen_id, highest_id)

    def announce_request_for_toast(self):
        offer = toaster.general_offer_of_toast()
        logger.info(f"Tooting this: {offer}")
        self._call_mastodon("ask_for_toast", self.mastodon.toot, offer)


def main():
    toaster_bot = TalkieToasterBot(
        Mastodon(
            access_token=os.getenv("SECRET_TOKEN"), api_base_url=os.getenv("BASE_URL")
        )
    )
    toaster_bot.get_initial_state()
    sleep(5)
    print("BOOT UP SEQUENCE INITIATED")
    sleep(1)
    print("VISUAL SYSTEM: CCD 517.3")
    sleep(1)
    print("ARTIFICIAL INTELLIGENCE SYSTEM: K177")
    sleep(1)
    print("MACHINE IDENT: TALKIE TOASTER")
    print("MAUFACTURER: CRAPOLA Inc TAIWAN")
    print("RECOMMENDED RETAIL PRICE: $£19.99 PLUS TAX")
    sleep(1)
    print("AURAL SYSTEM: ONLINE")
    sleep(1)
    print(toaster.general_offer_of_toast())
    sleep(1)
    time_of_next_announcement = datetime.now() + timedelta(minutes=30)
    while True:
        if time_of_next_announcement < datetime.now():
            try:
                logger.info("It's time to announce")
                toaster_bot.announce_request_for_toast()
                time_of_next_announcement = datetime.now() + timedelta(
                    minutes=generate_random_interval()
                )
                logger.info(f"Announcing again at {time_of_next_announcement}")
            except TalkieToasterBotException as e:
                logger.error(f"Error asking for toast: {e}")
        try:
            logger.debug("Getting my notifications")
            toaster_bot.process_notifications()
        except TalkieToasterBotException as e:
            logger.error(f"Couldn't process notifications: {e}")
        toaster_bot.save_state()
        sleep(UPDATE_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
