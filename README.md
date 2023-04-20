# External-Challenge-Toolkit
A suite of tools to manage challenges that are run external to Synapse but still use some of the Synapse functionality.

## Overview


### Entering the New Access Requests
When using the tool, make sure the `AccessRequests.csv` file is up to date with the latest N3C Access Requests. See the [Access Requests](https://unite.nih.gov/workspace/module/view/latest/ri.workshop.main.module.26e17ad9-728d-4f54-bd72-578d9156e6b6)

You'll have to manually add the requests to the file. The only required fields are First Name, Last Name, Email, and Onboarded status.
```
First Name,Last Name,Email,Accessing Institution,N3C Approved,Onboard Confirmation Sent
Timothy,Bergquist,timothy.bergquist@sagebase.org,,yes,
Marie,Wax,Marie.Wax@hhs.gov,,yes,
New,Person,np@email.edu,,no,
```
When you first enter the new person, set the `N3C Approved` status to no. When you accept the N3C access request, change the `N3C Approved` status to yes.

### Running the tool
There are eight options when running the tool.

#### Onboard
```
python ChallengeManagement.py onboard
```
When you run this command, this will gather two lists of people, (1) those who have fulfilled all the requirements and are ready to be onboarded, and (2) those who have requested access but have outstanding requirements. The `Validation Reason` column shows the outstanding requirements.

For the "Ready to Onboard" folks, find their folder in the [Team Folders](https://unite.nih.gov/workspace/compass/view/ri.compass.main.folder.4980fcc4-674f-46df-9d32-f93548d38af3) directory and use the share button to make the participants a `Project Collaborator` on that folder. Afterwards, go to the [My Projects](https://unite.nih.gov/workspace/module/view/latest/ri.workshop.main.module.26e17ad9-728d-4f54-bd72-578d9156e6b6) page and Approve the Collaborator. Once those two steps are completed, change their `N3C Approved` status to 'yes' in the `AccessRequests.csv` folder.

For the `Requested and Not Validated` participants, use the Email command to generate emails to send them next steps.

#### Email
```
python ChallengeManagement.py email
```
This will generate two emails that you can send to participants. One email will be sent to those who are registered in Synapse, but who haven't registered a team yet. The second email will be for participants who are not registered through Synapse, or who haven't made their first and last name in their Synapse profile match their N3C account.

#### Registered
```
python ChallengeManagement.py registered
```
This will show a full list of all the registered participants.

#### Status
```
python ChallengeManagement.py onboard
```
This will show a summary of the challenge (number of teams, number of participants, etc.) as well as build a file of all participants and their affiliated institutions.

#### Emails
```
python ChallengeManagement.py emails
```
show onboarded participants' email addresses

#### Active
```
python ChallengeManagement.py active
```
show fully onboarded participants

#### Outstanding
```
python ChallengeManagement.py outstanding
```
show who has registered through Synapse but not requested access in the external platform

#### Teams
```
python ChallengeManagement.py teams
```

#### Report
```
python ChallengeManagement.py report
```
gather the current list of participants and their institutions