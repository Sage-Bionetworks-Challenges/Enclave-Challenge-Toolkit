# External Challenge Toolkit
A suite of tools to manage challenges that are run external to Synapse but still use some of the Synapse functionality.

## Overview
This toolkit is designed to help challenge organizers manage challenges that are taking place on a platform external to Synapse (e.g. N3C, All of Us) while still using some of the features of Synapse for challenge management. 

This toolkit assumes that:

1. Challenge registration is taking place on Synapse.
2. Team formation is occuring through Synapse.
3. The challenge organizer has the ability to manage access to the challenge data on the external platform or, at least, is able to see who has access.
4. The organizers are able to collect the first and last names of the participants from the external platform.
5. The participants have a complete Synapse profile that includes their first name and last name.

### How it Works
This script checks the `AccessRequests.csv` file and compares the participants in that file to the full registration team associated with the challenge by linking on their first and last names. It then makes multiple checks on those users:

1. Is the participant in both the AccessRequests file and the registration team? (i.e. Has the participant registered with the challenge and agreed to the challenge rules and requested access in the external platform?)
2. Is the participant part of a challenge registered team? (Team membership is currently required)
3. Has the participant already been approved for access (i.e. `External Platform Access Approved == True` in the AccessRequests file).

Depending on which command is being used, the tool will then print out results to the command line.

## Setting Up an External Challenge
Just like normal challenges, external challenges assume that a Synapse challenge has been instantiated and a challenge bot has been created. In the `config.json` file, enter the challenge_id, project_id of the project linked to the challenge, and the challenge bot credentials.

In the external platform, this toolkit assumes that either participants need to request access to the challenge data or that the organizers are able to retrieve who has access to the challenge project.

In the `src/emails.py` script, fill in the email template for what should be sent to participants when they either haven't registered through Synapse but have requested access to the external platform, or when they have registered and requested access, but are not part of a Synapse team. Email templates from the previous [Long COVID Computational Challenge](https://www.synapse.org/l3c) are in `docs/EmailTemplates.md`.

### Entering the New Access Requests
When using the tool, make sure the `AccessRequests.csv` file is up to date with the latest external platform access requests.

You'll have to manually add the requests to the file. The only required fields are First Name, Last Name, Email, and External Platform Approved. The participant's institution is optional, but recommended if that data is available.
```
First Name,Last Name,Email,Accessing Institution,External Platform Approved
Timothy,Bergquist,timothy.bergquist@sagebase.org,Sage Bionetworks,yes
New,Person,np@email.edu,University,no
```
When you first enter the new person, set the `External Platform Approved` status to no. When you accept the participants access request or confirm that they have access, change the `External Platform Approved` status to yes. Depending on the challenge and the onboarding process, this variable could stand in for any number of situtions. The key take away is that once `External Platform Approved` is set to `yes`, the participant is considered fully onboarded into the challenge and is ready to compete. 

## Running the tool
There are eight options when running the tool.

```
usage: ChallengeManagement.py [-h] Task [Task ...]

Managing External Challenges.

positional arguments:
  Task        
              Management task options, you may select multiple options:            
                onboard:        show who is ready to be onboarded             
                email:          generate emails to be sent to incomplete applicants             
                registered:     show all registered participants, status: show challenge numbers             
                status:         show the current status of the challenge including team and participant counts             
                emails:         show onboarded participants' email addresses             
                outstanding:    show who has registered through Synapse but not requested access in the external platform             
                active:         show fully onboarded participants             
                report:         gather the current list of participants and their institutions             
                teams:          generate a list of teams who have been onboarded into the challenge
```

### Onboard
```
python ChallengeManagement.py onboard
```
When you run this command, this will gather two lists of people, (1) those who have fulfilled all the requirements and are ready to be onboarded/approved, and (2) those who have requested access but have outstanding requirements. The `Validation Reason` column shows the outstanding requirements.

For the "Ready to Onboard" folks, complete whatever steps are necessary to give them full access to the challenge data. Once that is completed, change their `External Platform Approved` status to 'yes' in the `AccessRequests.csv` folder.

For the `Requested and Not Validated` participants, use the Email command to generate emails to send them next steps.

### Email
```
python ChallengeManagement.py email
```
This will generate two emails that you can send to participants. One email will be sent to those who are registered in Synapse, but who haven't registered a team yet. The second email will be for participants who are not registered through Synapse, or who haven't made their first and last name in their Synapse profile match their N3C account. The print emails include a subject line as well as all the emails formatted to be copy and pasted into the BCC line.

### Registered
```
python ChallengeManagement.py registered
```
This command will print out a full list of all the participants who have registered in Synapse and who have requested access to the external challenge platform.

### Status
```
python ChallengeManagement.py status
```
This will show a summary of the challenge (number of teams, number of participants, etc.).

### Emails
```
python ChallengeManagement.py emails
```
This will print out a full list of the onboarded participants' email addresses formatted so they can be copy and pasted into the BCC input line.

### Active
```
python ChallengeManagement.py active
```
This will print out a full list of the fully onboarded participants.

### Outstanding
```
python ChallengeManagement.py outstanding
```
This will print out a full list of the participants who have registered through Synapse but not requested access in the external platform.

### Teams
```
python ChallengeManagement.py teams
```
This will print out a full list of all the teams that have at least one member fully onboarded into the challenge.

### Report
```
python ChallengeManagement.py report
```
This will gather the current list of onboarded participants and their institutions and build a file outputing the results into the `reports` folder. This is mainly useful for government challenges where conflict of interests need to be declared by federal judges.