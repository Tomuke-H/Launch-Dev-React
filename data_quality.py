#Plan & Profile: Make sure dates in profiles and plans that are uploaded are correct and in the future, web and excel
#Make sure all required fields are populated with the proper data types and with values within a line item
#Plan & Profile: Make sure we can handle empty files and or files that we don't expect
#Make sure we can handle duplicate combinations of launchprofile names in file or duplicate launch plan items and send to user
#Make sure we can handle negative values for quantities for plans and profiles
#Make sure we can handle error propogation from DB and or api layer
#Make sure we can handle removal of schema's columns either with null or error to user
#Make sure for profiles for the region(s) field all regions listed have a quantity in the profile field
#Make sure if columns or values for nodemodes are changed or do not exist provide the row/value combo that is invalid 


def launchprofile_check(val1):
    df = pd.DataFrame(val1.active.values)
    #Get the info of the dataframe
    df.info()
   




def launchplan_check(val1):