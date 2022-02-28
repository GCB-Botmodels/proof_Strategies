import yfinance as yf
import datetime as dt
import pandas as pd
import numpy as np
from time import time
import math





def run_req_res():
    
    
    class Requests_Response:

        def __init__(self):
            self.mDataClass = self.ModelingData()
            
            
            
        class Data:
            
            def inputs_tickers(self):
                            
                tickers=input("\nEscribir Ticker. Si es una lista se debe escribir los tickers separados por coma. Ejemplo AAA,BBBB,DDD\n"
                                "Los tickers de accciones argentinas escribirlos con los caracteres .BA al final del ticker. Ejemplo GGAL.BA : \n")
                
                tickers = str(tickers).upper()
                tickers = tickers.replace('[','').replace(']','')
                tickers = tickers.split(",")
                
                return tickers
                

            def inputs_dates(self):
                
                start=input("\nEscribir fecha de INICIO del período con el siguiente formato aaaa-mm-dd : \n")
                
                end=input("\nEscribir fecha de FIN del período con el siguiente formato aaaa-mm-dd : \n")
                
                try:              
        
                    parse_i = start.split("-")
                    year_i = parse_i[0]
                    month_i = parse_i[1]
                    day_i = parse_i[2]
                    
                    if ""==day_i.split('0')[0]:
                        day_i = day_i.split('0')[1]
                    if ""==month_i.split('0')[0]:
                        month_i = month_i.split('0')[1]
                        
                    parse_f = end.split("-")
                    year_f = parse_f[0]
                    month_f = parse_f[1]
                    day_f = parse_f[2]

                    if ""==day_f.split('0')[0]:
                        day_f = day_f.split('0')[1]
                    if ""==month_f.split('0')[0]:
                        month_f = month_f.split('0')[1]
                    
                except:            
                    print("\nLos fechas no siguen las consignas de los inputs, vuelva a ingresarlas siguiendo las intrucciones.\n")
                    return self.inputs_dates()
                
                
                difference_days = dt.datetime(int(year_f),int(month_f),int(day_f)) - dt.datetime(int(year_i),int(month_i),int(day_i))
                difference_days = difference_days.days+1

                if difference_days >= 63:
                    print("\nEl período de la muestra debe ser menor a 3 meses (63 días corridos). Vuelva a cargar siguiendo las instrucciones.\n")
                    return self.inputs_dates()
                elif difference_days <= 14:
                    print("\nEl período de la muestra debe ser igual o mayor a 14 días (14 días corridos). Vuelva a cargar siguiendo las instrucciones.\n")
                    return self.inputs_dates()
                else:
                    pass
                
                end = str(dt.datetime.strptime(end,"%Y-%m-%d") + dt.timedelta(days = 1))
                end = end.split(" ")[0]
                     
                
                return [start,end]
            

            def getData(self):
                
                data_feed=yf.download
                                                    
                tickers = self.inputs_tickers()
                dates = self.inputs_dates()
                start= dates[0]
                end= dates[1]
                    
                tickers = set(tickers)
                tickers = list(tickers)
                
                data = data_feed(tickers,start=start,end=end)['Close']
                           
                if data.size > 0 and len(tickers) == 1:
                    pass
                
                elif data.size == 0:
                    print("\nEl ticker/s ingresado no existe. Vuelva a cargar un ticker/s disponible en Yahoo Finance.\n")
                    return self.getData()
               
                else:
                    list_not_funds = []
                   
                    for i in data.columns:
                        if data.loc[:,[i]].isnull()[i][0] == True:
                            data.drop(i,axis=1,inplace=True)
                            list_not_funds.append(i)
                            tickers.remove(i)
                           
                    list_not_funds = str(list_not_funds).replace('[','').replace(']','')
                    if len(list_not_funds)>0:
                        print(f'\n\nLista de tickers no encontrados: {list_not_funds}\n')
                
                data.to_csv('SeriesSample.csv')
                print("\nSe ha guardado la muestra a analizar con el nombre SerieSample.csv\n")
                return data,tickers
            
            
            def getData_load(self):
                try:
                    name_file = input("\nEscriba el nombre del archivo con su extensión. Ejemplo SeriesSample.csv : \n")
                    data_L = pd.read_csv(name_file)
                    print(f"\nSe cargó el archivo con el nombre {name_file}\n")
                    return data_L
                except:
                    print("\nEl nombre del archivo no coincide o no se encuentra en la misma ubicación del archivo .py corriga ello y siga las intrucciones.\n")
                    return self.getData_load()



        class Initialize:
            
            def run_script(self):    
                response_data = (input("\nSi quiere cargar un archivo escriba SI en el caso de que no desee coloque NO : \n")).upper()
                if response_data == 'SI':
                    return self.getData_load()
                elif response_data == 'NO':                  
                    return self.getData()
                else:
                    print("\nEsta ingresando palabras que no coinciden con las solicitadas para ejecutar el script. Escribir por favor SI o NO.\n")
                    return self.run_script()
                
        
        
        class Portfolio:
        
            def __init__(self):
                
                funds = input("\nEscribir el monto monetario que se va a destinar a la cartera para operar. Ejemplo si quiere\n"
                                "cargar 100.000,55 debe tipear 100000.55. Máximo permitido = 100.000.000,00  y Mínimo permitido = 100.000,00 : \n")
                
                funds = funds.replace(",",".")
                
                try:                
                    self.funds = float(funds)
                except:
                    self.funds = ''
                    print("\nA escapado a la ejecución del script cargando caracteres que no siguen las instrucciones.\n"
                            "Vuelva a ejecutar el script si así lo desea.\n")
                
                
            def restrictions_portfolio(self):
                
                if float != type(self.funds):
                    pass
                
                else: 
                    if self.funds > 100_000_000:
                        funds = input("\nEl monto supera el máximo permitido de 100.000.000,00 , vuelva a ingresar un monto monetario : \n")
                        funds = funds.replace(",",".")
                        try: 
                            self.funds = float(funds)
                            return self.restrictions_portfolio()
                        except ValueError: 
                            print("\nA escapado a la ejecución del script cargando caracteres que no siguen las instrucciones.\n"
                                    "Vuelva a ejecutar el script si así lo desea.\n")
                        
                    elif self.funds < 100_000:
                        funds = input("\nEl monto es menor al mínimo permitido de 100.000,00 , vuelva a ingresar un monto monetario : \n")
                        funds = funds.replace(",",".")
                        try: 
                            self.funds = float(funds)
                            return self.restrictions_portfolio()
                        except ValueError: 
                            print("\nA escapado a la ejecución del script cargando caracteres que no siguen las instrucciones.\n"
                                    "Vuelva a ejecutar el script si así lo desea.\n")
                    
                    else:
                        return self.funds
            
                
            def balance(self):
                return round(self.funds,2)  
          
                
            
        class ModelingData(Initialize,Data,Portfolio):
            
            def __init__(self):
                super().__init__()
                self.maximum_purchase_amount = 1000
                
                
            def inputs_strategies_1_buy(self):
                
                response_data_buy = input("\nLa ESTRATEGIA 1 está configurada para COMPRAR acciones de un ticker/s si el precio cayo al menos un 1%\n"
                                           "con respecto al día anterior, si desea modificarlo cargue SI en el caso de no desearlo coloque NO : \n").upper()
                if response_data_buy == 'SI':
                    parameter_buy = input("\nCargue el número de variación porcentual en el que desea se ejecute la compra.\n"
                                            "También se puede trabajar con decimales. Ejemplo para -1.55% de caída del precio tipee -1.5 : \n")
                    parameter_buy = parameter_buy.replace(",",".")
                    
                    try:                
                        parameter_buy = float(parameter_buy)
                    except ValueError:
                        print("\nEsta ingresando caracteres que no coinciden con las instrucciones.\n")
                        return self.inputs_strategies_1_buy()
                elif response_data_buy == 'NO':
                    parameter_buy = -1
                else:
                    print("\nEsta ingresando palabras que no coinciden con las solicitadas para ejecutar el script. Escribir por favor SI o NO.\n")
                    return self.inputs_strategies_1_buy()
            
                return parameter_buy
            
            
            def inputs_strategies_1_sell(self):
                    
                response_data_sell = input("\nLa ESTRATEGIA 1 está configurada para VENDER acciones de un ticker/s si el precio sube 2% o más\n"
                                            "con respecto al día anterior, si desea modificarlo cargue SI en el caso de no desearlo coloque NO : \n").upper()
                if response_data_sell == 'SI':
                    parameter_sell = input("\nCargue el número de variación porcentual en el que desea se ejecute la venta.\n"
                                            "También se puede trabajar con decimales. Ejemplo para 5.33% de subida del precio tipee 5.33 : \n")
                    parameter_sell = parameter_sell.replace(",",".")
                    
                    try:                
                        parameter_sell = float(parameter_sell)
                    except ValueError:
                        print("\nEsta ingresando caracteres que no coinciden con las instrucciones.\n")
                        return self.inputs_strategies_1_sell() 
                elif response_data_sell == 'NO':
                    parameter_sell = 2  
                else:
                    print("\nEsta ingresando palabras que no coinciden con las solicitadas para ejecutar el script. Escribir por favor SI o NO.\n")
                    return self.inputs_strategies_1_sell()
                      
                return parameter_sell
            
            
            def inputs_strategies_2_buy(self):
                   
                response_data_buy = input("\nLa ESTRATEGIA 2 está configurada para COMPRAR acciones de un ticker/s si el precio equivale al menos\n"
                                        "El doble del promedio de las cotizaciones de la acción hasta esa fecha, si desea modificarlo cargue SI\n"
                                        "en el caso de no desearlo coloque NO : \n").upper()
                if response_data_buy == 'SI':
                    parameter_buy = input("\nCargue el número de variación en el que desea se ejecute la compra. También se puede trabajar con\n"
                                        "decimales. Ejemplo para 234.55% de subida del precio con respecto al promedio tipee 2.3455 : \n")
                    parameter_buy = parameter_buy.replace(",",".")
                    
                    try:                
                        parameter_buy = float(parameter_buy)
                    except ValueError:
                        print("\nEsta ingresando caracteres que no coinciden con las instrucciones.\n")
                        return self.inputs_strategies_2_buy()
                elif response_data_buy == 'NO':
                    parameter_buy = 1  
                else:
                    print("\nEsta ingresando palabras que no coinciden con las solicitadas para ejecutar el script. Escribir por favor SI o NO.\n")
                    return self.inputs_strategies_2_buy()
                
                return parameter_buy
                
            
            def inputs_strategies_2_sell(self):
               
                response_data_sell = input("\nLa ESTRATEGIA 2 está configurada para VENDER acciones de un ticker/s una acción luego de 5 días\n"
                                            "de haberla comprado, si desea modificarlo cargue SI en el caso de no desearlo coloque NO : \n").upper()
                if response_data_sell == 'SI':
                    parameter_sell = input("\nCargue el número de días que deben pasar desde la compra para que se ejecute la venta.\n"
                                        "Ejemplo para 10 días luego de la compra tipee 10. ADVERTENCIA si tipea un número decimal se redondeará\n" 
                                        "al menor número entero inmediato : \n")
                    parameter_sell = parameter_sell.replace(",",".")
                    
                    try:                
                        parameter_sell = int(parameter_sell)
                    except ValueError:
                        print("\nEsta ingresando caracteres que no coinciden con las instrucciones.\n")
                        return self.inputs_strategies_2_sell()
                elif response_data_sell == 'NO':
                    parameter_sell = 5  
                else:
                    print("\nEsta ingresando palabras que no coinciden con las solicitadas para ejecutar el script. Escribir por favor SI o NO.\n")
                    return self.inputs_strategies_2_sell()
                
                return parameter_sell
            
            
            def modeling_data(self):
                
                if self.restrictions_portfolio()  == None:
                    pass
                else:
                    self.restrictions_portfolio()    
                    
                    data_tickers = self.run_script()
                    
                    param_buy_1 = self.inputs_strategies_1_buy()
                    param_sell_1 = self.inputs_strategies_1_sell()
                    
                    param_buy_2 = self.inputs_strategies_2_buy()
                    param_sell_2 = self.inputs_strategies_2_sell()
                    
                
                    if len(data_tickers) == 2:
                        data = data_tickers[0] 
                        tickers = data_tickers[1] 
                    else: 
                        data = data_tickers
                        data = data.set_index(data.iloc[:,0])
                        data = data.drop('Date',axis=1) 
                        tickers = list(data.columns)
                                                    
                                
                    if len(tickers) == 1:
                        if type(data) == type(pd.Series()): 
                            data = data.to_frame(name=tickers[0])
                            data.insert(1, f'var_{data.columns[0]}',data.pct_change()*100)
                        else:
                            data.insert(1, f'var_{data.columns[0]}',data.pct_change()*100)
                    else:
                        for i in tickers:  
                            index_column_ticker = list(data.columns).index(i)
                            
                            column_var = data.loc[:,i]
                            
                            data.insert(index_column_ticker + 1, f'var_{i}',column_var.pct_change()*100)                   
                    
                            
                    list_columns_var =[]
                    for i in range(1,len(data.columns),2):
                        list_columns_var.append(data.columns[i])
                        
                            
                    for index_var ,name_col in enumerate(list_columns_var): 
                        
                        label_column_param = f'param_{tickers[index_var]}'
                        index_column_var = list(data.columns).index(name_col)   
                        
                        data.insert(index_column_var + 1, label_column_param , 0) 
                            
                        for index_index in range(2,len(data.index)+1): 
                            
                            parameter_mean = round(data[label_column_param[6:]][0:index_index].mean() * (param_buy_2+1),2)
                            data[label_column_param].iloc[index_index-1:index_index] = parameter_mean

                    
                    return data, self.maximum_purchase_amount, param_sell_2, param_buy_1, param_sell_1, self.balance()


    script = Requests_Response()
    dataset = script.mDataClass.modeling_data()
    
    return dataset





