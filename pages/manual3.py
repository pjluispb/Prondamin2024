



dfsis = dfPronda[dfPronda['paycon'] == 'SI']
dfsim = dfPronda[dfPronda['paycon'] == 'SI++']
dfSI = pd.concat([dfsis, dfsim])
dfnoSI = dfPronda.loc[~dfPronda.index.isin(dfSI.index)]
dfPronda24 = dfnoSI
