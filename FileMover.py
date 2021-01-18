#import datetime
#srcDir = r'\\MCS-PROFILE-P01\Users$\thensley\DownloadsTest\\'
#dstDir =  'C:\TEMP\TU %s - %s' % (datetime.date.today().strftime("%m%d%Y"),(datetime.date.today() - datetime.timedelta(days=30)).strftime("%m%d%Y"))

import shutil, os, glob, csv, re
def moveAllFilesinDir(srcDir, dstDir,consoleOut):
    # Make directory path if not available
    try:
        if os.path.isdir(dstDir) == False:
            consoleOut += "<br>" +("Making directory: %s" % (dstDir))
            os.mkdir(dstDir)
    # Check if both the are directories
        if os.path.isdir(srcDir) and os.path.isdir(dstDir) :
            # Iterate over all the files in source directory
            for filePath in glob.glob(srcDir + '\*'):
                # Move each file to destination Directory
                consoleOut += "<br>" +("Moving %s" % (filePath))
                shutil.move(filePath, dstDir);
            consoleOut += "<br>" +("Completed File Move")
            return consoleOut
    except Exception as e:
        consoleOut += "<br>" + str(e)
        consoleOut += "<br>" +("Move was unsuccessful")
        return consoleOut

def replaceExcelCellInfo(srcDir,consoleOut):
    os.chdir(srcDir)
    FileList = glob.glob('*.csv')
    #consoleOut += "<br>" +(FileList)

    #Set find / replace strings in file
    findStr1 = '='
    findStr2 = ',\n'
    replaceStr1 = ''
    replaceStr2 = '\n'
    #findStr3 = '==='

    #Iterates file from filelist / Checks rowcount / Removes replacestrings / Writes file
    for file in FileList:
        consoleOut += "<br>" +('Working on replacements ' + file)
        with open(file, 'r') as f:
            currentCsv = f.read()
            #currentCsv = [n for n in f.readlines() if not n.startswith('Transaction')]
        rowReader = open(file)
        rowCount = sum(1 for row in rowReader)
        consoleOut += "<br>" +("File has " + str(rowCount) + " rows")
        #Deletes Service account row from CSV file / Checks all files
        consoleOut = deleteRowsFromCsv(file,consoleOut)
        with open(file, 'r') as f:
            currentCsv = f.read()
        rowReader = open(file)
##        if rowCount > 10000:
##            consoleOut = deleteRowsFromCsv(file,consoleOut)
##            with open(file, 'r') as f:
##                currentCsv =  f.read()
##            rowReader = open(file)
##            rowCount = sum(1 for row in rowReader)
##            consoleOut += "<br>" +("File now has " + str(rowCount) + " rows")
        newCsv = re.sub(findStr1, replaceStr1, currentCsv)
        newCsv = re.sub(findStr2, replaceStr2, newCsv)
        #newCsv = re.sub(findStr3, replaceStr1, newCsv)
        
        filePath = '.\\' + file
        with open(file, 'w') as f:
             f.write(newCsv)
    consoleOut += "<br>" +('Finished replacements = / ,\n in files')
    return consoleOut

#Opens received file / Reads file lines / Writes line
def deleteRowsFromCsv(modifiedCsv,consoleOut):
    with open(modifiedCsv, 'r') as infile:
        data_in = infile.readlines()
        for index,lines in enumerate(data_in):
            if "Service Date" in lines:
                consoleOut += "<br>" + ("Service Text found at line {}.. Deleting".format(index))
                del data_in[index]
    with open(modifiedCsv, 'w+') as outfile:
        outfile.writelines(data_in)
    return consoleOut

# Testing script locally
#moveAllFilesinDir(srcDir,dstDir,consoleOut)
#replaceExcelCellInfo(srcDir,consoleOut)
