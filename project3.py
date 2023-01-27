DIRECTORIES_KEY = 'directories'
FILES_KEY = 'files'
ROOT_DIRECTORY_NAME = 'home'


def makeStartFileSystem():
    # make a starting file system to work with
    my_file_system = {
        ROOT_DIRECTORY_NAME: {
            DIRECTORIES_KEY: {},
            FILES_KEY: []
        }
    }

    # add directories you want to start with
    # my_file_system[DIRECTORIES_KEY] = {name of directorie:{}} #directories are stored in another dictionary
    # my_file_system[FILES_KEY] = [name of files] #files are stored in a list
    return my_file_system

def getDirectory(my_file_system, path):
    if path == '/':
        return my_file_system[ROOT_DIRECTORY_NAME]
    #remove first /
    string = path.strip()
    if path[0] == '/':
        string = string[1:]

    #remove lingering /
    if string[-1] == '/':
        string = string[:-1]

    parents = string.strip().split('/')
    direc = my_file_system.get(parents[0])
    for i in parents[1:]:
        direc = direc.get(DIRECTORIES_KEY).get(i)

    return direc

def pwd(my_file_system, PWD):
    # display the current working directory
    current_working_directory = PWD
    print("Current working directory is: " + str(current_working_directory))


def mkdir(my_file_system, components, PWD):
    if len(components) == 1:
        print("Error: Missing directory name")
        return False

    directory_name = components[1]

    # check if directory_name is legal
    if '/' in directory_name:
        print("Error: Directory name cannot contain the forward slash '/'")
        return False

    # check if directory name already exists
    currentDir = getDirectory(my_file_system, PWD)
    if directory_name in currentDir[DIRECTORIES_KEY]:
        print("Error: Directory already exists")
        return False

    # create directory
    currentDir[DIRECTORIES_KEY][directory_name] = {DIRECTORIES_KEY: {}, FILES_KEY: []}
    print(my_file_system)
    # return success
    return True


def cd(my_file_system, components, PWD):
    if len(components) == 1:
        print("Error: Missing directory name")
        return PWD

    directory_name_or_path = components[1]

    ## '/'
    if directory_name_or_path == '/':
        PWD = '/' + ROOT_DIRECTORY_NAME
        return PWD

    if directory_name_or_path[-1] == '/':  ##removing the last slash so strip() doesn't return blanks
        directory_name_or_path = directory_name_or_path[:-1]

    if len(directory_name_or_path.split('/')) == 1:
        ## they only gave us one folder to go in

        ## '' or '.'
        if directory_name_or_path == '' or directory_name_or_path == '.':
            return PWD  ## do nothing, you moved no where

        ## '..'
        if directory_name_or_path == '..':

            if PWD == '/' + ROOT_DIRECTORY_NAME:
                return PWD

            ## remove last folder from PWD
            parents = PWD.split('/')
            all_but_current = parents[:-1]
            PWD = all_but_current[0]
            for i in all_but_current[1:]:
                PWD += '/' + i
            return PWD

        ## 'foldername'
        currentDir = getDirectory(my_file_system, PWD)
        if directory_name_or_path not in currentDir[DIRECTORIES_KEY]:
            print('Error: Directory not found')
            return PWD
        else:
            PWD = PWD + '/' + directory_name_or_path
            return PWD



    else:
        ## they gave use a path
        if directory_name_or_path[0] == '/':  ##absolute path
            string = directory_name_or_path[1:]
            direcs = string.split('/')
            newPWD = '/' + ROOT_DIRECTORY_NAME  # start at root
            for i in direcs[1:]:
                if i in getDirectory(my_file_system, newPWD)[DIRECTORIES_KEY]:
                    newPWD += '/' + i
                else:
                    print('Error: Path does not exist')
                    return PWD  # return old path

            PWD = newPWD
            return PWD


        else:  ## relative path
            string = directory_name_or_path
            direcs = string.split('/')
            newPWD = PWD
            for i in direcs:
                if i in getDirectory(my_file_system, newPWD)[DIRECTORIES_KEY]:
                    newPWD += '/' + i
                else:
                    print('Error: Path does not exist')
                    return PWD  # return old path

            PWD = newPWD
            return PWD


