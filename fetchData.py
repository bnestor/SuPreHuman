"""
fetchData.py

collect reddit data according to api rules
"""
#import numpy as np
#import pandas as pd
#import h5py
import os
import praw

def main():
    """
    """
    with open('info.txt', 'rb') as f:
        lines=f.readlines()
        username=lines[0].decode().strip().replace("_", "")
        password=lines[1].decode().strip()
        client_id=lines[2].decode().strip()
        client_secret=lines[3].decode().strip()

    # name=input("Reddit Username: ")
    reddit = praw.Reddit(user_agent='Windows10:fetchData:v1.0 (by /u/{})'.format(username),
                     client_id=client_id, client_secret=client_secret, username=username, password=password)
    print(reddit.read_only)
    print(reddit.user.me())

    #connect
    # submission = reddit.submission(url='https://www.reddit.com/r/funny/comments/3g1jfi/buttons/')
    #
    # submission.comments.replace_more(limit=None)
    # for top_level_comment in submission.comments:
    #     print(top_level_comment.body)

    # for submission in reddit.subreddit('learnpython').hot(limit=10):
    #     print(submission.title)


    subreddit = reddit.subreddit('SuicideWatch')
    conversedict={}
    hot_python=subreddit.hot(limit=1000)
    # df=pd.DataFrame(columns=['Content', 'Parent'])


    with open("output.txt", 'wb') as f:
        for submission in hot_python:
            # print(submission)
            if not submission.stickied:
                print('Title: {}, ups: {}, downs: {}, Have we visited?: {}, subid: {}'.format(submission.title,submission.ups,submission.downs,submission.visited, submission.id))
                print('created:{}, distinguished:{}, edited:{},num_comments:{}, score:{}, upvote_ratio:{}'.format(submission.created_utc, submission.distinguished, submission.edited, submission.num_comments, submission.score, submission.upvote_ratio))
                f.write(35*"-".encode()+"\r\n".encode())
                f.write('subid: {}, Title: {}, author:{}, ups: {}, downs: {}, Have we visited?: {}'.format(submission.id, submission.title,submission.author, submission.ups,submission.downs,submission.visited).encode())
                # f.write("\n".encode())
                f.write(' created:{}, distinguished:{}, edited:{},num_comments:{}, score:{}, upvote_ratio:{}\r\n'.format(submission.created_utc, submission.distinguished, submission.edited, submission.num_comments, submission.score, submission.upvote_ratio).encode())
                f.write('OPbody:{}\r\n'.format(submission.selftext.replace('\n',"").replace('\r',"").replace('&#x200B',"")).encode())
                # f.write("\n".encode())
                # author, clicked, comments, created_utc, distinguished, edited, id, is_video,
                # print(dir(submission))

                # link_flair_css_class, link_flair_text, locked, num_comments, over_18, permalink, score,
                # selftext, stickied, subreddit, subreddit_id, title, upvote_ratio
                submission.comments.replace_more(limit=0)
                print(submission)
                for comment in submission.comments.list():
                    # print(dir(comment))
                    f.write('id:{}, comment author:{}, body:{}, ups:{}, downs:{}, parent:{}\r\n'.format(comment.id, comment.author, comment.body,  comment.ups, comment.downs, comment.parent()).encode())
                    # f.write("\n".encode())
                    if comment.id not in conversedict.keys():
                        conversedict[comment.id]=[comment.body, {}]
                        if comment.parent()!=submission.id:
                            parent=str(comment.parent())
                            conversedict[parent][1][comment.id]=[comment.ups, comment.body]

    for post_id in conversedict.keys():
        message = conversedict[post_id][0]
        replies = conversedict[post_id][1]
        if len(replies) > 0:
            print("\n")
            print(35*'-')
            print('Original Message: {}'.format(message))
            # print(35*'-')
            print('Replies:')
            for reply in replies:
                print(replies[reply])

    # print(conversedict)
    # for item in conversedict.keys():
    #     print(item, conversedict[item])
    #     print("\n")



if __name__=="__main__":
    main()
