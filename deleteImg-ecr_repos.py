import boto3
import botocore
from botocore.config import Config
from datetime import datetime
import re

from CmdConfigParser import AWSCliArgs

def connectECRClient(aws_region, access_key_id, secret_access_key):

	try:
		ecr_client = boto3.client(
			'ecr', aws_access_key_id = access_key_id, 
			aws_secret_access_key = secret_access_key, region_name = aws_region)
		return ecr_client
		# print (ecrClient)
	except e:
		print ("Error:\n", e)
		exit(0)

def getListOfImages(ecr_client, repository):
	print ("Listing all the images of repository: ", repository)
	response = ecr_client.list_images(
		repositoryName = repository,
	)
	return response['imageIds']

def descibeImages(ecr_client, repository):
	print ("Listing all the images of repository: ", repository)
	try:
		response = ecr_client.describe_images(
			repositoryName = repository,			
		)
		return response['imageDetails']
		# print ("Response Info: ", response['imageDetails'])
	except:
		print ("Unable to fetch the Image description.")
		exit(0)

def deleteECRImage(ecr_client, repository, imageTagNameArr, imageDigest):
	print ("Deleteing image having Digest: ", imageDigest, "\n")

	try:
		response = ecr_client.batch_delete_image(
			repositoryName = repository,
			imageIds=[
				{
					"imageDigest": imageDigest
				},
			]
		)
		# print ("Delete action response:\n", response['imageIds'])
		print ("--------------------------------------------------------------------------------------------")
		return response['imageIds']
		# print ("Response Info: ", response['imageDetails'])
	except botocore.exceptions.ClientError as error:
		print ("Unable to delete the Image from the ECR.", error)
		exit(0)


def main():

	missingInput = ''

	cmdArgs = AWSCliArgs()
	cmdArgs.setCLIArgs()
	missingInput = cmdArgs.verifyCmdArgs()

	if (missingInput != ''):
	    print ("Missing:",missingInput)
	    sys.exit(-1)

	inputValues = cmdArgs.CLIargs

	aws_region       	= inputValues['Location']
	access_key_id      	= inputValues['AccessKey']
	secret_access_key   = inputValues['SecretKey']
	repository   		= inputValues['Repository']
	

	# numberOfDays = 5
	validTagsRegEx = ["latest*", "prev*"]
	# repository = "econ-github-actions-test"

	oldImages = []
	ecr_client = connectECRClient(aws_region, access_key_id, secret_access_key)
	
	imageListRepo = descibeImages(ecr_client, repository)
	totalImages = len(imageListRepo)

	imageListToDelete = []
	imagesToSave = []
	i = 0
	
	if totalImages > 0:
		while i < totalImages:			
			imageTagName = ""
			imageDetailsObj = {}

			# for imageInfo in imageListRepo:
			if 'imageTags' in imageListRepo[i].keys():

				res = {k:[j  for j in imageListRepo[i]['imageTags'] if re.match(k,j)] for k in validTagsRegEx }

				if ((len(res["latest*"]) > 0) or (len(res["prev*"]) > 0)):
					# print ("Found the image with build tag", validTagsRegEx)
					print ("Build ", imageListRepo[i]['imageTags'], " will not be deleted as has a latest/prev tag associated")
					imageDetailsObj['imageTag'] = imageListRepo[i]['imageTags']
					imageDetailsObj['imageDigest'] = imageListRepo[i]['imageDigest']

					imagesToSave.append(imageDetailsObj)

				else:
					print ("Build ", imageListRepo[i]['imageTags'], " can be deleted. It's an old build ")
					imageDetailsObj['imageTag'] = imageListRepo[i]['imageTags']
					imageDetailsObj['imageDigest'] = imageListRepo[i]['imageDigest']

					imageListToDelete.append(imageDetailsObj)

					imageTagName = imageListRepo[i]['imageTags']
					# deleteECRImage(ecr_client, repository, imageTagName, imageListRepo[i]['imageDigest'])
					# exit(0)	

			else:
				print ("Image Details: Untagged | Image Digest: ", imageListRepo[i]['imageDigest'])
				imageDetailsObj['imageTag'] = "Untagged"
				imageDetailsObj['imageDigest'] = imageListRepo[i]['imageDigest']

				imageListToDelete.append(imageDetailsObj)

				# deleteECRImage(ecr_client, repository, imageTagName, imageListRepo[i]['imageDigest'])
				# exit(0)

			i = i + 1

		print ("\nImage deletion is completed.\n", "\nTotal number of images deleted: ", len(imageListToDelete))
	
	else:
		print ("Image list is Empty.")


if __name__ == "__main__":
	main()
