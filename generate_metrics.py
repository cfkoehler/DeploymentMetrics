## Read in the deployments.csv and generate metrics
## CSV Format is version, date of primary release, date of secondary release, failure (boolean)

import pandas as pd
import logging
import datetime
import plotly.graph_objects as go
import os

def get_failure_rate(df):
    non_failure_count = df['failure'].sum()
    failure_count = (~df['failure']).sum()
    return round((abs(failure_count - (failure_count + non_failure_count)) / (failure_count + non_failure_count)) * 100, 2)

def calculate_deployment_days(df):
    deployment_deltas = [None] # First Value is none
    for index, row in df.iloc[1:].iterrows():
        if pd.isna(row['pirmaryDeployment']):
            deployment_deltas.append(None)
            continue
        previous_deployment_date = pd.isna
        look_back_index = 1
        while previous_deployment_date == pd.isna:
            # Go back to find a Deployment Day
            if pd.isna(df.iloc[index-look_back_index]['pirmaryDeployment']):
                look_back_index = look_back_index + 1
                continue
            previous_deployment_date = df.iloc[index-look_back_index]['pirmaryDeployment']
            previous_deployment_date = datetime.datetime.strptime(df.iloc[index-look_back_index]['pirmaryDeployment'], '%m/%d/%y')
        current_deployment_date = datetime.datetime.strptime(row['pirmaryDeployment'], '%m/%d/%y')
        delta = current_deployment_date - previous_deployment_date
        deployment_deltas.append(delta.days)
    df['deploymentDelta'] = deployment_deltas
    return df

def calculate_avg_deployment_frequency(df):
    return round(df["deploymentDelta"].mean(),1)

# Sets Plot color based on value
def set_color(x):
    if(x == False):
        return "green"
    elif(x == True):
        return "red"

def create_plot(df):
    # Drop nan deploymentDelta for chart
    deployments_deltas=df.dropna(subset=['deploymentDelta'])

    layout = dict(plot_bgcolor='white',
              margin=dict(t=40, l=20, r=20, b=20),
              xaxis=dict(title='Deployment Date',
                         linecolor='#d9d9d9',
                         showgrid=False,
                         mirror=True),
              yaxis=dict(title='Days since Previous Deployment',
                         linecolor='#d9d9d9',
                         showgrid=False,
                         mirror=True))

    data = go.Scatter(x=deployments_deltas['pirmaryDeployment'],
                    y=deployments_deltas['deploymentDelta'],
                    text=deployments_deltas['version'],
                    textposition='top center',
                    textfont=dict(color='#E58606'),
                    mode='lines+markers+text',
                    marker=dict(color=list(map(set_color, deployments_deltas['failure'])), size=15),
                    line=dict(color='#52BCA3', width=2, dash='dash'),
                    name='version')

    fig = go.Figure(data=data, layout=layout)
    title = 'Deployment Frequency (Change Failure Rate: ' + str(get_failure_rate(df)) + '%)'
    fig.update_layout(
        title=title,
        font=dict(
            family="Courier New, monospace",
            size=20,
            color="Black"
        )
    )
    return(fig)


def main():
    try:
        deployments_df = pd.read_csv('deployments.csv')
        deployments_df = calculate_deployment_days(deployments_df)
        print(deployments_df)
        print('Failure Rate: ' + str(get_failure_rate(deployments_df)) + '%')
        print('Deployment Frequency: ' + str(calculate_avg_deployment_frequency(deployments_df)) +' days')
        if not os.path.exists("images"):
            os.mkdir("images")
        fig = create_plot(deployments_df)
        fig.write_image(file="images/deploymentFrequencyChart.png",engine="kaleido",width=2000,height=1000)

    except IOError as e:
        logging.error(e)

if __name__ == "__main__":
    main()