#############################
#       REWORK
#############################

df = df.sort_values(['cms_defendant_guid', 'arrest_date'])

df['prior_arrest'] = df.cms_defendant_guid.is_duplicated()

###########################################################################


#############################
#       ORIGINAL
#############################

def geocode(df):
    con = da.conn.hippo_sql()
    locations = da.pd.read_sql('SELECT * FROM CHARGE_LOCATIONS;', con)
    df['CrimeCase'] = df['CrimeCase'].astype(str)
    locations = locations[['CrimeCase', 'charge_sequence', 'gc_street_address', 'gc_zip_code', 'gc_lat', 'gc_lon']]
    df = da.pd.merge(df, locations, how='left', on=['CrimeCase', 'charge_sequence'])
    
    df['incident_lat_lon'] = df.gc_lat.astype(str) + ',' + df.gc_lon.astype(str)
    return df

def check_priors(priors, row):
    #Prior Arrest Flag
        if pd.notnull(row.arrest_date):
            priors[0] = 1
        
        #Prior Indictment Flag
        if row.charge_method == 'Grand Jury Indictment':
            priors[1] = 1
        
        #Prior Conviction Flag
        if row.case_disposition == 'Guilty':
            priors[2] = 1
        
        #Prior Violent Arrest Flag
        if pd.notnull(row.arrest_date)  and row.case_is_violent == True:
            priors[3] = 1
        
        #Prior Violent Indictment Flag
        if row.charge_method == 'Grand Jury Indictment' and row.case_is_violent == True:
            priors[4] = 1
        
        #Prior Violent Conviction Flag
        if row.case_disposition == 'Guilty' and row.case_is_violent == True:
            priors[5] = 1
        
        #Prior Felony Arrest Flag
        if pd.notnull(row.arrest_date) and row.case_has_felony == True:
            priors[6] = 1
        
        #Prior Felony Indictment Flag
        if row.charge_method == 'Grand Jury Indictment' and row.case_has_felony == True:
            priors[7] = 1
        
        #Prior Felony Conviction Flag
        if row.case_disposition == 'Guilty' and row.case_has_felony == True:
            priors[8] = 1
            
        return(priors)
##########################

df = dataio_stanford.pull_cms_master()
##########################

pdm_df = da.pdm.pull()

##########################

df = pd.merge(df, pdm_df, left_on = 'cms_case_num', right_on='pdm_cms_case_num', how='left')
df = geocode(df)
###########################

df2 = df.sort_values(by=['cms_defendant_guid', 'open_date', 'charge_sequence'], ignore_index=True)

###########################

df2 = df2.drop(labels = ['pdm_cms_case_num','pdm_number','pdm_def_last','pdm_def_first','pdm_def_dob',
                         'pdm_filedate','pdm_heardate','pdm_ada','pdm_judge','pdm_outcome','pdm_metro_num',
                         'pdm_psa_flag','pdm_psa_nca','pdm_psa_fta','pdm_firearm','pdm_fed_ref',
                         'pdm_psa_recommendation','pdm_psa_na','charge_enhancement','victim_name','victim_race',
                         'victim_ethnicity','victim_gender','victim_dob','victim_relationship',
                         'gc_street_address','gc_zip_code','gc_lat','gc_lon','incident_lat_lon'],  axis=1)
df2.drop_duplicates(inplace=True, ignore_index=True)

###########################

flag_df = df2[df2.charge_sequence==1].reset_index(drop=True)
flag_df['prior_arrest'] = False
flag_df['prior_indictment'] = False
flag_df['prior_conviction'] = False
flag_df['prior_violent_arrest'] = False
flag_df['prior_violent_indictment'] = False
flag_df['prior_violent_conviction'] = False
flag_df['prior_felony_arrest'] = False
flag_df['prior_felony_indictment'] = False
flag_df['prior_felony_conviction'] = False

##########################

priors_labels = ['prior_arrest', 'prior_indictment', 'prior_conviction',
                 'prior_violent_arrest', 'prior_violent_indictment', 'prior_violent_conviction',
                 'prior_felony_arrest', 'prior_felony_indictment', 'prior_felony_conviction']
prior_def = np.nan
counter = 0 
for i, row in flag_df.iterrows():
    current_def = row.cms_defendant_guid
    
    if current_def != prior_def:
        priors = [0,0,0,0,0,0,0,0,0]   
    
    flag_df.loc[i, priors_labels] = np.where(priors, True, False)

    priors = check_priors(priors, row)
    prior_def = current_def
    
    if i%10000==0: print()
    
    counter+=1
    if counter==1000: break

######################

merge_df = flag_df[['CrimeCase', 'prior_arrest', 'prior_indictment',
       'prior_conviction', 'prior_violent_arrest', 'prior_violent_indictment',
       'prior_violent_conviction', 'prior_felony_arrest',
       'prior_felony_indictment', 'prior_felony_conviction']]
final_df = df.merge(merge_df, how='left', on='CrimeCase')
final_df.to_csv(f'stanford_data_pull_final_{date.today()}')


###################

priors_labels = ['prior_arrest', 'prior_indictment', 'prior_conviction',
                 'prior_violent_arrest', 'prior_violent_indictment', 'prior_violent_conviction',
                 'prior_felony_arrest', 'prior_felony_indictment', 'prior_felony_conviction']
flag_df[priors_labels].head()
priors=[0,1,0,0,1,1,0,0,1]
flag_df.loc[0, priors_labels] = np.where(priors, True, False)
flag_df[priors_labels].head()