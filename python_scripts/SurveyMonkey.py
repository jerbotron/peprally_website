import json
import requests


class SurveyMonkey:
	#the location of the email part in the survey
	EMAIL_ANSWER_INDEX = 3; #the position of the field that contains the email ? 
	EMAIL_QUESTION_ID = '997420484'
	
	#hardcoded variables and endpoints
	PEP_RALLY_SURVEY_ID = '83094749'
	API_KEY = "nukeru4m4s3ch73pfhpwsawm"
	ACCESS_TOKEN = "aLDNio953G3ThNP3llk6VW3lVak1w1BrUgyJjUwOZZBPZWe3a7pnxPS0cdEJ5HL.z0XBuU.bS6GOWTLEgqdhiaoMKATcrTWRSyVtSR5pswyeGPcZXwMjzLNX326YXd6hsmvLF-tCPHBbcJ262pQRW1u3ln60xW8EO5BGFP5bD.fwpWi5YiSXIcQvmrQAT8EFlKkQBQJwSLAPWz8hBVQx2jX1Tz42d3cva93-BUMqO7Y="
	HOST = "https://api.surveymonkey.net"
	respondent_uri = "{}/v2/surveys/get_respondent_list".format(HOST)
	response_uri = "{}/v2/surveys/get_responses".format(HOST)
	survey_details_uri = "{}/v2/surveys/get_survey_details".format(HOST)
	survey_list_uri = "{}/v2/surveys/get_survey_list".format(HOST)

	def __init__(self):
		self.client = requests.session()
		self.client.headers = {
		    "Authorization": "bearer {}".format(self.ACCESS_TOKEN),
		        "Content-Type": "application/json",
			}
		self.client.params = {
		    "api_key": self.API_KEY
		    }

	#get a list of surveys and parse the json object to return them
	#returns a list of surveys in an array
	def list_surveys(self):
		data = {};
		response = self.client.post(self.survey_list_uri,data=json.dumps(data))
		jres = response.json()
		return jres['data']['surveys']
		
	#the format of the date is YYYY-MM-DD HH:MM:SS) 
	def get_respondents(self,survey_id=None,page=None,last_modified_date=None):
		if survey_id is None:
			survey_id = self.PEP_RALLY_SURVEY_ID
		post_data = {}
		post_data['survey_id'] = survey_id
		post_data['fields'] = ["date_modified","status"]
		if page is not None:
			post_data["page"] = page
		if last_modified_date is not None:
			post_data["start_modified_date"] = last_modified_date
		response = self.client.post(self.respondent_uri,data=json.dumps(post_data))
		jres = response.json()
		return jres['data']['respondents'] if 'data' in jres else 'omg error'
		#raise Exception("request to get all respondents failed. Response was {}".format(response))

	#returns an array of responses?
	#each one corresponds to a given respondent id 
	#the ['respondent_ids'] parameter can only contain up to a max of 100 ids
	def get_responses(self,respondent_ids,survey_id=None):
                if survey_id is None:
                        survey_id = self.PEP_RALLY_SURVEY_ID
		post_data = {}
		post_data['survey_id'] = survey_id
		post_data['respondent_ids'] = respondent_ids
		jres = self.client.post(self.response_uri,data=json.dumps(post_data)).json()
		return jres['data']

	#given the single response json, extract the email from it
	#return None if email could not be found
	def get_email_from_response(self,response_json):
		email = None;
		for question in response_json['questions']:
			if (question['question_id'] == self.EMAIL_QUESTION_ID):
				email = question['answers'][self.EMAIL_ANSWER_INDEX]['text']
		return email if email is not None else 'could not find email!'
