from file import save_to_file
from flask import Flask, render_template, request, redirect, send_file
from Extractor.wwr import extract_wwr_jobs
from Extractor.indeed import extract_indeed_jobs
from Extractor.jobkorea import extract_jobkorea_jobs

app = Flask('Job Scrapper', root_path='C:\Project\Web Scrapper', template_folder='templates')

db = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search')
def search():
    keyword = request.args.get('keyword')
    
    if keyword == None or keyword == '':
        return redirect('/')
    
    if keyword in db:
        jobs = db[keyword]
    else:
        wwr = extract_wwr_jobs(keyword)
        indeed = extract_indeed_jobs(keyword)
        jobkorea = extract_jobkorea_jobs(keyword)
    
        jobs = wwr + indeed + jobkorea
        
        db[keyword] = jobs
    
    return render_template('search.html', keyword=keyword, jobs=jobs)

@app.route('/export')
def export():
    keyword = request.args.get('keyword')

    if keyword == None or keyword == '':
        return redirect('/')
    
    if keyword not in db:
        return redirect(f'/search?keyword={keyword}')
    
    save_to_file(keyword, db[keyword])

    return send_file(f'{keyword}.csv', as_attachment=True)

app.run('127.0.0.1')