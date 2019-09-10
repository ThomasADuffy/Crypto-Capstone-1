import os
import getpass

def csv_combiner(csv_header,csv_out,csv_dir,csv_list):
    ''' This function combines csv files which were split up with the same headers into one
        
        Input
        ------
        csv_header - This is the actually header in plain text which is present in all of the CSV files
        csv_out - This is file name which you want to write the new combined csv file
        csv_dir - this is the folder containing all of the CSVs
        csv_list - this is a lst of all the file names to combine
        
        Return
        -------
        Technically nothing but it will write the csv in that folder designated'''


    csv_merge = open(csv_dir+csv_out, 'w')
    csv_merge.write(csv_header)
    csv_merge.write('\n')

    for file in csv_list:
        csv_in = open(csv_dir+f"{file}")
        for line in csv_in:
            if line.startswith(csv_header):
                continue
            csv_merge.write(line)
        csv_in.close()
    csv_merge.close()
    print('Please Verify consolidated CSV file : ' + csv_out)

if __name__ == "__main__":
    csv_header = 'Tweet ID, Conversation ID, Author Id , Author Name, isVerified, DateTime, Language, Tweet Text, Replies, Retweets, Favorites, Mentions, Hashtags, Permalink, URLs, isPartOfConversation, isReply, isRetweet, Reply To User ID, Reply To User Name, Quoted Tweet ID, Quoted Tweet User Name, Quoted Tweet User ID'
    csv_out = 'BTC.csv'
    csv_dir = f"/media/{getpass.getuser()}/extra/Crypto-Capstone-1/data/BTC-tweets/"
    csv_list = [str(x)+'.csv' for x in range(0,12)]
    csv_combiner(csv_header,csv_out,csv_dir,csv_list)