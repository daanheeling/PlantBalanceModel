#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 13:39:56 2025

@author: daanheeling
"""

#%% Functions and Ranges
# Ranges
lettuce_ranges = {
    "PPFD": (250, 700),  # µmol·m⁻²·s⁻¹
    "Photoperiod": (16, 20),  # hours
    "LI": (85, 100),  # %
    "LUE": (1.2, 1.8),  # g·mol
    "HI": (95, 95),  # % 
    "DM_percent": (3.0, 3.5),  # %
    "AGD": (365, 365),  # days
    "T": (22, 28),  # °C 
    "HW": (125, 125),  # g 
    "SD": (0, 0),  # stems/m² (not applicable)
    "FNT": (0, 0),  # fruits/truss (not applicable)
    "PD": (75, 105),  # plants/m²
    "CCT": (0, 0)
}

tomato_ranges = {
    "PPFD": (350, 1000),  # µmol·m⁻²·s⁻¹
    "Photoperiod": (16, 20),  # hours
    "LI": (100, 100),  # %
    "LUE": (1.2, 1.8),  # g·mol⁻¹
    "HI": (65, 65),  # %
    "DM_percent": (7.5, 7.5),  # %
    "AGD": (360, 360),  # days
    "T": (22, 28),  # °C
    "HW": (40, 40),  # g 
    "SD": (4, 6),  # stems/m²
    "FNT": (10, 12),  # fruits/truss
    "PD": (0, 0),  # plants/m² (not applicable)
    "CCT": (360, 360)
}

# Scenarios ranges
lettuce_current = {
    "PPFD": lettuce_ranges["PPFD"][0],
    "Photoperiod": lettuce_ranges["Photoperiod"][0],
    "LI": lettuce_ranges["LI"][0],
    "LUE": lettuce_ranges["LUE"][0],
    "HI": lettuce_ranges["HI"][0],
    "DM_percent": lettuce_ranges["DM_percent"][1],
    "AGD": lettuce_ranges["AGD"][0],
    "T": lettuce_ranges["T"][0],
    "HW": lettuce_ranges["HW"][0],
    "SD": lettuce_ranges["SD"][0],
    "FNT": lettuce_ranges["FNT"][0],
    "PD": lettuce_ranges["PD"][0],
    "CCT": lettuce_ranges["CCT"][0]
}

lettuce_future = {
    "PPFD": lettuce_ranges["PPFD"][1],
    "Photoperiod": lettuce_ranges["Photoperiod"][1],
    "LI": lettuce_ranges["LI"][1],
    "LUE": lettuce_ranges["LUE"][1],
    "HI": lettuce_ranges["HI"][1],
    "DM_percent": lettuce_ranges["DM_percent"][0],
    "AGD": lettuce_ranges["AGD"][1],
    "T": lettuce_ranges["T"][1],
    "HW": lettuce_ranges["HW"][1],
    "SD": lettuce_ranges["SD"][1],
    "FNT": lettuce_ranges["FNT"][1],
    "PD": lettuce_ranges["PD"][1],
    "CCT": lettuce_ranges["CCT"][0]
}


tomato_current = {
    "PPFD": tomato_ranges["PPFD"][0],
    "Photoperiod": tomato_ranges["Photoperiod"][0],
    "LI": tomato_ranges["LI"][0],
    "LUE": tomato_ranges["LUE"][0],
    "HI": tomato_ranges["HI"][0],
    "DM_percent": tomato_ranges["DM_percent"][1],
    "AGD": tomato_ranges["AGD"][0],
    "T": tomato_ranges["T"][0],
    "HW": tomato_ranges["HW"][0],
    "SD": tomato_ranges["SD"][0],
    "FNT": tomato_ranges["FNT"][0],
    "PD": tomato_ranges["PD"][0],
    "CCT": tomato_ranges["CCT"][0]
}

tomato_future = {
    "PPFD": tomato_ranges["PPFD"][1],
    "Photoperiod": tomato_ranges["Photoperiod"][1],
    "LI": tomato_ranges["LI"][1],
    "LUE": tomato_ranges["LUE"][1],
    "HI": tomato_ranges["HI"][1],
    "DM_percent": tomato_ranges["DM_percent"][0],
    "AGD": tomato_ranges["AGD"][1],
    "T": tomato_ranges["T"][1],
    "HW": tomato_ranges["HW"][1],
    "SD": tomato_ranges["SD"][1],
    "FNT": tomato_ranges["FNT"][1],
    "PD": tomato_ranges["PD"][1],
    "CCT": tomato_ranges["CCT"][1]
}
#%% Model Calculations
def calculate_yield(PPFD, Photoperiod, LI, LUE, HI, DM_percent, AGD, T, crop_type, SD, FNT, HW, PD, CCT):
    # Calculate source-limited yield
    DLI = PPFD * Photoperiod * 3600 * 10**(-6)  # mol·m⁻²·day⁻¹
    DLA = DLI * (LI / 100)  # mol·m⁻²·day⁻¹
    DM = DLA * LUE  # g·m⁻²·day⁻¹
    DMharvest = DM * (HI / 100)  # g·m⁻²·day⁻¹
    FW = DMharvest / (DM_percent / 100)  # g·m⁻²·day⁻¹
    T_ref = 21
    FMP_ref = 55
    TSF_fmp = 5.4
    FMP = max(FMP_ref + ((T_ref - T) * TSF_fmp), 1)  # Ensure days_from_flower_to_harvest is at least 1 day
    
    if crop_type == 'fruiting crop':
        source_restricted_yield = (AGD - FMP) * FW / 1000  # kg·m⁻²·year⁻¹
    elif crop_type == 'leafy crop':
        source_restricted_yield = AGD * FW / 1000  # kg·m⁻²·year⁻¹
    else:
        raise ValueError("Invalid crop_type. Must be 'fruiting crop' or 'leafy crop'.")
    
    # Sink-limited yield
    if crop_type == "fruiting crop":
        TI_ref = 6.9  # days
        T_ref = 21
        TSF_ti = 0.6
        TI = max(TI_ref + ((T_ref - T) * TSF_ti), 1)  # Ensure Growth_cycle is at least 1 day
        FMP_ref = 55
        TSF_fmp = 5.4
        FMP = max(FMP_ref + ((T_ref - T) * TSF_fmp), 1)  # Ensure days_from_flower_to_harvest is at least 1 day
        CTN = (CCT - FMP) / TI + 1
        sink_restricted_yield = AGD / CCT * CTN * SD * FNT * HW / 1000  # kg·m⁻²·year⁻¹
    elif crop_type == "leafy crop":
        CCT_ref = 22.5  # days
        T_ref = 20
        TSF_cct = 1.0
        CCT = max(CCT_ref + ((T_ref - T) * TSF_cct), 1)  # Ensure Growth_cycle is at least 1 day
        sink_restricted_yield = AGD / CCT * PD * HW / 1000  # kg·m⁻²·year⁻¹
    else:
        raise ValueError("Invalid crop_type. Must be 'fruiting crop' or 'leafy crop'.")
    
    # The actual yield is the minimum of the two yields
    actual_yield = min(source_restricted_yield, sink_restricted_yield)
    return actual_yield, source_restricted_yield, sink_restricted_yield
#%% Results: Yields
# Define the scenarios
scenarios = {
    "lettuce_current": lettuce_current,
    "lettuce_future": lettuce_future,
    "tomato_current": tomato_current,
    "tomato_future": tomato_future
}

# Function to print the yields for each scenario
def print_yields(scenarios):
    for scenario_name, scenario in scenarios.items():
        crop_type = "leafy crop" if "lettuce" in scenario_name else "fruiting crop"
        actual_yield, source_restricted_yield, sink_restricted_yield = calculate_yield(
            scenario["PPFD"], scenario["Photoperiod"], scenario["LI"], scenario["LUE"], scenario["HI"],
            scenario["DM_percent"], scenario["AGD"], scenario["T"], crop_type, scenario["SD"],
            scenario["FNT"], scenario["HW"], scenario["PD"], scenario["CCT"]
        )
        print(f"{scenario_name.replace('_', ' ').title()}:")
        print(f"  Source-Restricted Yield: {source_restricted_yield:.2f} kg·m⁻²·year⁻¹")
        print(f"  Sink-Restricted Yield: {sink_restricted_yield:.2f} kg·m⁻²·year⁻¹")
        print(f"  Actual Yield: {actual_yield:.2f} kg·m⁻²·year⁻¹")
        print()

# Call the function to print the yields
print_yields(scenarios)

#%% Results: required PPFD at given sink_limited yield
def calculate_required_PPFD(target_yield, Photoperiod, LI, LUE, HI, DM_percent, AGD, T, crop_type):
    # Rearrange the formula for source-restricted yield to solve for PPFD
    if crop_type == 'fruiting crop':
        T_ref = 21
        FMP_ref = 55
        TSF_fmp = 5.4
        FMP = max(FMP_ref + ((T_ref - T) * TSF_fmp), 1)  # Ensure days_from_flower_to_harvest is at least 1 day
        EAGD = AGD - FMP
    elif crop_type == 'leafy crop':
        EAGD = AGD
    else:
        raise ValueError("Invalid crop_type. Must be 'fruiting crop' or 'leafy crop'.")

    FW = (target_yield * 1000) / EAGD  # g·m⁻²·day⁻¹
    DMharvest = FW * (DM_percent / 100)  # g·m⁻²·day⁻¹
    DM = DMharvest / (HI / 100)  # g·m⁻²·day⁻¹
    DLA = DM / LUE  # mol·m⁻²·day⁻¹
    DLI = DLA / (LI / 100)  # mol·m⁻²·day⁻¹
    PPFD = DLI / (Photoperiod * 3600 * 10**(-6))  # µmol·m⁻²·s⁻¹
    return PPFD

# lettuce
lettuce_current_yield, lettuce_current_source_yield, lettuce_current_sink_yield = calculate_yield(
    lettuce_current["PPFD"], lettuce_current["Photoperiod"], lettuce_current["LI"], lettuce_current["LUE"], 
    lettuce_current["HI"], lettuce_current["DM_percent"], lettuce_current["AGD"], lettuce_current["T"], 
    "leafy crop", lettuce_current["SD"], lettuce_current["FNT"], lettuce_current["HW"], lettuce_current["PD"], 
    lettuce_current["CCT"]
)

if lettuce_current_yield < lettuce_current_source_yield:
    required_PPFD = calculate_required_PPFD(
        lettuce_current_yield,
        lettuce_current["Photoperiod"],
        lettuce_current["LI"],
        lettuce_current["LUE"],
        lettuce_current["HI"],
        lettuce_current["DM_percent"],
        lettuce_current["AGD"],
        lettuce_current["T"],
        "leafy crop"
    )
    print(f"Required PPFD for lettuce current scenario to reach actual yield: {required_PPFD:.2f} µmol·m⁻²·s⁻¹")
    # Verify by recalculating yields with the required PPFD
    lettuce_current["PPFD"] = required_PPFD
    recalculated_yield, recalculated_source_yield, recalculated_sink_yield = calculate_yield(
        lettuce_current["PPFD"], lettuce_current["Photoperiod"], lettuce_current["LI"], lettuce_current["LUE"], 
        lettuce_current["HI"], lettuce_current["DM_percent"], lettuce_current["AGD"], lettuce_current["T"], 
        "leafy crop", lettuce_current["SD"], lettuce_current["FNT"], lettuce_current["HW"], lettuce_current["PD"], 
        lettuce_current["CCT"]
    )
    print(f"Recalculated Yield: {recalculated_yield:.2f} kg·m⁻²·year⁻¹ (Source-limited: {recalculated_source_yield:.2f}, Sink-limited: {recalculated_sink_yield:.2f})")

lettuce_future_yield, lettuce_future_source_yield, lettuce_future_sink_yield = calculate_yield(
    lettuce_future["PPFD"], lettuce_future["Photoperiod"], lettuce_future["LI"], lettuce_future["LUE"], 
    lettuce_future["HI"], lettuce_future["DM_percent"], lettuce_future["AGD"], lettuce_future["T"], 
    "leafy crop", lettuce_future["SD"], lettuce_future["FNT"], lettuce_future["HW"], lettuce_future["PD"], 
    lettuce_future["CCT"]
)

if lettuce_future_yield < lettuce_future_source_yield:
    required_PPFD = calculate_required_PPFD(
        lettuce_future_yield,
        lettuce_future["Photoperiod"],
        lettuce_future["LI"],
        lettuce_future["LUE"],
        lettuce_future["HI"],
        lettuce_future["DM_percent"],
        lettuce_future["AGD"],
        lettuce_future["T"],
        "leafy crop"
    )
    print(f"Required PPFD for lettuce future scenario to reach actual yield: {required_PPFD:.2f} µmol·m⁻²·s⁻¹")
    # Verify by recalculating yields with the required PPFD
    lettuce_future["PPFD"] = required_PPFD
    recalculated_yield, recalculated_source_yield, recalculated_sink_yield = calculate_yield(
        lettuce_future["PPFD"], lettuce_future["Photoperiod"], lettuce_future["LI"], lettuce_future["LUE"], 
        lettuce_future["HI"], lettuce_future["DM_percent"], lettuce_future["AGD"], lettuce_future["T"], 
        "leafy crop", lettuce_future["SD"], lettuce_future["FNT"], lettuce_future["HW"], lettuce_future["PD"], 
        lettuce_future["CCT"]
    )
    print(f"Recalculated Yield: {recalculated_yield:.2f} kg·m⁻²·year⁻¹ (Source-limited: {recalculated_source_yield:.2f}, Sink-limited: {recalculated_sink_yield:.2f})")

# Tomato
tomato_current_yield, tomato_current_source_yield, tomato_current_sink_yield = calculate_yield(
    tomato_current["PPFD"], tomato_current["Photoperiod"], tomato_current["LI"], tomato_current["LUE"], 
    tomato_current["HI"], tomato_current["DM_percent"], tomato_current["AGD"], tomato_current["T"], 
    "fruiting crop", tomato_current["SD"], tomato_current["FNT"], tomato_current["HW"], tomato_current["PD"], 
    tomato_current["CCT"]
)

if tomato_current_yield < tomato_current_source_yield:
    required_PPFD = calculate_required_PPFD(
        tomato_current_yield,
        tomato_current["Photoperiod"],
        tomato_current["LI"],
        tomato_current["LUE"],
        tomato_current["HI"],
        tomato_current["DM_percent"],
        tomato_current["AGD"],
        tomato_current["T"],
        "fruiting crop"
    )
    print(f"Required PPFD for tomato current scenario to reach actual yield: {required_PPFD:.2f} µmol·m⁻²·s⁻¹")
    # Verify by recalculating yields with the required PPFD
    tomato_current["PPFD"] = required_PPFD
    recalculated_yield, recalculated_source_yield, recalculated_sink_yield = calculate_yield(
        tomato_current["PPFD"], tomato_current["Photoperiod"], tomato_current["LI"], tomato_current["LUE"], 
        tomato_current["HI"], tomato_current["DM_percent"], tomato_current["AGD"], tomato_current["T"], 
        "fruiting crop", tomato_current["SD"], tomato_current["FNT"], tomato_current["HW"], tomato_current["PD"], 
        tomato_current["CCT"]
    )
    print(f"Recalculated Yield: {recalculated_yield:.2f} kg·m⁻²·year⁻¹ (Source-limited: {recalculated_source_yield:.2f}, Sink-limited: {recalculated_sink_yield:.2f})")

tomato_future_yield, tomato_future_source_yield, tomato_future_sink_yield = calculate_yield(
    tomato_future["PPFD"], tomato_future["Photoperiod"], tomato_future["LI"], tomato_future["LUE"], 
    tomato_future["HI"], tomato_future["DM_percent"], tomato_future["AGD"], tomato_future["T"], 
    "fruiting crop", tomato_future["SD"], tomato_future["FNT"], tomato_future["HW"], tomato_future["PD"], 
    tomato_future["CCT"]
)

if tomato_future_yield < tomato_future_source_yield:
    required_PPFD = calculate_required_PPFD(
        tomato_future_yield,
        tomato_future["Photoperiod"],
        tomato_future["LI"],
        tomato_future["LUE"],
        tomato_future["HI"],
        tomato_future["DM_percent"],
        tomato_future["AGD"],
        tomato_future["T"],
        "fruiting crop"
    )
    print(f"Required PPFD for tomato future scenario to reach actual yield: {required_PPFD:.2f} µmol·m⁻²·s⁻¹")
    # Verify by recalculating yields with the required PPFD
    tomato_future["PPFD"] = required_PPFD
    recalculated_yield, recalculated_source_yield, recalculated_sink_yield = calculate_yield(
        tomato_future["PPFD"], tomato_future["Photoperiod"], tomato_future["LI"], tomato_future["LUE"], 
        tomato_future["HI"], tomato_future["DM_percent"], tomato_future["AGD"], tomato_future["T"], 
        "fruiting crop", tomato_future["SD"], tomato_future["FNT"], tomato_future["HW"], tomato_future["PD"], 
        tomato_future["CCT"]
    )
    print(f"Recalculated Yield: {recalculated_yield:.2f} kg·m⁻²·year⁻¹ (Source-limited: {recalculated_source_yield:.2f}, Sink-limited: {recalculated_sink_yield:.2f})")

# Calculate required PPFD for current scenarios to achieve the same yield
lettuce_current_required_PPFD = calculate_required_PPFD(
    lettuce_current_yield,
    lettuce_current["Photoperiod"],
    lettuce_current["LI"],
    lettuce_current["LUE"],
    lettuce_current["HI"],
    lettuce_current["DM_percent"],
    lettuce_current["AGD"],
    lettuce_current["T"],
    "leafy crop"
)

tomato_current_required_PPFD = calculate_required_PPFD(
    tomato_current_yield,
    tomato_current["Photoperiod"],
    tomato_current["LI"],
    tomato_current["LUE"],
    tomato_current["HI"],
    tomato_current["DM_percent"],
    tomato_current["AGD"],
    tomato_current["T"],
    "fruiting crop"
)

print(f"Required PPFD for lettuce current scenario to achieve current yield: {lettuce_current_required_PPFD:.2f} µmol·m⁻²·s⁻¹")
print(f"Required PPFD for tomato current scenario to achieve current yield: {tomato_current_required_PPFD:.2f} µmol·m⁻²·s⁻¹")
