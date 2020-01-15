import os, json
import boto3
import time
from create_logo import create_logo
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def watch_requests():
    session = boto3.Session(
        aws_access_key_id = os.getenv("AWS_ACCESS"),
        aws_secret_access_key = os.getenv("AWS_SECRET"),
        region_name='us-west-2'
    )
    s3 = session.resource('s3')
    watch_requests_directory(s3)

def watch_requests_directory(s3):
    bucket = s3.Bucket(os.getenv('S3_BUCKET_NAME'))
    while True:
        print('--- WATCHING REQUESTS DIRECTORY ---')

        # List and iterate overr all objects in requests bucket
        for object in bucket.objects.filter(Prefix='requests/'):
            if '.json' in object.key:
                file_data = json.loads(object.get()['Body'].read().decode('utf-8'))
		try:
                    logo_result = process_request(file_data)
                except:
		    print("Error Processing -- Moving to Processed")
	            move_to_processed(s3, file_data['filename'])

                if logo_result['result'] == True:
                    print('--- LOGO CREATED --')
                    print('Location: %s' % logo_result['filepath'])
                    # Upload File to S3
                    upload_to_s3(s3, logo_result['filepath'], file_data['filename'])
                else:
                    print('--- LOGO COULD NOT BE CREATED --')
                move_to_processed(s3, file_data['filename'])
        time.sleep(8)

def process_request(file_data):
    logo_generated = False

    print('--- Request Found ---')
    print("FILENAME: %s \nColor: %s \nTAGS %s, %s\n" % (file_data['filename'], file_data['color'], file_data['tag1'], file_data['tag2'] ))

    print("--- CREATING LOGO ---")
    start_time = time.time()
    print('time %s' % start_time)
    create_logo([file_data['tag1'], file_data['tag2']], file_data['color'], file_data['filename'])

    while logo_generated == False:
        print('--- WAITING FOR LOGO ---')

        # CHECK FOR FILE EXISTANCE
        print('Looking for order %s' % os.getenv('LOCAL_IMAGE_STORAGE_PATH')+'/'+file_data['filename']+'.png')
        logo_generated = os.path.exists("%s/%s.png" % (os.getenv('LOCAL_IMAGE_STORAGE_PATH'), file_data['filename']))
        print('LOGO GENERATED: %s' % logo_generated)

        # If time is expired and file not found then
        # we can exit
        if int(time.time() - start_time) > 60 and logo_generated == False:
            print('--- TIMEOUT REACHED ---')
            break

        # Sleep between Searches
        time.sleep(3)

    return {
            'result': logo_generated,
            'filepath': "%s/%s.png" % (os.getenv('LOCAL_IMAGE_STORAGE_PATH'), file_data['filename'])
            }

def upload_to_s3(s3, filepath, filename):
    print('--- UPLOAD TO RESULTS --')
    s3.Bucket(os.getenv('S3_BUCKET_NAME')).upload_file(filepath, 'results/%s.png' % filename, ExtraArgs={'ContentType': 'image/png'})

def move_to_processed(s3, filename):
    print('--- COPY ORDER TO PROCESSED --')
    # Copy object A as object B
    s3.Object(os.getenv('S3_BUCKET_NAME'), 'processed/%s.json' % filename).copy_from(CopySource = os.getenv('S3_BUCKET_NAME')+'/requests/%s.json' % filename)
    # Delete the former object A
    print('--- DELETE ORDER FROM REQUESTS --')
    s3.Object(os.getenv('S3_BUCKET_NAME'), 'requests/%s.json' % filename).delete()

watch_requests()
