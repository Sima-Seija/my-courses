from tkinter import *

# Let's create the Tkinter window
window = Tk()

# Then, you will define the size of the window in width(312) and height(324) using the 'geometry' method
window.geometry("347x480")

# In order to prevent the window from getting resized you will call 'resizable' method on the window
#window.resizable(0, 0)

#Finally, define the title of the window
window.title("Calculator")


# Let's now define the required functions for the Calculator to function properly.

# 1. First is the button click 'btn_click' function which will continuously update the input field whenever a number is entered or any button is pressed it will act as a button click update.
def btn_click(item):
    global expression
    expression = expression + str(item)
    input_text.set(expression)

# 2. Second is the button clear 'btn_clear' function clears the input field or previous calculations using the button "C"
def btn_clear():
    global expression
    expression = ""
    input_text.set("")

# 3. Third and the final function is button equal ("=") 'btn_equal' function which will calculate the expression present in input field. For example: User clicks button 2, + and 3 then clicks "=" will result in an output 5.
def btn_equal():
    global expression
    try:
        import math
        import re
        def replace_factorial(s):
            while '!' in s:
                idx = s.find('!')
                start = idx - 1
                if s[start] == ')':
                    count = 1
                    start -= 1
                    while start >= 0 and count > 0:
                        if s[start] == ')': count += 1
                        elif s[start] == '(': count -= 1
                        start -= 1
                    start += 1
                else:
                    while start >= 0 and (s[start].isdigit() or s[start]=='.' or s[start]=='x'):
                        start -= 1
                    start += 1
                inner = s[start:idx]
                s = s[:start] + "math.gamma((" + inner + ")+1)" + s[idx+1:]
            return s
        expr = replace_factorial(expression)
        expr = re.sub(r'(\d)(x)', r'\1*\2', expr)
        expr = re.sub(r'(x)(\d)', r'\1*\2', expr)

        if 'x' in expr or '=' in expr:
            if '=' in expr:
                left, right = expr.split('=')
                func_str = f"({left})-({right})"
            else:
                func_str = expr
            def f(x_val):
                eval_str = func_str.replace('x', f"({x_val})")
                return eval(eval_str, {"math": math})
            x0, x1 = 0.0, 1.0
            found = False
            for _ in range(100):
                try:
                    fx0 = f(x0)
                    fx1 = f(x1)
                except Exception:
                    break
                if abs(fx1) < 1e-7:
                    x_sol = x1
                    found = True
                    break
                if fx1 - fx0 == 0:
                    break
                x_new = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
                x0, x1 = x1, x_new

            if not found:
                try:
                    c_val = f(1j)
                    if c_val.imag != 0:
                        x_sol = -c_val.real / c_val.imag
                        found = True
                except:
                    pass

            if found:
                if abs(round(x_sol) - x_sol) < 1e-7:
                    x_sol = int(round(x_sol))
                else:
                    x_sol = round(x_sol, 5)
                input_text.set("x=" + str(x_sol))
                expression = str(x_sol)
            else:
                input_text.set("Can't Solve")
                expression = ""
        else:
            result = eval(expr, {"math": math})
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            elif isinstance(result, float):
                result = round(result, 5)
            input_text.set(str(result))
            expression = str(result)
    except Exception as e:
        input_text.set("Error")
        expression = ""

expression = ""
# In order to get the instance of the input field 'StringVar()' is used
input_text = StringVar()

# Once all the functions are defined then comes the main section where you will start defining the structure of the calculator inside the GUI.

# The first thing is to create a frame for the input field
input_frame = Frame(window, width = 312, height = 50, bd = 0, highlightbackground = "black", highlightcolor = "black", highlightthickness = 1)
input_frame.pack(side = TOP)


# Then you will create an input field inside the 'Frame' that was created in the previous step. Here the digits or the output will be displayed as 'right' aligned
input_field = Entry(input_frame, font = ('arial', 18, 'bold'), textvariable = input_text, width = 50, bg = "#eee", bd = 0, justify = RIGHT)
input_field.grid(row = 0, column = 0)
input_field.pack(ipady = 10) # 'ipady' is an internal padding to increase the height of input field


# Once you have the input field defined then you need a separate frame which will incorporate all the buttons inside it below the 'input field'
btns_frame = Frame(window, width = 312, height = 330, bg = "grey")
btns_frame.pack()