def rm(my_file_system, components, PWD):
    if len(components) == 1:
        print("Error: Missing file name")
        return False

    file_name = components[1]
    # check if file exists
    currentDir = getDirectory(my_file_system, PWD)
    if file_name in currentDir.get(FILES_KEY):
        currentDir.get(FILES_KEY).remove(file_name)
        print("File deleted")
    else:
        print("File does not exist")


def ls(my_file_system, components, PWD):
    if len(components) == 1:
        ## look in current folder
        path = PWD

    else:
        directory_name_or_path = components[1]
        newPath = cd(my_file_system, ['cd', directory_name_or_path], PWD)
        path = newPath

    currentDir = getDirectory(my_file_system, path)
    print('contents for ' + path)
    for i in currentDir[DIRECTORIES_KEY]:
        print(i)
    for i in currentDir[FILES_KEY]:
        print(i)

    return


def touch(my_file_system, components, PWD):
    if len(components) == 1:
        print("Error: Missing directory name")
        return False

    file_name = components[1]
    currentDir = getDirectory(my_file_system, PWD)

    # Check if the file already exists
    if file_name in currentDir[FILES_KEY]:
        print('File already exists')
        return

    # Create the file and add it to the root directory
    currentDir[FILES_KEY].append(file_name)
    print('File created')
    return

def locate(my_file_system, PWD, components):
    filename = components[1]
    if '/' in filename:
        print('Error: File name cannot contain the forward slash '/'"')

    # start a list for all possible paths
    paths = []
    # get reference to current file system
    current = getDirectory(my_file_system, PWD)
    # start recursive search
    locate_recursive(current, filename, PWD, paths)
    for i in paths:
        print(i)
    # return list of all possible paths
    return paths

def locate_recursive(current_dir, file_name, PWD, paths):
    # check if file_name is in current_dir
    if file_name in current_dir[FILES_KEY]:
        # if it is, add current path to paths
        paths.append(PWD + '/' + file_name)

    # loop over all directories in current_dir
    for dir_name in current_dir[DIRECTORIES_KEY]:
        # add directory name to paths
        newPWD = PWD + '/' + dir_name
        # get reference to directory
        dir_ref = current_dir[DIRECTORIES_KEY][dir_name]
        # recursively call locate_recursive
        locate_recursive(dir_ref, file_name, newPWD, paths)




# RETURNS 0 IF USER WANTS TO EXIT
# RETURNS 1 IF USER CHOOSES ANY OTHER COMMANDS
def doCommands(input_string, my_file_system, PWD):
    retVal = 1
    components = input_string.strip().split(' ')
    command = components[0]
    directory = ROOT_DIRECTORY_NAME
    current_directory = {}

    if (command == 'mkdir'):
        mkdir(my_file_system, components, PWD)
    elif (command == 'cd'):
        PWD = cd(my_file_system, components, PWD)  ## changes PWD
    elif (command == 'ls'):
        ls(my_file_system, components, PWD)
    elif (command == 'pwd'):
        pwd(my_file_system, PWD)
    elif (command == 'rm'):
        rm(my_file_system, components, PWD)
    elif (command == 'touch'):
        touch(my_file_system, components, PWD)
    elif (command == 'locate'):
        locate(my_file_system, PWD, components)
    elif (command == 'exit'):
        retVal = 0
        print("Thank you for using our program!")
    elif (command == 'print'):  ## self made
        print(my_file_system)
    else:
        print('Command not recognized...')

    return retVal, PWD


def run_file_system():
    my_file_system = makeStartFileSystem()
    PWD = '/' + ROOT_DIRECTORY_NAME  # update PWD with cd()


    exit_Val = 1
    while (exit_Val != 0):
        commands = input("Enter your value: ")
        exit_Val, PWD = doCommands(commands, my_file_system, PWD,)


if __name__ == '__main__':
    run_file_system()