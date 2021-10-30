# import json
from datetime import datetime

from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import pandas_gbq
import os
import glob
import datefinder
import uuid
from google.protobuf.json_format import MessageToJson
from json import dumps, loads, JSONEncoder, JSONDecoder



credentials = service_account.Credentials.from_service_account_file(
    'tfa-global-data-system-2-f4fdc6472510.json')

project_id = 'tfa-global-data-system-2'
client = bigquery.Client(credentials=credentials, project=project_id)
# client = bigquery.Client()
table_id = 'tfa-global-data-system-2.alumni_survey.survey'
table_idversion = 'tfa-global-data-system-2.alumni_survey.survey_version'
table_idquestion = 'tfa-global-data-system-2.alumni_survey.question'
table_idanswer = 'tfa-global-data-system-2.alumni_survey.answer_choice'
table_idresponse = 'tfa-global-data-system-2.alumni_survey.response'

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
# errors = client.insert_rows_json(table_id, rows_to_insert)
# if errors == []:
#     print('SURVEY rows added')
# else:
#     print(errors)

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
        {u'survey_version_id': surverversionid, u'survey_id': 'C_002', u'partner_id': str(partnerid),
         u'survey_date': str(surverdate), u'survey_name': surveyname, u'Notes': ''}
    ]

    errorssurvey = client.insert_rows_json(table_idversion, rows_to_insertsurvey)
    if errorssurvey == []:
        print('SURVEY version rows added')
    else:
        print(errorssurvey)

    # print(dfAnswers.loc[dfAnswers['question_id'] == 'C_002_0091_0001'])
    questionjsondata = dfReadQuestion.to_json(orient='records')

    answerjsondata = dfAnswers.to_json(orient='records')

    # print(questionjsondata)
    # pandas_gbq.to_gbq(dfReadQuestion, table_idquestion, project_id=project_id, if_exists='append', credentials=credentials)

    for indexq, rowq in dfReadQuestion.iterrows():
        rows_to_insertquestion = [
            {u'question_id': dfReadQuestion.iloc[indexq, 0], u'question_wording': dfReadQuestion.iloc[indexq, 1],
             u'variable': dfReadQuestion.iloc[indexq, 2]}
        ]
        errorsquestion = client.insert_rows_json(table_idquestion, rows_to_insertquestion)
        if errorsquestion == []:
            print('SURVEY question rows added')
        else:
            print(errorsquestion)

    for indexq, rowq in dfAnswers.iterrows():
        rows_to_insertanswer = [
            {u'answer_choice_id': dfAnswers.iloc[indexq, 0], u'answer_choice_text': str(dfAnswers.iloc[indexq, 1]).strip(),
             u'question_id': dfAnswers.iloc[indexq, 2]}
        ]
        errorsanswer = client.insert_rows_json(table_idanswer, rows_to_insertanswer)
        if errorsanswer == []:
            print('SURVEY answer rows added')
        else:
            print(errorsanswer)


    lstCols = list(dfResponses.columns.values)
    responseDS = []

    for colname in lstCols:
        dataTypeObj = dfResponses.dtypes[colname]
        if dataTypeObj == 'datetime64[ns]':
            dfResponses[colname] = dfResponses[colname].astype(str)

    dataTypeSeries = dfResponses.dtypes

    dfResponses = dfResponses.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    dfAnswers = dfAnswers.apply(lambda x: x.str.strip() if x.dtype == "object" else x)


    for index, row in dfResponses.iterrows():
        uniqueid = uuid.uuid4().hex[:10]

        ij = 0

        for cols in lstCols:

            questionid = lstCols[ij]
            dataTypeObj = dfResponses.dtypes[cols]
            print(dataTypeObj)
            valuedata = ''

            if dataTypeObj == 'datetime64[ns]':
                print('hitted')
                print(dfResponses.iloc[index, ij])
                valuedata = datetime.strftime(dfResponses.iloc[index, ij], '%Y-%m-%d %H:%M:%S')

                print(valuedata)
            elif dataTypeObj == 'bool':
                if dfResponses.iloc[index, ij]:
                    print('truedata')
                    valuedata = 'true'
                else:
                    valuedata = 'false'
                print('boolvalue')
                print(valuedata)
            else:
                valuedata = dfResponses.iloc[index, ij]
                print('hitted2')
                print(valuedata)

            if pd.isna(valuedata):
                ij = ij + 1
                continue
            else:
                dfResult = dfAnswers.loc[dfAnswers['question_id'] == questionid]
                if dfResult.empty:
                    rows_to_insertresponse = [
                        {u'response_id': uniqueid, u'question_id': questionid,
                         u'answer_choice_id': 'null',
                         u'value': str(valuedata), u'survey_version_id': surverversionid}
                    ]
                    # responseDS.append([uniqueid, questionid, dfResponses.iloc[index, ij], 'null', surverversionid])
                else:
                    tempdf = pd.DataFrame()

                    tempdf = dfResult.loc[dfResult['answer_choice_text'] == dfResponses.iloc[index, ij]]
                    # if dataTypeObj == 'bool':
                    #     tempdf = dfResult.loc[dfResult['answer_choice_text'] == dfResponses.iloc[index, ij]]
                    # elif dataTypeObj == 'datetime64[ns]':
                    #     tempdf = dfResult.loc[dfResult['answer_choice_text'] == dfResponses.iloc[index, ij]]
                    # elif dfResponses.iloc[index, ij] == 'Yes' or dfResponses.iloc[index, ij] == 'No':
                    #     tempdf = dfResult.loc[dfResult['answer_choice_text'] == dfResponses.iloc[index, ij]]
                    # elif dataTypeObj == 'object':
                    #     tempvalue = str(dfResponses.iloc[index, ij]).strip()
                    #     tempdf = dfResult.loc[str(dfResult['answer_choice_text']).strip() == str(dfResponses.iloc[index, ij]).strip()]
                    #

                    if tempdf.empty:
                        rows_to_insertresponse = [
                            {u'response_id': uniqueid, u'question_id': questionid,
                             u'answer_choice_id': 'null',
                             u'value': str(valuedata), u'survey_version_id': surverversionid}
                        ]

                    else:

                        rows_to_insertresponse = [
                            {u'response_id': uniqueid, u'question_id': questionid,
                             u'answer_choice_id': tempdf.iloc[0, 0],
                             u'value': str(valuedata), u'survey_version_id': surverversionid}
                        ]


            errorsresponse = client.insert_rows_json(table_idresponse, rows_to_insertresponse)
            if errorsresponse == []:
                print('SURVEY Response rows added')
            else:
                print(errorsresponse)

            ij = ij + 1
