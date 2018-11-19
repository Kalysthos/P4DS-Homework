import pandas as pd

def analyze(data, parameter='GDP per capita (current US$)', world=True):
    '''Generates the Dataframe of data(list of Dataframes) from year (int), index (str) or country (str with "c-" at start)'''
    
    countries = ['Australia', 'Cuba', 'Grenada', 'Syrian Arab Republic', 'Bermuda', 'British Virgin Islands', 'Central African Republic', 'Angola', 'Iceland', 'West Bank and Gaza', 'Congo, Dem. Rep.', 'Belgium', 'Kenya', 'Virgin Islands (U.S.)', 'Vanuatu', 'Peru', 'South Africa', 'Moldova', 'Armenia', "Cote d'Ivoire", 'Channel Islands', 'Trinidad and Tobago', 'Togo', 'Liechtenstein', 'Northern Mariana Islands', 'Djibouti', 'Czech Republic', 'El Salvador', 'Korea, Dem. People’s Rep.', 'Italy', 'Somalia', 'Bahrain', 'Mexico', 'Cyprus', 'Zambia', 'Algeria', 'Madagascar', 'Sweden', 'Slovak Republic', 'Norway', 'Fiji', 'Jordan', 'Kyrgyz Republic', 'Netherlands', 'New Zealand', 'Greece', 'Denmark', 'Nauru', 'Tonga', 'Mauritania', 'St. Martin (French part)', 'Palau', 'Bahamas, The', 'Ireland', 'Nepal', 'Hong Kong SAR, China', 'Kazakhstan', 'Switzerland', 'Uruguay', 'Turks and Caicos Islands', 'Cayman Islands', 'Uzbekistan', 'Papua New Guinea', 'American Samoa', 'Costa Rica', 'Marshall Islands', 'Malawi', 'Sint Maarten (Dutch part)', 'Comoros', 'United States', 'St. Lucia', 'Serbia', 'Bolivia', 'India', 'Israel', 'Dominican Republic', 'Mongolia', 'Morocco', 'Myanmar', 'Chad', 'Mali', 'Guinea-Bissau', 'Philippines', 'Sierra Leone', 'Suriname', 'Estonia', 'Macedonia, FYR', 'United Kingdom', 'Austria', 'Turkey', 'Bosnia and Herzegovina', 'Argentina', 'Rwanda', 'Andorra', 'Cameroon', 'Ukraine', 'Samoa', 'Gambia, The', 'Nicaragua', 'Bulgaria', 'Paraguay', 'Lao PDR', 'Micronesia, Fed. Sts.', 'Bangladesh', 'Poland', 'Singapore', 'Benin', 'Bhutan', 'Eswatini', 'Latvia', 'Lebanon', 'United Arab Emirates', 'Libya', 'Brazil', 'Indonesia', 'Luxembourg', 'Seychelles', 'Burkina Faso', 'Ethiopia', 'Egypt, Arab Rep.', 'South Sudan', 'Malaysia', 'Russian Federation', 'Timor-Leste', 'Lesotho', 'Kuwait', 'San Marino', 'Guam', 'Afghanistan', 'Colombia', 'Montenegro', 'Finland', 'Qatar', 'Gibraltar', 'Korea, Rep.', 'Venezuela, RB', 'Tajikistan', 'Haiti', 'Liberia', 'Tunisia', 'Ghana', 'Kosovo', 'France', 'St. Vincent and the Grenadines', 'Honduras', 'Ecuador', 'Guyana', 'Portugal', 'Iraq', 'Equatorial Guinea', 'Mozambique', 'Aruba', 'Vietnam', 'Hungary', 'Monaco', 'Chile', 'Croatia', 'Slovenia', 'Kiribati', 'Greenland', 'Belarus', 'Saudi Arabia', 'Turkmenistan', 'Sao Tome and Principe', 'Dominica', 'Sudan', 'Romania', 'Isle of Man', 'New Caledonia', 'Malta', 'Cambodia', 'Guatemala', 'Guinea', 'Thailand', 'French Polynesia', 'Iran, Islamic Rep.', 'Burundi', 'Jamaica', 'Namibia', 'Yemen, Rep.', 'Tanzania', 'Barbados', 'Panama', 'Belize', 'Brunei Darussalam', 'Oman', 'Sri Lanka', 'Gabon', 'St. Kitts and Nevis', 'Macao SAR, China', 'Uganda', 'Georgia', 'Spain', 'Tuvalu', 'Maldives', 'Lithuania', 'China', 'Germany', 'Niger', 'Zimbabwe', 'Curacao', 'Antigua and Barbuda', 'Puerto Rico', 'Azerbaijan', 'Botswana', 'Cabo Verde', 'Eritrea', 'Faroe Islands', 'World', 'Albania', 'Congo, Rep.', 'Senegal', 'Japan', 'Canada', 'Nigeria', 'Mauritius', 'Solomon Islands', 'Pakistan']
    
    if not world:
        countries.remove('World')
    
    if type(parameter) == int:
        country = pd.DataFrame(data[0][str(parameter)]).rename(columns=lambda x: data[0]['Indicator Name'][0])
        for k,i in enumerate(data[1:]):
            country = country.join(pd.Series(i[str(parameter)], name=data[k+1]["Indicator Name"][0]))
        return country.reindex(countries).dropna(how='all') 
    
    elif parameter[0:2] == "c-":
        years = pd.DataFrame(data[0].T[parameter[2:]][4:]).rename(columns=lambda x: data[0]["Indicator Name"][0])
        for k,i in enumerate(data[1:]):
            years = years.join(pd.Series(i.T[parameter[2:]][4:], name=data[k+1]["Indicator Name"][0]))
        return years.dropna(how='all')
        
    else:
        for i in data:
            if i['Indicator Name'][0] == parameter:
                return i.drop("Indicator Name", axis=1).reindex(countries).dropna(how='all') 
