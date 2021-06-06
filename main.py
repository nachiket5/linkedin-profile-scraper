from flask import Flask, request, render_template,jsonify,redirect
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    
db = SQLAlchemy(app)
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    desig = db.Column(db.String(500), nullable=False)
    p_link = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.name} - {self.des} - {self.p_l} - {self.date_created} "
   

@app.route('/', methods=['GET','POST'])
def my_form_post():
    if request.method=='POST':
        text = request.form['Type']
        text1 = request.form['Area']
        email = request.form['email']
        password = request.form['password']
        option = webdriver.ChromeOptions()
        option.add_argument('headless')

        driver = webdriver.Chrome('/home/nachiket/api_python/chromedriver')#,options=option)
        # driver = webdriver.Chrome(executable_path=str(os.environ.get('CHROMEDRIVER_PATH')),options=option)

        url = 'https://www.linkedin.com/checkpoint/lg/login'
        driver.get(url)
        driver.find_element_by_xpath('//*[@id="username"]').send_keys(email)
        driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
        driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button').click()

        url = 'https://google.com'
        driver.get(url)
        driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(f'site:linkedin.com/in/ AND "{text}"  AND "{text1}"',Keys.RETURN)
        final_r =[]
        for j in range(1):
            content = driver.page_source
            soup = BeautifulSoup(content,'lxml')
            for i in soup.findAll('div',{'class':'yuRUbf'}):
                p =i.find('a')
                link =p['href']
                final_r.append(link)

            # driver.find_element_by_xpath('//*[@id="xjs"]/table/tbody/tr/td[12]').click()
        for i in final_r[:5]:
            driver.get(i)
            pg = driver.page_source
            namme= 'nachi'
            desig = ''
            string_desig = "patel"
            s = BeautifulSoup(pg,'lxml')
            for sf in s.findAll('div',{'class':'pv-text-details__left-panel mr5'}):
                n = sf.find('h1',{'class':'text-heading-xlarge inline t-24 v-align-middle break-words'}).text
                namme = n
                desig =sf.find('div',{'class':'text-body-medium break-words'}).text
                desig = desig.split("\n")
                non_empty_lines_desig = [line for line in desig if line.strip() != ""]
                string_without_empty_lines_desig = ""
                for line in non_empty_lines_desig:
                    string_without_empty_lines_desig += line
                string_without_empty_lines_desig = string_without_empty_lines_desig.replace(' ','')
                string_desig = string_without_empty_lines_desig
                # print(string_without_empty_lines_desig)   
                # print(namme)

            todo = Todo(name = namme,desig = string_desig, p_link = i)
            db.session.add(todo)
            db.session.commit()
        
    allTodo = Todo.query.all()
    return render_template('html_cd.html',allTodo = allTodo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True,port=8000)
