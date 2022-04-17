from flask import Flask, render_template, request, jsonify, json, abort
import os
from flask_cors import CORS
import base64
from jwt import (
    JWT,
    jwk_from_dict,
)

app = Flask(__name__)
CORS(app)

public_okta_key="eyJrdHkiOiJSU0EiLCJhbGciOiJSUzI1NiIsImtpZCI6ImZSRGU5UVAtUUZNTTMySkhTUkQ0VUdrR1NnNE5XQmRRUXpxRmNfNkRuNjAiLCJ1c2UiOiJzaWciLCJlIjoiQVFBQiIsIm4iOiJ0TzlCOXVtY0x1bVJ4b1dCSDNiUHVBWWJKWlk3UGxkTlBzR2ZGdjVzOURZM05zcHJibThLU3AtT2xheFRZeEhMWUVzWFhLUTY4S3JxYkNpbTN6dEI4NVRUdl9NdVhoY2JHLVRPRThIYVF5UTl3bEJkRjhXek9sNTFQczBycGRibWZUM1JLQmRuMk9tcDF5ZTRRZTBBbjJRbDZFbHVyMWd2RVBkTG1NZzh2TElGd0dDcDM0eVM3VjlWb1dUYlV1a2VUN3FNWEFDU1JXSGItMXdhOE0zZ1RZOGk2ZThNNGR3VHVtZjkybG9ZNkhZaHhCUHNBMW5SeXZ5VHBNNXBoOU10WlFPVHd0cVlFcWxSbXFqM1l4Ml9rUjBySGwzT2l0Q0Y0M0FKWGtXY1NONlFLTmZNbDN6bGd5bkhYQnBHMmdVYkRfSVhoWGZkTHJzajlBRFd2TXpUSlEifQ=="

instance = JWT()

@app.route('/', methods=['POST', 'GET'])
def home():
    head = dict(request.headers)
    data=request.data.decode("utf-8")

    try:
      dataDict = json.loads(data)
    except:
      return ({"error":"No json body submitted"},400)

    key= json.loads(base64.b64decode(public_okta_key).decode("utf-8"))

    origin=head.get("Origin")

    try:
      assert (origin == "https://ec2-44-202-139-20.compute-1.amazonaws.com" or origin == "http://localhost:3000")
    except:
      return ({"error":"REST call must originate from application"},400)

    jwt_token = request.headers.get('authorization', None).replace("Bearer ","")

    verifying_key = jwk_from_dict(key)

    try:
      message_received = instance.decode(jwt_token, verifying_key, do_time_check=True)
      aud = message_received.get("aud")
      iss = message_received.get("iss")
      assert iss == "https://dev-73981180.okta.com/oauth2/default"
      assert aud == "0oa4o7fp4fViV9tfl5d7"
    except:
      return ({"error":"Token is invalid"},401)


    firstName=dataDict.get("firstName","")
    lastName=dataDict.get("lastName","")
    language=dataDict.get("lang","")
    date=dataDict.get("dt","date")

    ret = {
        "firstName": firstName,
        "lastName": lastName,
        "language":language,
        "date":date
      }

    if firstName and lastName and language:
      return ret
    else:
      return ({"error":"validation failed"},400)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')