from flask import Flask, render_template, request
from flask_mysqldb import MySQL

import gensim
import pandas as pd
import nltk
import numpy as np
import re
from scipy.spatial import distance
from nltk.corpus import stopwords

app = Flask(__name__)

model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
stop_words = stopwords.words('english')

'''app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ePaper'
app.config['MySQL_CURSORCLASS'] = 'DictCursor'''

#mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('QA.html')

'''@app.route('/collegeLogin/', methods = ['GET', 'POST'])
def collegeLogin():
    return render_template('collegeLogin.html')

@app.route('/studentLogin/')
def studentLogin():
    return render_template('studentLogin.html')'''

'''@app.route('/collegeLoggedIn/')
def collegeLoggedIn():
    if request.method == 'POST':
        cID = request.form['cID']
        cPassword = request.form['cPass']

        print(cID)

        cur = mysql.connection.cursor()
        result = cur.execute("select * from teacherUser where tID = %s", [cID])

        if result>0:
            data = cur.fetchone()
            password = data['tPassword']

            if sha256_crypt.verify(cPassword,password):
                app.logger.info('Password Matched')
            else:
                app.loogger.info('Wrong Password')
        else:
            app.logger.info('No User')

        cur.close()'''

@app.route('/QA/', methods = ['POST'])
def QA():
    def preprocess(text):
        text = re.sub("[^a-zA-Z]", " ", text)
        text = text.lower().split()
        stopwords_set = set(stopwords.words("english"))
        text = list(set([w for w in text if w not in stopwords_set]))

        s = []
        for i in text:
            if i in model.vocab:
                s.append(i);

        return s

    M1 = "Introduction of Deadlock in Operating System A process in operating systems uses different resources and uses resources in following way. 1) Requests a resource 2) Use the resource 2) Releases the resource  Deadlock is a situation where a set of processes are blocked because each process is holding a resource and waiting for another resource acquired by some other process. Consider an example when two trains are coming toward each other on same track and there is only one track, none of the trains can move once they are in front of each other. Similar situation occurs in operating systems when there are two or more processes hold some resources and wait for resources held by other(s). For example, in the below diagram, Process 1 is holding Resource 1 and waiting for resource 2 which is acquired by process 2, and process 2 is waiting for resource 1.  Deadlock can arise if following four conditions hold simultaneously (Necessary Conditions) Mutual Exclusion: One or more than one resource are non-sharable (Only one process can use at a time) Hold and Wait: A process is holding at least one resource and waiting for resources. No Preemption: A resource cannot be taken from a process unless the process releases the resource. Circular Wait: A set of processes are waiting for each other in circular form. Methods for handling deadlock There are three ways to handle deadlock 1) Deadlock prevention or avoidance: The idea is to not let the system into deadlock state. One can zoom into each category individually, Prevention is done by negating one of above mentioned necessary conditions for deadlock. Avoidance is kind of futuristic in nature. By using strategy of “Avoidance”, we have to make an assumption. We need to ensure that all information about resources which process WILL need are known to us prior to execution of the process. We use Banker’s algorithm (Which is in-turn a gift from) in order to avoid deadlock.  2) Deadlock detection and recovery: Let deadlock occur, then do preemption to handle it once occurred.  3) Ignore the problem all together: If deadlock is very rare, then let it happen and reboot the system. This is the approach that both Windows and UNIX take."

    M2 = "A thread is the smallest unit of processing that can be performed in an OS. In most modern operating systems, a thread exists within a process - that is, a single process may contain multiple threads. You can imagine multitasking as something that allows processes to run concurrently, while multithreading allows sub-processes to run concurrently. When multiple threads are running concurrently, this is known as multithreading, which is similar to multitasking. Basically, an operating system with multitasking capabilities allows programs (or processes) to run seemingly at the same time. On the other hand, a single program with multithreading capabilities allows individual sub-processes (or threads) to run seemingly at the same time. One example of multithreading is downloading a video while playing it at the same time. Multithreading is also used extensively in computer-generated animation. Among the widely-used programming languages that allow developers to work on threads in their program source code are Java, Python and .NET."

    M1 = preprocess(M1)
    M2 = preprocess(M2)

    if request.method == 'POST':
        A1 = request.form['A1']
        A2 = request.form['A2']

        A1 = preprocess(A1)
        A2 = preprocess(A2)

        vector1 = np.mean([model[word] for word in M1], axis=0)
        vector2 = np.mean([model[word] for word in A1], axis=0)

        vector3 = np.mean([model[word] for word in M2], axis=0)
        vector4 = np.mean([model[word] for word in A2], axis=0)

        cosine = distance.cosine(vector1, vector2)
        sim1 = round((1-cosine)*100, 2)

        cosine = distance.cosine(vector3, vector4)
        sim2 = round((1-cosine)*100, 2)

    return render_template('QA.html', A1 = '{}'.format(A1), A2 = '{}'.format(A2), sim1 = '{}'.format(sim1), sim2 = '{}'.format(sim2))

if __name__=="__main__":
    app.run(debug = True)
