import json
import bwdt.lib.aws.apigateway as ag
result = ag.post(
    key_id='AKIA4L2WHQDNQFKQMEYM',
    secret_key='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',
    region='ca-central-1',
    host='42mydti3lg.execute-api.ca-central-1.amazonaws.com',
    body={'name': 'THIS GUY, EH'},
    uri='/test',
    query='')

    #body={'name': 'THIS GUY'},

#print('####################')
#print('####################')
#print('####################')

from pprint import pprint
pprint(json.loads(result.text))


result2 = ag.get(
    key_id='AKIA4L2WHQDNQFKQMEYM',
    secret_key='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',
    region='ca-central-1',
    host='42mydti3lg.execute-api.ca-central-1.amazonaws.com',
    uri='/test',
    query='')


pprint(json.loads(result2.text))
