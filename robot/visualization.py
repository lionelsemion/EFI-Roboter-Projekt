from patterns import CURVES, draw_curve
from virtual import run


while 1:
    for i, curve in enumerate(CURVES):
        print(f"{i}: {curve}")
    try:
        i = int(input("Curve number? "))
    except ValueError:
        i = -1
    if i == -1 or i >= len(CURVES) or i < 0:
        for curve in CURVES:
            print(f"Selected curve: {curve}")
            draw_curve(curve, run)
        continue
    selected_curve = i
    print(f"Selected curve: {CURVES[selected_curve]}")
    draw_curve(CURVES[selected_curve], run)
