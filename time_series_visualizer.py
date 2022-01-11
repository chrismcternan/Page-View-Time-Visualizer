import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import calendar
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
with open('fcc-forum-pageviews.csv', 'r') as f:
  df = pd.read_csv(f, header=0)
  df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    plt.clf()
    fig = plt.figure()
    ax = plt.axes()
    ax.plot(df['date'], df['value'])
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_xticks(['2016-07-01', '2017-01-01', '2017-07-01', '2018-01-01', '2018-07-01', '2019-01-01', '2019-07-01', '2020-01-01'], labels=['2016-07', '2017-01', '2017-07', '2018-01', '2018-07', '2019-01', '2019-07', '2020-01'])
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    # df_bar['date'] = pd.to_datetime(df_bar['date'], format='%Y-%m-%d')
    df_bar['Months'] = df_bar['date'].dt.month_name()
    df_bar['Years'] = df_bar['date'].dt.year
    monthly_averages = pd.DataFrame(columns=['Years', 'Months', 'value'])
    df_bar_years = df_bar.groupby('Years')
    
    for year, group in df_bar_years:
      df_bar_months = group.groupby('Months')
      for month, daily_data in df_bar_months:
        avg = daily_data['value'].mean()
        new_row = pd.DataFrame([[year, month, avg]], columns=['Years', "Months", 'value'])
        monthly_averages = monthly_averages.append(new_row, ignore_index=True)

    # Draw bar plot
    # clear figures
    plt.clf()
    fig2 = plt.figure()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    sns.set_theme(style='whitegrid')
    fig2 = sns.barplot(y='value', x='Years', hue='Months', data=monthly_averages, hue_order=months).figure
    for ax in fig2.axes:
      ax.set_title('')
      ax.set_xlabel('Years')
      ax.set_ylabel('Average Page Views')
      ax.legend(months)


    # Save image and return fig (don't change this part)
    fig2.savefig('bar_plot.png')
    return fig2

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['Year'] = [d.year for d in df_box.date]
    df_box['Month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    plt.clf()
    fig3 = plt.figure()
    ax0 = fig3.add_subplot(1, 2, 1)
    ax0.set_title('Year-wise Box Plot (Trend)')
    sns.boxplot(x='Year', y='value', data=df_box, ax=ax0)
    ax1 = fig3.add_subplot(1, 2, 2)
    ax1.set_title('Month-wise Box Plot (Seasonality)')
    ax1.set_xlabel(months)
    sns.boxplot(x='Month', y='value', data=df_box, ax=ax1, order=months)
    for ax in fig3.axes:
      ax.set_ylabel('Page Views')



    # Save image and return fig (don't change this part)
    fig3.savefig('box_plot.png')
    return fig3

