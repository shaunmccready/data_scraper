import csv
import os
import psycopg2


def formatWorldDataValues(lineArray,fileNameToInsert):
    numOfFields = 8
    count = 1
    result = ""

    ## Problem here with avoiding splitting on quoted commas
    print("BEFORE:", lineArray.splitlines())
    test = csv.reader(lineArray.splitlines(), quotechar='"', quoting=csv.QUOTE_NONE)


    # for item in lineArray.split(","):
    for arrayString in test:
        for item in arrayString:
            # print(len(item))

            val = item
            item.replace('\'', '\\\'')
            print("INSIDE:", item)

            if 1 <= count <= 2:
                if not item:
                    result = result + "NULL"
                else:
                    result = result + "\'{}\'".format(item)
            elif count == 3:
                if not item:
                    result = result + "NULL"
                else:
                    if fileNameToInsert < '02-02-2020.csv':
                        result = result + "TO_TIMESTAMP(\'{}\',\'M-DD-YYYY HH24:MI\')".format(item)
                    else:
                        # Example: 2020-02-02T23:43:02
                        result = result + "TO_TIMESTAMP(\'{}\',\'YYYY-MM-DDTHH24:MI:SS\')".format(item)
            else:
                if not item:
                    result = result + "NULL"
                else:
                    result = result + "{}".format(item)
            
            result = result + ","
            count += 1

    while count <= numOfFields:
        result = result + "NULL" + ","
        count += 1


    result = result[:-1]
    return result


def insertSingleFileWithData(fileNameToInsert):
    if fileNameToInsert < '02-01-2020.csv':
        return

    insertFileNameStatement = "INSERT INTO public.daily_files_processed(file_name) VALUES" 
    insertFileNameData = ""

    ## Step 1 - Try to insert the filename into the daily_files_processed table
    insertFileNameData = insertFileNameData + '(\'' + fileNameToInsert + '\')'

    # insertFileNameData = insertFileNameData[:-1]
    statementToExecute = insertFileNameStatement + insertFileNameData + ';'
    print("\n", statementToExecute)
    insertFileNameData = ""

    try:    
        cur.execute(statementToExecute)

    except (Exception, psycopg2.DatabaseError) as error:
        print("File Name Insert PROBLEM!!!!")
        print(error)
        return

    ## Step 2 - Insert the data from the file if there were no errors to the world_data table
    print("##### Filename {} inserted SUCCESSFULLY. Now for data... #####\n".format(fileNameToInsert))
    fileToOpen = open(os.path.join(current_path , fileNameToInsert)) 

    #skip header line
    iterLines = iter(fileToOpen.readlines())
    next(iterLines)

    insertCsvDataStatement = "INSERT INTO public.world_data(province_state, country_region, last_update_in_utc, confirmed, deaths, recovered, latitude, longitude) VALUES"
    for line in iterLines:
        lineArray = line.rstrip("\n")

        values = formatWorldDataValues(lineArray,fileNameToInsert)
        statementToExecute = insertCsvDataStatement + "(" + values + ");"    

        try:    
            cur.execute(statementToExecute)

        except (Exception, psycopg2.DatabaseError) as error:
            print("Data insert PROBLEM!!!!   Original statement:")
            print(statementToExecute)
            print("data:" , lineArray)
            print(error)
            continue

    conn.commit()
    cur.close



current_path = os.path.abspath('../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports')

allfiles = os.listdir(current_path)
allfiles.sort()
csvFiles = []

for csvfile in allfiles:
    if (".csv" in csvfile):
        csvFiles.append(csvfile)


for csvfile in csvFiles:
    conn = psycopg2.connect(host="localhost", database="coronavirus-tracker", user="coronavirus-tracker-api-admin", password="coronavirus-tracker-api-admin")
    cur = conn.cursor()

    insertSingleFileWithData(csvfile)




if conn is not None:
    conn.close()
    print('Database connection closed.')