#v0.0.2 Machine Learning Thesis Server
#James Rusty Haner
#University of Memphis

#Import Modules
import socket
import select
import sys
import os
import csv
import pandas
import string
import numpy as np
from io import StringIO
from random import *
from _thread import *

##################################
#CONFIGURATION VARIABLES
##################################

variables = ["uniqueID"]
userBasePath = 'data/users.pkl'
userDataPathCSV = 'data/users.csv'
userGamePath = 'data/'
questionPath = 'data/survey_questions.csv'
answerPath = 'data/survey_answers.pkl'
answerPathCSV = 'data/survey_answers.csv'


#Start Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((socket.gethostname(), 8888))
server.listen(100)
list_of_clients = [] 


#Server Behavior
def main():
    if is_not_file(userBasePath):
        create_userbase(userBasePath)    
    else:
        print("Userbase Loaded")
    global userBaseData 
    userBaseData = pandas.read_pickle(userBasePath)    
    global surveyQuestionData
    surveyQuestionData = pandas.read_csv(questionPath)
    global surveyAnswerData 
    surveyAnswerData = pandas.read_pickle(answerPath)



    while True:
        conn, addr = server.accept()
        list_of_clients.append(conn)
        start_new_thread(clientthread,(conn,addr))

    conn.close()
    server.close()

######################            
#Project Functions
######################

#functions

def clientthread(conn, addr):
    while True:
        try:
            command = conn.recv(2048)
            if command:
                command = command.decode()
                command = str.rstrip(command)
               
                commandargs = command.split(",")
             
                arg = commandargs[1:len(commandargs)]
                if commandargs[0] in func_dict:
                    func_dict[commandargs[0]](conn,arg)
                else:
                    message = "Error"
                    conn.send(message.encode())
                
            else:
                conn.close()
            
        except:
            continue

def answer_question(conn,args):
    df = surveyAnswerData
    uniqueID = int(args[0])
    questionNo = "QID" + str(args[1])
    lookup = df.loc[df['UniqueID'] == uniqueID]
    answer = args[2]
    if(len(lookup) == 0):
        data = {'UniqueID':[uniqueID]}
        pd = pandas.DataFrame(data,columns= ['UniqueID'])
        df = pandas.concat([df,pd], ignore_index=True)
    df.loc[df['UniqueID'] == uniqueID, questionNo] = answer
    df.to_pickle(answerPath)
    df.to_csv(answerPathCSV)
    conn.send("True".encode())
 


def create_userbase(userBasePath):
    data = {'UniqueID':[0],'Survey':[0],'Consent':[0]}
    pd = pandas.DataFrame(data, columns = ['UniqueID','Survey','Consent'])
    pd['Survey'][0] = 0
    pd.to_pickle(userBasePath)
    pd.to_csv(userDataPathCSV)
    print("Created Userbase.")
    data2 = {'UniqueID':[0]}
    df2 = pandas.DataFrame(data2, columns = ['UniqueID'])
    pd.to_pickle(answerPath)
    pd.to_csv(answerPathCSV)

def create_user_game_data(uID):
    data = {'UniqueID':[uID],'GameNo':[1],'LastState':[0],'RR':[.33],'RP':[.33],'RS':[.33],'PR':[.33],'PP':[.33],'PS':[.33],'SR':[.33],'SP':[.33],'SS':[.33], 'Win':[0]}
    pd = pandas.DataFrame(data, columns = ['UniqueID','GameNo','LastState','RR','RP',"RS","PR","PP","PS","SR","SP","SS","Win"])
    storePath = userGamePath + "Player_" + str(uID) + ".pkl"
    storePathCSV = userGamePath + "Player_" + str(uID) + ".csv"
    pd.to_pickle(storePath)
    pd.to_csv(storePathCSV)
 

def load_questions():   
    pd = surveyQuestionData
    return pd

