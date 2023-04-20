## return a list of emails from the input dataframe
def getEmails(info):
    output = ','.join(list(info["Email"]))
    return output


## print out 
def createEmails(info, parameters):

    join_team_email = f"""
SUBJECT {parameters['challenge name']}: Please join a team
bcc: {getEmails(info[info["Synapse Registered"]=='yes'])}

Hello {parameters['challenge name']} participant!

[Body of Email with instructions for joining a synapse team.]
"""


    join_team_and_register_email = f"""
SUBJECT {parameters['challenge name']}: Please register with Synapse and join a team
bcc: {getEmails(info[info["Synapse Registered"]=='no'])}

Hello {parameters['challenge name']} participant!

[Body of Email with instructions for registering with Synapse and joining a synapse team.]
"""
        
    print (join_team_email)
    print ('\n')
    print (join_team_and_register_email)