# The first row will comprise of the buttons 'Clear (C)', '(', ')' and 'Divide (/)'
clear = Button(btns_frame, text = "C", fg = "black", width = 10, height = 3, bd = 0, bg = "#eee", cursor = "hand2", command = lambda: btn_clear()).grid(row = 0, column = 0, padx = 1, pady = 1)
l_paren = Button(btns_frame, text = "(", fg = "black", width = 10, height = 3, bd = 0, bg = "#eee", cursor = "hand2", command = lambda: btn_click("(")).grid(row = 0, column = 1, padx = 1, pady = 1)
r_paren = Button(btns_frame, text = ")", fg = "black", width = 10, height = 3, bd = 0, bg = "#eee", cursor = "hand2", command = lambda: btn_click(")")).grid(row = 0, column = 2, padx = 1, pady = 1)
divide = Button(btns_frame, text = "/", fg = "black", width = 10, height = 3, bd = 0, bg = "#eee", cursor = "hand2", command = lambda: btn_click("/")).grid(row = 0, column = 3, padx = 1, pady = 1)


# The second row will comprise of the buttons '7', '8', '9' and 'Multiply (*)'
seven = Button(btns_frame, text = "7", fg = "black", width = 10, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(7)).grid(row = 1, column = 0, padx = 1, pady = 1)
eight = Button(btns_frame, text = "8", fg = "black", width = 10, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(8)).grid(row = 1, column = 1, padx = 1, pady = 1)
nine = Button(btns_frame, text = "9", fg = "black", width = 10, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(9)).grid(row = 1, column = 2, padx = 1, pady = 1)
multiply = Button(btns_frame, text = "*", fg = "black", width = 10, height = 3, bd = 0, bg = "#eee", cursor = "hand2", command = lambda: btn_click("*")).grid(row = 1, column = 3, padx = 1, pady = 1)


# The third row will comprise of the buttons '4', '5', '6' and 'Subtract (-)'
four = Button(btns_frame, text = "4", fg = "black", width = 10, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(4)).grid(row = 2, column = 0, padx = 1, pady = 1)
five = Button(btns_frame, text = "5", fg = "black", width = 10, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(5)).grid(row = 2, column = 1, padx = 1, pady = 1)
six = Button(btns_frame, text = "6", fg = "black", width = 10, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(6)).grid(row = 2, column = 2, padx = 1, pady = 1)
minus = Button(btns_frame, text = "-", fg = "black", width = 10, height = 3, bd = 0, bg = "#eee", cursor = "hand2", command = lambda: btn_click("-")).grid(row = 2, column = 3, padx = 1, pady = 1)


# The fourth row will comprise of the buttons '1', '2', '3' and 'Addition (+)'
one = Button(btns_frame, text = "1", fg = "black", width = 10, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(1)).grid(row = 3, column = 0, padx = 1, pady = 1)
two = Button(btns_frame, text = "2", fg = "black", width = 10, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(2)).grid(row = 3, column = 1, padx = 1, pady = 1)
three = Button(btns_frame, text = "3", fg = "black", width = 10, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(3)).grid(row = 3, column = 2, padx = 1, pady = 1)
plus = Button(btns_frame, text = "+", fg = "black", width = 10, height = 3, bd = 0, bg = "#eee", cursor = "hand2", command = lambda: btn_click("+")).grid(row = 3, column = 3, padx = 1, pady = 1)


# The fifth row will comprise of the buttons '0', 'Decimal (.)', 'x', and 'Factorial (!)'
zero = Button(btns_frame, text = "0", fg = "black", width = 10, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(0)).grid(row = 4, column = 0, padx = 1, pady = 1)
point = Button(btns_frame, text = ".", fg = "black", width = 10, height = 3, bd = 0, bg = "#eee", cursor = "hand2", command = lambda: btn_click(".")).grid(row = 4, column = 1, padx = 1, pady = 1)
x_btn = Button(btns_frame, text = "x", fg = "black", width = 10, height = 3, bd = 0, bg = "#eee", cursor = "hand2", command = lambda: btn_click("x")).grid(row = 4, column = 2, padx = 1, pady = 1)
fact_btn = Button(btns_frame, text = "!", fg = "black", width = 10, height = 3, bd = 0, bg = "#eee", cursor = "hand2", command = lambda: btn_click("!")).grid(row = 4, column = 3, padx = 1, pady = 1)

# Finally, the sixth row will comprise of the equation '=' and 'Enter' buttons
eq_btn = Button(btns_frame, text = "=", fg = "black", width = 21, height = 3, bd = 0, bg = "#eee", cursor = "hand2", command = lambda: btn_click("=")).grid(row = 5, column = 0, columnspan = 2, padx = 1, pady = 1)
eval_btn = Button(btns_frame, text = "Enter", fg = "black", width = 21, height = 3, bd = 0, bg = "#eee", cursor = "hand2", command = lambda: btn_equal()).grid(row = 5, column = 2, columnspan = 2, padx = 1, pady = 1)


window.mainloop()

