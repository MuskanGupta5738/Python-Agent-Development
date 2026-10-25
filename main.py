print("Hello Muskan!")
print("Welcome to Python for Agent Development")
name = "Muskan"
print("Hello", name)



def add(a, b):
    return a + b

def greet(name):
    return f"Hello, {name}! Welcome."

tools = {
    "add": add,
    "greet": greet,
}
def agent_brain():
    result = tools["add"](10, 20)
    print("Addition:", result)
    message = tools["greet"]("name")
    print(message)

print("Direct function calls:")
print(add(5, 7))
print(greet("muskan"))

agent_brain()



# Student details
name = "Muskan"
age = 20
cgpa = 7.80
is_student = True

# Display details
print("Name:", name)
print("Age:", age)
print("CGPA:", cgpa)
print("Is Student:", is_student)














