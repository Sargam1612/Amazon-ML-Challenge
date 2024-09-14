import easyocr
reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory
result = reader.readtext('student_resource 3/images/\'images\'.jpg')

print(result)
