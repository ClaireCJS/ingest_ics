"""
    Google Calendar event is created from ICS files.  Includes ability to monitor a folder.

    USAGE:
        python ingest-ics.py monitor              -     monitors c:/calendar for ics files being dropped into
        python ingest-ics.py whatever.ics         -     create event from a single ics file
"""
import os
import re
import sys
import time
import glob
import random
import webbrowser
from urllib.parse import urlencode
from datetime import datetime
#import pytz
import emoji
import arrow
import pyperclip
from ics import Calendar as icsCalendar
from colorama import Fore, Style, init
init(autoreset=True)

FOLDER_TO_DROP_ICS_FILES_IN                  = r"c:/calendar"                   #processed ics files will be moved to a subfolder named "processed" along with a companion file containing the event creation URL
HOW_OFTEN_TO_CHECK                           = 1                                #how many seconds between checking FOLDER_TO_DROP_ICE_FILES_IN repeatedly
AUTOMATICALLY_GO_TO_GOOGLE_CALENDAR_CREATION = True                             #open link in web browser automatically?
COPY_URL_TO_CLIPBOARD                        = False                            #copy event link to clipboard?
EMOJI_TO_ADD_TO_BEGINNING_OF_EVENT_TITLE     = "smiling_face_with_horns"        #set to "" to disable, or change to another emoj
MY_TIME_ZONE                                 = "America/New_York"
DOT_COLORS                                   = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA, Fore.WHITE, Fore.LIGHTBLACK_EX, Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX]

def create_google_calendar_link(start, end, title, location, description):
    """
    Creates a google calendar link with the appropriate attributes
    """
    global EMOJI_TO_ADD_TO_BEGINNING_OF_EVENT_TITLE
    BASE_URL   = "https://www.google.com/calendar/render"
    start      = arrow.get(start).to("UTC").format("YYYYMMDDTHHmmss") + "Z"
    end        = arrow.get(end  ).to("UTC").format("YYYYMMDDTHHmmss") + "Z"

    if EMOJI_TO_ADD_TO_BEGINNING_OF_EVENT_TITLE:
        emoj  = emoji.emojize(":" + EMOJI_TO_ADD_TO_BEGINNING_OF_EVENT_TITLE  + ":")
        title = emoj + title

    event_data = {
        "action"   : "TEMPLATE"         ,
        "text"     : title              ,
        "dates"    : f"{start}/{end}"   ,
        "location" : location           ,
        "details"  : description        ,
    }
    url = BASE_URL + "?" + urlencode(event_data)
    return url


def fix_ics(ics_string):
    """
    Fixes malformed ics files that are missing DESCRIPTION tags from the VEVENT and VALARM subsections
    """
    print("* Fixing ics data...")
    summary_search = re.search(r"SUMMARY:(.*)", ics_string)
    if summary_search is None: raise ValueError("Error: Could not find SUMMARY in the ics file.")
    summary       = summary_search.group(1)
    vevent_search = re.compile(r"(BEGIN:VEVENT.*?)(END:VEVENT)", re.DOTALL)
    valarm_search = re.compile(r"(BEGIN:VALARM.*?)(END:VALARM)", re.DOTALL)
    updated_ics   = ics_string
    def replace_vevent_func(match):
        if "DESCRIPTION:" in match.group(0): return match.group(0)
        return match.group(1) + "\nDESCRIPTION:" + summary + "\n" + match.group(2)
    def replace_valarm_func(match):
        if "DESCRIPTION:" in match.group(0): return match.group(0)
        return match.group(1) + "\nDESCRIPTION:Alarm\n" + match.group(2)
    updated_ics = vevent_search.sub(replace_vevent_func, updated_ics)
    updated_ics = valarm_search.sub(replace_valarm_func, updated_ics)
    #pdated_ics = updated_ics.replace(   "☻",   "")
    updated_ics = updated_ics.replace("\n\n", "\n")
    return updated_ics


