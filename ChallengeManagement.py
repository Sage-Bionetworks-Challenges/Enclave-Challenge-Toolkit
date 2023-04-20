import synapseclient
from challengeutils.challenge import ChallengeApi

import pandas as pd
import argparse
from argparse import RawTextHelpFormatter
import json

from src.emails import createEmails, getEmails
from src.validate_registration import validateRegistrationInformation
from src.participants import get_participant_status, getRequestedandNotValidated

pd.set_option('display.max_rows', 500)


class ChallengeManagement:
    """
    Creates a ChallengeManagement object used coordinate between a challenge on Synapse
    and an external platform where the bulk of the challenge will occur.
    """
    def __init__(self):
        ## collect configurations
        config_file = open('config.json', 'r')
        self.configs = json.load(config_file)
        config_file.close()

        ## Synapse login
        self.syn = synapseclient.Synapse()

        username = self.configs['username']
        password = self.configs['password']
        try:
            self.syn.login(username, password, silent=True)
        except synapseclient.core.exceptions.SynapseAuthenticationError:
            raise Exception("Unable to login to Synapse. Please check the config.json file.")

        ## collect challenge information
        self.CHALLENGEID = self.configs['challengeid']
        self.PROJECTID = self.configs['projectid']

        self.chalutils = ChallengeApi(self.syn)

        self.challenge = self.chalutils.get_challenge(self.CHALLENGEID, self.PROJECTID)

        self.registeredParticipants = self.getRegisteredParticpantsSynapse()


    def getUserInformation(self, user):

        participant = {}
        try:
            participant["First Name"] = user["firstName"]
        except KeyError:
            participant["First Name"] = None
        
        try:
            participant["Last Name"] = user["lastName"]
        except KeyError:
            participant["Last Name"] = None

        participant["username"] = user["userName"]
        participant["userId"] = user["ownerId"]

        return participant


    def getRegisteredParticpantsSynapse(self):
        RegisteredParticipants = []

        ChallengeTeam = self.chalutils.get_registered_participants(self.CHALLENGEID)

        for p in ChallengeTeam:
            
            user = self.syn.getUserProfile(p)

            RegisteredParticipants.append(self.getUserInformation(user))

        RegisteredParticipants = pd.DataFrame(RegisteredParticipants)
        RegisteredParticipants["Synapse Registered"] = 'yes'

        ChallengeTeams = self.chalutils.get_registered_teams(self.CHALLENGEID)
        ParticipantsWithTeam = []
        for team in ChallengeTeams:
            team = self.syn.getTeam(team["teamId"])

            members = self.syn.getTeamMembers(team)
            for m in members:
                memberInfo = self.getUserInformation(m["member"])
                memberInfo["Team"] = team["name"]
                memberInfo["TeamID"] = team["id"]
                ParticipantsWithTeam.append(memberInfo)

        ParticipantsWithTeam = pd.DataFrame(ParticipantsWithTeam)

        AllParticipants = RegisteredParticipants.merge(ParticipantsWithTeam, on=["First Name", "Last Name", "username", "userId"], how="left")

        #print (AllParticipants)

        return AllParticipants


    def getRegisteredParticpants(self):
        return self.registeredParticipants


    def getAccessRequests(self):
        accessRequests = pd.read_csv("AccessRequests.csv")

        accessRequests["External Platform Access Requested"] = 'yes'
        
        return accessRequests

    def getAllRegistrationInformation(self):
        REQUESTS = self.getAccessRequests()

        REGISTRANTS = self.getRegisteredParticpants()

        REGISTRANTS["First Name"] = REGISTRANTS["First Name"].str.lower().str.strip()
        REGISTRANTS["Last Name"] = REGISTRANTS["Last Name"].str.lower().str.strip()

        REQUESTS["First Name"] = REQUESTS["First Name"].str.lower().str.strip()
        REQUESTS["Last Name"] = REQUESTS["Last Name"].str.lower().str.strip()

        REGISTRANTS["Team"] = REGISTRANTS["Team"].combine_first(REQUESTS["Team"])
        REQUESTS = REQUESTS.drop("Team", axis=1)

        ALL = REGISTRANTS.merge(REQUESTS, on=["First Name", "Last Name"], how="outer")

        ALL[["Synapse Registered", "External Platform Access Requested", "External Platform Approved"]] = ALL[["Synapse Registered", "External Platform Access Requested", "External Platform Approved"]].fillna("no")
        
        ALL[["username", "userId", "Team", "TeamID", "Email", "Accessing Institution"]] = ALL[["username", "userId", "Team", "TeamID", "Email", "Accessing Institution"]].fillna("")
        
        ALL = validateRegistrationInformation(ALL)
        
        return ALL


    def getParticipantStatus(self, status):

        registrationInformation = self.getAllRegistrationInformation()

        return get_participant_status(status=status, registrationInformation=registrationInformation)


    def create_COI_document(self):
        info = self.getAllRegistrationInformation()
        submitted_teams = pd.read_csv("Submitting_Teams.csv")

        active = info[info["Onboarded"]==True]
        active = active[['First Name', 'Last Name', 'Team', 'Accessing Institution']].sort_values("Accessing Institution").drop_duplicates()

        def blank_map(row):
            blank_team_map = {
                "sanjoy dey":"Long COVID IBM",
                "zach pryor":"Kalman L3C Team",
                "saarthak kapse":"SBU BMI",
                "kai zhang":"UTHealth SBMI",
                "jiehuan sun":"sunny_J_team",
                "ciara crosby":"LongCOVIDLearning",
            }
            try:
                return blank_team_map[f"{row['First Name']} {row['Last Name']}"]
            except KeyError:
                return ""
        
        blank = active[active["Team"]==""]
        blank["Team"] = blank.apply(lambda r: blank_map(r), axis=1)
        blank = blank[blank["Team"]!=""]

        final_list = pd.concat([active.merge(submitted_teams, on="Team",how="inner"),blank]).sort_values(["Team","Accessing Institution"])
        final_list = final_list[["Team","Accessing Institution"]].drop_duplicates()
        final_list['Combined Accessing Institution'] = final_list[["Team","Accessing Institution"]].groupby("Team")['Accessing Institution'].transform(lambda x: ';'.join(x))
        final_list = final_list[['Team', 'Combined Accessing Institution']].drop_duplicates()
        final_list.to_csv("Team_Institution_List.csv",sep=",",index=False)
        print (final_list)
        exit()
        final_list.to_csv("Participant_Institution_COI_List.csv", sep=",")
        print (final_list)


    def gather_team_list(self):

        registrationInformation = self.getAllRegistrationInformation()
        teams = registrationInformation[registrationInformation["Onboarded"]==True][["Team"]].drop_duplicates().sort_values('Team')
        teams.to_csv('reports/Team_List.csv', index=False)
        print (teams)


    def getChallengeStatus(self):
        
        info = self.getAllRegistrationInformation()
        info = info[["First Name", "Last Name", "username", "Email", "Team", "Synapse Registered", "Onboarded"]].drop_duplicates()

        onboarded = info[info["Onboarded"]==True]
        onboarded_teams = onboarded[["Team"]].drop_duplicates()

        registeredNotOnboarded = info[info["Onboarded"]==False]
        registeredNotOnboarded_teams = registeredNotOnboarded[["Team"]].drop_duplicates()
        registeredNotOnboarded_teams = registeredNotOnboarded_teams[~registeredNotOnboarded_teams["Team"].isin(onboarded_teams)]

        registered_teams = info[["Team"]].drop_duplicates()

        stats = pd.DataFrame([
            {
                "Category": "Fully Onboarded",
                "Person Count": len(onboarded),
                "Team Count": len(onboarded_teams)
            },
            {
                "Category": "Registered Pending",
                "Person Count": len(registeredNotOnboarded),
                "Team Count": len(registeredNotOnboarded_teams)
            },
            {
                "Category": "Registered Total",
                "Person Count": len(info),
                "Team Count": len(registered_teams)
            }
        ])
        print (stats)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Managing External Challenges.", formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        metavar='Task',
        dest='Task',
        type=str, nargs='+', choices=['onboard','email','registered','status','active', 'emails', 'outstanding', 'report', 'teams'], 
        help="\nManagement task options, you may select multiple options:\
            \n\tonboard:   \tshow who is ready to be onboarded \
            \n\temail:     \tgenerate emails to be sent to incomplete applicants \
            \n\tregistered:\tshow all registered participants, status: show challenge numbers \
            \n\tstatus:    \tshow the current status of the challenge including team and participant counts \
            \n\temails:    \tshow onboarded participants' email addresses \
            \n\toutstanding:\tshow who has registered through Synapse but not requested access in the external platform \
            \n\tactive:    \tshow fully onboarded participants \
            \n\treport:     \tgather the current list of participants and their institutions \
            \n\tteams:     \tgenerate a list of teams who have been onboarded into the challenge")
    
    args = parser.parse_args()
    
    barda = ChallengeManagement()

    for task in args.Task:
        print (task)
        ## collect and show all fully onboarded participants
        if task == 'onboard':
            
            STATUS = "Ready to Onboard"
            print (f"===================== {STATUS} =======================")
            print (barda.getParticipantStatus(status=STATUS))

            print (" ")
            
            STATUS = "Requested and Not Validated"
            print (f"===================== {STATUS} =======================")
            print (barda.getParticipantStatus(status=STATUS))
        
        ## collect and show emails to be sent to participants with incomplete registration
        if task == 'email':
            parameters = {
                "challenge name": barda.syn.get(barda.PROJECTID).name
            }
            createEmails(getRequestedandNotValidated(barda.getAllRegistrationInformation()), parameters)

        ## collect and show all teams registered with the challenge
        if task == 'teams':
            barda.gather_team_list()

        ## collect and show all registered participants
        if task == 'registered':

            STATUS = "Gather all registrants"
            print (f"====================={STATUS}=======================")
            print (barda.getParticipantStatus(status=STATUS))

        ## collect and show cumulative numbers of the challenge
        if task == 'status':
            print ("===================== CHALLENGE STATUS =======================")
            barda.getChallengeStatus()
            #

        ## collect and show all onboarded participants
        if task == 'active':
            STATUS = "Onboarded"
            print (f"====================={STATUS}=======================")
            print (barda.getParticipantStatus(status=STATUS))

        ## collect and show all email addresses of all onboarded participants
        if task == 'emails':
            STATUS = "Onboarded"
            print (f"====================={STATUS}=======================")
            print (getEmails(barda.getParticipantStatus(status=STATUS)))

        ## collect and show all participants who have registered but have not requested access on the external platform
        if task == 'outstanding':
            STATUS = "Registered and Not Requested"
            print (f"====================={STATUS}=======================")
            print (barda.getParticipantStatus(status=STATUS))

        ## generate the possible conflict of interests list.
        if task == 'report':
            barda.create_COI_document()
    