def games_played(conn,args):
    uniqueID = args[0]
    playerGameData = userGamePath + "Player_" + uniqueID + ".pkl"
    if(is_not_file(playerGameData)):
        bob = ""
    else:
        pd = pandas.read_pickle(playerGameData)


def get_consent(conn,args):
    print("Login:" + args[0])
    uniqueID = int(args[0])
    df = userBaseData
    df.loc[df['UniqueID'] == uniqueID, 'Consent'] = 1
    message = "Consent Given"
    conn.send(str(message).encode())
    df.to_pickle('data/users.pkl')
    df.to_csv('data/users.csv')


def get_notifications(conn,args):
    print("Not implemented.")

def get_question(conn,args):
    pd = load_questions()
    question = int(args[0]) - 1
    noQuestions = pd.shape[1] - 4
    i = 0
    component = "Question"
    df = pd.iloc[question]
    message= str(df[component])
    component = "Type"
    df = pd.iloc[question]
    message = message + "," + str(df[component])
    while i < noQuestions:
        component = "Answer" + str(i + 1)
        message = message + "," + str(df[component]) 
        i = i + 1
    conn.send(message.encode())

    


def get_no_of_questions(conn,args):
    survey = load_questions()
    message = str(survey.shape[0])
    conn.send(message.encode())

def get_no_of_questions_answers(conn,args):
    survey = load_questions()
    message = str(survey.shape[1] - 4)
    conn.send(message.encode())


def get_survey_selected(conn,args):
    uniqueID = int(args[0])
    df = pandas.read_csv(userDataPathCSV)
    df2 = df.loc[df['UniqueID'] == uniqueID]
    message = int(df2['Survey'])
    conn.send(str(message).encode())
    
def heartbeat(conn,args):

    message = "True"
    conn.send(message.encode())

def is_not_file(file):
    return not os.path.isfile(file)

def login(conn,args):
    print("Login:" + args[0])
    uniqueID = int(args[0])
    df = pandas.read_pickle(userBasePath)
    print ("Userbase loaded.")
    df2 = df.loc[df['UniqueID'] == uniqueID]
    print(df2)
    if len(df2) == 0:
        message = "False"
        conn.send(message.encode())
    else:
        message = "True"
        conn.send(message.encode())

def register(conn,args):
    df = pandas.read_pickle(userBasePath)
    success = False
    while success == False:
    
        rando = randint(0,999)
        print("Try:" + str(rando))
        df2 = df.loc[df['UniqueID'] == rando]
        if len(df2) == 0:
     
            data = {'UniqueID':[rando],'Survey':[0],'Consent':[0]}
    
            pd = pandas.DataFrame(data, columns = ['UniqueID','Survey','Consent'])
   
            dfnew = pandas.concat([df,pd], ignore_index=True)
    
            dfnew.to_pickle(userBasePath)
            dfnew.to_csv(userDataPathCSV)
            
            create_user_game_data(rando)
            success = True
            conn.send(str(rando).encode())
            





