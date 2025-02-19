from flask import Flask, render_template, request, url_for, redirect, flash, jsonify, make_response, json
from restaurants import getListOfRestaurants
from reviews import getReviews
from forms import SearchForm
from sentiment import analyzeReviews, translate
from jsonUtils import dictToJSONdata, JSONtoDict
from fileUtils import createSearchRestaurantsFileName, createRestaurantReviewsFileName
from dataVisualizationPrep import prepareMostRepeatedWords

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ac4baecbcecee02735c522e42072ede1'

userInput = {}

@app.route("/", methods=['GET'])
def home():
    form = SearchForm(request.form)
    return render_template('index.html', title='Home', form=form)

@app.route("/restaurants", methods=['POST'])
def searchRestaurantList():
    form = SearchForm(request.form)
    if form.validate_on_submit():
        near = form.near.data
        find = form.find.data
        # todo: look up JSON file for this search to reduce scraping same data

        restaurants = getListOfRestaurants(find, near)
        dictToJSONdata({'data': restaurants, 'fileName': createSearchRestaurantsFileName(find, near)})
        return render_template('showList.html', title="Restaurant List", find=find, near=near, restaurants=restaurants)
    else:
        print(form.errors)
        return render_template('index.html', title='Home', form=form)


@app.route("/loading")
def loading():
    urlPath = request.args.get('url')
    name = request.args.get('name')
    return render_template('loading.html', title="Loading", loadingLabel="Analyzing reviews..", data={'url':urlPath,'name':name})

@app.route("/analyze-reviews")
def loadingAndAnalyzingReviews():
    urlPath = request.args.get('url')
    name = request.args.get('name')
    userInput['name'] = name
    reviews = getReviews(urlPath)
    analyzedData = analyzeReviews(reviews)
    dictToJSONdata({'data': {"reviews": reviews, "analyzedData": analyzedData}, 'fileName': createRestaurantReviewsFileName(name)})

    return {"reviews":reviews, "data":analyzedData, "name":name}


@app.route("/reviews", methods=['GET'])
def showAnalyzedReviews():
    name = request.args.get('name')
    data = JSONtoDict(createRestaurantReviewsFileName(name))
    return render_template('reviews.html', title="Reviews", reviews=data.get('reviews'), data=data.get('analyzedData'), name=name)


@app.route("/about")
def about():
    return render_template('about.html', title="About")


@app.route("/bubble")
def bubble():
    name = userInput.get('name')
    data = JSONtoDict(createRestaurantReviewsFileName(name))
    prepareMostRepeatedWords(data['reviews'])
    return render_template('bubble.html', title="Bubble Chart", name=name)


@app.route("/contact")
def contact():
    return render_template('contact.html', title="Contact")

@app.route("/translate", methods=['GET'])
def translateReviews():
    name = userInput.get('name')
    data = JSONtoDict(createRestaurantReviewsFileName(name))
    language = request.args.get('lang')

    return render_template('lang.html', title="Translation", reviews=translate(data['reviews'], language), name=name, data=data['analyzedData'])


if __name__ == '__main__':
    app.run(debug=True)
