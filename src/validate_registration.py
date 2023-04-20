
## Check if a participant is registered with the challenge in synapse
def checkIsRegistered(user):
    if user["Synapse Registered"] == 'yes':
        return True
    else:
        return False

# Check if Organizers have approved access to the N3C enclave
def checkIsN3CApproved(user):
    if user["N3C Approved"] == 'yes':
        return True
    else:
        return False

# Check if a participant has requested access to the N3C enclave
def checkIsN3CRequested(user):
    if user["N3C Access Requested"] == 'yes':
        return True
    else:
        return False

# Check if registered participants are on a 
# Team that is registered for the challenge
def checkIsOnTeam(user):
    if user["TeamID"] != "":
        return True
    else:
        return False


def validateRow(user):
    registered = checkIsRegistered(user)
    requested = checkIsN3CRequested(user)
    team = checkIsOnTeam(user)

    return (registered) & (team) & (requested)


def reasonForValidation(user):
    
    reason = ''

    registered = checkIsRegistered(user)
    requested = checkIsN3CRequested(user)
    team = checkIsOnTeam(user)

    if not registered:
        reason += 'Not registered; '
    if not requested:
        reason += 'No N3C request; '
    if not team:
        reason += 'Not associated with team; '

    return reason


def validateRegistrationInformation(info):
    info["Validated"] = info.apply(lambda row: validateRow(row), axis=1)
    info["Onboarded"] = info.apply(lambda row: checkIsN3CApproved(row), axis=1)
    info["Validation Reason"] = info.apply(lambda row: reasonForValidation(row), axis=1)
    return info