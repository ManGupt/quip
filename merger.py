
# Return first set of digits, used for sorting
def fdigit(x):
    stf = etf = False
    st, et = 0, len(x)
    for j, i in enumerate(x):
        if i.isdigit() and not stf:
            st = j
            stf = True
        elif not i.isdigit() and stf and not etf:
            et = j
            etf = True
            break
    return x[st:et]

import quip
import sys

token = None
if len(sys.argv) == 2:
    print ("Using Login Token: " + sys.argv[1])
    token = sys.argv[1]
else:
    # no default token
    print ("Must provide login token")
    sys.exit(1)
    
try:
    client = quip.QuipClient(access_token=token)
    user = client.get_authenticated_user()
except Exception as e:
    print (e)
    client = user = None
    sys.exit(1)

def proceed(client, user):
    print ("Logged in user: " + str(user['name']))
    folders = {}
    threads = {}

    def getData(client, threads, tid):
        thread = client.get_thread(tid)
        threads[thread['thread']['title']] = (thread['thread']['id'], (thread['html']))

    def storeThread(client, threads, fid):
        fold = client.get_folder(fid)
        for ch in fold['children']:
            for k, v in ch.items():
                if 'thread_id' in k:
                    getData(client, threads, v)

    def storeFolder(client, folders, fid):
        fold = client.get_folder(fid)
        folders[fold['folder']['title']] = fold['folder']['id']
        for ch in fold['children']:
            for k, v in ch.items():
                if 'folder_id' in k:
                    storeFolder(client, folders, v)

    def iterFolder(client, user, folders):
        for k, v in user.items():
            if 'folder_ids' in k:
                folders[k] = []
                for f in v:
                    folders[k].append(f)
                    storeFolder(client, folders, f)
            elif 'folder_id' in k:
                folders[k] = v
                storeFolder(client, folders, v)

    # Get All Folders
    iterFolder(client, user, folders)
    fnames = list(folders.keys())
    for i, k in enumerate(fnames):
        print (str(i+1) + '.' + str(k))
    
    # Get Specified folder from User
    idx = input("No. of Folder whose threads need merging: ")
    fid = folders[fnames[int(idx)-1]]
    
    # Get Threads from Specified folder
    storeThread(client, threads, fid)
    
    # Create Folder for merging
    idx = input("No. of Folder where merged file is to be placed: ")
    fid = folders[fnames[int(idx)-1]]

    # Create new thread for merged file
    content = input("Heading for merged file: ")
    tid = client.new_document(content, member_ids=[fid])

    # Sorting done based on digits in heading
    # TODO: can be enhanced to ask user for order.
    sorted_list = []
    try:
        # Try sorting the threads based on integers in headings
        # Ex: Thread 1, Thread 10, Thread 5
        # will be sorted as Thread 1, Thread 5, Thread 10
        sorted_list = sorted(threads.keys(), key=lambda x: int(fdigit(x)))
    except:
        # Use default Python sorting
        sorted_list = sorted(threads.keys())
    # Actual Merging
    for k in sorted(threads.keys(), key=lambda x: int(fdigit(x))):
        id, content = threads[k]
        client.edit_document(tid['thread']['id'], content, 0)
    
    # Done
    print ("Merging Done.")
    
if user:
    proceed(client, user)