# watson-waste-sorter
***Work in progress***

# To Use

First provision a Free tier [Visual Recognition](https://console.bluemix.net/catalog/services/visual-recognition) 
Service and name it `visual-recognition-wws`.

## On Cloud Foundry
```
cf push
```

## Running on Local
```
python run.py
```

## Backend API usage

Do a POST request at `https://watson-waste-sorter.mybluemix.net/api/sort` with the image as the parameter. 
Return value should be in JSON.

Example in Bash:

Input: png/jpg/jpeg file
```
curl -X POST -F "images_file=@plastic_fork.jpg" "https://watson-waste-sorter.mybluemix.net/api/sort"
```

Output: 
```
{"status code": 200, "result": "landfill", "accuracy rate": 0.908}
```