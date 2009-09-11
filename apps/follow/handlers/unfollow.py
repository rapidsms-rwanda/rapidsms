#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from apps.handlers import KeywordHandler
from rapidsms.search import find_objects
from apps.follow.utils import followable_models


class FollowHandler(KeywordHandler):
    keyword = "unfollow|unwatch"

    def help(self):
        self.respond("To stop following something, send UNFOLLOW <NAME>")

    def handle(self, text):

        to_unfollow = find_objects(
            followable_models(),
            text)

        for obj in to_unfollow:
            try:
                obj.followers.get(**self.msg.persistance_dict).delete()

            except obj.DoesNotExist:
                pass

        if to_unfollow:
            self.respond(
                "You are no longer following: %s" %
                (", ".join(map(unicode, to_unfollow))))

        else:
            self.respond("Sorry, I couldn't understand what you want to stop following.")
