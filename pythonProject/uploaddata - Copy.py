from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import os
import glob
import datefinder
import uuid

credentials = service_account.Credentials.from_service_account_file(
    'surveypro-327210-483d6c7c9bb4.json')

project_id = 'surveypro'
client = bigquery.Client(credentials=credentials, project=project_id)
# client = bigquery.Client()
table_id = 'surveypro-327210.Alumni_survey.survey'
table_idversion = 'surveypro-327210.Alumni_survey.survey_version'
table_idquestion = 'surveypro-327210.Alumni_survey.question'
table_idanswer = 'surveypro-327210.Alumni_survey.answer_choice'
table_idresponse = 'surveypro-327210.Alumni_survey.response'

# gets your current directory
dirname = os.path.dirname(__file__)
# concatenates your current directory with your desired subdirectory
folderpath = os.path.join(dirname, r'Data')
# print(folderpath)
# results = os.path.join(dirname, r'Data\data.xlsx')

files = os.listdir(folderpath)
rows_to_insert = [
    {u'survey_id': 'C_002', u'survey_name': 'Alumni Survey'}
]
errors = client.insert_rows_json(table_id, rows_to_insert)
if errors == []:
    print('SURVEY rows added')
else:
    print(errors)

for file in files:
    results = os.path.join(folderpath, file)

    xls1 = pd.ExcelFile(results)
    dfReadQuestion = pd.read_excel(xls1, 'Questions (uploaded)')
    dfResponses = pd.read_excel(xls1, 'Responses (uploaded)')
    dfAnswers = pd.read_excel(xls1, 'Answer choices (uploaded)')
    dfSurvey = pd.read_excel(xls1, 'Survey version (uploaded)')
    surverversionid = dfSurvey.iloc[0, 0]
    partnerid = dfSurvey.iloc[0, 2]
    surverdate = dfSurvey.iloc[0, 3]
    surverid = dfSurvey.iloc[0, 1]
    surveyname = dfSurvey.iloc[0, 4]
    notes = dfSurvey.iloc[0, 5]

    rows_to_insertsurvey = [
        {u'survey_version_id': surverversionid, u'survey_id': 'C_002', u'partner_id': str(partnerid), u'survey_date': str(surverdate), u'survey_name': surveyname, u'Notes': ''}
    ]

    errorssurvey = client.insert_rows_json(table_idversion, rows_to_insertsurvey)
    if errorssurvey == []:
        print('SURVEY version rows added')
    else:
        print(errorssurvey)

    #print(dfAnswers.loc[dfAnswers['question_id'] == 'C_002_0091_0001'])
    questionjsondata = dfReadQuestion.to_json(orient='records')


    print(questionjsondata)


    answerjsondata = dfAnswers.to_json(orient='records')

    errorsquestion = client.insert_rows_json(table_idquestion, questionjsondata)
    if errorsquestion == []:
        print('SURVEY question rows added')
    else:
        print(errorsquestion)

    errorsanswer = client.insert_rows_json(table_idanswer, answerjsondata)
    if errorsanswer == []:
        print('SURVEY question rows added')
    else:
        print(errorsanswer)
    lstCols = list(dfResponses.columns.values)
    responseDS = []
    for index, row in dfResponses.iterrows():
        uniqueid = uuid.uuid4().hex[:10]

        ij = 0

        for cols in lstCols:

            questionid = lstCols[ij]

            valuedata = dfResponses.iloc[index, ij]
            if pd.isna(valuedata):
                ij = ij + 1
                continue
            else:
                dfResult = dfAnswers.loc[dfAnswers['question_id'] == questionid]
                if dfResult.empty:
                    responseDS.append([uniqueid, questionid, dfResponses.iloc[index, ij], 'null', surverversionid])
                else:
                    tempdf = dfResult.loc[dfResult['answer_choice_text'] == dfResponses.iloc[index, ij]]
                    if tempdf.empty:
                        responseDS.append([uniqueid, questionid, dfResponses.iloc[index, ij], 'null', surverversionid])
                    else:
                        responseDS.append(
                            [uniqueid, questionid, dfResponses.iloc[index, ij], tempdf.iloc[0, 0], surverversionid])

            #print(responseDS)

            ij = ij + 1
    dfFinal = pd.DataFrame(responseDS, columns=["response_id", "question_id", "value", "answer_choice_id", "survey_version_id"])
    responsejsondata = dfFinal.to_json(orient='records')

    errorsresponse = client.insert_rows_json(table_idresponse, responsejsondata)
    if errorsresponse == []:
        print('SURVEY response rows added')
    else:
        print(errorsresponse)

    # temp1 = df1.iloc[3, 0]
    # matches = datefinder.find_dates(temp1)
    # for match in matches:
    #     print(match)
    # jsondata = df1.to_json(orient='records')
    # print(jsondata)

    # rows_to_insert = [
    #     {u'survey_id':'C_002_0091', u'survey_name':'Cambodia-2021'}
    # ]

# xls1 = pd.ExcelFile(results)
# df1 = pd.read_excel(xls1, 'Responses')
# jsondata = df1.to_json(orient='records')
# print(jsondata)


# errors = client.insert_rows_json(table_id, rows_to_insert)
# if errors == []:
#     print('rows added')
# else:
#     print(errors)


# print(results)
#
# xls1 = pd.ExcelFile(results)
# df1 = pd.read_excel(xls1, 'Responses')
# print(df1)
#
# PROJECT = 'surveypro'
# DATASET = 'Alumni_survey'
#
# table = bq_client.get_table("{}.{}.{}".format(PROJECT, DATASET, TABLE))
# df = pd.read_excel(results)
# print(df)
