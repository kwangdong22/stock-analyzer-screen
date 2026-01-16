from flask import Flask, render_template, request
import yfinance as yf

app= Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    data= None
    error= None
    if request.method == 'POST':
        ticker = request.form.get('ticker').upper()
        try: #fetch real data
            stock= yf.Ticker(ticker)
            history= stock.history(period="5d") # get the last two days to calculate

            if len(history) >=2:
                current_price= history['Close'].iloc[-1]
                prev_price= history['Close'].iloc[-2]   
                change_percent= ((current_price- prev_price)/prev_price) *100

                # data packaging for html #
                data= {
                    'symbol':ticker,
                    'price': round(current_price,2),
                    'change': round(change_percent,2)
                }
            else:
                error= 'Ticker not found or no data available'
        except Exception as e:
            error = f"System Error: {str(e)} Please try again."
    return render_template('index.html', data=data, error=error)

if __name__ == '__main__':
    app.run(debug=True)