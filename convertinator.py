import argparse
import datetime
import json
import re
import sys
import time
from collections import Counter

import praw

import credentials
from units import units


def init_praw():
    return praw.Reddit(
        client_id=credentials.REDDIT_CLIENT_ID,
        client_secret=credentials.REDDIT_SECRET_KEY,
        password=credentials.REDDIT_PASSWORD,
        username=credentials.REDDIT_USERNAME,
        user_agent="TheConvertinator: Metric Conversion Bot"
    )


def get_existing_comment_ids(reddit=None):
    # Get a list of IDs of comments we've already replied to
    if reddit is None:
        reddit = init_praw()

    me = reddit.user.me()
    my_comments = me.comments.new(limit=None)
    comment_ids = [
        comment.parent().id for comment in my_comments
        if type(comment.parent()) is praw.models.reddit.comment.Comment
    ]

    return comment_ids


def deduplicate_measurements(measurements):
    count = Counter((i[0]) for i in measurements)
    out = [i for i in measurements if count[i[0]] == 1]
    return out


def strip_urls(comment_text):
    return re.sub(r'https?:\/\/.*[\r\n]*', '', comment_text, flags=re.MULTILINE)


def get_imperial_measurements(comment_body, min_matches=1):
    comment_body = strip_urls(comment_body).replace(',', '')
    measurements = []
    for regex in units:
        matches = re.findall(regex['regex'], comment_body, re.MULTILINE)
        for match in matches:
            measurements.append((match[0], regex))

    ret = deduplicate_measurements(measurements)

    if len(ret) >= min_matches:
        return ret
    else:
        return []


def convert_to_metric_old(quantity, unit):
    new_unit = ureg(units[unit])
    orig_quantity = float(quantity) * ureg(unit)
    converted = orig_quantity.to(new_unit).to_tuple()
    return converted[0], converted[1][0][0]


def process_comment(comment):
    imperial_measurements = get_imperial_measurements(comment.body, min_matches=2)
    if len(imperial_measurements) > 0:
        comment_text = "Hi, I'm a bot! Here are metric conversions of the imperial units found in your comment:\n\n"

        for quantity, matched_regex in imperial_measurements:
            try:
                metric_quantity, metric_unit = matched_regex['convert_function'](quantity, matched_regex['from_unit'], matched_regex['to_unit'])
                comment_text += "* {} {} ~= {:.2f} {}\n\n".format(
                    quantity, matched_regex['from_symbol'],
                    metric_quantity, matched_regex['to_symbol']
                )
            except Exception as e:
                print("Error!")
                print(e)
                print(comment.body)

        comment_text += "\n\nI hope this was helpful. DM me if there were any problems!\n\n"
        comment_text += "*TheConvertinator*"

        return comment_text, len(imperial_measurements)
    else:
        return None, 0


def run_on_subreddit(subreddit_name, list_function, limit=30, dryrun=False, do_logging=False, reddit=None):
    if not reddit:
        reddit = init_praw()

    subreddit = reddit.subreddit(subreddit_name)
    comments_to_make = []
    replied_comment_ids = get_existing_comment_ids(reddit)

    for submission in getattr(subreddit, list_function)(limit=limit):
        all_comments = submission.comments.list()
        print("Submission: {} [{} comments] {}".format(submission.title, len(all_comments), submission.url))
        i = 0
        for comment in all_comments:
            if not type(comment) is praw.models.reddit.comment.Comment:
                continue

            if comment.id in replied_comment_ids:
                print("Found a comment we've already replied to")
                continue

            comment_text, num_measurements = process_comment(comment)
            if comment_text:
                comments_to_make.append((comment, comment_text, num_measurements))
                i += 1

        if i > 0:
            print("{} comments with units found!".format(i))

    for parent_comment, comment_text, num_measurements in sorted(comments_to_make, key=lambda x: x[0].score, reverse=True):
        print("----")
        print(comment_text)
        print("----")
        if not dryrun:
            # TODO: Reply to the comments
            print("Posting comment reply...")
            try:
                parent_comment.reply(comment_text)
                time.sleep(2)
            except Exception as e:
                print("Got an exception: {}".format(e))
                time.sleep(2)

    if do_logging:
        logfile_name = 'runlog_{}_{}.json'.format(
            subreddit_name,
            datetime.datetime.now().strftime('%Y%m%d-%H%M'))

        with open(logfile_name, 'w') as logfile:
            json.dump({
                "log": [
                    {
                        'parent_text': parent_comment.body,
                        'parent_id': parent_comment.id,
                        'reply_text': comment_text
                    }
                    for parent_comment, comment_text in comments_to_make
                ]
            }, logfile)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="The Convertinator")
    parser.add_argument('subreddit', type=str, nargs=1,
                        help="The name of the subreddit to process")
    parser.add_argument('list_name', type=str, nargs=1,
                        help="Which list to process (new, hot, rising etc.)")
    parser.add_argument('count', type=int, nargs='?', default=30,
                        help="How many submissions to get")
    parser.add_argument('--dryrun', action='store_true')
    parser.add_argument('--log', action='store_true')

    namespace = parser.parse_args(sys.argv[1:])
    run_on_subreddit(
        namespace.subreddit[0],
        namespace.list_name[0],
        limit=namespace.count,
        dryrun=namespace.dryrun,
        do_logging=namespace.log
    )
