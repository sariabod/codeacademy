import pandas as pd


ac = pd.read_csv("ad_clicks.csv")

#print(ac.head(10))
#print(ac.info())

source_clicks = ac.groupby('utm_source')['user_id'].count().reset_index()

#print(source_clicks)

ac['is_click'] = ac['ad_click_timestamp'].map(lambda x: 'True' if x==x else 'False')
#ac['is_click'] = ac.ad_click_timestamp.apply(lambda x: False if pd.isnull(x) else True)

#print(ac)



clicks_by_source = ac.groupby(['utm_source','is_click'])['user_id'].count().reset_index()

clicks_by_group = ac.groupby(['experimental_group','is_click'])['user_id'].count().reset_index()


clicks_pivot = clicks_by_source.pivot(index='utm_source', columns='is_click', values='user_id')

group_pivot = clicks_by_group.pivot(index='experimental_group', columns='is_click', values='user_id')


clicks_pivot['percent_clicked'] = 100 * (clicks_pivot['True'] / (clicks_pivot['True'] + clicks_pivot['False']))
group_pivot['percent_clicked'] = 100 * (group_pivot['True'] / (group_pivot['True'] + group_pivot['False']))


a_clicks = ac[ac['experimental_group']=='A']
b_clicks = ac[ac['experimental_group']=='B']

clicks_by_a = a_clicks.groupby(['day','is_click'])['user_id'].count().reset_index()
clicks_pivot_a = clicks_by_a.pivot(index='day', columns='is_click', values='user_id')
clicks_pivot_a['percent_clicked'] = 100 * (clicks_pivot_a['True'] / (clicks_pivot_a['True'] + clicks_pivot_a['False']))

clicks_by_b = b_clicks.groupby(['day','is_click'])['user_id'].count().reset_index()
clicks_pivot_b = clicks_by_b.pivot(index='day', columns='is_click', values='user_id')
clicks_pivot_b['percent_clicked'] = 100 * (clicks_pivot_b['True'] / (clicks_pivot_b['True'] + clicks_pivot_b['False']))


print(clicks_pivot_a)
print(clicks_pivot_b)



