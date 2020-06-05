import argparse
from functions import scrap_thread, scrap_forum
 
parser=argparse.ArgumentParser(description="Tool for scraping posts from the toribash forum")
group = parser.add_mutually_exclusive_group()
group.add_argument('-f', nargs=3, help="scrapes all the threads in a forum and saves it in /output/(forumname)  |  usage: -f (from page) (to page)", type=int)
group.add_argument('-t', nargs=3, help="scrapes all the posts in a thread and saves it in /output/threads  |  usage: -f (from page) (to page)", type=int)
parser.add_argument('-json', nargs='?', help="writes json dicts in the txt output", default='heysa')
parser.add_argument('-posts_by', help='saves only the posts of the User passed as argument')

args=parser.parse_args()
print(args.json)
scrap_forum(297,posts_by="DarkScorpion", json=args.json)

