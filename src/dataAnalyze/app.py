import psycopg2
import psycopg2.extras
from flask import Flask, jsonify, request, send_file

import io

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

import matplotlib.pyplot as plt

app = Flask(__name__)


def connect_DB():

    user = 'postgres'  
    password = 'MosheForer97'  
    dbname = 'tweets'
    port = '5432' 
    host = 'postgres-service'  
    # Connecting
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    return conn


def if_tweets():
    try:
        conn = connect_DB()
        cur = conn.cursor()
        # select 10
        cur.execute("SELECT EXISTS(SELECT 10 FROM db_digested LIMIT 10);")
        is_ready = cur.fetchone()[0]
        
        return is_ready
    except Exception as e:
        print(f"if_tweets:error {e}")
        return False


def return_dist():
    
    conn = connect_DB()
    cur = conn.cursor()
    # query to DB
    cur.execute("SELECT author, COUNT(tweet_id) as tweet_count FROM user_tweets GROUP BY author;")
    response = cur.fetchall()
    conn.close()
    # query the db
    '''
    author_data = [
        ('AuthorA', 10),
        ('AuthorB', 120),
        ('AuthorC', 13),
        ('AuthorD', 20),
        ('AuthorE', 70)
    ]
    '''
    res_tweets_list = [row[1] for row in response]
    res_author_list = [row[0] for row in response]
    # plotting the results
    plt.figure(figsize=(10, 6))
    plt.bar(res_author_list, res_tweets_list, color='skyblue')
    
    
    plt.xlabel('results authors')
    plt.ylabel('Tweets')
    plt.title('Distribution of Tweets per Author')
    plt.xticks(rotation=45)
    plt.tight_layout()

    show = io.BytesIO()
    plt.savefig(show, format='png')
    show.seek(0)
    
    return show



@app.route('/')
def home():
    return "home page"


@app.route('/show_dist')
def show_dist():
    try:
        # distrebution the tweets
        show = return_dist()
        # return 
        return send_file(show, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': f"show_dist{e}"}), 500
    
@app.route('/show_tweets')
def show_tweets():
    if not if_tweets():
        return jsonify({"error": "Data is not yet available, please try again later."}), 503 
    author_name = request.args.get('tokens')
    if not author_name:
        return jsonify({'error': 'Query parameter "author" is missing'}), 400
    
    try:
        img = evaluate_sentiment_visualization(author_name)
        return send_file(img, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def evaluate_sentiment_visualization(author_name):
    # Replace this part with your actual logic to fetch tweets
    '''
    dummy_tweets = [
        {'author': 'AuthorA', 'content': "I love sunny days, they're amazing!"},
        {'author': 'AuthorB', 'content': "This is quite disappointing."},
        {'author': 'AuthorA', 'content': "I'm not sure how I feel about this."},
        {'author': 'AuthorC', 'content': "Today is a great day!"},
        {'author': 'AuthorB', 'content': "This is the worst!"},
    ]

    '''
    conn = connect_DB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Query all tweets from the specified author
    #cur.execute("SELECT content FROM user_tweets WHERE author = %s;", (author_name,))
    cur.execute("SELECT content FROM user_tweets WHERE author = %s ORDER BY tweet_id DESC LIMIT 5;", (author_name,))

    tweets = cur.fetchall()

    if not tweets:
        return jsonify({'error': 'No tweets found for this author'}), 404

    #tweets = [tweet for tweet in dummy_tweets if tweet['author'] == author_name]

    sentiments = [evaluate_sentiment(tweet['content']) for tweet in tweets]

    # Generate a simple plot
    plt.figure(figsize=(10, 6))
    plt.plot(sentiments, marker='o', linestyle='-', color='b')
    plt.title(f"Sentiment Analysis of {author_name}'s Tweets")
    plt.ylabel('Sentiment Score')
    plt.xlabel('Tweet')
    plt.xticks(range(len(sentiments)), ['Tweet '+str(i+1) for i in range(len(sentiments))], rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    buf.seek(0)
    plt.close()

    return buf
    

@app.route('/get_tweet')
def get_tweet(tweet_id=None):
    if not if_tweets():
        return jsonify({"error": "get_tweet: try again not ready."}), 503 
    try:
        if not tweet_id:
            tweet_id = request.args.get('tweet_id')
            
            if not tweet_id:
                
                
                return jsonify({'error': 'get_tweet: check parameters'}), 400

        conn = connect_DB()
        
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # quering to DB by likes and tweets id
        cur.execute("SELECT content FROM tweets_by_likes WHERE tweet_id = %s;", (tweet_id,))
        row = cur.fetchone()

        if row:
            # this is for the DB schema do not change
            tweet = row['content']  
            return jsonify(tweet=tweet), 200
        else:
            return jsonify({'error': 'no such tweet'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/show_tweets_top')
def show_tweets_top():
    if not if_tweets():
        return jsonify({"error": "show_tweets_top: not ready yet."}), 503 
    try:
        conn = connect_DB()
        cur = conn.cursor()
        # 10 most chared tweets
        cur.execute("SELECT * FROM tweets_by_share ORDER BY number_of_shares LIMIT 20;")
        shares = cur.fetchall()
        # 10 most liked twwets
        cur.execute("SELECT * FROM tweets_by_likes ORDER BY number_of_likes LIMIT 10;")
        likes = cur.fetchall()
        conn.close()

        return jsonify({
            'show_tweets_top_by_likes': likes,
            'show_tweets_top_by_shares': shares
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/show_users')
def show_users():
    if not if_tweets():
        # not ready tweets
        return jsonify({"error": "not ready yet"}), 503 
    try:
        # ready connecting to DB
        
        conn = connect_DB()
        
        cur = conn.cursor()
# executing
        cur.execute("""
        SELECT author, COUNT(*) AS tweet_count 
        FROM user_tweets 
        GROUP BY author 
        ORDER BY tweet_count 
        LIMIT 30;
        """)
        users = cur.fetchall()

        conn.close()

        return jsonify({'show_users_by_content': users})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def evaluate_sentiment(text):
    """
    Evaluates and categorizes the sentiment of the given text.

    Utilizes NLTK's SentimentIntensityAnalyzer to calculate sentiment scores.
    The function returns a sentiment category based on the compound score: 
    'positive', 'neutral', or 'negative'.

    Parameters:
    - text (str): The text to analyze.

    Returns:
    - str: The sentiment category ('positive', 'neutral', 'negative').
    """
    # Initialize the sentiment intensity analyzer
    analyzer = SentimentIntensityAnalyzer()
    # Get sentiment scores for the text
    sentiment_scores = analyzer.polarity_scores(text)

    # Determine sentiment category based on compound score
    if sentiment_scores['compound'] >= 0.05:
        sentiment_category = 'positive'
    elif sentiment_scores['compound'] <= -0.05:
        sentiment_category = 'negative'
    else:
        sentiment_category = 'neutral'

    return sentiment_category

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)