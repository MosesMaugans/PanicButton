from flask import Flask, jsonify, request
from twilio.rest import Client
app = Flask(__name__)
@app.route('/')
def TestConnect():
    return "Conencted!"
@app.route("/sendLocation",methods=["POST"])
def LocationSend():
    data = request.get_json()
    userID = data["userid"]
    location = data["location"]
    dataFile = open("dataHolder.txt","r").split('\n')
    for line in dataFile:
        datasec = line.split("|")
        if (datasec[0] == userID):
            datasec[2] = location
            line = "|".join(datasec)
            break
    open("dataHolder.txt","w").write("\n".join(dataFile))
    notifyPolice = data["notify police"]
    msg = "ALERT! {} IS IN TROUBLE! LOCATION: {}".format(userID,location)
    sendTextMSG(msg.data["emergency contacts"]["contact phone"])
    if (notifyPolice):
        sendTextMSG(msg,"+13173191985")
    return "Complete"
@app.route("/endHelp",methods=["POST"])
def endHelp():
    data = request.get_json()
    userID = data["userid"]
    dataFile = open("dataHolder.txt","r").split('\n')
    found = False
    for line in dataFile:
        datasec = line.split("|")
        if (datasec[0] == userID and datasec[1] == data["password"]):
            datasec[2] =  "NO_LOCATION"
            line = "|".join(datasec)
            found = True
            break
    if (found == False):
        return "Incorrect Password!"
    open("dataHolder.txt","w").write("\n".join(dataFile))
    return "Ended!"
@app.route("/register",methods=["POST"])
def RegisterUser():
    try:
        data = request.get_json()
        userID = data["userid"]
        password = data["password"]
        emergencyContacts = data["emergency contacts"]
        dataFile = open("dataHolder.txt","a")
        dataFile.write('\n'+userID + "|" + password + "|" + "NO_LOCATION" + "|" + emergencyContacts)
        return "Registered!"
    except:
        return "Registration Error!"
def sendTextMSG(message,phone):
    account_sid = 'AC757ad136e22280293939be6c13fba6bd'
    auth_token = 'ce2ee24ae81bb49a7f7ae2539d33ed75'
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=message,
                        from_='+12056289978',
                        to=phone
                    )
# UserID = this is the user ID
# UserLocation = GeoLocation
# EmergencyContact[] { "their name" , "their phone" , "their email"}
# Notify police
# 
#Connection string: mongodb+srv://admin:<password>@cluster0-sexcl.gcp.mongodb.net/test?retryWrites=true&w=majority
#Mongo user pass: y6LVXXHfDfFFdHKg
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)