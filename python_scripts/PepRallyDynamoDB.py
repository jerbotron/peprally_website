import boto.dynamodb2
from boto.dynamodb2.table import Table
from boto.dynamodb2.exceptions import ConditionalCheckFailedException

class PepRallyDynamoDB:

	#hardcoded variables
	AWS_REGION = "us-east-1"
	SURVEY_RESULTS_TABLE = "SurveyResults"

	def __init__(self):
		#keys found in ~/.aws/credentials file with profile pep-rally
		self.conn = boto.dynamodb2.connect_to_region(self.AWS_REGION,profile_name="pep-rally")
		self.conn.list_tables()	
		self.survey_table = Table(self.SURVEY_RESULTS_TABLE,connection=self.conn)

	#hashkey is RESPONDENT_ID
	#rangekey is DATE_MODIFIED
	def write_survey_results(self,respondent_id,date_modified,email,raw_json=None):
		item_data = {}
		item_data['RESPONDENT_ID'] = respondent_id
		item_data['DATE_EXTRACTED'] = date_modified
		item_data['EMAIL_ADDRESS'] = email
		if raw_json is not None:
			item_data['raw_response'] = raw_json
		try: 
			self.survey_table.put_item(data=item_data)
		except ConditionalCheckFailedException,e:
			print 'Respondent_id: {} already exists in the db!'.format(respondent_id)
			#print e
