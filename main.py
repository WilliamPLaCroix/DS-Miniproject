from datetime import datetime, timedelta

import pandas as pd
import torch
import yahoo_fin.stock_info as si
from stocksent import Sentiment
from transformers import AutoModelForSequenceClassification, AutoTokenizer

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
sentiment_model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert").to(device)

def get_sentiment(input_text: str, model=sentiment_model, tokenizer=tokenizer, device=device):

    inputs = tokenizer(input_text, return_tensors="pt").to(device)
    with torch.no_grad():
        logits = model(**inputs).logits.to(device)

    return torch.nn.Softmax(dim=1)(logits)[0].tolist()

def get_stock_data(ticker: str) -> "tuple[torch.tensor(), float]": # type: ignore
    today: datetime = datetime.today()
    yesteryear: str = (today - timedelta(days=345)).strftime('%Y-%m-%d')
    column_names: "list[str]" = ["low","open","volume","high","close","adjclose","Annual Percent Change","positive","negative","neutral"]

    stock_news = Sentiment(ticker)
    sentiment_score = stock_news.get_dataframe(days=1)
    stories = sentiment_score['headline'].tolist()[:10]
    sentiments: "list[float]" = []

    for story in stories:
        sentiment = get_sentiment(story)
        sentiments.append(sentiment)

    sentiments_df = pd.DataFrame(sentiments, columns=['positive', 'negative', 'neutral'])
    mean_sentiments: pd.Series = sentiments_df.mean()
    stock_sentiment: "list[float]" = mean_sentiments.values.tolist()

    ticker_info: pd.DataFrame = si.get_data(ticker, start_date=yesteryear, end_date=today, interval="1mo")
    ticker_info = ticker_info.drop(columns=['ticker'])
    ticker_info['Annual Percent Change'] = (ticker_info.iloc[-1]['close'] - ticker_info.iloc[0]['close']) / ticker_info.iloc[0]['close'] * 100
    annualized_ticker_info: pd.Series = ticker_info.mean()

    annualized_ticker_info['positive'] = stock_sentiment[0]
    annualized_ticker_info['negative'] = stock_sentiment[1]
    annualized_ticker_info['neutral'] = stock_sentiment[2]

    annualized_ticker_info = annualized_ticker_info[column_names] # reorder columns

    return torch.Tensor(annualized_ticker_info.values.tolist()), annualized_ticker_info['Annual Percent Change']
