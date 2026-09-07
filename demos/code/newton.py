def f(x):
    return x**3 - 2*x - 5

def df(x):
    return 3*x**2 - 2

def newton(x0, tol=1e-12):
    # slope:here setup
    x = x0
    # slope:begin loop
    for _ in range(50):
        step = f(x) / df(x)
        x = x - step
    # slope:end loop
        # slope:begin test
        if abs(step) < tol:
            break
        # slope:end test
    return x
