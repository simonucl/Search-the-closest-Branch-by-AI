from flask import Flask, render_template, request
from ukpostcodeutils import validation
import hack
import js

app = Flask(__name__)
hasGreated = [False,False,False]
num = [0]
postcode = []

def process(userText):
    postcode_without_space = postcode[0].replace(" ","")
    if (validation.is_valid_postcode(postcode_without_space) and " " in postcode[0]):
        if (num[0] == 2):
            response = hack.getMeATM(postcode[0])
            return response
        elif (num[0] == 1):
            if (userText =="no" or userText == "No"):
                response = hack.getMeBranches(postcode[0])
                return response
            else:
                try:
                    response = hack.getMeBranchesForSpecificBank(postcode[0],userText)
                    return response
                except:
                    return ("Invalid bank input")
    else:
        return ("Invalid Postcode.")

def chosen(userText):
    if (userText  == "1"):
        num[0] = 1
        return("You have chosen [1. Find your nearest Bank.]\nPlease input your postcode.")
    elif (userText == "2"):
        num[0] = 2
        return("You have chosen [2. Find your nearest ATM.]\nPlease input your postcode.")
    else:
        return ("[3.Exit]")

def specific(userText):
    postcode[0] = userText
    if (num[0] == 2):
        return process(userText)
    if (num[0]== 1):
        return ("Do you have any specific bank you want to go?")




@app.route("/")
def home():
    return render_template("home.html")

@app.route("/greeting")
def greeting():
    userText = request.args.get('msg')
    return ("Thanks " + userText +", nice to meet you!")

@app.route("/choosing")
def choosing():
    userText = request.args.get('msg')
    reply = ""
    if userText == "3":
        num[0] = userText
        reply = "[3.exit]"
        return ({"You have chosen " + reply })
    elif userText == "2":
        num[0] = userText
        reply = "[2.Find your nearest ATM.]"
    elif userText == "1":
        num[0] = userText
        reply = "[1.Find your nearest Bank.]"
    return ("You have chosen " + reply + ". Please input your postcode.")

@app.route("/getvalidPostcode")
def getvalidPostcode():
    userText = request.args.get('msg')
    postcode.append(userText)
    postcode_without_space = userText.replace(" ","")
    if (validation.is_valid_postcode(postcode_without_space) and " " in userText):
        return "1"
    else:
        return "2"

@app.route("/getATM")
def getATM():
    userText = request.args.get('msg')
    response = hack.getMeATM(userText)
    return response

@app.route("/getATMLong")
def getATMLong():
    userText = request.args.get('msg')
    response = hack.getMeATMLL(userText)[1]
    return response

@app.route("/getATMLati")
def getATMLati():
    userText = request.args.get('msg')
    response = hack.getMeATMLL(userText)[0]
    return response

@app.route("/gotPostcode")
def gotPostcode ():
    postcode[0] = request.args.get('msg')
    response = "Do you have any specific bank you want to go?"
    return response

@app.route("/getBranches")
def getBranches ():
    userText = request.args.get('msg')
    if (userText == "no" or userText == "No"):
        response = hack.getMeBranches(postcode[0])
        return response
    else:
        response = hack.getMeBranchesForSpecificBank(postcode[0],userText)
        return response

@app.route("/getBranchesLong")
def getBranchesLong():
    userText = request.args.get('msg')
    if (userText == "no" or userText == "No"):
        response = hack.getMeBranchesLL(postcode[0])[1]
        return response
    else:
        response = hack.getMeBranchesForSpecificBankLL(postcode[0],userText)[1]
        return response
    
@app.route("/getBranchesLati")
def getBranchesLati():
    userText = request.args.get('msg')
    if (userText == "no" or userText == "No"):
        response = hack.getMeBranchesLL(postcode[0])[0]
        return response
    else:
        response = hack.getMeBranchesForSpecificBankLL(postcode[0],userText)[0]
        return response

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    if not hasGreated[1]:
        hasGreated[1] = True
        return chosen(userText)
    elif not hasGreated[2]:
        hasGreated[2] = True
        return specific(userText)
    else:
        return process(userText)


@app.route("/postcode")
def updatepostcode():
    t = request.args.get('postcode')



if __name__ == "__main__":
    app.run(debug=True)

