from flask import Flask, render_template, request, Response
import requests

app = Flask(__name__)

@app.route('/')
def home():
    """
    Serves the home page of the web application.
    """
    return render_template('index.html')

@app.route('/show_users_front', methods=['POST'])
def show_users_front():
    """
    Fetches and displays information about users from the backend service.
    """
    # Request user-related information from the backend service.
    response = requests.get(f"http://backend-service:5000/show_users", stream=True)
    
    # Return the backend service's response directly to the client.
    return Response(response.content, content_type=response.headers['Content-Type'])


@app.route('/digest', methods=['POST'])
def digest():
    """
    Handles the request to digest tokens and fetch relevant tweets.
    This route forwards the request to the backend service and returns its response.
    """
    # Retrieve tokens from the form data submitted with the POST request.
    tokens = request.form['tokens']

    # Make a request to the backend service to process the given tokens and fetch tweets.
    response = requests.get(f"http://backend-service:5000/show_tweets?tokens={tokens}", stream=True)

    # Return the backend service's response directly to the client.
    return Response(response.content, content_type=response.headers['Content-Type'])


@app.route('/show_tweets_top', methods=['POST'])
def top_tweets_front():
    """
    Retrieves and displays the top tweets based on certain criteria from the backend service.
    """
    # Request the top tweets visualization from the backend service.
    response = requests.get(f"http://backend-service:5000/show_tweets_top", stream=True)
    
    # Return the backend service's response directly to the client.
    return Response(response.content, content_type=response.headers['Content-Type'])


@app.route('/show_dist', methods=['POST'])
def tweets_distribution():
    """
    Fetches and displays the distribution of tweets from the backend service.
    """
    # Request the tweet distribution visualization from the backend service.
    response = requests.get(f"http://backend-service:5000/show_dist", stream=True)
    
    # Return the image response directly to the client, maintaining the content type.
    return Response(response.content, content_type=response.headers['Content-Type'])



if __name__ == '__main__':
    # Start the Flask application on the specified host and port, making it accessible across the network.
    app.run(host='0.0.0.0', port=80)
