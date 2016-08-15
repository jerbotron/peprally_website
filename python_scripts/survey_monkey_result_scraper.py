
#script that gets responses from survey monkey and updates dynamo with the latest responses
#can pass in a date and then the script only looks for responses that were completed after that
#given date

import argparse
from SurveyMonkey import *
from PepRallyDynamoDB import *

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--last_modified_date', default='2016-08-01 00:00:00')

args = parser.parse_args()
survey_monkey = SurveyMonkey()
#max_modified_respondent_date = args.last_modified_date
sm_dynamo_db = PepRallyDynamoDB()

respondents_cur_page = 1
while True:
    print 'searching for respondents with date after {} and current page {}'.format(args.last_modified_date,respondents_cur_page)
    respondent_json = survey_monkey.get_respondents(last_modified_date=args.last_modified_date,page=respondents_cur_page)
    if len(respondent_json) == 0:
	print 'no more respondents to get...terminating script!'
        break

    respondent_ids = []
    for respondent in respondent_json:
        # keep track of the max modified date - not needed anymore b/c of how script works
        #if respondent["date_modified"] > max_modified_respondent_date:
        #    max_modified_respondent_date = respondent["date_modified"]

        # only want finished responses
        if respondent["status"] == "completed":
            respondent_ids.append(respondent["respondent_id"])

    # get_responses can only take in 100 respondent_ids, we need to
    # batch these requests in chunks of 100
    print "Got {} respondents back. Calling the get responses API now...".format(len(respondent_ids))
    start_pos = 0
    respondent_count = len(respondent_ids)
    while start_pos < respondent_count:
        batch_respondent_ids = respondent_ids[start_pos:start_pos + 100]
	sm_responses = survey_monkey.get_responses(batch_respondent_ids)
        for response in sm_responses:
	    #extract the email and then save it in dynamo
	    email = survey_monkey.get_email_from_response(response)
	    print 'Writing entry for respondent_id: {} to the db'.format(response['respondent_id'])
	    sm_dynamo_db.write_survey_results(response['respondent_id'],args.last_modified_date,email,response)
        start_pos += 100
    print('Current iteration finished. Increasing page num...')
    respondents_cur_page += 1


