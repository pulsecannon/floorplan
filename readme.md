#Floorplan project.

Requirements:
1. Python3 with pip3.
2. Use pip3 to install all requirements listed in requirements.txt.

To Run: python3 main.py


Allows for creating/listing/getting/updating/deleting of:
1. Project
2. Floorplan

Using REST API's
1. Create using POST by form submit.
2. List using GET.
3. Get using GET and passing ID.
4. Update using PATCH request by form submit.
5. Delete using DELETE request passing ID.

Response to most things will be a JSON response except for getting file and 
thumbnails.

Project:
1. List: curl --request GET localhost:5000/project
2. Create: curl --request POST localhost:5000/project -F name="{NAME}"
3. Get: curl --request GET localhost:5000/project/{ID}
4. Update: curl --request PATCH localhost:5000/project -F id="{ID}" -F name="{NAME}"
5. Delete: curl --request DELETE localhost:5000/project/{ID}

Floorplan:
1. List: curl --request GET localhost:5000/floorplan
2. Create: curl --request POST localhost:5000/floorplan -F project_id="{ID}" -F original="@{FILEPATH}"
3. Get: curl --request GET localhost:5000/floorplan/1
4. Update: curl --request PATCH localhost:5000/floorplan -F id="{ID}" -F name="{NAME}" -F original="@{FILEPATH}"
5. Delete: curl --request DELETE localhost:5000/floorplan/1

File:
1. Get: curl --request GET localhost:5000/floorplan/file/{FLOORPLAN_ID}

Thumb
1. Get: curl --request GET localhost:5000/floorplan/{FLOORPLAN_ID}/thumb/{THUMB_ID}
