import people.database
import prj.database
import auction.database

def init (person_no = 3, project_no = 5, auction_no = 7, bid_no = 11):

    if person_no > 0  : people.database.init (person_no)
    if project_no > 0 : prj.database.init (project_no)
    if auction_no > 0 : auction.database.init (auction_no, bid_no)
