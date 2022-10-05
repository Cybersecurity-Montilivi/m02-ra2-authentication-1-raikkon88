import json, names, argparse, time
from log4python.Log4python import log

parser = argparse.ArgumentParser(description='Auth and names generator params', prog="generator")
parser.add_argument('-s', '--source-path', help='Source path to read the authentication methods', type=str, default='./auth.json')
parser.add_argument('-d', '--dest-path', help='Destination path to store the generated file', type=str, default='./generated.json')
parser.add_argument('-n', '--total-people', help='Number of people to generate', type=int, default=10)
args = vars(parser.parse_args())

Logger = log("Generator")

def read_json_file(path): 
    f = open(path, 'r')
    data = json.load(f)
    f.close()
    return data

def write_json_file(path, data): 
    f = open(path, 'w')
    f.write(json.dumps(data))
    f.close()

def generate_name():
    return names.get_full_name() + ' ' + names.get_last_name()

def create_entire_person(name, authenticationMethods):
    return {
        "name": name,
        "authentications": authenticationMethods
    }

def generate_list(maxPeople, authenticationMethods):
    peopleCounter = 0
    people = list()
    while(peopleCounter < args['total_people']):
        name = generate_name()
        person = create_entire_person(name, authenticationMethods)
        people.append(person)
        peopleCounter+=1
    return people

def with_timer(title, f, *args):
    before = time.time()
    result = f(*args)
    after=time.time()
    Logger.info(f'[{after-before}s]: {title}')
    return result

data = []
try:
    data = read_json_file(args["source_path"])
    Logger.info(f'Parameters readed, I have { str(len(data)) } authentication methods')
except:
    Logger.error('Invalid source path')


people = with_timer('list generation', generate_list, args['total_people'], data)

try:
    with_timer('writting json', write_json_file, args['dest_path'], people)
    Logger.info(' -- -- Finished -- -- ')
except: 
    Logger.error('Unable to write result')

