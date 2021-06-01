#Floorplan project.

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
List: curl --request GET localhost:5000/project
Create: curl --request POST localhost:5000/project -F name="{NAME}"
Get: curl --request GET localhost:5000/project/{ID}
Update: curl --request PATCH localhost:5000/project -F id="{ID}" -F name="{NAME}"
Delete: curl --request DELETE localhost:5000/project/{ID}

Floorplan:
List: curl --request GET localhost:5000/floorplan
Create: curl --request POST localhost:5000/floorplan -F project_id="{ID}" -F original="@{FILEPATH}"
Get: curl --request GET localhost:5000/floorplan/1
Update: curl --request PATCH localhost:5000/floorplan -F id="{ID}" -F name="{NAME}" -F original="@{FILEPATH}"
Delete: curl --request DELETE localhost:5000/floorplan/1

File:
Get: curl --request GET localhost:5000/floorplan/file/{FLOORPLAN_ID}

Thumb
Get: curl --request GET localhost:5000/floorplan/{FLOORPLAN_ID}/thumb/{THUMB_ID}
