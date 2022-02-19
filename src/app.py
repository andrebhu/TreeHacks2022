#!/usr/bin/env python

from base64 import b64encode
from flask import Flask, render_template, request
# from flask_bootstrap import Bootstrap
import requests

from getImageUrl import getImageUrl
from check_image_exists_online import duplicates

from getJSON import getJSON


app = Flask(__name__)

# app.config["BOOTSTRAP_SERVE_LOCAL"] = True
# bootstrap = Bootstrap(app)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        
        # Retrieve NFT information from page, rename `file` later
        token_id = 0
        contract_address="None"
        try:
            token_id = int(request.form["tokenId"])
            contract_address = request.form["contractAddress"]
            
        except Exception as e:
            print(e)
            output = f"[ERROR] Not Found\
            \nContract Address: {contract_address}\
            \nToken Id: {token_id}"
            return render_template("index.html", output=output)

        # Information to send back to page
        output = "Picture Found." # output can be a string
        image = "" # image should be returned as a b64 encoded string

        if token_id:
            try:
                # TODO: Check max file size of NFT? Could it crash the server?
                # TODO: Function that retrieves image from NFT token

                image_metadata = getJSON(contract_address, token_id) # Currently executes two requests to the network, make it one later
                image_url = getImageUrl(image_metadata)
            
                output = str(image_metadata)

                # b64 encode file to pass back to page
                # image = b64encode(file).decode("utf-8")
                # imageUrl = getImageUrl(contract_address, token_id)
                # dups_found = duplicates(imageUrl)
                # if dups_found == 0:
                #     output += "Image is Original."
                # else:
                #     output += f"Image has {dups_found} duplicates online."

            # If anything goes wrong
            except Exception as e:
                print(e)
                output = "[Error] Invalid NFT"
        else:
            return render_template("index.html")

        print(image[:50])
        return render_template("index.html", output=output, image=image_url)

    elif request.method == "GET":
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
