import os
import numpy as np
from typing import Dict, List, Union

def calculateResults(lamdaByL: float, length: float, draft: float, displacement: float, bml: float) -> Dict[str, Union[float, List[float]]]:
    """
    Calculate marine system parameters from input data.
    
    Args:
        lamdaByL: Wave length to ship length ratio
        length: Ship length in meters
        draft: Ship draft in meters
        displacement: Ship displacement in tons
        bml: Metacentric height in meters
        
    Returns:
        Dictionary containing calculated parameters
    """
    try:
        with open('./uploads/in.txt', 'r') as f:
            cc = [[float(j) for j in i.split('\t')] for i in f.read().strip().split('\n')]

        n = len(cc)  # Number of rows
        m = len(cc[0])  # Number of columns

        # Constants
        g = 9.8  # Gravitational acceleration (m/s²)
        pi = 3.14  # Pi approximation
        rho = 1.025  # Water density (kg/m³)

        # Calculate wave frequency squared
        wsq = g * 2 * pi / length / lamdaByL

        # Initialize ratio lookup dictionary
        ratio_in = {8: 7, 10: 7, 11: 8}
        for i in range(1, 12):
            if i not in ratio_in:
                ratio_in[i] = i - 1

        # Initialize arrays for calculations
        sa = []      # Sectional areas
        beta = []    # Shape coefficient
        b_by_t = []  # Beam to draft ratio
        xaxis = []   # Frequency parameter
        a_cf = []    # Added mass coefficients
        d_cf = []    # Damping coefficients

        # Process each column (ship section)
        for i in range(1, m):
            pr = 0    # Previous value
            pr2 = 0   # Previous x-coordinate
            ar = 0    # Area
            b = 0     # Maximum breadth
            
            # Calculate sectional area and find maximum breadth
            for j in range(1, n):
                ar += (cc[j][i] + pr) * (cc[j][0] - pr2)
                pr = cc[j][i]
                pr2 = cc[j][0]
                b = max(b, cc[j][i])
            
            sa.append(ar)
            beta.append(round(sa[-1] / (b * 2 * draft), 1))
            
            if beta[-1] < 0.5:
                beta[-1] = 0.5
            
            b_by_t.append(b * 2 / draft)
            xaxis.append(wsq * b / g)
            
            # Read added mass coefficients
            with open(f'data/{int(beta[-1] * 10)}.txt', 'r') as f:
                con = [[0 if j == '' else float(j) for j in i.split('\t')] for i in f.read().split('\n')]
                tem = ratio_in[max(1, round(b_by_t[-1] * 2.5, 0))]
                dd = 1000
                y = -1
                
                for row in con:
                    if abs(xaxis[-1] - row[tem * 2]) < dd:
                        dd = abs(xaxis[-1] - row[tem * 2])
                        y = row[tem * 2 + 1]
                
                a_cf.append(y)
            
            # Read damping coefficients
            with open(f'damping/{int(beta[-1] * 10)}.txt', 'r') as f:
                con = [[0 if j == '' else float(j) for j in i.split('\t')] for i in f.read().split('\n')]
                tem = ratio_in[max(1, round(b_by_t[-1] * 2.5, 0))]
                dd = 1000
                y = -1
                
                for row in con:
                    if abs(xaxis[-1] - row[tem * 2]) < dd:
                        dd = abs(xaxis[-1] - row[tem * 2])
                        y = row[tem * 2 + 1]
                
                d_cf.append(y)

        # Calculate heave and pitch parameters
        aa = list(a_cf[::-1])
        aa.append(0)
        aa = list(aa[::-1])

        a3 = 0       # Heave added mass
        a55 = 0      # Pitch added mass moment
        i_mass = 0   # Mass moment of inertia

        for idx, i in enumerate(cc[0][1:]):
            a3 += (aa[idx] + aa[idx + 1]) / 2 * (i - cc[0][idx]) * sa[idx] * rho
            a55 += (aa[idx] + aa[idx + 1]) / 2 * (i - cc[0][idx]) * sa[idx] * rho * (length / 2 - i) ** 2
            i_mass += (i - cc[0][idx]) * sa[idx] * rho * (length / 2 - i) ** 2

        # Calculate damping coefficients
        aa = list(d_cf[::-1])
        aa.append(0)
        aa = list(aa[::-1])

        b3 = 0  # Heave damping
        b55 = 0 # Pitch damping moment

        for idx, i in enumerate(cc[0][1:]):
            b3 += (aa[idx] + aa[idx + 1]) / 2 * (i - cc[0][idx]) * sa[idx] * rho
            b55 += (aa[idx] + aa[idx + 1]) / 2 * (i - cc[0][idx]) * sa[idx] * rho * (length / 2 - i) ** 2

        # Calculate waterplane area
        draft_index = min(range(1, n), key=lambda i: abs(cc[i][0] - draft))
        wpa = 0
        pr = 0
        pr2 = 0

        for j in range(1, m):
            wpa += (cc[draft_index][j] + pr) * (cc[0][j] - pr2)
            pr = cc[draft_index][j]
            pr2 = cc[0][j]

        return {
            "a33": round(a3, 3),
            "a55": round(a55, 3),
            "b33": round(b3, 4),
            "b55": round(b55, 3),
            "I55": round(i_mass, 3),
            "Awl": round(wpa, 2),
            "c33": round(wpa * rho * g, 2),
            "c55": bml * displacement,
            "omega": wsq,
            "section_positions": cc[0]
        }

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        return {}