def generate_google_calendar_url_from_ics_file(file_path):                                                                                  #pylint: disable=C0103
    """
    Process an individual ics file and opens a Google Calendar event create page in cresponse
    """
    global COPY_URL_TO_CLIPBOARD, AUTOMATICALLY_GO_TO_GOOGLE_CALENDAR_CREATION           ;print(f"* Processing ics file: {file_path}")
    with open(file_path, 'r', encoding="utf-8") as file: ics_content = file.read()       ;print(f"\t- contents of original ics file={Fore.LIGHTBLACK_EX}{ics_content}{Fore.WHITE}")
    updated_ics_content = fix_ics(ics_content)                                           ;print(f"\t- updated_ics_content is: {Fore.GREEN}{updated_ics_content}{Fore.WHITE}")
    calendar            = icsCalendar(updated_ics_content)                               ;print(f"{Fore.RED}\t- calendar={calendar}{Fore.WHITE}")
    events              = calendar.events                                                ;print(f"\t- # events={len(events)}")
    for event in events:
        #print(f"{Fore.CYAN}\tevent={event}{Fore.WHITE}")
        print(f"{Fore.CYAN}\tevent.begin={event.begin}{Fore.WHITE}")
        print(f"{Fore.BLUE}\tevent.begin.datetime={event.begin.datetime}{Fore.WHITE}")
        title           = event.name
        location        = event.location
        description     = event.description.replace('\n','<BR>')
        #start          = arrow.get(event.begin.datetime)
        #end            = arrow.get(event.end  .datetime)
        #start          = arrow.get(event.begin.datetime).to("UTC").format("YYYYMMDDTHHmmss") + "Z"
        #end            = arrow.get(event.end  .datetime).to("UTC").format("YYYYMMDDTHHmmss") + "Z"
        #start          = arrow.get(event.begin.datetime).replace(tzinfo="UTC")
        #end            = arrow.get(event.end  .datetime).replace(tzinfo="UTC")
        local_tz        = arrow.now().tzinfo
        start           = arrow.get(event.begin.datetime).to(local_tz)
        end             = arrow.get(event.end  .datetime).to(local_tz)
        print(f"{Fore.LIGHTBLUE_EX}\tarrow.get(event.begin.datetime)={arrow.get(event.begin.datetime)}{Fore.WHITE}")
        print(f"{Fore.LIGHTCYAN_EX}\tarrow.get(event.begin.datetime).to(local_tz)={arrow.get(event.begin.datetime).to(local_tz)}{Fore.WHITE}")

        url             = create_google_calendar_link(start, end, title, location, description)
        print(url)
        if AUTOMATICALLY_GO_TO_GOOGLE_CALENDAR_CREATION:
            successful = webbrowser.open_new(url)                                              # open in browser (remove "_new" to not open in new window)
            if not successful:
                print(f"{Fore.RED}ERROR: Couldn't open web browser, so copying URL to clipboard instead.")
                pyperclip.copy(url)
    if COPY_URL_TO_CLIPBOARD: pyperclip.copy(url)                                              # if the ics has multiple events (which it won't, ever, in our cases), only copy the last one to the clipboard
    return url





