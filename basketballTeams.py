'''
    Project Name: Basketball Teams
    Name: Zixi Zhong
    Purpose: This program takes in an input file with teams and their
    conferences, processes the information, and outputs the conferences
    with the highest win ratio among the conferences in the file.
'''

import sys

class Team:
    '''
        This class represents information about a team. It read in a
        line of information, parses it, and extracts the team name,
        its conference, and its win ratio.
        Parameters: self
                    line - line of team information
        Returns: none, sets value to self._name, self._conf
                 and self._ratio
        Pre-condition: line must be a string
        Post-condition: this class will initialize 3 values
    '''
    def __init__(self, line):

        assert type(line) == str, "ERROR: Line must be a string."

        if line.find(")") != line.rfind(")"): # If line as 2 pairs of ()
            name_end = line.find(")") + 1     # sets name_end to ) of
                                              # first ()
        else:                                 # If line as 1 pair of ()
            name_end = line.find("(")         # sets name_end to beginning
                                              # ( of ()

        conf_left = line.rfind("(")   # Finds conf name inside of ()
        conf_right = line.rfind(")")  # from the right to find last ()

        name = line[0:name_end]
        conf = line[conf_left + 1:conf_right]

        stats = line[conf_right + 1:].split()
        win = int(stats[0])
        loss = int(stats[1])

        ratio = win / (win + loss)

        self._name = name
        self._conf = conf
        self._ratio = ratio


    def name(self):
        '''
            This method returns the team name.
            Parameters: self
            Returns: self._name
        '''
        return self._name


    def conf(self):
        '''
            This method returns the team conference.
            Parameters: self
            Returns: self._conf
        '''
        return self._conf


    def win_ratio(self):
        '''
            This method returns the team win ratio.
            Parameters: self
            Returns: self._ratio
        '''
        return self._ratio


    def __str__(self):
        '''
            This method formats the team object to be easily printed.
            Parameters: self
            Returns: printable format for team
        '''
        return  "{} : {}".format(self._name, self._ratio)




class Conference:
    '''
        This class represents information about the set of teams belonging
        to a conference.
        Parameters: self
                    conf - conference name
        Returns: none, sets value to self._conf, and initializes
                 self._conf_list as a list
        Pre-condition: none
        Post-condition: list of conferences is created
    '''
    def __init__(self, conf):
        self._conf = conf
        self._conf_list = []


    def __contains__(self, team):
        '''
            This method returns whether or not a team is in the
            conf_list.
            Parameters: self, team
            Returns: True if team in conf_list, False if not
            Pre-condition: team must be a valid value
            Post-condition: none
        '''
        return team in self._conf_list


    def name(self):
        '''
            This method returns the conference name.
            Parameters: self
            Returns: self._conf
        '''
        return self._conf


    def add(self, team):
        '''
            This method adds a team to the conf_list.
            Parameters: self
                        team - team object
            Returns: none
            Pre-condition: team isn't in conf_list
            Post-condition: team is in conf_list
        '''
        self._conf_list.append(team)


    def win_ratio_avg(self):
        '''
            This method calculates the average win ratio of the
            teams within the conf_list.
            Parameters: self
            Returns: self._avg
            Pre-condition: conf_list is a string of len > 0
            Post-condition: avg is calculated
        '''
        sum = 0

        assert len(self._conf_list) > 0, "ERROR: No teams in conference."

        for team in self._conf_list:
            sum += team.win_ratio()

        self._avg = sum / len(self._conf_list)

        return self._avg


    def __str__(self):
        '''
            This method formats the conference object to be easily printed.
            Parameters: self
            Returns: printable format for conference
        '''
        "{} : {}".format(str(self._conf), str(self._avg))




class ConferenceSet:
    '''
        This class represents a set of conferences. It creates conference
        objects, adds teams to the objects, and calculates the higest
i        win average for each conference.
        Parameters: self
        Returns: none, initializes self._conf_set as a dictionary
        Pre-condition: none
        Post-condition: conf_set will contain all conferences
    '''
    def __init__(self):
        self._conf_set = {}


    def add(self, team):
        '''
            This method adds a team to the appropriate conference in
            the list of conferences, and creates a Conference object
            if there is not one already.
            Parameters: self
            Returns: none
            Pre-condition: team is not in the Conference object or
                           ConferenceSet
            Post-condition: team is added into Conference object
        '''
        team_conf = team.conf()  # String representation of conference object

        if team_conf not in self._conf_set:
            conf_obj = Conference(team_conf)
            self._conf_set[team_conf] = conf_obj
        self._conf_set[team_conf].add(team)



    def best(self):
        '''
            This method calculates highest win ratio of the
            conferences within the conf_set dictionary.
            Parameters: self
            Returns: self._highest_conf
            Pre-condition: conf_set must be fully updates
            Post_condition: Highest win average is found and paired
                            with conferences
        '''
        avg_dict = {}  # Dict of conferences and average win rate
        highest_conf = {}  # Dict of conferences and the highest
                           # win avg

        for conf in self._conf_set:            # Makes a dict of avg win
            name = self._conf_set[conf].name() # rate to make it easier
            avg = self._conf_set[conf].win_ratio_avg() # to find highest
            avg_dict[name] = avg                       # win avg

        highest_avg = max(avg_dict.values()) # Finds highest win avg

        for key, val in avg_dict.items(): # Makes dict of conf's with
            if val == highest_avg:        # highest win avg to make it
                highest_conf[key] = val   # easy to print

        return highest_conf




def print_highest_conf(highest_conf):
    '''
        This function accepts a list of the conferences with the highest
        win ratios and prints them out.
        Parameters: highest_conf
        Returns: none, prints conf with highest win ratio and their ratio
        Pre-condition: highest win avg is calculated and collected
        Post-condition: conferences with highest win avg are printed
    '''
    for key, val in highest_conf.items():
        print("{} : {}".format(str(key), str(val)))




def main():
    '''
        This function opens a file and creates a ConferenceSet object.
        It creates a team object for every noncomment line in the file
        and sends each line into the team object to be processed.
        Then it sends the team object to the ConferenceSet object,
        calculates the conferences with the highest win ratio,
        and prints them out.
        Parameters: None
        Returns: None
        Pre-condition: none
        Post-condition: conferences with highest win avg are printed
    '''

    file = input()

    try:
        file = open(file)
    except:
        print("ERROR: Could not open file " + file)
        sys.exit()


    conf_set = ConferenceSet() #{}

    for line in file:
        if line[0] != "#":   # Makes sure line is noncomment line
            if line[0].isdigit():  # Makes sure line doesnt start with number
                line = line[1:].strip()  # Makes new line without number if
                                         # it does
            team = Team(line)
            conf_set.add(team)
    highest_conf = conf_set.best()

    print_highest_conf(highest_conf)



main()