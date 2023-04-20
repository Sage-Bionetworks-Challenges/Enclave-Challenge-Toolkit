
"""
Functions to selected different filterings from main participants table. Each function filters 
the table down to only the participants who meet the criteria in each function.
"""

## filter to participants who are ready to be onboarded.
def getValidatedNotOnboarded(info):
    info = info[(info["Validated"]==True) & (info["Onboarded"]==False)].drop_duplicates()
    return info

## filter to participants who have incomplete registration requests.
def getNotValidated(info):
    info = info[(info["Validated"]==False) & (info["Onboarded"]==False)].drop_duplicates()
    return info

## filter to participants who have requested access to the external platform but have not
## registered through Synpase.
def getNotRegistered(info):
    info = info[(info["Synapse Registered"]=='no') & (info["Onboarded"]==False)].drop_duplicates()
    return info

## filter to participants who have requested external platform access but are not fully validated to
## be onboarded.
def getRequestedandNotValidated(info):
    info = info[(info["External Platform Access Requested"]=='yes') & (info["Validated"]==False) & (info["Onboarded"]==False)].drop_duplicates()
    return info

## filter to participants who have registered through both synapse and the external platform but
## have not been fully onboarded nor are cleared to be onboarded.
def getRegisteredAndRequested(info):
    info = info[(info["Synapse Registered"]=='yes') & (info["External Platform Access Requested"]=='yes') & (info["External Platform Approved"]=='no') & (info["Validated"]==False)].drop_duplicates()
    return info

## filter to participants who have registered through Synapse but have not registered through
## the external platform.
def getRegisteredAndNotRequested(info):
    info = info[(info["Synapse Registered"]=='yes') & (info["External Platform Access Requested"]=='no') & (info["External Platform Approved"]=='no') & (info["Validated"]==False)].drop_duplicates()
    return info

## filter to participants who have registered through the external platform but have not been approved
## for onboarding.
def getRequested(info):
    info = info[(info["External Platform Access Requested"]=='yes') & (info["External Platform Approved"]=='no')].drop_duplicates()
    return info


## return a list of participants with a given status from a given registration information dataframe
def get_participant_status(status, registrationInformation):

    if status == 'Ready to Onboard' or status == "Ready to Onboard, Not Contacted": ##
        info = getValidatedNotOnboarded(registrationInformation)

        if status == 'Ready to Onboard, Not Contacted':
            info = info[info["External Platform Approved"] != 'yes']


    elif status == 'Not Validated':
        info = getNotValidated(registrationInformation)


    elif status == 'Need Team':
        info = getRegisteredAndRequested(registrationInformation)


    elif status == 'N3C Requested':
        info = getRequested(registrationInformation)

    
    elif status == 'Not Registered':
        info = getNotRegistered(registrationInformation)


    elif status == 'Requested and Not Validated': ##
        info = getRequestedandNotValidated(registrationInformation)

    elif status == 'Registered and Not Requested': ##
        info = getRegisteredAndNotRequested(registrationInformation)


    elif status == "Onboarded": ##
        info = registrationInformation[registrationInformation["Onboarded"]==True]
        info.to_csv("reports/Active Participants.csv", index=False)

    else:
        info = registrationInformation
    
    return info[["First Name", "Last Name", "Email", "username", "Team", "Accessing Institution"]]