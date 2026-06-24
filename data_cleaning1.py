import pandas as pd
import plotly.express as px

def combine_my_files(orders_path, customers_path):
    df_orders = pd.read_csv(orders_path)
    df_customers = pd.read_csv(customers_path)
    df_combined = pd.merge(df_orders, df_customers, on="customer_id")
    return df_combined

def clean_and_sort_data_and_month_added(df):
    df.columns = df.columns.str.upper()
    df["ORDER_DATE"] = pd.to_datetime(df["ORDER_DATE"])
    df = df.sort_values(by=["ORDER_DATE", "ORDER_ID"], ascending=[True, True])
    month_column = df['ORDER_DATE'].dt.strftime('%B')
    df.insert(loc=3, column='MONTH', value=month_column)
    df["PROFIT"] = df["REVENUE"] - df["COST"]
    return df

def create_profit_margin_chart(df):
    monthly_data = df.groupby(['MONTH','SEGMENT'])[['PROFIT', 'REVENUE']].sum().reset_index()
    
    monthly_data['PROFIT_MARGIN'] = (monthly_data['PROFIT'] / monthly_data['REVENUE']) * 100
    
    fig = px.bar(
        monthly_data,
        x='MONTH',
        y='PROFIT_MARGIN',
        barmode='group',
        title='Month-wise Profit Margin (%)',
        # color='SEGMENT',
        text_auto='.1f'
    )
    
    fig.update_layout(xaxis_title='Months',yaxis_title='Profit Margin (%)',yaxis_ticksuffix='%',legend_title_text='Segments')
    
    fig.update_xaxes(categoryorder='array', categoryarray=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
    
    fig.show()

def main():
    orders_input = "/Users/nikhilkhola/Downloads/largedatasetwithgoodseed/ch2_orders.csv"
    customers_input = "/Users/nikhilkhola/Downloads/largedatasetwithgoodseed/ch2_customers.csv"
    
    df = combine_my_files(orders_input, customers_input)
    df = clean_and_sort_data_and_month_added(df)
    df.info()
    
    create_profit_margin_chart(df)

if __name__ == "__main__":
    main()