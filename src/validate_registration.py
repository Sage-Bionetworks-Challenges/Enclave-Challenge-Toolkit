
## Check if a participant is registered with the challenge in synapse
def checkIsRegistered(user):
    return user["Synapse Registered"] == 'yes'

# Check if Organizers have approved access to the external platform
def checkIsApproved(user):
    return user["External Platform Approved"] == 'yes'

# Check if a participant has requested access to the external platform
def checkIsRequested(user):
    return user["External Platform Access Requested"] == 'yes'

# Check if registered participants are on a 
# Team that is registered for the challenge
def checkIsOnTeam(user):
    return user["TeamID"] != ""


def validateRow(user):
    registered = checkIsRegistered(user)
    requested = checkIsRequested(user)
    team = checkIsOnTeam(user)

    return (registered) & (team) & (requested)


def reasonForValidation(user):
    
    reason = ''

    registered = checkIsRegistered(user)
    requested = checkIsRequested(user)
    team = checkIsOnTeam(user)

    if not registered:
        reason += 'Not registered; '
    if not requested:
        reason += 'No external platfrom request; '
    if not team:
        reason += 'Not associated with team; '

    return reason


def validateRegistrationInformation(info):
    info["Validated"] = info.apply(lambda row: validateRow(row), axis=1)
    info["Onboarded"] = info.apply(lambda row: checkIsApproved(row), axis=1)
    info["Validation Reason"] = info.apply(lambda row: reasonForValidation(row), axis=1)
    return info