#Markov Chain
def markov_chain_play(conn, arg):
    uniqueID = arg[0]
    playerState = arg[1]
    playerGameData = userGamePath + "Player_" + uniqueID + ".pkl"
    if(is_not_file(playerGameData)):
        print("Error: UID not found. Register.")
    else:
        pd = pandas.read_pickle(playerGameData)
        
        states = ["Rock","Paper","Scissors"]
        choice = randint(1,100) / 100
        lastGame = pd.shape[0]
        lastState = int(pd.tail(1)['LastState'])

        if lastState == 0:
         
            lastState = randint(1,3)
            
    
        if lastState == 1:
            lastState = "R"
        if lastState == 2:
            lastState = "P"
        if lastState == 3:
            lastState = "S" 
        randomizer = randint(0,100) / 100
        predRock = str(lastState + "R")
        predPaper = str(lastState + "P")
        predSci = str(lastState + "S")
        gamesPlayed = pd.shape[0]
        wins = pd.loc[pd['Win'] == 1].shape[0]
        acc = round(int(wins) / int(gamesPlayed) * 100 ,2)
  
        

      
        data2 = {'UniqueID':[uniqueID],'GameNo':[1],'LastState':[0],'RR':[.33],'RP':[.33],'RS':[.33],'PR':[.33],'PP':[.33],'PS':[.33],'SR':[.33],'SP':[.33],'SS':[.33],'Win':[0]}
        df2 = pandas.DataFrame(data2, columns = ['UniqueID','GameNo','LastState','RR','RP',"RS","PR","PP","PS","SR","SP","SS","Win"])

        if randomizer > 1 - float(pd.tail(1)[predSci]):
            move = "Rock"
            moveInt = 1
        elif randomizer < float(pd.tail(1)[predRock]) + float(pd.tail(1)[predPaper]):
            move = "Paper"
            moveInt = 2
        elif randomizer < float(pd.tail(1)[predRock]):
            move = "Scissors"
            moveInt = 3
        if playerState == "1" and moveInt == 1:
            message = move + ",Tie," + str(acc)
            result = 0
        elif playerState == "1" and moveInt == 2:
            message = move + ",Loss," + str(acc)  
            result = 1
        elif playerState == "1" and moveInt == 3:
            message = move + ",Win," + str(acc) 
            result = 0
        elif playerState == "2" and moveInt == 2:
            message = move + ",Tie," + str(acc)  
            result = 0
        elif playerState == "2" and moveInt == 1:
            message = move + ",Win," + str(acc) 
            result = 0
        elif playerState == "2" and moveInt == 3:
            message = move + ",Loss," + str(acc)  
            result = 1
        elif playerState == "3" and moveInt == 3:
            message = move + ",Tie," + str(acc)  
            result = 0
        elif playerState == "3" and moveInt == 1:
            message = move + ",Loss," + str(acc)  
            result = 1
        elif playerState == "3" and moveInt == 2:
            message = move + ",Win," + str(acc) 
            result = 0
        else:
            message = "Error."
        if playerState == "1":
            thisState = "R"
            notState1 = "P"
            notState2 = "S"
        elif playerState == "2":
            thisState = "P"
            notState1 = "R"
            notState2 = "S"
        elif playerState == "3":
            thisState = "S"
            notState1 = "P"
            notState2 = "R"
        else: 
            message = "Error."

        df2.tail(1)['LastState'] = int(playerState)
        count = int(pd.tail(1)['GameNo']) + 1
        df2.tail(1)['GameNo'] = count
        increase = 1 / count / 2
        pred = str(lastState + thisState)
        prednot1 = str(lastState + notState1)
        prednot2 = str(lastState + notState2)
        df2.is_copy = False

        df2[pred][0] = pd[pred].tail(1) + increase
        if df2[pred][0] > 1:
            df2[pred][0] = 1
  
        df2.is_copy = False

        df2[prednot1][0] = (1 - df2[pred][0]) / 2
        df2[prednot2][0] = (1 - df2[pred][0]) / 2
        df2['Win'] = result
        
        #FIX: NOT CONCATING CORRECTLY
    
      
        df3 = pandas.concat([pd,df2], ignore_index=True)

        storePath = userGamePath + "Player_" + str(uniqueID) + ".pkl"
        storePathCSV = userGamePath + "Player_" + str(uniqueID) + ".csv"
        df3.to_pickle(storePath)
        df3.to_csv(storePathCSV)


                

    

    conn.send(message.encode())


    





#Function Dictionary
func_dict = {'heartbeat':heartbeat, 'register':register, 'login':login, 'markov':markov_chain_play, 'gamesplayed':games_played, 'get_if_selected':get_survey_selected, 'get_consent':get_consent, 'get_question':get_question, 'answer_question':answer_question, 'get_no_of_answers':get_no_of_questions_answers, 'get_no_of_questions':get_no_of_questions}

#EXECUTE
main()
