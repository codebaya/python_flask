from flask import Flask, render_template,\
    request, redirect, send_file
from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_jobs
from file import save_to_file

app = Flask("JobScrapper")

db = {}
print("db : ", db)
@app.route("/")
def home():
    return render_template("hommie.html", name="glory")

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else:
        indeed = extract_indeed_jobs(keyword)
        wwr = extract_jobs(keyword)
        jobs = indeed + wwr
        db[keyword] = jobs

    print(f"db {db}")
    return render_template("search.html", keyword=keyword, jobs=jobs)

@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")

    save_to_file(keyword, db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)

app.run("0.0.0.0")










# from extractors.indeed import extract_indeed_jobs
# from extractors.wwr import extract_jobs
# from file import save_to_file
#
# # keyword = input("What do you want to search for a job : ")
# keyword = "python"
# indeed = extract_indeed_jobs(keyword)
# wwr = extract_jobs(keyword)
# jobs = indeed + wwr
#
# save_to_file(keyword, jobs)



