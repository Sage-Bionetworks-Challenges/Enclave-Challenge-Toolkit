
def getValidatedNotOnboarded(info):
    info = info[(info["Validated"]==True) & (info["Onboarded"]==False)].drop_duplicates()
    return info


def getNotValidated(info):
    info = info[(info["Validated"]==False) & (info["Onboarded"]==False)].drop_duplicates()
    return info


def getNotRegistered(info):
    info = info[(info["Synapse Registered"]=='no') & (info["Onboarded"]==False)].drop_duplicates()
    return info


def getRequestedandNotValidated(info):
    info = info[(info["N3C Access Requested"]=='yes') & (info["Validated"]==False) & (info["Onboarded"]==False)].drop_duplicates()
    return info


def getRegisteredAndRequested(info):
    info = info[(info["Synapse Registered"]=='yes') & (info["N3C Access Requested"]=='yes') & (info["N3C Approved"]=='no') & (info["Validated"]==False)].drop_duplicates()
    return info


def getRegisteredAndNotRequested(info):
    info = info[(info["Synapse Registered"]=='yes') & (info["N3C Access Requested"]=='no') & (info["N3C Approved"]=='no') & (info["Validated"]==False)].drop_duplicates()
    return info


def getRequested(info):
    info = info[(info["N3C Access Requested"]=='yes') & (info["N3C Approved"]=='no')].drop_duplicates()
    return info


def get_participant_status(status, registrationInformation):

    if status == 'Ready to Onboard' or status == "Ready to Onboard, Not Contacted":
        info = getValidatedNotOnboarded(registrationInformation)

        if status == 'Ready to Onboard, Not Contacted':
            info = info[info["N3C Approved"] != 'yes']


    elif status == 'Not Validated':
        info = getNotValidated(registrationInformation)


    elif status == 'Need Team':
        info = getRegisteredAndRequested(registrationInformation)


    elif status == 'N3C Requested':
        info = getRequested(registrationInformation)

    
    elif status == 'Not Registered':
        info = getNotRegistered(registrationInformation)


    elif status == 'Requested and Not Validated':
        info = getRequestedandNotValidated(registrationInformation)

    elif status == 'Registered and Not Requested':
        info = getRegisteredAndNotRequested(registrationInformation)


    elif status == "Onboarded":
        info = registrationInformation[registrationInformation["Onboarded"]==True]
        info.to_csv("reports/Active Participants.csv", index=False)

    else:
        info = registrationInformation


    #print (info[["First Name", "Last Name", "Email", "username", "Team", "Validated", "Onboarded", "Validation Reason"]].sort_values("Team").to_string())

    return info[["First Name", "Last Name", "Email", "username", "Team", "Accessing Institution"]]