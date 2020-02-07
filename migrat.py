import json
import tilda as t
import boto3
import botocore
import botocore.exceptions as bce
from botocore.vendored import requests as dow

def migrat():
    for n in t.project.css:
        # pulling file name from the url
        upload_name = n.split('/')[-1]
        try:
            # file existence check
            if client.get_object(Bucket = bucket, Key = upload_name):
			    print '\n' + upload_name + 'already exists\n'
        # catch no file error
        except client.exceptions.NoSuchKey:    
            # saving the contents to a string
            response = dow.get(n)
            css = response.content
            # pushing files to s3 bucket
            try:
                client.put_object(Bucket = bucket, Key = upload_name, Body = css, ContentType = 'text/css')
                client.put_object(Bucket = bucket, Key = 'blog/' + upload_name, Body = css, ContentType = 'text/css')
                client.put_object(Bucket = bucket, Key = 'services/' + upload_name, Body = css, ContentType = 'text/css')
                print '\npushed ' + upload_name + '\n'
            # catch empty body error
            except bce.ParamValidationError:
                print '\ncouldn`t upload ' + upload_name + '\n'
        # catch empty name error
        except bce.ParamValidationError:
            print '\n' + upload_name + ' is empty\n'
	print '\nAll css are pushed\n'

    for n in t.project.js:
        # pulling file name from the url
        upload_name = n.split('/')[-1]
        try:
            # file existence check
            if client.get_object(Bucket = bucket, Key = upload_name):
				print upload_name + 'already exists\n'
        # catch no file error
        except client.exceptions.NoSuchKey:    
            # saving the contents to a string
            response = dow.get(n)
            js = response.content
            # pushing files to s3 bucket
            try:
                client.put_object(Bucket = bucket, Key = upload_name, Body = js, ContentType = 'text/js')
                client.put_object(Bucket = bucket, Key = 'blog/' + upload_name, Body = js, ContentType = 'text/js')
                client.put_object(Bucket = bucket, Key = 'services/' + upload_name, Body = js, ContentType = 'text/js')
                print 'pushed ' + upload_name + '\n'
            # catch empty body error
            except bce.ParamValidationError:
                print 'couldn`t upload ' + upload_name + '\n'
        # catch empty name error
        except bce.ParamValidationError:
            print upload_name + ' is empty\n'
	print 'All js are pushed\n'

    page_counter = 0
    for n in t.pages :
        t.page = t.api.get_page_full_export(page_id = t.pages[page_counter].id)
        try:
            # checks if file exists in the bucket and uploads it of not
            if client.get_object(Bucket = bucket, Key = t.page.alias):
				print t.page.alias + 'already exists\n'
        # catch no file error
        except client.exceptions.NoSuchKey:
            try:
                client.put_object(Bucket = bucket, Key = t.page.alias, Body = t.page.html, ContentType = 'text/html')
                print 'pushed ' + t.page.alias + '\n'
            # catch empty body error
            except bce.ParamValidationError:
                print t.page.alias + '`s html code is empty\n'
        # catch empty name error
        except bce.ParamValidationError:
            print t.page.alias + '`s name is empty\n'

        for n in t.page.images:
            # pulling file name from the url
            upload_name = n['to']
            try:
                if client.get_object(Bucket = bucket, Key = upload_name):
					print upload_name + 'already exists\n'
            # catch no file error and then push to s3
            except client.exceptions.NoSuchKey:
                # determine image extension
                image_format = n['from'].split('.')[-1]
                if image_format == 'svg':
                    image_format = 'svg+xml'
                # saving the contents to a string
                response = dow.get(n['from'])
                image = response.content
                try:
                    client.put_object(Bucket = bucket, Key = upload_name, Body = image, ContentType = 'image/' + image_format)
                    client.put_object(Bucket = bucket, Key = 'blog/' + upload_name, Body = image, ContentType = 'image/' + image_format)
                    client.put_object(Bucket = bucket, Key = 'services/' + upload_name, Body = image, ContentType = 'image/' + image_format)
                    print 'pushed ' + upload_name + '\n'
                # catch empty body error
                except bce.ParamValidationError:
                    print image + ' is an empty image\n'
            # catch empy name error
            except bce.ParamValidationError:
                print upload_name + '`s name is empty\n'
        page_counter += 1

def notificator():
	webhook_url = 'https://hooks.slack.com/services/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'
	slack_data = {
    'text': 'Hi, there. Glad to notify you, that the amazon bucket has been successfuly updated. Have a nice day!'
	}

	response = dow.post(
    webhook_url, data = json.dumps(slack_data),
    headers={'Content-Type': 'application/json'}
	)

	if response.status_code != 200:
		raise ValueError(
    	'Request to Slack returned an error %s, the response is:\n%s'
        	%(response.status_code, response.text)
    )

# connecting to tilda api and aws s3 service
t.api = t.Client(public='xxxxxxx', secret='xxxxxxx')
t.projects = t.api.get_projects_list()
t.project = t.api.get_project(project_id=xxxxxx)
t.pages = t.api.get_pages_list(project_id=xxxxxx)
session = botocore.session.get_session()
client = session.create_client('s3')
bucket = 'xxxxx-website'

migrat()
notificator()