def execution_time():
    
    dataset = run_req_res()
 
    if dataset == None:
        pass
    else:
        
        
        
        
        class Strategy1:
            
            def __init__(self):
                self.reportsClass = self.Reports()
                        
            
            class PortfolioManagement:
            
                def __init__(self):
                    self.funds = dataset[5]
                
                def balance(self):
                    return round(self.funds,2)       
                
                def buy(self,buy):
                    self.funds -= buy
                    return round(self.funds,2)
                
                def sell(self,sell):
                    self.funds += sell
                    return round(self.funds)
                    
                
            class TraderStrategy(PortfolioManagement):
                
                def strategies_1(self):
                    
                    data = dataset[0]
                    
                    data_3_col =  data.copy()
                    
                    param_buy_1 = dataset[3]
                    
                    param_sell_1 = dataset[4]

                    maximum_purchase_amount = dataset[1]
                    
                    
                    list_columns_var = []
                    for i in range(1,len(data_3_col.columns),3):
                        list_columns_var.append(data_3_col.columns[i])
                    
                    for i,n in enumerate(list_columns_var):
                        
                        index_column_var = list(data_3_col.columns).index(n)
                        label_column_trades = f'trades_{list_columns_var[i][4:]}'
                        
                        data_3_col.insert(index_column_var + 2, label_column_trades , "no_signal")
                    
                                    
                        data_3_col.loc[ data_3_col[list_columns_var[i]] <= param_buy_1, label_column_trades ] = 'buy'
                        data_3_col.loc[ data_3_col[list_columns_var[i]] >= param_sell_1, label_column_trades ] = 'sell'
                    
                    
                    data_global = pd.DataFrame()
                    
                    
                    for i in range(0,len(data_3_col.columns),4):
                        f = i+4
                        data_individual = data_3_col.loc[:,list(data_3_col.columns)[i:f]]
                        

                        ticker = data_individual.columns[0]
                        
                        label_column_trades = list(data_individual.columns)[-1] 
                        label_column_orders = f'orders_{ticker}'
                        
                        values=["buy","sell"]
                        df_filtered = data_individual[data_individual[label_column_trades].isin(values)] 

                        df_filtered.insert(list(df_filtered.columns).index(label_column_trades) + 1, label_column_orders , "no_signal")
                    
                    
                        try:
                            first_trade = df_filtered[label_column_trades].values[0]            
                        
                            if first_trade == "sell":
                                for index_row in df_filtered.index:
                                    if df_filtered.loc[index_row,[label_column_trades]][0] == 'sell':
                                        df_filtered.drop(index_row,inplace=True)
                                    elif df_filtered.loc[index_row,[label_column_trades]][0] == 'buy':
                                        break
                                    
                            first_trade = df_filtered[label_column_trades].values[0] 
                            if first_trade == "buy":
                                df_filtered[label_column_orders][0:1] = "open"       
                        
                        except IndexError:
                            pass     
                                
                        
                        df_filtered[f'position_nominal_{ticker}'] = None
                        df_filtered[f'position_monetary_{ticker}'] = None
                        
                        data_global = pd.concat([data_global,df_filtered],axis=1)
                    
                                 
                    data_global.sort_index(inplace=True)
                    
                                   
                    for row in range(0,len(data_global.index)):
                        for col in range(3,len(data_global.columns),7):
                            
                            
                            if data_global.iloc[row,col] == 'buy' and data_global.iloc[row,col+1] == 'open' :
                                price = round(data_global.iloc[row,col-3],3)
                                
                                if price < maximum_purchase_amount:
                                    nominal = math.floor(maximum_purchase_amount / price)
                                    cash = round(nominal * price, 2)
                                    
                                    if self.balance() >= cash:
                                        data_global.iloc[row,col+2] = nominal
                                        data_global.iloc[row,col+3] = cash
                                        self.buy(cash) 
                                            
                                    else:
                                        data_global.iloc[row,col+1] = 'no_funds'

                                else: 
                                    data_global.iloc[row,col+1] = 'no_funds'
                    
                    
                            elif data_global.iloc[row,col] == 'sell':
                    
                                try: 
                                    values = ['open','close']
                                    pre_filtered = data_global.iloc[:row,:] 
                                    filtered = pre_filtered[pre_filtered[pre_filtered.columns[col+1]].isin(values)][data_global.columns[col+1]]
                                    last_value = filtered[-1]
                                    index_last_value = filtered.index[-1]                                    
                                    col_nominal = data_global.columns[col+2]
                                
                                    if last_value == 'open':
                                    
                                        price = round(data_global.iloc[row,col-3],3)
                                        nominal = data_global.loc[index_last_value,col_nominal]
                                        cash = round(nominal * price, 2)
                                    
                                        data_global.iloc[row,col+2] = 0 
                                        data_global.iloc[row,col+3] = cash 
                                        self.sell(cash)
                                        
                                        data_global.iloc[row,col+1] = 'close'
                                
                                except IndexError:
                                    pass
                                                        
                        
                            elif data_global.iloc[row,col] == 'buy':
                                
                                try:
                                    values = ['open','close']
                                    pre_filtered = data_global.iloc[:row,:] 
                                    filtered = pre_filtered[pre_filtered[pre_filtered.columns[col+1]].isin(values)][data_global.columns[col+1]] 
                                    last_value = filtered[-1] 
                                                    
                                    if last_value == 'close': 
                                        price = round(data_global.iloc[row,col-3],3) 
                                        
                                        if price < maximum_purchase_amount:
                                            nominal = math.floor(maximum_purchase_amount / price) 
                                            cash = round(nominal * price, 2) 
                                                                
                                            if self.balance() >= cash:
                                                data_global.iloc[row,col+2] = nominal 
                                                data_global.iloc[row,col+3] = cash 
                                                self.buy(cash) 
                                                data_global.iloc[row,col+1] = 'open'
                                      
                                            else:
                                                data_global.iloc[row,col+1] = 'no_funds' 

                                        else:
                                            data_global.iloc[row,col+1] = 'no_funds'

                                except IndexError:
                                    pass
                
                    
                    report_Assets = pd.DataFrame() 


                    for i in range(0,len(data_global.columns),7):
                        
                        try: 
                            f = i+7
                            data_individual = data_global.loc[:,list(data_global.columns)[i:f]]

                            ticker = data_individual.columns[0] 
                            
                            label_column_trades = list(data_individual.columns)[3] 
                            label_column_orders = list(data_individual.columns)[4] 
                            
                            values = ['open','close']
                            df_filtered = data_individual[data_individual[label_column_orders].isin(values)] 
                        
                            last_trade = df_filtered[label_column_trades].values[-1]
                            last_order = df_filtered[label_column_orders].values[-1]
                            ticker = list(df_filtered.columns)[0]
                                      
                            if list(df_filtered.index)[-1] != list(data_individual.index)[-1]:
                                                                                                                
                                if df_filtered[label_column_orders].tail(1)[0] == 'open':
                                    
                                    data_individual[ticker][-1] = data[ticker][-1]
                                    df_filtered = pd.concat([df_filtered,data_individual.tail(1)])
                                    
                                    df_filtered[label_column_orders].iloc[-1] = 'close'
                                    price = round(df_filtered[ticker][-1],3)
                                    nominal = df_filtered.iloc[-2,5] 
                                    cash = round(nominal * price, 2) 
                                
                                    df_filtered.iloc[-1,5] = 0 
                                    df_filtered.iloc[-1,6] = cash 
                                    self.sell(cash) 
          
                            else:
                                if last_trade == "buy" and last_order == "open":
                                    df_filtered[label_column_orders].iloc[-1] = "no_action"
                                    
                        except IndexError:
                            pass
                        
                            
                        df_filtered['profit'] = np.where((df_filtered.iloc[:,4] == 'close'), df_filtered.iloc[:,6] - df_filtered.iloc[:,6].shift(1),0)
                        
                        
                        try:
                            winner_purchases = (df_filtered.profit > 0).value_counts()[True]
                        except:
                            winner_purchases = 0
                
                        report_asset = [list(df_filtered.columns)[0],{'profit':df_filtered.profit.sum(),
                                                'amount_purchases':int(round(df_filtered.profit.count()/2,0)),
                                                'winner_purchases':winner_purchases}] 
                        
                        report_Assets = pd.concat([report_Assets,pd.DataFrame(data=report_asset[1],index=[report_asset[0]])])
                                
                    return report_Assets

            
            class Reports(TraderStrategy):
                
                def report_Strategies(self):
                    
                    report = self.strategies_1()


                    for_research = pd.DataFrame({'Dinero ganado': round(report.profit.sum(),2), 
                                    'Cantidad de compras':report.amount_purchases.sum(),
                                    'Cantidad de compras ganadoras':report.winner_purchases.sum()},index=['Estrategia 1']) 
                    
                    
                    five_most_purchased = report.sort_values(by=['amount_purchases'],ascending=False).head(5)
                    five_most_purchased = five_most_purchased.rename(columns={'profit':'Dinero ganado',
                                                                            'amount_purchases':'Cantidad de compras',
                                                                            'winner_purchases':'Cantidad de compras ganadoras'}).rename_axis("5 acciones más compradas")

                    three_most_winners = report.sort_values(by=['profit'],ascending=False).head(3)
                    three_most_winners = three_most_winners.rename(columns={'profit':'Dinero ganado',
                                                                            'amount_purchases':'Cantidad de compras',
                                                                            'winner_purchases':'Cantidad de compras ganadoras'}).rename_axis("3 acciones más ganadoras")


                    return for_research, five_most_purchased, three_most_winners
        
                


        class Strategy2: 
            
            def __init__(self):
                self.reportsClass = self.Reports()
            
            
            class PortfolioManagement:
            
                def __init__(self):
                    self.funds = dataset[5]
                
                def balance(self):
                    return round(self.funds,2)       
                
                def buy(self,buy):
                    self.funds -= buy
                    return round(self.funds,2)
                
                def sell(self,sell):
                    self.funds += sell
                    return round(self.funds)
                    
                
            class TraderStrategy(PortfolioManagement):
                
                def strategies_2(self):

                    data_global = dataset[0] 
                    
                    data_3_col =  data_global.copy()
                    
                    param_sell_2 = dataset[2]
                    
                    maximum_purchase_amount = dataset[1]
                    
                    
                    list_columns_var = []
                    for i in range(1,len(data_3_col.columns),3):
                        list_columns_var.append(data_3_col.columns[i])
                    
                    for i,n in enumerate(list_columns_var):
                        
                        index_column_var = list(data_3_col.columns).index(n)
                        label_column_trades = f'trades_{list_columns_var[i][4:]}'
                        
                        data_3_col.insert(index_column_var + 2, label_column_trades , "no_signal")

                    
                    list_param = [] 
                    list_trades = [] 
                    for i_name_col in enumerate(data_3_col.columns):
                        if i_name_col[1][0:5] == 'param':
                            list_param.append(i_name_col[1])
                        elif i_name_col[1][0:6] == 'trades':
                            list_trades.append(i_name_col[1])
                    
                    
                    tickers =[] 
                    for i in range(0,len(data_3_col.columns),4):
                        tickers.append(data_3_col.columns[i])        
                    

                    for index ,name_col in enumerate(tickers):
                        data_3_col.loc[ data_3_col[name_col]>= data_3_col[list_param[index]], list_trades[index] ] = 'buy'                      
                        data_3_col[list_trades[index]][0:1] = 'no_signal' 
                    

                    data_global = pd.DataFrame() 
                    
                    
                    for i in range(0,len(data_3_col.columns),4):
                        f = i+4
                        data_individual = data_3_col.loc[:,list(data_3_col.columns)[i:f]]
                        

                        ticker = data_individual.columns[0] 
                        
                        label_column_trades = list(data_individual.columns)[-1] 
                        label_column_orders = f'orders_{ticker}' 
                        

                        data_individual[label_column_orders] = "no_signal"
                        
                        try:
                            for index in data_individual[label_column_trades].index:
                                first_trade = data_individual.loc[index,label_column_trades]
                                            
                                if first_trade == 'buy':
                                    data_individual.loc[index,label_column_orders] = 'open' 
                                    break
                        except IndexError:
                            pass
                        
                        
                        data_individual[f'position_nominal_{ticker}'] = None 
                        data_individual[f'position_monetary_{ticker}'] = None 
                        
                        data_global = pd.concat([data_global,data_individual],axis=1) 
                    
                      
                    for row in range(0,len(data_global.index)): 
                        for col in range(3,len(data_global.columns),7): 
                            
                            
                            if data_global.iloc[row,col] == 'buy' and data_global.iloc[row,col+1] == 'open' :
                                price = round(data_global.iloc[row,col-3],3) 
                                
                                if price < maximum_purchase_amount: 
                                    nominal = math.floor(maximum_purchase_amount / price) 
                                    cash = round(nominal * price, 2) 
                                    
                                    if self.balance() >= cash:
                                        data_global.iloc[row,col+2] = nominal 
                                        data_global.iloc[row,col+3] = cash 
                                        self.buy(cash) 
                                        
                                        try:
                                            data_global.iloc[row+param_sell_2,col] = 'sell' 
                                        except IndexError:
                                            pass
                    
                                    else:
                                        data_global.iloc[row,col+1] = 'no_funds' 
                                   
                                else: 
                                    data_global.iloc[row,col+1] = 'no_funds'
                                
                
                            elif data_global.iloc[row,col] == 'sell':
                                                        
                                try: 
                                    values = ['open','close']
                                    pre_filtered = data_global.iloc[:row,:] 
                                    filtered = pre_filtered[pre_filtered[pre_filtered.columns[col+1]].isin(values)][data_global.columns[col+1]] 
                                    last_value = filtered[-1]
                                    index_last_value = filtered.index[-1]                                    
                                    col_nominal = data_global.columns[col+2]
                                
                                    if last_value == 'open':
                                        
                                        price = round(data_global.iloc[row,col-3],3) 
                                        nominal = data_global.loc[index_last_value,col_nominal] 
                                        cash = round(nominal * price, 2)
                                    
                                        data_global.iloc[row,col+2] = 0 
                                        data_global.iloc[row,col+3] = cash 
                                        self.sell(cash) 
                                        
                                        data_global.iloc[row,col+1] = 'close' 
                                
                                except IndexError:
                                    pass
                
                
                            elif data_global.iloc[row,col] == 'buy':
                                
                                try: 
                                    values = ['open','close']
                                    pre_filtered = data_global.iloc[:row,:] 
                                    filtered = pre_filtered[pre_filtered[pre_filtered.columns[col+1]].isin(values)][data_global.columns[col+1]] 
                                    last_value = filtered[-1] 
                                    
                                    if last_value == 'close': 
                                        price = round(data_global.iloc[row,col-3],3) 
                                        
                                        if price < maximum_purchase_amount: 
                                            nominal = math.floor(maximum_purchase_amount / price)
                                            cash = round(nominal * price, 2) 
                                                        
                                            if self.balance() >= cash:
                                                data_global.iloc[row,col+2] = nominal 
                                                data_global.iloc[row,col+3] = cash 
                                                self.buy(cash) 
                                                data_global.iloc[row,col+1] = 'open'
                                                
                                                try:
                                                    data_global.iloc[row+param_sell_2,col] = 'sell' 
                                                except IndexError:
                                                    pass
                                                    
                                            else:
                                                data_global.iloc[row,col+1] = 'no_funds' 
                                            
                                        else:
                                            data_global.iloc[row,col+1] = 'no_funds'
                                                    
                                except IndexError:
                                    pass
                                
                    
                    report_Assets = pd.DataFrame() 


                    for i in range(0,len(data_global.columns),7):
                        
                        try: 
                            f = i+7
                            data_individual = data_global.loc[:,list(data_global.columns)[i:f]]

                            ticker = data_individual.columns[0] 
                            
                            label_column_trades = list(data_individual.columns)[3] 
                            label_column_orders = list(data_individual.columns)[4] 
                            
                            values = ['open','close']
                            df_filtered = data_individual[data_individual[label_column_orders].isin(values)] 
                        
                            last_trade = df_filtered[label_column_trades].values[-1]
                            last_order = df_filtered[label_column_orders].values[-1]
                            ticker = list(df_filtered.columns)[0]
                                        
                            if list(df_filtered.index)[-1] != list(data_individual.index)[-1]:
                                                                                                
                                if df_filtered[label_column_orders].tail(1)[0] == 'open':
                                    
                                    data_individual[ticker][-1] = data_global[ticker][-1] 
                                    df_filtered = pd.concat([df_filtered,data_individual.tail(1)])
                                    
                                    df_filtered[label_column_orders].iloc[-1] = 'close'
                                    price = round(df_filtered[ticker][-1],3) 
                                    nominal = df_filtered.iloc[-2,5] 
                                    cash = round(nominal * price, 2) 
                                
                                    df_filtered.iloc[-1,5] = 0 
                                    df_filtered.iloc[-1,6] = cash 
                                    self.sell(cash) 
    
                            else:
                                if last_trade == "buy" and last_order == "open": 
                                    df_filtered[label_column_orders].iloc[-1] = "no_action"
                        
                        except IndexError:
                            pass
                                
                        
                        df_filtered['profit'] = np.where((df_filtered.iloc[:,4] == 'close'), df_filtered.iloc[:,6] - df_filtered.iloc[:,6].shift(1),0)
                        
                        
                        try:
                            winner_purchases = (df_filtered.profit > 0).value_counts()[True]
                        except:
                            winner_purchases = 0
                
                        report_asset = [list(df_filtered.columns)[0],{'profit':df_filtered.profit.sum(),
                                                'amount_purchases':int(round(df_filtered.profit.count()/2,0)),
                                                'winner_purchases':winner_purchases}] 
                        
                        report_Assets = pd.concat([report_Assets,pd.DataFrame(data=report_asset[1],index=[report_asset[0]])])
                                
                    return report_Assets

            
            class Reports(TraderStrategy):
                
                def report_Strategies(self):
                    
                    report = self.strategies_2() 

                    for_research = pd.DataFrame({'Dinero ganado': round(report.profit.sum(),2), 
                                    'Cantidad de compras':report.amount_purchases.sum(),
                                    'Cantidad de compras ganadoras':report.winner_purchases.sum()},index=['Estrategia 2']) 
                    
                    
                    five_most_purchased = report.sort_values(by=['amount_purchases'],ascending=False).head(5)
                    five_most_purchased = five_most_purchased.rename(columns={'profit':'Dinero ganado',
                                                                            'amount_purchases':'Cantidad de compras',
                                                                            'winner_purchases':'Cantidad de compras ganadoras'}).rename_axis("5 acciones más compradas")

                    three_most_winners = report.sort_values(by=['profit'],ascending=False).head(3)
                    three_most_winners = three_most_winners.rename(columns={'profit':'Dinero ganado',
                                                                            'amount_purchases':'Cantidad de compras',
                                                                            'winner_purchases':'Cantidad de compras ganadoras'}).rename_axis("3 acciones más ganadoras")


                    return for_research, five_most_purchased, three_most_winners
                



        class Strategy3: 

            def __init__(self):   
                self.reportsClass = self.Reports()


            class PortfolioManagement: 
                
                def __init__(self):
                    self.funds = dataset[5]
                
                def balance(self):
                    return round(self.funds,2)       
                
                def buy(self,buy):
                    self.funds -= buy
                    return round(self.funds,2)
                
                def sell(self,sell):
                    self.funds += sell
                    return round(self.funds)


            class TraderStrategy(PortfolioManagement): 
                
                
                def strategies_2(self): 
                    
                    data_global = dataset[0] 

                    data_3_col =  data_global.copy()
                    
                    param_sell_2 = dataset[2] 
                    

                    list_columns_var = []
                    for i in range(1,len(data_3_col.columns),3):
                        list_columns_var.append(data_3_col.columns[i])
                    
                    for i,n in enumerate(list_columns_var):
                        
                        index_column_var = list(data_3_col.columns).index(n)
                        label_column_trades = f'trades_s2_{list_columns_var[i][4:]}'
                        
                        data_3_col.insert(index_column_var + 2, label_column_trades , "no_signal")
                    
                    
                    list_param = [] 
                    list_trades = [] 
                    for i_name_col in enumerate(data_3_col.columns):
                        if i_name_col[1][0:5] == 'param':
                            list_param.append(i_name_col[1])
                        elif i_name_col[1][0:9] == 'trades_s2':
                            list_trades.append(i_name_col[1])
                            
                            
                    list_columns_tickers = []
                    for i in range(0,len(data_3_col.columns),4):
                        list_columns_tickers.append(data_3_col.columns[i])
                    
                    for index, name_col in enumerate(list_columns_tickers):
                        data_3_col.loc[ data_3_col[name_col]>= data_3_col[list_param[index]], list_trades[index] ] = 'buy'                      
                        data_3_col[list_trades[index]][0:1] = 'no_signal'
                    
                    
                    data_global_s2 = pd.DataFrame() 
                    
                    
                    for i in range(0,len(data_3_col.columns),4):
                        f = i+4
                        data_individual = data_3_col.loc[:,list(data_3_col.columns)[i:f]]
                        

                        ticker = data_individual.columns[0] 
                        
                        label_column_trades = list(data_individual.columns)[-1] 
                        label_column_orders = f'orders_s2_{ticker}' 
                        

                        data_individual[label_column_orders] = "no_signal"
                        
                        try:
                            for index in data_individual[label_column_trades].index:
                                first_trade = data_individual.loc[index,label_column_trades]
                                            
                                if first_trade == 'buy':
                                    data_individual.loc[index,label_column_orders] = 'open' 
                                    break
                        
                        except IndexError:
                            pass
                        
                        
                        data_global_s2 = pd.concat([data_global_s2,data_individual],axis=1) 
                    
                    
                    for row in range(0,len(data_global_s2.index)): 
                        for col in range(3,len(data_global_s2.columns),5): 
                            
                            
                            if data_global_s2.iloc[row,col] == 'buy' and data_global_s2.iloc[row,col+1] == 'open' :
                                
                                try:
                                    data_global_s2.iloc[row+param_sell_2,col] = 'sell' 
                                except IndexError:
                                    pass
                                    
                    
                            elif data_global_s2.iloc[row,col] == 'sell':
                                                        
                                try: 
                                    values = ['open','close']
                                    pre_filtered = data_global_s2.iloc[:row,:] 
                                    filtered = pre_filtered[pre_filtered[pre_filtered.columns[col+1]].isin(values)][data_global_s2.columns[col+1]] 
                                    last_value = filtered[-1]
                                
                                    if last_value == 'open':
                                        data_global_s2.iloc[row,col+1] = 'close' 
                                
                                except IndexError:
                                    pass
                
                
                            elif data_global_s2.iloc[row,col] == 'buy':
                                
                                try: 
                                    values = ['open','close']
                                    pre_filtered = data_global_s2.iloc[:row,:] 
                                    filtered = pre_filtered[pre_filtered[pre_filtered.columns[col+1]].isin(values)][data_global_s2.columns[col+1]] 
                                    last_value = filtered[-1] 
                                    
                                    if last_value == 'close': 
                                        
                                        data_global_s2.iloc[row,col+1] = 'open'
                                        
                                        try:
                                            data_global_s2.iloc[row+param_sell_2,col] = 'sell' 
                                        except IndexError:
                                            pass
                                            
                                except IndexError:
                                    pass
                                
                    
                    data_global_s2_end = pd.DataFrame() 
                    
                    
                    for i in range(0,len(data_global_s2.columns),5):
                        
                        try: 
                            f = i+5
                            data_individual = data_global_s2.loc[:,list(data_global_s2.columns)[i:f]]

                            ticker = data_individual.columns[0] 
                            
                            label_column_trades = list(data_individual.columns)[3] 
                            label_column_orders = list(data_individual.columns)[4] 
                            
                            values = ['open','close']
                            df_filtered = data_individual[data_individual[label_column_orders].isin(values)] 
                        
                            last_trade = df_filtered[label_column_trades].values[-1]
                            last_order = df_filtered[label_column_orders].values[-1]
                            ticker = list(df_filtered.columns)[0]
                                        
                            if list(df_filtered.index)[-1] != list(data_individual.index)[-1]:
                                                                                                
                                if df_filtered[label_column_orders].tail(1)[0] == 'open':
                                    
                                    data_individual[ticker][-1] = data_3_col[ticker][-1] 
                                    df_filtered = pd.concat([df_filtered,data_individual.tail(1)])
                                    
                                    df_filtered[label_column_orders].iloc[-1] = 'close'
  
                            else:
                                if last_trade == "buy" and last_order == "open": 
                                    df_filtered[label_column_orders].iloc[-1] = "no_action"
                        
                        except IndexError:
                            pass
                        
                        
                        data_global_s2_end = pd.concat([data_global_s2_end,df_filtered],axis=1)

                    
                    data_global_s2_end.sort_index(inplace=True)
                                    
                    return data_global, data_global_s2_end
                
                    
                def strategies_1(self): 
                    
                    return_strategies_2 = self.strategies_2()
                    
                    data_global, data_global_s2_end  = return_strategies_2
                    
                    data_3_col = data_global.copy()
                    
                    param_buy_1 = dataset[3]
                    
                    param_sell_1 = dataset[4]
                    
                
                    list_columns_var =[]
                    for i in range(1,len(data_3_col.columns),3):
                        list_columns_var.append(data_3_col.columns[i])
                    
                    for i,n in enumerate(list_columns_var):
                        
                        index_column_var = list(data_3_col.columns).index(n)
                        label_column_trades = f'trades_s1_{list_columns_var[i][4:]}'
                        
                        data_3_col.insert(index_column_var + 2, label_column_trades , "no_signal")
                        
                        data_3_col.loc[ data_3_col[list_columns_var[i]] <= param_buy_1, label_column_trades ] = 'buy'
                        data_3_col.loc[ data_3_col[list_columns_var[i]] >= param_sell_1, label_column_trades ] = 'sell'
                    
                    
                    data_global_s1 = pd.DataFrame() 
                    
                    
                    for i in range(0,len(data_3_col.columns),4):
                        f = i+4
                        data_individual = data_3_col.loc[:,list(data_3_col.columns)[i:f]]
                        

                        ticker = data_individual.columns[0]
                        
                        label_column_trades = list(data_individual.columns)[-1] 
                        label_column_orders = f'orders_s1_{ticker}' 
                        
                        values=["buy","sell"]
                        df_filtered = data_individual[data_individual[label_column_trades].isin(values)] 

                        df_filtered.insert(list(df_filtered.columns).index(label_column_trades) + 1, label_column_orders , "no_signal")
                        

                        try:
                            first_trade = df_filtered[label_column_trades].values[0]            
                            
                            if first_trade == "sell":
                                for index_row in df_filtered.index:
                                    if df_filtered.loc[index_row,[label_column_trades]][0] == 'sell':
                                        df_filtered.drop(index_row,inplace=True)
                                    elif df_filtered.loc[index_row,[label_column_trades]][0] == 'buy': 
                                        break
                                    
                            first_trade = df_filtered[label_column_trades].values[0] 
                            if first_trade == "buy":
                                df_filtered[label_column_orders][0:1] = "open"       
                        
                        except IndexError:
                            pass     
                        
                        
                        data_global_s1 = pd.concat([data_global_s1,df_filtered],axis=1) 
                    
                              
                    data_global_s1.sort_index(inplace=True)
                    
                             
                    for row in range(0,len(data_global_s1.index)):
                        for col in range(3,len(data_global_s1.columns),5): 
                            
                    
                            if data_global_s1.iloc[row,col] == 'sell':
                    
                                try: 
                                    values = ['open','close']
                                    pre_filtered = data_global_s1.iloc[:row,:] 
                                    filtered = pre_filtered[pre_filtered[pre_filtered.columns[col+1]].isin(values)][data_global_s1.columns[col+1]]
                                    last_value = filtered[-1]
                                
                                    if last_value == 'open':                  
                                        data_global_s1.iloc[row,col+1] = 'close'
                                
                                except IndexError:
                                    pass
                                                    
                            
                            elif data_global_s1.iloc[row,col] == 'buy':
                                
                                try: 
                                    values = ['open','close'] 
                                    pre_filtered = data_global_s1.iloc[:row,:] 
                                    filtered = pre_filtered[pre_filtered[pre_filtered.columns[col+1]].isin(values)][data_global_s1.columns[col+1]] 
                                    last_value = filtered[-1] 
                                                        
                                    if last_value == 'close': 
                                            data_global_s1.iloc[row,col+1] = 'open'

                                except IndexError:
                                    pass
                    
                    
                    data_global_s1_end = pd.DataFrame() 


                    for i in range(0,len(data_global_s1.columns),5):
                        
                        try: 
                            f = i+5
                            data_individual = data_global_s1.loc[:,list(data_global_s1.columns)[i:f]]

                            ticker = data_individual.columns[0] 
                            
                            label_column_trades = list(data_individual.columns)[3] 
                            label_column_orders = list(data_individual.columns)[4] 
                            
                            values = ['open','close']
                            df_filtered = data_individual[data_individual[label_column_orders].isin(values)] 
                        
                            last_trade = df_filtered[label_column_trades].values[-1]
                            last_order = df_filtered[label_column_orders].values[-1]
                            ticker = list(df_filtered.columns)[0]
                                    
                            if list(df_filtered.index)[-1] != list(data_individual.index)[-1]:
                                                                                                                    
                                if df_filtered[label_column_orders].tail(1)[0] == 'open':
                                    
                                    data_individual[ticker][-1] = data_global[ticker][-1] 
                                    df_filtered = pd.concat([df_filtered,data_individual.tail(1)])
                                    
                                    df_filtered[label_column_orders].iloc[-1] = 'close'
      
                            else:
                                if last_trade == "buy" and last_order == "open":
                                    df_filtered[label_column_orders].iloc[-1] = "no_action"
                                    
                        except IndexError:
                            pass
                        
                        data_global_s1_end = pd.concat([data_global_s1_end,df_filtered],axis=1)
                        
                    
                    data_global_s1_end.sort_index(inplace=True)
                    
                    return data_global, data_global_s2_end, data_global_s1_end
                    

                def strategies_3(self): 
                    
                    return_strategies_s1 = self.strategies_1()
                    
                    data_global, data_global_s2_end, data_global_s1_end = return_strategies_s1
                    
                    data_3_col = data_global.copy()
                    
                    maximum_purchase_amount = dataset[1] 
                    

                    list_columns_tickers =[] 
                    for i in range(0,len(data_3_col.columns),3):
                        list_columns_tickers.append(data_3_col.columns[i])
                        
                    data_1_col = pd.DataFrame()
                    for i,n in enumerate(list_columns_tickers): 
                        data_1_col.insert(i,n,data_3_col.loc[:,n]) 
                        
                    list_columns_s1 = [] 
                    for i in range(4,len(data_global_s1_end.columns),5):
                        list_columns_s1.append(data_global_s1_end.columns[i])
                        
                    list_columns_s2 = [] 
                    for i in range(4,len(data_global_s2_end.columns),5):
                        list_columns_s2.append(data_global_s2_end.columns[i])


                    data_global_s3 = pd.DataFrame()
                    
                    for i in range(0,len(data_1_col.columns),1):
                        f = i+1
                        data_individual = data_1_col.loc[:,list(data_1_col.columns)[i:f]]
                        ticker = list_columns_tickers[i]
                        col_i = i+4*(i+1)
                            
                        data_individual[list_columns_s1[i]] = data_global_s1_end.iloc[:,col_i] 
                        data_individual[list_columns_s2[i]] = data_global_s2_end.iloc[:,col_i] 
                        
                        label_column_trades = f'trades_s3_{ticker}' 
                        label_column_orders = f'orders_s3_{ticker}' 
                        
                        data_individual[label_column_trades] = "no_signal" 
                        
                        data_individual.loc[ (data_individual[list_columns_s1[i]] == 'open') &
                                                (data_individual[list_columns_s2[i]] == 'open'),
                                                label_column_trades ] = 'buy'                      
                        
                        data_individual.loc[ (data_individual[list_columns_s1[i]] == 'close') |
                                                (data_individual[list_columns_s2[i]] == 'close'),
                                                label_column_trades ] = 'sell'   
                        
                        data_individual[label_column_orders] = "no_signal" 
                        
                        data_individual[f'position_nominal_{ticker}'] = None 
                        data_individual[f'position_monetary_{ticker}'] = None 
                        
                        try:
                            for index in data_individual[label_column_trades].index:
                                first_trade = data_individual.loc[index,label_column_trades]
                                            
                                if first_trade == 'buy':
                                    data_individual.loc[index,label_column_orders] = 'open' 
                                    break
                        except IndexError:
                            pass
                        
                     
                        data_global_s3 = pd.concat([data_global_s3,data_individual],axis=1)
                    
                                     
                    for row in range(0,len(data_global_s3.index)): 
                        for col in range(3,len(data_global_s3.columns),7): 
                            
                            
                            if data_global_s3.iloc[row,col] == 'buy' and data_global_s3.iloc[row,col+1] == 'open' :
                                price = round(data_global_s3.iloc[row,col-3],3) 
                                
                                if price < maximum_purchase_amount: 
                                    nominal = math.floor(maximum_purchase_amount / price) 
                                    cash = round(nominal * price, 2) 
                                    
                                    if self.balance() >= cash:
                                        data_global_s3.iloc[row,col+2] = nominal 
                                        data_global_s3.iloc[row,col+3] = cash 
                                        self.buy(cash) 
                         
                                    else:
                                        data_global_s3.iloc[row,col+1] = 'no_funds' 

                                else: 
                                    data_global_s3.iloc[row,col+1] = 'no_funds'
                                
                         
                            elif data_global_s3.iloc[row,col] == 'sell':
                                                       
                                try: 
                                    values = ['open','close']
                                    pre_filtered = data_global_s3.iloc[:row,:] 
                                    filtered = pre_filtered[pre_filtered[pre_filtered.columns[col+1]].isin(values)][data_global_s3.columns[col+1]] 
                                    last_value = filtered[-1] 
                                    index_last_value = filtered.index[-1] 
                                    col_nominal = data_global_s3.columns[col+2] 
                    
                                    if last_value == 'open':
 
                                        price = round(data_global_s3.iloc[row,col-3],3) 
                                        nominal = data_global_s3.loc[index_last_value,col_nominal] 
                                        cash = round(nominal * price, 2) 
                                    
                                        data_global_s3.iloc[row,col+2] = 0 
                                        data_global_s3.iloc[row,col+3] = cash 
                                        self.sell(cash) 
                                        
                                        data_global_s3.iloc[row,col+1] = 'close' 
                                
                                except IndexError:
                                    pass
                    
                    
                            elif data_global_s3.iloc[row,col] == 'buy':
                                
                                try: 
                                    values = ['open','close'] 
                                    pre_filtered = data_global_s3.iloc[:row,:] 
                                    filtered = pre_filtered[pre_filtered[pre_filtered.columns[col+1]].isin(values)][data_global_s3.columns[col+1]] 
                                    last_value = filtered[-1] 
                                    
                                    if last_value == 'close': 
                                        price = round(data_global_s3.iloc[row,col-3],3) 
                                        
                                        if price < maximum_purchase_amount: 
                                            nominal = math.floor(maximum_purchase_amount / price) 
                                            cash = round(nominal * price, 2) 
                                                        
                                            if self.balance() >= cash:
                                                data_global_s3.iloc[row,col+2] = nominal 
                                                data_global_s3.iloc[row,col+3] = cash 
                                                self.buy(cash) 
                                                data_global_s3.iloc[row,col+1] = 'open'
                                                       
                                            else:
                                                data_global_s3.iloc[row,col+1] = 'no_funds'
                                        
                                        else: 
                                            data_global_s3.iloc[row,col+1] = 'no_funds'
                                            
                                except IndexError:
                                    pass
                    
                    
                    report_Assets = pd.DataFrame() 


                    for i in range(0,len(data_global_s3.columns),7):
                        
                        try: 
                            f = i+7
                            data_individual = data_global_s3.loc[:,list(data_global_s3.columns)[i:f]]

                            ticker = data_individual.columns[0] 
                            
                            label_column_trades = list(data_individual.columns)[3] 
                            label_column_orders = list(data_individual.columns)[4] 
                            
                            values = ['open','close']
                            df_filtered = data_individual[data_individual[label_column_orders].isin(values)] 
                        
                            last_trade = df_filtered[label_column_trades].values[-1]
                            last_order = df_filtered[label_column_orders].values[-1]
                            ticker = list(df_filtered.columns)[0]
                                        
                            if list(df_filtered.index)[-1] != list(data_individual.index)[-1]:
                                                                                                
                                if df_filtered[label_column_orders].tail(1)[0] == 'open':
                                    
                                    data_individual[ticker][-1] = data_global[ticker][-1] 
                                    df_filtered = pd.concat([df_filtered,data_individual.tail(1)])
                                    
                                    df_filtered[label_column_orders].iloc[-1] = 'close'
                                    price = round(df_filtered[ticker][-1],3) 
                                    nominal = df_filtered.iloc[-2,5] 
                                    cash = round(nominal * price, 2) 
                                
                                    df_filtered.iloc[-1,5] = 0 
                                    df_filtered.iloc[-1,6] = cash 
                                    self.sell(cash) 
    
                            else:
                                if last_trade == "buy" and last_order == "open": 
                                    df_filtered[label_column_orders].iloc[-1] = "no_action"
                        
                        except IndexError:
                            pass
                        
                        
                        df_filtered['profit'] = np.where((df_filtered.iloc[:,4] == 'close'), df_filtered.iloc[:,6] - df_filtered.iloc[:,6].shift(1),0)
                        
                    
                        try:
                            winner_purchases = (df_filtered.profit > 0).value_counts()[True]
                        except:
                            winner_purchases = 0
                
                        report_asset = [list(df_filtered.columns)[0],{'profit':df_filtered.profit.sum(),
                                                'amount_purchases':int(round(df_filtered.profit.count()/2,0)),
                                                'winner_purchases':winner_purchases}] 
                        
                        report_Assets = pd.concat([report_Assets,pd.DataFrame(data=report_asset[1],index=[report_asset[0]])])
                                
                                    
                    return report_Assets

                
            class Reports(TraderStrategy): 
                
                def report_Strategies(self):
                    
                    report = self.strategies_3() 

                    for_research = pd.DataFrame({'Dinero ganado': round(report.profit.sum(),2), 
                                    'Cantidad de compras':report.amount_purchases.sum(),
                                    'Cantidad de compras ganadoras':report.winner_purchases.sum()},index=['Estrategia 3']) 
                    
                    
                    five_most_purchased = report.sort_values(by=['amount_purchases'],ascending=False).head(5)
                    five_most_purchased = five_most_purchased.rename(columns={'profit':'Dinero ganado',
                                                                            'amount_purchases':'Cantidad de compras',
                                                                            'winner_purchases':'Cantidad de compras ganadoras'}).rename_axis("5 acciones más compradas")
                    
                    
                    three_most_winners = report.sort_values(by=['profit'],ascending=False).head(3)
                    three_most_winners = three_most_winners.rename(columns={'profit':'Dinero ganado',
                                                                            'amount_purchases':'Cantidad de compras',
                                                                            'winner_purchases':'Cantidad de compras ganadoras'}).rename_axis("3 acciones más ganadoras")

                    
                    return for_research, five_most_purchased, three_most_winners


        def sampleReport():
            start = str(dataset[0].index[0]).split(" ")[0]
            end = str(dataset[0].index[-1]).split(" ")[0]
            tickers = []
            for t in range(0,len(dataset[0].columns),3):
                tickers.append(dataset[0].columns[t])
            
            return [start, end, str(tickers).replace('[','').replace(']','').replace("'","").replace(" ","")]



        script1 = Strategy1() 
        script2 = Strategy2() 
        script3 = Strategy3() 


        start = time()
        
        instance_reports_1 = script1.reportsClass.report_Strategies() 
        instance_reports_2 = script2.reportsClass.report_Strategies() 
        instance_reports_3 = script3.reportsClass.report_Strategies() 


        most_bought_1 = instance_reports_1[1] 
        most_bought_1['Estrategia'] = 'Estrategia 1'
        most_bought_2 = instance_reports_2[1] 
        most_bought_2['Estrategia'] = 'Estrategia 2'
        most_bought_3 = instance_reports_3[1] 
        most_bought_3['Estrategia'] = 'Estrategia 3'
        most_bought = pd.concat([most_bought_1,most_bought_2,most_bought_3])
        most_bought.sort_values(by='Cantidad de compras',ascending=False,inplace=True)
        most_bought = most_bought.reset_index() 
        most_bought.set_index('Estrategia',inplace=True) 
        most_bought.rename(columns={'5 acciones más compradas':'Tickers'},inplace=True)
        
        count_5 = set()
        most_bought_5 = pd.DataFrame()
        for i,values in enumerate(most_bought.iloc[:,0].values):
            count_5.add(values)
            most_bought_5 = most_bought_5.append(most_bought.iloc[i])
            if 5 == len(count_5): 
                break
        
        last_column = most_bought_5.pop('Tickers') 
        most_bought_5.insert(0, 'Tickers', last_column) 
        last_column = most_bought_5.pop('Dinero ganado') 
        most_bought_5.insert(1, 'Dinero ganado', last_column) 
        
            
        more_winners_1 = instance_reports_1[2] 
        more_winners_1['Estrategia'] = 'Estrategia 1'
        more_winners_2 = instance_reports_2[2] 
        more_winners_2['Estrategia'] = 'Estrategia 2'
        more_winners_3 = instance_reports_3[2] 
        more_winners_3['Estrategia'] = 'Estrategia 3'
        more_winners = pd.concat([more_winners_1,more_winners_2,more_winners_3])
        more_winners.sort_values(by='Dinero ganado',ascending=False,inplace=True)
        more_winners = more_winners.reset_index() 
        more_winners.set_index('Estrategia',inplace=True) 
        more_winners.rename(columns={'3 acciones más ganadoras':'Tickers'},inplace=True)
        
        count_3 = set()
        more_winners_stocks = pd.DataFrame()
        for i,values in enumerate(more_winners.iloc[:,0].values):
            count_3.add(values)
            more_winners_stocks = more_winners_stocks.append(more_winners.iloc[i])
            if 3 == len(count_3): 
                break
   
        last_column = more_winners_stocks.pop('Tickers') 
        more_winners_stocks.insert(0, 'Tickers', last_column)
        last_column = more_winners_stocks.pop('Dinero ganado')
        more_winners_stocks.insert(1, 'Dinero ganado', last_column)  
        
        
        def strategiesReport():
                strategies_more_winners = pd.concat([instance_reports_1[0].iloc[:,0],instance_reports_2[0].iloc[:,0],instance_reports_3[0].iloc[:,0]])
                strategies_more_winners = strategies_more_winners.rename_axis('Estrategias Más Ganadoras').sort_values(ascending=False).to_string() 
                print(f"\n\n\nEstrategias más Ganadoras:\n{strategies_more_winners}\n\n\n"
                      f"\n\n\n5 Acciones más Compradas de todas las Estrategias:\n{most_bought_5}\n\n\n"
                      f"\n\n\n3 Acciones que Ganaron más Dinero de todas las Estrategias:\n{more_winners_stocks}\n\n\n")                                                             


        print(f'''\n\n\n{instance_reports_1[0]}
                \n\n\n{instance_reports_1[1]}
                \n\n\n{instance_reports_1[2]}
                \n\n\n
                \n\n\n{instance_reports_2[0]}
                \n\n\n{instance_reports_2[1]}
                \n\n\n{instance_reports_2[2]}
                \n\n\n
                \n\n\n{instance_reports_3[0]}
                \n\n\n{instance_reports_3[1]}
                \n\n\n{instance_reports_3[2]}
                \n\n\n''')
        
        
        strategiesReport()
        
        end = time()
        
        
        sampleReport = sampleReport()
        date_start = sampleReport[0]
        date_end = sampleReport[1]
        tickers = sampleReport[2]
        
        
        print(f"\n\n\nPrimer día hábil bursátil de la muestra: {date_start}.\n" 
              f"Últimp día hábil bursátil de la muestra: {date_end}.\n"
              f"Tickers analizados: {tickers}\n")
        
        
        
        amount_time = end - start
        end = dt.datetime.fromtimestamp(end).isoformat() 
        start = dt.datetime.fromtimestamp(start).isoformat()
        
        
        print(f'\nTiempo de ejecución del script {amount_time}.\n' 
            f'El scrip inició la ejecución el {start} y finalizó el {end}\n\n')
        


        execute_soft = input("Si desea analizar una nueva estrategia tipee SI : ").upper()
        if execute_soft.upper() == "SI":
            execution_time()
        else:
            print("\nPrograma cerrado. Si desea analizar las estrategias debe ejecutar el programa nuevamente.\n\n")



if __name__ == "__main__":
    execution_time()    



