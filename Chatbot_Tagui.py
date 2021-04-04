from chatterbot import  ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import rpa as r
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext as ScrolledText
import time
from beepy import beep
import threading

class TaguiGUI(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)

        self.chatbot = ChatBot(storage_adapter='chatterbot.storage.SQLStorageAdapter',name='TaguiBot',read_only=True,logic_adapters=["chatterbot.logic.MathematicalEvaluation","chatterbot.logic.BestMatch"],database_uri='sqlite:///database-chatbot.d')
        self.small_talk = ['hi there!',
          'hi!',
          'how do you do?',
          'how are you?',
          'i\'m cool.',
          'fine, you?',
          'always cool.',
          'i\'m ok',
          'glad to hear that.',
          'i\'m fine',
          'glad to hear that.',
          'i feel awesome',
          'excellent, glad to hear that.',
          'not so good',
          'sorry to hear that.',
          'what\'s your name?',
          'i\'m pybot. ask me a math question, please.']

        self.data_talk_1=['Can you do me a favour','yes sure, tell me please!']
        self.data_talk = ['I need to do currency conversion',
             'enter the details please!']
        self.data_talk_2 = ['Thank you',
             'You are welcome!']
        self.data_talk_3= ['How are you?','i am fine']
        self.data_talk_4= ['I am fine!','Good to know that, May i know how can i help you!']
        self.list_trainer = ListTrainer(self.chatbot)

        for item in (self.small_talk,self.data_talk,self.data_talk_1,self.data_talk_2,self.data_talk_3,self.data_talk_4):
            
            
            
            self.list_trainer.train(item)
    
    
    
    
    

        self.corpus_trainer = ChatterBotCorpusTrainer(self.chatbot)
        self.corpus_trainer.train('chatterbot.corpus.english')    
        self.title('Tagui Chatbot')
        self.counter=0
        self.l =[]
        self.intialize()

    def intialize(self):
        self.grid()
        self.response = ttk.Button(self,text='Send Message',command =self.get_operate)
        self.response.grid(column=0,row=1,padx=3,pady=3)
        self.bind('<Return>', lambda event=None: self.response.invoke())
        self.usr_input = ttk.Entry(self, state='normal',font = "Helvetica 14")
        self.usr_input.grid(column=1, row=1, ipadx=30,ipady=20)

        self.conversation = ScrolledText.ScrolledText(self, state='disabled',width = 70,height=20,font = "Helvetica 14",bg = "#17202A",fg = "#EAECEE",)
        self.conversation.grid(column=0, row=0, columnspan=2, padx=3, pady=3)
        self.conversation.focus()
        
    def get_operate(self):
        th = threading.Thread(target=self.get_response)
        th.start()
    
    def currency_conversion(self,amount,fr,to):
        
        r.init()
        r.url('https://www.calculator.net/currency-calculator.html')
        r.type('//input[@type="text"]','[clear]'+amount)
        r.select('//select[@name="efrom"]',fr)
        r.select('//select[@name="eto"]',to)
        r.click('//input[@value="Calculate"]')
        data = r.read('//font[@color="green"]')
        result=f'{amount} {fr} is equal to {data} {to}'
        r.close()
        return result
        
    def get_answer(self,answer):
        
        time.sleep(0.5)    
        self.conversation['state'] = 'normal'
        self.conversation.insert(
            tk.END,  "Tagui_Bot: " + str(answer) + "\n\n"
        )
        self.conversation['state'] = 'disabled'
        beep(sound='coin')
        time.sleep(0.5)
        




        
    def get_response(self):

        
        user_input = self.usr_input.get()
        self.conversation['state'] = 'normal'
        self.conversation.insert(
            tk.END, "You: " + user_input+"\n"
        )
        self.conversation['state'] = 'disabled'
        

        
        self.usr_input.delete(0, tk.END)
        if user_input=='I need to do currency conversion':
            answer = 'Enter the amount'
            self.counter=1
            
        elif self.counter==1:
            amount = user_input
            self.l.append(amount)
            answer = 'Enter the currency type u need conversion from'
            self.counter=2
        elif self.counter ==2:
            fr = user_input
            self.l.append(fr)
            answer = 'Enter the currency type u need conversion to'
            
            self.counter=3
        elif self.counter==3:
            answer='Please wait..., getting latest forex rate to calculate for you..'
            self.get_answer(answer)
            to = user_input
            self.l.append(to)
            answer = 'The currency conversion is here , '+self.currency_conversion(self.l[0],self.l[1],self.l[2])
            self.l=[]
            self.counter=0
        else:
            response = self.chatbot.get_response(user_input)
            answer=response.text

        time.sleep(0.5)    
        self.conversation['state'] = 'normal'
        self.conversation.insert(
            tk.END,  "Tagui_Bot: " + str(answer) + "\n\n"
        )
        self.conversation['state'] = 'disabled'
        beep(sound='coin')
        time.sleep(0.5)
        

        





gui_example = TaguiGUI()
gui_example.mainloop()

        
        
            
            

        
