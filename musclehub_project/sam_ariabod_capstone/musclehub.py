import sqlite3
from sqlite3 import Error
import pandas as pd
#import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import chi2_contingency


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None


 
conn = create_connection('example.db')

#cur = conn.cursor()
#cur.execute("select v.first_name, v.last_name,v.email,v.gender,v.visit_date,coalesce(f.fitness_test_date,0) as fitness_test_date, coalesce(a.application_date,0) as application_date, coalesce(p.purchase_date,0) as purchase_date from visits v left join fitness_tests f on f.first_name=v.first_name and f.last_name=v.last_name and f.email=v.email left join purchases p on p.first_name=v.first_name and p.last_name=v.last_name and p.email=v.email left join applications a on a.first_name=v.first_name and a.last_name=v.last_name and a.email=v.email where v.visit_date >= '7-1-17'")
query = "select v.first_name, v.last_name,v.email,v.gender,v.visit_date,f.fitness_test_date, a.application_date, p.purchase_date from visits v left join fitness_tests f on f.first_name=v.first_name and f.last_name=v.last_name and f.email=v.email left join purchases p on p.first_name=v.first_name and p.last_name=v.last_name and p.email=v.email left join applications a on a.first_name=v.first_name and a.last_name=v.last_name and a.email=v.email where v.visit_date >= '7-1-17'"
 
df = pd.read_sql(query, con=conn)

df['ab_test_group'] = df['fitness_test_date'].apply(lambda x: 'B' if pd.isnull(x) else 'A' )
df['is_application'] = df['application_date'].apply(lambda x: 'No Application' if pd.isnull(x) else 'Application' )
df['is_member'] = df['purchase_date'].apply(lambda x: 'Not Member' if pd.isnull(x) else 'Member' )

ab_counts = df.groupby('ab_test_group')['email'].count()

app_counts = df.groupby(['is_application','ab_test_group'])['email'].count().reset_index()
app_pivot = app_counts.pivot('ab_test_group', 'is_application', 'email').reset_index()
app_pivot['Total'] = app_pivot['Application'] + app_pivot['No Application']
app_pivot['Percent with Application'] = app_pivot['Application'] / app_pivot['Total']
chi2, pval, dof, expected = chi2_contingency([ [app_pivot.iloc[0]['Application'],app_pivot.iloc[1]['Application']], [app_pivot.iloc[0]['No Application'],app_pivot.iloc[1]['No Application']]])
#print(pval)

just_apps = df[df.is_application == 'Application']
just_apps_count = just_apps.groupby(['ab_test_group','is_member'])['email'].count().reset_index()
member_pivot = just_apps_count.pivot('ab_test_group', 'is_member', 'email').reset_index()
member_pivot['Total'] = member_pivot['Member'] + member_pivot['Not Member']
member_pivot['Percent Purchase'] = member_pivot['Member'] / member_pivot['Total']
chi2x, pvalx, dofx, expectedx = chi2_contingency([ [member_pivot.iloc[0]['Member'],member_pivot.iloc[1]['Member']], [member_pivot.iloc[0]['Not Member'],member_pivot.iloc[1]['Not Member']]])
#print(pvalx)

final_member_count = df.groupby(['ab_test_group', 'is_member'])['email'].count().reset_index()
final_member_pivot = final_member_count.pivot('ab_test_group','is_member','email').reset_index()
final_member_pivot['Total'] = final_member_pivot['Member'] + final_member_pivot['Not Member']
final_member_pivot['Percent Purchase'] = final_member_pivot['Member'] / final_member_pivot['Total']
chi2z, pvalz, dofz, expectedz = chi2_contingency([ [final_member_pivot.iloc[0]['Member'],final_member_pivot.iloc[1]['Member']], [final_member_pivot.iloc[0]['Not Member'],final_member_pivot.iloc[1]['Not Member']]])
#print(pvalz)


yticks = [0,.10,.20,.30,.40,.50,.60,.70,.80,.90,.1]
ytickl = [yticks * 100]
ytickl = [i * 100 for i in yticks]

ax0 = plt.subplot()
plt.pie(ab_counts,labels=['A', 'B'], autopct='%0.2f%%')
plt.axis('equal')
plt.savefig('ab_test_pie_chart.png')
#plt.show()
plt.clf()

ax1 = plt.subplot()
plt.title('Percent of Visitors that Apply')
plt.bar(range(len(app_pivot)),app_pivot['Percent with Application'].values)
ax1.set_xticks(range(len(app_pivot)))
ax1.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax1.set_yticks(yticks[0:5])
ax1.set_yticklabels(ytickl[0:5])
plt.savefig('percent_visitor_apply.png')
#plt.show()
plt.clf()

ax3 = plt.subplot()
plt.title('Percent of Applicants that Purchase')
plt.bar(range(len(member_pivot)),member_pivot['Percent Purchase'].values)
ax3.set_xticks(range(len(app_pivot)))
ax3.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax3.set_yticks(yticks)
ax3.set_yticklabels(ytickl)
plt.savefig('percent_apply_purchase.png')
#plt.show()
plt.clf()

ax4 = plt.subplot()
plt.title('Percent of Visitors that Purchase')
plt.bar(range(len(final_member_pivot)),final_member_pivot['Percent Purchase'].values)
ax4.set_xticks(range(len(app_pivot)))
ax4.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax4.set_yticks(yticks[0:5])
ax4.set_yticklabels(ytickl[0:5])
plt.savefig('percent_visitor_apply_purchase.png')
#plt.show()
plt.clf()





















