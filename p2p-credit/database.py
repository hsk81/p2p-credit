__author__ = "hsk81"
__date__ = "$Apr 23, 2012 10:15:15 AM$"

################################################################################
################################################################################

"""
Populates the database with random data, which we can work with. Execute some -
thing similar like below, if the existing fixtures' initial data is not
sufficient or desired:

$$ ./manage.py shell
>> import database
>> import random
>>
>> database.init (
>>     person_no = random.randint (3,3),
>>     project_no = random.randint (5,5),
>>     auction_no = random.randint (7,7),
>>     bid_no = random.randint (11,11)
>> )
"""

################################################################################
################################################################################

import people.database
import prj.database
import auction.database

################################################################################
################################################################################

def init (person_no = 3, project_no = 5, auction_no = 7, bid_no = 11):

    if person_no > 0 : people.database.init (person_no)
    if project_no > 0 : prj.database.init (project_no)
    if auction_no > 0 : auction.database.init (auction_no, bid_no)

################################################################################
################################################################################