def monitor_folder(folder_to_drop_ics_files_in):
    """
    Monitors a folder for new ics files and processes them accordingly.
    After processing, they are moved into a processing subfolder.
    A new file with the same filename but ".url" added on to the end will be created with the generated URL, so that it is also saved
    """
    global HOW_OFTEN_TO_CHECK, DOT_COLORS
    processed_files = 0
    processed_folder = os.path.join(folder_to_drop_ics_files_in, 'processed')
    if not os.path.exists(folder_to_drop_ics_files_in):
        os.makedirs(folder_to_drop_ics_files_in)
        print(Fore.RED + '\n' + 'Folder did not exist, created new one at ' + folder_to_drop_ics_files_in + '\n\n')
        print(Fore.RED + 'You can now drop your .ics files into this folder for processing!!!\n' * 5)
    print('\n' + f'{Fore.GREEN}{Style.BRIGHT}!!!!!!!!!!!!!!!!!!!!! Starting calendar monitor !!!!!!!!!!!!!!!!!!!!!!\n' * 5, end="")
    dot_count = 0
    while True:
        dot_count += 1
        print(random.choice(DOT_COLORS) + ".", end="")
        if dot_count > 1000: dot_count = 1
        if dot_count == 1:
            print(f'\n\n{Fore.GREEN}{Style.NORMAL}Just save ics files into {folder_to_drop_ics_files_in} to create Google Calendar events!\n')
        ics_files = glob.glob(folder_to_drop_ics_files_in + '/*.ics')
        for ics_file in ics_files:
            # solve the problem this script intends to solve: generating the google calendar URL from our ICS file:
            url = generate_google_calendar_url_from_ics_file(ics_file)

            # Now move our file to processing, because it has now been processed

            # ensure our processed folder exists
            if not os.path.exists(processed_folder):
                print(f"\n\n{Fore.YELLOW}Creating processed folder: {processed_folder}{Fore.RESET}")
                print("ics files will be moved here as they are processed")
                print("url files will be moved here as they are generated from the processed ics files")
                os.makedirs(processed_folder)

            # move file to processed folder when we are done with it...
            file_name                      = os.path.basename(ics_file)
            #file_directory                = os.path.dirname (ics_file)
            file_name_base, file_extension = os.path.splitext(file_name)
            new_file_name                  = f"{file_name_base}.{file_extension}"
            new_file_path                  = os.path.join(processed_folder, new_file_name)

            # ...but make sure target filename is unique..
            counter = 0
            while os.path.exists(new_file_path):
                counter = counter + 1
                new_file_name = f"{file_name_base}.{str(counter)}{file_extension}"
                new_file_path = os.path.join(processed_folder, new_file_name)
            os.rename(ics_file, new_file_path)

            # Let the user know the processing was done
            processed_files += 1
            print(Fore.GREEN + '\n\nProcessed file: ' + ics_file + '\nTotal processed files: ' + str(processed_files))

            # Store our generated google calendar URL result in a file
            results_file = f"{processed_folder}/{os.path.basename(ics_file)}.url"       # had processed.on.{time.strftime("%Y%m%d%H%M%S")} in filename but realized the file's date is already exactly that
            with open(results_file, 'w', encoding="utf-8") as file: file.write(url)     # store our URL for posterity/postprocesing
        time.sleep(HOW_OFTEN_TO_CHECK)                                                  # check every HOW_OFTEN_TO_CHECK seconds


def main():
    global FOLDER_TO_DROP_ICS_FILES_IN                                                  #, MY_TIME_ZONE
    if len(sys.argv) < 2:
        print(f"{Fore.CYAN}{Style.BRIGHT}\n* Options:\n")
        print(f"{Fore.CYAN}{Style.NORMAL}1. Run with a filename of an .ics file as argument.")
        print(f"{Fore.CYAN}{Style.NORMAL}2. Run with 'monitor' as argument to monitor the folder {FOLDER_TO_DROP_ICS_FILES_IN} for new .ics files")
        sys.exit(777)

    #local_timezone = pytz.timezone(MY_TIME_ZONE)                                       # Replace 'America/New_York' with your local time zone

    if sys.argv[1] == 'monitor':
        monitor_folder(FOLDER_TO_DROP_ICS_FILES_IN)
        sys.exit()
    elif not os.path.exists(sys.argv[1]):
        print(f"\n{Fore.RED}File {sys.argv[1]} does not exist!\n")
        sys.exit(666)                                                                   # return a non-zero error level
    generate_google_calendar_url_from_ics_file(sys.argv[1])

if __name__ == "__main__":
    main()
