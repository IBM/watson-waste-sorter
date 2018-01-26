cf create-service-key visual-recognition-wws waste-sorter
API_KEY=$(cf service-key visual-recognition-wws waste-sorter --guid | tr -d "-")
if [ ${#API_KEY} -eq 0 ]; then
	echo 'Cannot retrieve your visual recognition api-key, exiting now.'
	exit 1
fi
curl -X POST -F "Landfill_positive_examples=@resources/landfill.zip" -F "Recycle_positive_examples=@resources/recycle.zip" -F "Compost_positive_examples=@resources/compost.zip" -F "negative_examples=@resources/negative.zip" -F "name=waste" "https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classifiers?api_key=$API_KEY&version=2016-05-20"

echo '' && echo 'Your custom model is now created and start training.'