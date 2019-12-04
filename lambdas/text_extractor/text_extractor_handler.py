import json
import os
import uuid
import urllib
import datastore
from helper import FileHelper

def processRequest(request):

    output = ""

    print(f"request: {request}")
    bucketName = request["bucketName"]
    objectName = request["objectName"]
    documentsTable = request["documentsTable"]
    outputTable = request["outputTable"]

    print(f"Input Object: {bucketName}/{objectName}")

    ext = FileHelper.getFileExtenstion(objectName.lower())
    print(f"Extension: {ext}")

    if(ext and ext in ["jpg", "jpeg", "png", "pdf"]):
        documentId = str(uuid.uuid1())
        ds = datastore.DocumentStore(documentsTable, outputTable)
        ds.createDocument(documentId, bucketName, objectName)

        output = f"Saved document {documentId} for {bucketName}/{objectName}"
        print(output)

    return {
        'statusCode': 200,
        'body': json.dumps(output)
    }

def lambda_handler(event, context):
    print(f"event: {event}")

    request = {}
    request["bucketName"] = event['Records'][0]['s3']['bucket']['name']
    request["objectName"] = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    request["documentsTable"] = os.environ['DOCUMENTS_TABLE']
    request["outputTable"] = os.environ['OUTPUT_TABLE']

    return processRequest(request)