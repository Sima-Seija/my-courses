import math

def solve_expression(expr):
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
                while start >= 0 and (s[start].isdigit() or s[start]=='.'):
                    start -= 1
                start += 1
            inner = s[start:idx]
            s = s[:start] + f"math.factorial(int({inner}))" + s[idx+1:]
        return s

    expr = replace_factorial(expr)

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
        for _ in range(100):
            try:
                fx0 = f(x0)
                fx1 = f(x1)
            except Exception as e:
                return f"Error: {e}"
            if abs(fx1) < 1e-7:
                # If int, return int
                if abs(round(x1) - x1) < 1e-7:
                    return int(round(x1))
                return round(x1, 5)
            if fx1 - fx0 == 0:
                # if the function is flat and we're not at 0, maybe the solution is a complex linear, let's use the complex trick as fallback!
                break
            x_new = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
            x0, x1 = x1, x_new
            
        # fallback to complex method for linear equations:
        try:
            c_val = f(1j)
            if c_val.imag != 0:
                sol = -c_val.real / c_val.imag
                if abs(round(sol) - sol) < 1e-7:
                    return int(round(sol))
                return round(sol, 5)
        except:
            pass
            
        return "Cannot solve"
    else:
        return eval(expr, {"math": math})

with open("out.txt", "w") as f:
    f.write(str(solve_expression("5!")) + "\n")
    f.write(str(solve_expression("(2+3)!")) + "\n")
    f.write(str(solve_expression("2*x=10")) + "\n")
    f.write(str(solve_expression("2*x+5=15")) + "\n")
    f.write(str(solve_expression("x*x=25")) + "\n")
