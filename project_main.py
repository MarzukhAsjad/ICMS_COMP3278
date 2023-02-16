from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from datetime import datetime
import sys
import smtplib
import ssl
from email.message import EmailMessage

import mysql.connector
from main_window import *
from face_login import *


class Main(QMainWindow):
    def __init__(self):
        email_body_string = []
        lecture, tutorials, others_ = [], [], []
        super().__init__()
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.user_name = ""
        self.logged_in = False

        if self.logged_in == False:
            self.ui.weekly_timetable_button.setEnabled(False)
            self.ui.activity_record_button.setEnabled(False)
            self.ui.course_info_one_hour_button.setEnabled(False)


        myconn = mysql.connector.connect(host="localhost", user="root", passwd="sonovabitch123", database="project")
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M")
        
        
        def login(username):
            print("User name is ", username)
            result = try_login(username)
            if result == True:
                msg = QMessageBox()
                msg.setText("Login Sucessful!")
                self.user_name = username
                x = msg.exec_()
                self.ui.stackedWidget.setCurrentWidget(self.ui.course_info)
                self.logged_in = True
                self.ui.accounts_button.setEnabled(False)
                self.ui.weekly_timetable_button.setEnabled(True)
                self.ui.activity_record_button.setEnabled(True)
                self.ui.course_info_one_hour_button.setEnabled(True)
                upcoming_class()

            elif result == False:
                msg = QMessageBox()
                msg.setText("Cannot Identify Your Face!")
                x = msg.exec_()

            elif result == "not found":
                msg = QMessageBox()
                msg.setText("User Name Not Found!")
                x = msg.exec_() 

        # this is the upcoming_class function (tuple)
        # this function will run if the check_upcoming_class function returns true
            # will execute a query to find out the corresponding class information and course materials
            # the result from the query will be a tuple
            # the tuple will then be formatted to display to the upcoming class page
            # INSERT the current time, date and "Upcoming Class" page into the activity_record table

        def upcoming_class():
            # QUERY
            select = f'''SELECT
                C.course_id, C.course_name,
                CM.material_type, CM.material,
                T1.classroom_address, TIMEDIFF(T1.start_time, CURRENT_TIMESTAMP) AS time_to_class
            FROM
                (SELECT course_id, classroom_address, start_time
                FROM Class
                WHERE HOUR(TIMEDIFF(CURRENT_TIMESTAMP,start_time)) < 1
                AND MINUTE(TIMEDIFF(CURRENT_TIMESTAMP,start_time)) < 60) T1,
                Course C, Course_Materials CM, Student, Study
            WHERE
                T1.course_id = C.course_id AND 
                T1.course_id = CM.course_id AND 
                T1.course_id = Study.course_id AND 
                Student.student_id = Study.student_id 
                AND Student.name = '{self.user_name}' '''
            
            myconn = mysql.connector.connect(host="localhost", user="root", passwd="sonovabitch123", database="project")
            cursor = myconn.cursor()
            #insert view record to activity record
            insert = f'''INSERT INTO Activity(activity,activity_time,student_id)
                        SELECT 'View Course Info',CURRENT_TIMESTAMP,T1.student_id
                        FROM (
                            SELECT student_id
                            FROM Student
                            WHERE Student.name = "{self.user_name}") T1;'''
            cursor.execute(insert)
            myconn.commit()
            #get course info in one hour
            cursor.execute(select)
            
            result = cursor.fetchall()

            columns = ["course_id", "course_name", "material_type", "material" , "address", "time_to_class"]

            data = {key: [] for key in columns}

            if (result == []):
                # you have no upcoming class
                pass 
            else:
                # enable the button for the upcoming class
                for i in result:
                    for k, j in zip(columns, i):
                        data[k].append(j)
            
            
            # display the data into the UI

            there_is_class_text = ""
            course_code_text = ""
            lecture_notes_text = ""
            tutorial_notes_text = ""
            others_text = ""
            zoom_link_text = ""
            latest_message_text = ""

            if (result == []): # if there is no class within the next one hour
                there_is_class_text = "You have no class within the next one hour"
                course_code_text = "---- No class now ----"
                lecture_notes_text = "Lecture Notes\n"
                tutorial_notes_text = "Tutorial Notes\n"
                others_text = "Others\n"
                zoom_link_text = "Lecture Zoom Link\n%s\nTutorial Zoom Link\n%s\n" % ("\n", "\n")
                latest_message_text = "No latest message right now"
            else:
                there_is_class_text = "You have %s at %s in %s minutes" % (data["course_id"][0], 
                                data["address"][0], str(data["time_to_class"][0])[2:4])
                course_code_text = "%s %s" % ( data["course_id"][0], data["course_name"][0])
                zoom_link_text = " Lecture Zoom Link\n%s\nTutorial Zoom Link\n%s\n" % ("https://hku.zoom.us/j/94999822117?pwd=MDBSR0J3d3FiWHo3RmlFZHlzNTNwQT09#success", "\n")
                lecture_notes = ""
                tutorial_notes= ""
                others = ""
                for i in result:
                    if i[2] == "lecture_notes":
                        lecture_notes+= i[3] + "\n\n"
                for i in result:
                    if i[2] == "tutorial_notes":
                        tutorial_notes+= i[3] + "\n\n"
                for i in result:
                    if i[2] == "others":
                        others+= i[3] + "\n\n"


                lecture_notes_text = "Lecture \n\n" + lecture_notes
                tutorial_notes_text = "Tutorial Notes\n\n" + tutorial_notes
                others_text = "Others\n\n" + others

                lecture.append(lecture_notes_text)
                tutorials.append(tutorial_notes_text)
                others_.append(others_text)

                email_body_string.append(lecture[-1] + tutorials[-1] + others_[-1])
                # THE FOLLOWING ARE FROM COURSE MATERIALS WHICH HAVE TO BE DECOMPOSED
                # implement lecture notes
                # implement tutorial notes
                # implement others
                # implement latest message
            self.ui.welcome.setFontPointSize(45)
            self.ui.welcome.setText(f"Welcome Back,{self.user_name} !")
            self.ui.whether_have_class.setText(there_is_class_text)
            self.ui.course_code.setText(course_code_text)
            self.ui.lecture_notes.setText(lecture_notes_text)
            self.ui.tutorial_notes.setText(tutorial_notes_text)
            self.ui.others.setText(others_text)
            self.ui.zoom_link.setText(zoom_link_text)
            self.ui.latest_message.setText(latest_message_text)
            current_time = now.strftime("%Y-%m-%d %H:%M")
            self.ui.time_now.setText("The time now is " + current_time)

            # ----- TO BE IMPLEMENTED ------
            # self.ui.welcome
            # self.ui.time_now
         
            # insert current time into the activity records page
            # ------- TO BE IMPLEMENTED -------

            # changes the current widget into the 1 hour course info page
            self.ui.stackedWidget.setCurrentWidget(self.ui.course_info)


        # this is the timetable function (list of tuples)
            # will execute a query to find out class timings and corresponding course information and return in list of tuples (fetchall)
            # the list of tuples will be split into different records for each days
            # each day will be displayed with its corresponding classes, course code, title and address
            # INSERT the current time, date and "Timetable" page into the activity_record table

        def timetable():
            # QUERY
            select = f"""
                SELECT CL.start_time, CL.end_time, CL.course_id, CO.course_name, CL.classroom_address
                FROM Class CL, Course CO, Student, Study
                WHERE CL.course_id = CO.course_id
                AND Study.student_id = Student.student_id
                AND Study.course_id = CO.course_id
                AND DATEDIFF(CL.start_time,CURRENT_TIMESTAMP) < 7
                AND Student.name = '{self.user_name}'
                ORDER BY CL.start_time;
                """
            myconn = mysql.connector.connect(host="localhost", user="root", passwd="sonovabitch123", database="project")
            cursor = myconn.cursor()
            #insert view record to activity record
            insert = f'''INSERT INTO Activity(activity,activity_time,student_id)
                        SELECT 'View Timetable',CURRENT_TIMESTAMP,T1.student_id
                        FROM (
                            SELECT student_id
                            FROM Student
                            WHERE Student.name = "{self.user_name}") T1;'''
            cursor.execute(insert)
            myconn.commit()

            cursor.execute(select)
            # and store the tuples in result
            result = cursor.fetchall()
            
            # the columns in the result
            columns = ["start_time", "end_time", "course_id", "course_name", "classroom_address"]
            # the data dictionary 
            data = {key: [] for key in columns}
            # appending the data to the dictionary
            if (result != []): # if not an empty list
                for i in result:
                    for k, j in zip(columns, i):
                        data[k].append(j)

            # display the data into the UI
            
            # self.ui.welcome_2
            # self.ui.time_now_2

            length_data = len(data['start_time'])

            rows = []
            for i in range(length_data):
                duration = str(data["start_time"][i]) + " - " + str(data["end_time"][i])
                course_code = data["course_id"][i]
                course_name = data["course_name"][i]
                classroom = data["classroom_address"][i]
                row_string = "\n\n" + duration + "  " + course_code + "  " + course_name + "  at classroom  " + classroom 
                rows.append(row_string)

            
            timetable_string = '\n'.join(rows)
            email_body_string = timetable_string
            self.ui.weekly_timetable.setText(timetable_string)
            self.ui.welcome_2.setFontPointSize(45)
            self.ui.welcome_2.setText(f"Welcome Back,{self.user_name} !")
            current_time = now.strftime("%Y-%m-%d %H:%M")
            self.ui.time_now_2.setFontPointSize(25)
            self.ui.time_now_2.setText("The time now is " + current_time)

            # insert current time into the activity records page
            # ------- TO BE IMPLEMENTED -------

            # set email button to function
            self.ui.email_button.setEnabled(True)
            # changes the current widget into the 1 hour course info page
            self.ui.stackedWidget.setCurrentWidget(self.ui.timetable)


        # this is the activity function (list of tuples)
            # will execute a query to return the top 6 entries of the activity_record table
            # resulting tuple will be decomposed into separate tuples and then inserted into tabulated form in the ui
            # INSERT the current time, date and "Activity" page into the activity_record table

        def activity_records():
            # QUERY
            select = f"""
                SELECT activity, activity_time
                FROM Activity, Student
                where Student.name = '{self.user_name}' AND
                Student.student_id = Activity.student_id
                ORDER BY activity_time DESC
                LIMIT 6;
                """
            myconn = mysql.connector.connect(host="localhost", user="root", passwd="sonovabitch123", database="project")
            cursor = myconn.cursor()
            #insert view record to activity record
            insert = f'''INSERT INTO Activity(activity,activity_time,student_id)
                        SELECT 'View Activity Record',CURRENT_TIMESTAMP,T1.student_id
                        FROM (
                            SELECT student_id
                            FROM Student
                            WHERE Student.name = "{self.user_name}") T1;'''
            cursor.execute(insert)
            myconn.commit()

            cursor.execute(select)
            # and store the tuples in result
            result = cursor.fetchall() # [] or [(efne, enfje, eifne), (ejnfjej, efnef, efne)]
            # the columns in the result
            columns = ["activity", "activity_time"]
            # the data dictionary 
            data = {key: [] for key in columns}
            # appending the data to the dictionary
            if (result != []): # if not an empty list
                for i in result:
                    for k, j in zip(columns, i):
                        data[k].append(j)

            # display the data into the UI
            
            activity_names = [self.ui.activity_0, self.ui.activity_1, self.ui.activity_2, self.ui.activity_3,
            self.ui.activity_4, self.ui.activity_5]

            activity_dates = [self.ui.date_0, self.ui.date_1, self.ui.date_2, self.ui.date_3, self.ui.date_4, 
            self.ui.date_5]

            length_data = len(data['activity'])
           
            # setting the text of the buttons
            for k in range(length_data):
                activity_names[k].setText(data['activity'][k])
                activity_dates[k].setText(str(data['activity_time'][k]))

            # insert current time into the activity records page
            # ------- TO BE IMPLEMENTED -------

            # changes the current widget into the 1 hour course info page
            self.ui.stackedWidget.setCurrentWidget(self.ui.activity_record)

        def email_to_user(subject_p):
            # Define email sender and receiver
            email_sender = 'icms.comp3278@gmail.com'
            email_password = 'gzlazooevbjddpkx'
            email_receiver = 'marz.asjad00@gmail.com'

            # Set the subject and body of the email
            if (subject_p == None):
                subject = 'Course Timetable'
            elif (subject_p == 'timetable'):
                subject = 'Course Timetable'
            elif (subject_p == 'upcoming class info'):
                subject = 'Upcoming Class Information'
         
            
            body = email_body_string[-1]

            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.set_content(body)

            # Add SSL (layer of security)
            context = ssl.create_default_context()

            # Log in and send the email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())
        

        # deafult is account page
        self.ui.stackedWidget.setCurrentWidget(self.ui.accounts_page)


        # ---------- NOTES FOR ME -----------
        # in these sections, setEnabled only disables them but does not remove them. hide() removes it
        # button.setText changes the Text, but font and everything is different ------ solve required

        self.ui.welcome.setReadOnly(True)
        self.ui.time_now.setReadOnly(True)
        self.ui.whether_have_class.setReadOnly(True)
        self.ui.course_code.setReadOnly(True)

        # the following three sections are columns (check whether they are strings with new line or something else)
        self.ui.lecture_notes.setReadOnly(True)
        self.ui.tutorial_notes.setReadOnly(True)
        self.ui.others.setReadOnly(True)
        # --- text box? ---
        self.ui.latest_message.setReadOnly(True)
        self.ui.zoom_link.setReadOnly(True)
        self.ui.welcome_to_icms.setReadOnly(True)
        self.ui.welcome_2.setReadOnly(True)
        self.ui.time_now_2.setReadOnly(True)
        self.ui.below_timetable.setReadOnly(True)
        # Note that weekly time table requires us to input as string only (could be changed into table format if there's time left)
        self.ui.weekly_timetable.setReadOnly(True)

        
        self.ui.activity_0.setReadOnly(True)
        self.ui.activity_1.setReadOnly(True)
        self.ui.activity_2.setReadOnly(True)
        self.ui.activity_3.setReadOnly(True)
        self.ui.activity_4.setReadOnly(True)
        self.ui.activity_5.setReadOnly(True)

        self.ui.date_0.setReadOnly(True)
        self.ui.date_1.setReadOnly(True)
        self.ui.date_2.setReadOnly(True)
        self.ui.date_3.setReadOnly(True)
        self.ui.date_4.setReadOnly(True)
        self.ui.date_5.setReadOnly(True)

        self.ui.activity_record_text.setReadOnly(True)
        self.ui.date_and_time.setReadOnly(True)






        # STACKED PAGES NAVIGATION/////////////////
        #Using side menu buttons


        #navigate to Accounts page
        self.ui.accounts_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.accounts_page))

        # call the login function when login button is pressed
        self.ui.login_button.clicked.connect(lambda: login(self.ui.user_name_input.text()))
        
        # call the upcoming_class function when this button is clicked
        self.ui.course_info_one_hour_button.clicked.connect(lambda: upcoming_class())

        # call the timetable function when this button is clicked
        self.ui.weekly_timetable_button.clicked.connect(lambda: timetable())

        # call the activity_record function when this button is clicked
        self.ui.activity_record_button.clicked.connect(lambda: activity_records())

        # call the email_timetable function when this button is clicked
        self.ui.email_button.clicked.connect(lambda: email_to_user('timetable'))

        self.ui.email_button_2.clicked.connect(lambda: email_to_user('upcoming class info'))
        
        self.show()



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())