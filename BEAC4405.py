import requests

ROOT_URL = "http://localhost:8081/api/v1/dashboard/teacher"

CLASS_URL = "/classes"
ASSIGNMENT_URL = "/assignmentsv2/list"
THINKLET_URL = "/students/thinkletsdatalite"
NEW_THINKLET_URL = "/thinkletsdatalite"

COOKIE = {"JSESSIONID":"2AD5A3BD1B513E5029F5D68D0C58791C"}

def get(url,params={}):
    req = requests.get()
    return requests

def compareAssignmentNThinklet():
    params = {"classIds":668}
    assignment_r = requests.get(ROOT_URL+ASSIGNMENT_URL, cookies=COOKIE)
    assignment = assignment_r.json()["data"]
    assignment_array = [x['id'] for x in assignment]
    print("----- assignment -----")
    print(assignment_array)
    print(len(assignment_array))

    thinklet_r = requests.get(ROOT_URL+NEW_THINKLET_URL, cookies=COOKIE)
    thinklets = thinklet_r.json()["data"]
    thinklets_array = []
    [thinklets_array.append(x['assignmentId']) for x in  thinklets if x['assignmentId'] not in thinklets_array]
    print("----- thinklet:assignmentId -----")

    print(thinklets_array)
    print(len(thinklets_array))


    thinkletNotInAssignment = []
    assignmentNotInthinklet = []
    for a in assignment_array:
        if a not in thinklets_array:
            assignmentNotInthinklet.append(a)

    for t in thinklets_array:
        if t not in assignment_array:
            thinkletNotInAssignment.append(t)


    print("thinkletNotInAssignment:",thinkletNotInAssignment)
    print(len(thinkletNotInAssignment))

    print("assignmentNotInthinklet:",assignmentNotInthinklet)
    print(len(assignmentNotInthinklet))

def compareClassNThinklet():
    classes_r = requests.get(ROOT_URL+CLASS_URL, cookies=COOKIE)
    classes = classes_r.json()["data"]
    class_array = [x['id'] for x in classes]
    print("----- class -----")
    print(class_array)
    print(len(class_array))

    thinklet_r = requests.get(ROOT_URL+THINKLET_URL, cookies=COOKIE)
    thinklets = thinklet_r.json()["data"]
    thinklets_array = []
    [thinklets_array.append(x['class_id']) for x in  thinklets if x['class_id'] not in thinklets_array]
    print("----- thinklet:classId -----")
    print(thinklets_array)
    print(len(thinklets_array))

    thinkletNotInclasses = []
    classesNotInthinklet = []

    for c in class_array:
        if c not in thinklets_array:
            classesNotInthinklet.append(c)

    for t in thinklets_array:
        if t not in class_array:
            thinkletNotInclasses.append(t)

    print("thinkletNotInclasses:",thinkletNotInclasses)
    print("classesNotInthinklet:",classesNotInthinklet)
    print(len(classesNotInthinklet))
if __name__ == '__main__':
    compareAssignmentNThinklet()
