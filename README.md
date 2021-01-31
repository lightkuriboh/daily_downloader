## Project description  
- A job to daily download trading history on [SGX](https://www.sgx.com/research-education/derivatives).  
  
## Project features
- Based on user's command, on a specific time in day, downloading historic trading data.   
- Based on user's instruction, being able to download trading history in ```N (N >= 1)``` previous days, \
  up to the number of published data.  
- Logging information for future debugging and resolving issues.  
- Running in background, starting with the system, and auto restarting on failure.  
- Skipping downloaded files, in casual running schedule or restart.  
- Retrying to download files that were failed to download on previous days.  
- Recovery plan on crashing (killed, interrupted, ...).  
  
## Analysis on SGX 's data  
- Only working days have trading data.  
- Not all consecutive working days have trading data (especially with early published days).  
- With each day in the past that had trading history published, SGX associates it with an auto-increment ID.
- Data's format (```TickData_structure.dat```, ```TC_structure.dat```) may change overtime, in the past or in the future.  
- Data's structure on different days might be different (On early days, main datas are not zipped files).
  
## Project design details  
#### Downloaded files structures  
- Files are grouped by the date it was published.  
- Files' name is kept as published on the SGX website.  
- Saves format files (```.dat``` files) for each day.  
  
#### Logging information  
- Uses Python's logging module, writes to ```logs/main.logs```.  
- With ```WARNING```, ```ERROR```, and ```CRITICAL``` levels, logs both to file and console. \
  Otherwise, logs to file only.  
- Logs the following kinds of information:
  * ```INFO```: file size, file name that is going to be downloaded; downloaded successfully; skipped downloaded files; \
    enter action phases (download, recovery).  
  * ```WARN```: file size is larger than ```1 GB```.  
  * ```ERROR```: failed to download files (file not found on the server, failed to write to local files, \
    and in-completed download).  
  
#### Scheduling plan  
- At start-up, user provides the program with information: daily time-to-run, ```past_days```.  
- At first run after starting up, downloads on the server at most ```past_days```  previous days, also tries to\
  recovery failed files within that amount of days.  
- At following runs, downloads and recoveries with ```past_days = 1```.  
- With this scheduling plan, in case the program crashes (killed, ...), if given ```past_days``` at first run is larger than 2,\ 
  it could be able to recover. Files that were not downloaded \
  on the previous day will still be downloaded when it is not marked in the ```success.txt```.  
  
#### Download plan    
- Downloads file based on just one information: date_id - the associate ID with date, fixed by SGX. \
  (ex: ```https://links.sgx.com/1.0.0/derivatives-historical/2101/WEBPXTICK_DT.zip``` - ```date_id=2101```)  
- Get the file's name from the server (called ```server_filename```), and the file size. \
  If the header ```Content-Length=0```, marks ```file not found```.   
- At first, just downloads to ```temp/``` folder. After the download is complete, move it to the ```downloaded/``` folder. \
  This will not have us clean the wanted ```downloaded/``` folder in case downloads failed.  
- When a file is downloaded and moved to ```downloaded/``` successfully, immediately logs it to the ```recovery/success.txt``` with information: ```date_id-server_filename```.  
- At the program's start-up, load the success logs and skips files that haves ```date_id-server_filename``` exists.  
  
#### Recovery plan  
- Recovery schedule is mentioned above.  
- Keeps recovery information in files by the date it is logged (in ```recovery``` folder,\
  format ```recovery_{date}.txt```).  
- On each run, loads ```past_days``` recovery logs, retries to download failed files. \
  Writes files that are failed to download today to ```recovery_{today}.txt```.  
  
## Systemd serving  
- I provided a .service file that allows user to run the job as ```systemd``` process.  
- I tended to send a notification email is the ```systemd``` process is ```on-failure```, \
  but was not success (deadline) on setting up ```bds-mailx```.  
  